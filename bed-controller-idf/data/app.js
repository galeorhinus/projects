const UI_BUILD_TAG = "__UI_BUILD_TAG__";
const UI_ROLE = "__UI_ROLE__";
const UI_ROLES = "__UI_ROLES__";
const roles = UI_ROLES ? UI_ROLES.split(',').filter(Boolean) : [UI_ROLE];
// Expose build info globally for easy cache verification
window.UI_BUILD_TAG = UI_BUILD_TAG;
window.UI_ROLE = UI_ROLE;
window.UI_ROLES = roles.slice();
let autoPeerHosts = [];
let peerHosts = [];
let peerList = [];
let bedTargets = [];
let bedTargetsById = {};
let lightTargets = [];
let lightTargetsById = {};
let currentBedTargetId = null;
var PEER_CACHE_KEY = 'peerCacheV1';
var PEER_STALE_MS = 60000;
var PEER_EXPIRE_MS = 5 * 60 * 1000;
var bedSummaryCollapsed = true;
var bedLastStatus = {
    headPos: 0,
    footPos: 0,
    headDir: "STOPPED",
    footDir: "STOPPED",
    uptimeText: "-",
    lastSeenText: "-"
};
var relayLogEnabled = false; // toggle for relay/UI logs
function logUiEvent(msg) {
    if (!msg) return;
    console.log(msg);
    fetch('/rpc/Bed.Log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ msg: msg })
    }).catch(function(_) {});
}
logUiEvent("UI startup v2 " + UI_BUILD_TAG + " @ " + new Date().toISOString());

function setRelayLog(enabled) {
    relayLogEnabled = !!enabled;
    console.log("Relay logging " + (relayLogEnabled ? "enabled" : "disabled"));
}

// --- Peer discovery helpers ---
function loadPeerHosts() {
    try {
        var stored = localStorage.getItem('peerHosts');
        if (stored) peerHosts = JSON.parse(stored);
    } catch (e) {
        peerHosts = [];
    }
}
function setPeerHosts(hosts) {
    if (!Array.isArray(hosts)) return;
    peerHosts = hosts.filter(Boolean);
    localStorage.setItem('peerHosts', JSON.stringify(peerHosts));
    refreshPeersInternal();
}
loadPeerHosts();

function peerCacheKey(peer) {
    var host = peer && (peer.isLocal ? "local" : (peer.host || peer.ip || ""));
    var rolesKey = (peer && peer.roles) ? peer.roles.slice().sort().join(',') : "";
    return host + "|" + rolesKey;
}

function loadPeerCache() {
    try {
        var raw = localStorage.getItem(PEER_CACHE_KEY);
        if (!raw) return [];
        var parsed = JSON.parse(raw);
        return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
        return [];
    }
}

function savePeerCache(list) {
    try {
        localStorage.setItem(PEER_CACHE_KEY, JSON.stringify(list));
    } catch (e) {}
}

function cacheEntryToPeer(entry) {
    if (!entry || (!entry.host && !entry.ip && !entry.isLocal)) return null;
    var roles = Array.isArray(entry.roles) ? entry.roles : (entry.roles ? entry.roles.split(',').filter(Boolean) : []);
    return {
        host: entry.host || "",
        ip: entry.ip || "",
        device_name: entry.device_name || "",
        room: entry.room || "Unknown",
        fw: entry.fw || "",
        type: entry.type || "",
        model: entry.model || "",
        wiring_type: entry.wiring_type || "",
        roles: roles,
        isLocal: !!entry.isLocal,
        last_seen: entry.last_seen || 0
    };
}

function peerToCacheEntry(peer, lastSeen) {
    return {
        host: peer.host || "",
        ip: peer.ip || "",
        device_name: peer.device_name || "",
        room: peer.room || "Unknown",
        fw: peer.fw || "",
        type: peer.type || "",
        model: peer.model || "",
        wiring_type: peer.wiring_type || "",
        roles: Array.isArray(peer.roles) ? peer.roles.slice() : [],
        isLocal: !!peer.isLocal,
        last_seen: lastSeen || Date.now()
    };
}

function mergePeerCache(currentPeers) {
    var now = Date.now();
    var cached = loadPeerCache();
    var cacheMap = new Map();
    cached.forEach(function(entry) {
        var peer = cacheEntryToPeer(entry);
        if (!peer) return;
        var key = peerCacheKey(peer);
        if (!key) return;
        cacheMap.set(key, entry);
    });
    (currentPeers || []).forEach(function(peer) {
        var key = peerCacheKey(peer);
        if (!key) return;
        cacheMap.set(key, peerToCacheEntry(peer, now));
    });
    var merged = [];
    cacheMap.forEach(function(entry) {
        var age = now - (entry.last_seen || 0);
        if (age <= PEER_EXPIRE_MS) {
            merged.push(entry);
        }
    });
    savePeerCache(merged);
    return merged;
}

function applyCachedPeers() {
    var now = Date.now();
    var cached = loadPeerCache();
    if (!cached.length) return;
    var live = cached.filter(function(entry) {
        return (now - (entry.last_seen || 0)) <= PEER_EXPIRE_MS;
    });
    if (!live.length) return;
    peerList = live.map(cacheEntryToPeer).filter(Boolean);
    buildTargetsFromPeers();
    ensureActiveModule();
    updateTabVisibility();
    var nextLightRenderKey = lightTargets.map(getLightCacheKey).sort().join(';');
    if (nextLightRenderKey !== lightRenderKey) {
        lightRenderKey = nextLightRenderKey;
        renderLightRooms();
    }
    renderLightFilters();
    updateBedTargetLabel();
}

function normalizePeerHost(peer) {
    var h = peer.host || peer.ip || "";
    if (!h) return "";
    if (peer.host && peer.host.indexOf('.') === -1) {
        h = peer.host + '.local';
    }
    return h;
}

function targetLabel(role, peer) {
    var name = peer.device_name || peer.host || "Unknown";
    var room = peer.room || "";
    if (peer.isLocal) name = "Local";
    if (room && room.toLowerCase() !== "unknown") {
        return role.toUpperCase() + ": " + name + " - " + room;
    }
    return role.toUpperCase() + ": " + name;
}

function buildTargetsFromPeers() {
    bedTargets = [];
    bedTargetsById = {};
    lightTargets = [];
    lightTargetsById = {};
    lightCacheKeyById = {};

    peerList.forEach(function(peer) {
        (peer.roles || []).forEach(function(role) {
            if (role !== "bed" && role !== "light") return;
            var id = role + ":" + (peer.isLocal ? "local" : peer.host);
            var target = {
                id: id,
                role: role,
                host: peer.host,
                device_name: peer.device_name || peer.host || "Unknown",
                room: peer.room || "Unknown",
                fw: peer.fw || "",
                type: peer.type || "",
                model: peer.model || "",
                wiring_type: peer.wiring_type || "",
                isLocal: !!peer.isLocal,
                last_seen: peer.last_seen || 0
            };
            if (role === "bed" && !bedTargetsById[id]) {
                bedTargetsById[id] = target;
                bedTargets.push(target);
            }
            if (role === "light" && !lightTargetsById[id]) {
                lightTargetsById[id] = target;
                lightTargets.push(target);
                lightCacheKeyById[id] = getLightCacheKey(target);
                if (target.last_seen && !lightLastSeenById[lightCacheKeyById[id]]) {
                    lightLastSeenById[lightCacheKeyById[id]] = target.last_seen;
                }
            }
        });
    });
}

function ensureActiveModule() {
    if (currentModule === 'light' && lightTargets.length > 0) {
        return;
    }
    if (currentModule.startsWith('bed:') && bedTargetsById[currentModule]) {
        currentBedTargetId = currentModule;
        return;
    }
    if (lightTargets.length > 0) {
        currentModule = 'light';
        return;
    }
    if (bedTargets.length > 0) {
        var localBed = bedTargets.find(function(t){ return t.isLocal; }) || bedTargets[0];
        currentBedTargetId = localBed.id;
        currentModule = currentBedTargetId;
        return;
    }
}

function updateBedTargetLabel() {
    var targetEl = document.getElementById('bed-summary-target');
    var roomEl = document.getElementById('bed-summary-room');
    var hostEl = document.getElementById('bed-summary-host');
    var fwEl = document.getElementById('bed-summary-fw');
    var pillRoomEl = document.getElementById('bed-pill-room');
    var subtitleEl = document.getElementById('bed-summary-subtitle');
    if (!targetEl || !roomEl || !hostEl || !fwEl) return;
    if (!currentBedTargetId || !bedTargetsById[currentBedTargetId]) {
        targetEl.textContent = "Unknown";
        roomEl.textContent = "Unknown";
        hostEl.textContent = "-";
        fwEl.textContent = "-";
        if (pillRoomEl) pillRoomEl.textContent = "";
        if (subtitleEl) subtitleEl.textContent = "Summary";
        return;
    }
    var t = bedTargetsById[currentBedTargetId];
    targetEl.textContent = t.device_name || t.host || "Unknown";
    roomEl.textContent = t.room || "Unknown";
    hostEl.textContent = t.isLocal ? "local" : (t.host || "-");
    fwEl.textContent = t.fw || "-";
    if (pillRoomEl) {
        pillRoomEl.textContent = formatRoomShort(t.room);
    }
    if (subtitleEl) {
        subtitleEl.textContent = t.device_name || t.host || "Summary";
    }
}

function formatRoomShort(room) {
    if (!room) return "";
    var trimmed = String(room).trim();
    if (!trimmed || trimmed.toLowerCase() === "unknown") return "";
    if (trimmed.length <= 4) return trimmed.toUpperCase();
    var parts = trimmed.split(/\s+/).filter(Boolean);
    if (!parts.length) return "";
    var initials = parts.map(function(p){ return p[0]; }).join("").toUpperCase();
    return initials.slice(0, 4);
}

function setBedSummaryCollapsed(collapsed) {
    bedSummaryCollapsed = !!collapsed;
    var card = document.getElementById('bed-summary');
    if (card) {
        card.classList.toggle('is-collapsed', bedSummaryCollapsed);
    }
    var pill = document.querySelector('.bed-status-chip');
    if (pill) {
        pill.classList.toggle('is-open', !bedSummaryCollapsed);
    }
    try {
        localStorage.setItem('bedSummaryCollapsed', bedSummaryCollapsed ? '1' : '0');
    } catch (e) {}
}

function toggleBedSummary() {
    setBedSummaryCollapsed(!bedSummaryCollapsed);
}

function loadBedSummaryState() {
    try {
        var stored = localStorage.getItem('bedSummaryCollapsed');
        if (stored === null) {
            bedSummaryCollapsed = true;
        } else {
            bedSummaryCollapsed = stored === '1';
        }
    } catch (e) {
        bedSummaryCollapsed = true;
    }
    setBedSummaryCollapsed(bedSummaryCollapsed);
}

function formatSecondsShort(value) {
    var num = Math.round((parseFloat(value) || 0) * 10) / 10;
    var text = num.toFixed(1).replace(/\.0$/, "");
    return text + "s";
}

function updateBedSummaryStatus(isOnline) {
    var statusEl = document.getElementById('bed-pill-status');
    if (!statusEl) return;
    statusEl.textContent = isOnline ? "ON" : "OFF";
    statusEl.classList.toggle('is-offline', !isOnline);
}

function updateBedSummaryFromStatus(result) {
    var posEl = document.getElementById('bed-summary-positions');
    var motionEl = document.getElementById('bed-summary-motion');
    var uptimeEl = document.getElementById('bed-summary-uptime');
    var lastSeenEl = document.getElementById('bed-summary-last-seen');
    if (!posEl || !motionEl || !uptimeEl || !lastSeenEl) return;
    bedLastStatus.headPos = parseFloat(result.headPos) || 0;
    bedLastStatus.footPos = parseFloat(result.footPos) || 0;
    bedLastStatus.headDir = result.headDir || "STOPPED";
    bedLastStatus.footDir = result.footDir || "STOPPED";
    bedLastStatus.uptimeText = formatDuration(result.uptime || 0);
    bedLastStatus.lastSeenText = lastConnectedText || "-";
    posEl.textContent = "Head " + formatSecondsShort(bedLastStatus.headPos) + ", Foot " + formatSecondsShort(bedLastStatus.footPos);
    if (bedLastStatus.headDir === "STOPPED" && bedLastStatus.footDir === "STOPPED") {
        motionEl.textContent = "Idle";
    } else {
        motionEl.textContent = "Head " + bedLastStatus.headDir + ", Foot " + bedLastStatus.footDir;
    }
    uptimeEl.textContent = bedLastStatus.uptimeText || "-";
    lastSeenEl.textContent = bedLastStatus.lastSeenText || "-";
}

function setActiveModule(mod) {
    if (mod.startsWith('bed:')) {
        currentBedTargetId = mod;
        isFirstPoll = true;
        lastStatusOkTs = Date.now();
        offlineShown = false;
        updateBedTargetLabel();
        updateBedSummaryStatus(true);
        logUiEvent("Bed target set to " + mod);
    }
    currentModule = mod;
    updateTabVisibility();
}

function renderTabs() {
    var container = document.getElementById('tab-switch');
    if (!container) return;
    container.innerHTML = '';

    if (bedTargets.length > 0) {
        bedTargets.forEach(function(t){
            var btn = document.createElement('button');
            btn.className = 'tab-btn';
            btn.dataset.module = t.id;
            btn.innerHTML = '<i class="fas fa-bed"></i><span class="tab-label">' + targetLabel('bed', t) + '</span>';
            btn.addEventListener('click', function(){ setActiveModule(t.id); });
            if (currentModule === t.id) btn.classList.add('active');
            container.appendChild(btn);
        });
    }
    if (lightTargets.length > 0) {
        var lightBtn = document.createElement('button');
        lightBtn.className = 'tab-btn';
        lightBtn.dataset.module = 'light';
        lightBtn.innerHTML = '<i class="fas fa-lightbulb"></i><span class="tab-label">Lights</span>';
        lightBtn.addEventListener('click', function(){ setActiveModule('light'); });
        if (currentModule === 'light') lightBtn.classList.add('active');
        container.appendChild(lightBtn);
    }
}

function renderLightRooms() {
    var roomsEl = document.getElementById('light-rooms');
    var subtitleEl = document.getElementById('light-subtitle');
    if (!roomsEl) return;
    roomsEl.innerHTML = '';
    if (subtitleEl) {
        subtitleEl.textContent = lightTargets.length ? (lightTargets.length + " device(s)") : "No devices found";
    }
    if (!lightTargets.length) return;

    var groups = {};
    lightTargets.forEach(function(t){
        lightCacheKeyById[t.id] = getLightCacheKey(t);
        var room = t.room || "Unknown";
        if (!groups[room]) groups[room] = [];
        groups[room].push(t);
    });

    var template = document.getElementById('light-card-template');
    if (!template || !template.content) return;
    Object.keys(groups).sort().forEach(function(room){
        if (lightRoomFilter !== 'all' && room !== lightRoomFilter) return;
        var groupEl = document.createElement('div');
        groupEl.className = 'light-room-group';
        groupEl.dataset.room = room;
        if (lightRoomCollapsed[room]) {
            groupEl.classList.add('is-collapsed');
        }
        var headerEl = document.createElement('div');
        headerEl.className = 'light-room-header';
        var titleEl = document.createElement('div');
        titleEl.className = 'light-room-title';
        titleEl.textContent = "Room: " + room + " (" + groups[room].length + ")";
        var actionsEl = document.createElement('div');
        actionsEl.className = 'light-room-actions';
        var toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'light-room-action';
        toggleBtn.textContent = lightRoomCollapsed[room] ? 'Expand' : 'Collapse';
        toggleBtn.addEventListener('click', function() {
            lightRoomCollapsed[room] = !lightRoomCollapsed[room];
            renderLightRooms();
        });
        var allOffBtn = document.createElement('button');
        allOffBtn.type = 'button';
        allOffBtn.className = 'light-room-action';
        allOffBtn.dataset.action = 'all-off';
        allOffBtn.textContent = 'All Off';
        allOffBtn.addEventListener('click', function() {
            groups[room].forEach(function(t) { sendLightCmd('OFF', t.id); });
        });
        var allOnBtn = document.createElement('button');
        allOnBtn.type = 'button';
        allOnBtn.className = 'light-room-action';
        allOnBtn.dataset.action = 'all-on';
        allOnBtn.textContent = 'All On';
        allOnBtn.addEventListener('click', function() {
            groups[room].forEach(function(t) { sendLightCmd('ON', t.id); });
        });
        actionsEl.appendChild(toggleBtn);
        actionsEl.appendChild(allOffBtn);
        actionsEl.appendChild(allOnBtn);
        headerEl.appendChild(titleEl);
        headerEl.appendChild(actionsEl);
        groupEl.appendChild(headerEl);

        var gridEl = document.createElement('div');
        gridEl.className = 'light-room-grid';
        groups[room].forEach(function(t){
            var card = template.content.firstElementChild.cloneNode(true);
            card.dataset.id = t.id;
            card.dataset.cacheKey = lightCacheKeyById[t.id] || "";
            var title = card.querySelector('.light-device-title');
            var deviceName = card.querySelector('.light-device-name');
            var deviceHost = card.querySelector('.light-device-host');
            var deviceRoom = card.querySelector('.light-device-room');
            var deviceFw = card.querySelector('.light-device-fw');
            var toggleBtn = card.querySelector('.light-toggle-btn');
            var cardToggle = card.querySelector('.light-card-toggle');
            var brightnessSlider = card.querySelector('.light-brightness-slider');
            var brightnessValues = card.querySelectorAll('.light-brightness-value');
            var brightnessDown = card.querySelector('.light-brightness-step--down');
            var brightnessUp = card.querySelector('.light-brightness-step--up');
            var cacheKey = lightCacheKeyById[t.id] || getLightCacheKey(t);
            if (t.wiring_type) {
                var wiringFromPeer = normalizeLightWiring({ type: t.wiring_type });
                lightWiringByKey[cacheKey] = wiringFromPeer;
                applyLightWiringToCard(card, wiringFromPeer);
            }
            if (title) title.textContent = t.device_name || "Light";
            if (deviceName) deviceName.textContent = t.device_name || "Unknown";
            if (deviceHost) deviceHost.textContent = t.isLocal ? "local" : (t.host || "Unknown");
            if (deviceRoom) deviceRoom.textContent = t.room || "Unknown";
            if (deviceFw) deviceFw.textContent = t.fw || "Unknown";
            if (toggleBtn) toggleBtn.addEventListener('click', function(){
                lightCmdInFlightById[t.id] = true;
                toggleBtn.disabled = true;
                sendLightCmd('TOGGLE', t.id);
            });
            if (brightnessSlider) {
                brightnessSlider.value = 0;
                brightnessSlider.addEventListener('change', function(e){
                    var value = parseInt(e.target.value || "0", 10);
                    if (lightBrightnessDebounceById[t.id]) {
                        clearTimeout(lightBrightnessDebounceById[t.id]);
                        lightBrightnessDebounceById[t.id] = null;
                    }
                    sendLightBrightness(t.id, value);
                });
                brightnessSlider.addEventListener('input', function(e){
                    var value = parseInt(e.target.value || "0", 10);
                    if (brightnessValues && brightnessValues.length) {
                        brightnessValues.forEach(function(el){ el.textContent = value + "%"; });
                    }
                    updateLightStepDisabled(card, value, card.classList.contains('is-offline'));
                    queueLightBrightnessSend(t.id, value);
                });
            }
            if (brightnessDown) {
                brightnessDown.addEventListener('click', function() {
                    applyBrightnessStep(t.id, brightnessSlider, brightnessValues, -1);
                });
            }
            if (brightnessUp) {
                brightnessUp.addEventListener('click', function() {
                    applyBrightnessStep(t.id, brightnessSlider, brightnessValues, 1);
                });
            }
            if (lightCardCollapsedByKey[cacheKey] === undefined) {
                lightCardCollapsedByKey[cacheKey] = true;
            }
            if (cardToggle) {
                cardToggle.addEventListener('click', function() {
                    lightCardCollapsedByKey[cacheKey] = !lightCardCollapsedByKey[cacheKey];
                    card.classList.toggle('is-collapsed', lightCardCollapsedByKey[cacheKey]);
                    cardToggle.innerHTML = lightCardCollapsedByKey[cacheKey]
                        ? '<i class="fas fa-chevron-right"></i>'
                        : '<i class="fas fa-chevron-down"></i>';
                });
            }
            if (lightCardCollapsedByKey[cacheKey]) {
                card.classList.add('is-collapsed');
                if (cardToggle) cardToggle.innerHTML = '<i class="fas fa-chevron-right"></i>';
            } else if (cardToggle) {
                cardToggle.innerHTML = '<i class="fas fa-chevron-down"></i>';
            }
            if (brightnessValues && brightnessValues.length) {
                brightnessValues.forEach(function(el){ el.textContent = "0%"; });
            }
            updateLightStepDisabled(card, 0, false);
            gridEl.appendChild(card);
            updateLightCardState(
                t.id,
                '',
                'Ready',
                0,
                { skipLastSeen: true }
            );
            var wiring = getLightWiringForTarget(t.id);
            if (wiring) {
                applyLightWiringToCard(card, wiring);
            }
            ensureLightWiring(t);
        });
        groupEl.appendChild(gridEl);
        roomsEl.appendChild(groupEl);
    });
    updateLightStatusPill();
    updateLightRoomActionStates();
}

function renderLightFilters() {
    var filtersEl = document.getElementById('light-filters');
    if (!filtersEl) return;
    filtersEl.innerHTML = '';
    if (!lightTargets.length) return;

    var counts = {};
    lightTargets.forEach(function(t){
        var room = t.room || "Unknown";
        counts[room] = (counts[room] || 0) + 1;
    });
    if (lightRoomFilter !== 'all' && !counts[lightRoomFilter]) {
        lightRoomFilter = 'all';
    }
    var rooms = Object.keys(counts).sort();
    var allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = 'light-filter-chip' + (lightRoomFilter === 'all' ? ' active' : '');
    allBtn.textContent = 'All (' + lightTargets.length + ')';
    allBtn.addEventListener('click', function() {
        lightRoomFilter = 'all';
        renderLightFilters();
        renderLightRooms();
    });
    filtersEl.appendChild(allBtn);
    rooms.forEach(function(room){
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'light-filter-chip' + (lightRoomFilter === room ? ' active' : '');
        btn.textContent = room + ' (' + counts[room] + ')';
        btn.addEventListener('click', function() {
            lightRoomFilter = room;
            renderLightFilters();
            renderLightRooms();
        });
        filtersEl.appendChild(btn);
    });
}

function addLocalPeers(localInfo) {
    var localRoles = roles.slice();
    var deviceName = "Local";
    var room = "Local";
    var host = "";
    var infoRoles = "";
    if (localInfo) {
        if (typeof localInfo.roles === "string") infoRoles = localInfo.roles;
        if (!infoRoles && typeof localInfo.role === "string") infoRoles = localInfo.role;
        if (infoRoles) {
            localRoles = infoRoles.split(',').filter(Boolean);
        }
        deviceName = localInfo.device_name || deviceName;
        room = localInfo.room || room;
        host = localInfo.host || host;
    }
    localRoles.forEach(function(role){
        peerList.push({
            host: host,
            device_name: deviceName,
            room: room,
            fw: (localInfo && localInfo.fw) ? localInfo.fw : UI_BUILD_TAG,
            type: role,
            model: (localInfo && localInfo.model) ? localInfo.model : "local",
            wiring_type: (localInfo && localInfo.wiring_type) ? localInfo.wiring_type : "",
            roles: [role],
            isLocal: true
        });
    });
}

function setRefreshStatus(message, isError) {
    var el = document.getElementById('light-refresh-status');
    if (!el) return;
    if (!message) {
        el.textContent = '';
        el.classList.remove('error');
        return;
    }
    el.textContent = message;
    el.classList.toggle('error', !!isError);
    if (refreshStatusTimerId) clearTimeout(refreshStatusTimerId);
    refreshStatusTimerId = setTimeout(function() {
        el.textContent = '';
        el.classList.remove('error');
    }, 4000);
}

function refreshPeersInternal(opts) {
    opts = opts || {};
    if (opts.manual) {
        var now = Date.now();
        if (refreshInFlight || (now - lastManualRefreshTs) < refreshCooldownMs) {
            setRefreshStatus('Please wait...', true);
            return;
        }
        refreshInFlight = true;
        lastManualRefreshTs = now;
        setRefreshStatus('Refreshing...');
        if (opts.force) {
            lightRenderKey = '';
        }
    }
    var controller = new AbortController();
    setTimeout(function() { controller.abort(); }, 2000);
    var lookupHosts = [];

    fetch('/rpc/Peer.Lookup')
        .then(function(resp){ return resp.json(); })
        .then(function(list){
            console.log("Peer.Lookup response", list || []);
            peerList = [];

            if (Array.isArray(list)) {
                list.forEach(function(p){
                    var h = normalizePeerHost(p);
                    if (h) lookupHosts.push(h);
                    var peer = {
                        host: h,
                        device_name: p.device_name || p.host || h,
                        room: p.room || "Unknown",
                        fw: p.fw || "",
                        type: p.type || "",
                        model: p.model || "",
                        wiring_type: p.wiring_type || "",
                        roles: (p.roles ? p.roles.split(',').filter(Boolean) : [])
                    };
                    peerList.push(peer);
                });
            }

            return fetch('/rpc/Peer.Discover')
                .then(function(resp){ return resp.json(); })
                .catch(function(){
                    return null;
                })
                .then(function(localInfo){
                    // Add local roles as pseudo-peers for per-device tabs/tiles.
                    addLocalPeers(localInfo);
                });

        })
        .then(function(){
            autoPeerHosts = lookupHosts;
            var mergedCache = mergePeerCache(peerList);
            if (mergedCache.length) {
                peerList = mergedCache.map(cacheEntryToPeer).filter(Boolean);
            }
            buildTargetsFromPeers();
            ensureActiveModule();
            updateTabVisibility();
            if (hasLocalRole('light') && !lightWiringLoaded) {
                loadLightWiring();
            }
            var nextLightRenderKey = lightTargets.map(getLightCacheKey).sort().join(';');
            if (nextLightRenderKey !== lightRenderKey) {
                lightRenderKey = nextLightRenderKey;
                renderLightRooms();
            }
            renderLightFilters();
            updateBedTargetLabel();
            console.log("Peer poll result", { manualPeers: peerHosts, autoPeers: autoPeerHosts, bedTargets: bedTargets, lightTargets: lightTargets });
            logUiEvent("Peers: beds=" + bedTargets.length + " lights=" + lightTargets.length);
            if (opts.manual) {
                setRefreshStatus('Found ' + (bedTargets.length + lightTargets.length) + ' peer(s)');
                refreshInFlight = false;
            }
        })
        .catch(function(err){
            console.error("Peer poll error", err);
            applyCachedPeers();
            if (opts.manual) {
                setRefreshStatus('Using cached peers', true);
                refreshInFlight = false;
            }
        });
}

// Expose helpers immediately so console can call them
window.refreshPeers = function() { refreshPeersInternal({ manual: true, force: true }); };
window.setPeerHosts = setPeerHosts;
window.logPeers = function() {
    fetch('/rpc/Peer.Lookup').then(function(r){ return r.json(); }).then(function(list){
        console.log("Peer.Lookup direct", list);
    }).catch(function(err){ console.error("Peer.Lookup error", err); });
};

var pressStartTime = 0;
var activeCommand = "";
var presetTimerId = null; 
var presetData = {}; 
var currentLiveHeadMs = 0; 
var currentLiveFootMs = 0; 
var modalCurrentSlot = 'zg'; 
var currentStyle = 'style-b';
var brandingData = null;
var currentBrandKey = 'homeyantric';
function hasLocalRole(r) { return roles.indexOf(r) !== -1; }
function isRoleAvailable(r) {
    if (r === 'bed') return bedTargets.length > 0;
    if (r === 'light') return lightTargets.length > 0;
    return hasLocalRole(r);
}
var currentModule = hasLocalRole('bed') ? 'bed:local' : (hasLocalRole('light') ? 'light' : 'bed:local');
var lightPollTimer = null;
var lastStatusOkTs = Date.now();
var offlineThresholdMs = 5000;
var offlineShown = false;
var lastConnectedText = "";
var holdThresholdMs = 400;
var holdPressStartTs = 0;
var holdActive = false;
var stopBtnEl = null;
var activeMotionBtn = null;
var activeMotionCmd = null;
var lastPointerType = '';
var lastPointerTime = 0;
var duplicatePointerWindowMs = 600;
var lightLastSeenById = {};
var lightCacheKeyById = {};
var lightRenderKey = "";
var lightLastKnownStateById = {};
var lightOfflineThresholdMs = 5000;
var lightStatusTimeoutMs = 3000;
var lightStateStreakById = {};
var lightRoomFilter = 'all';
var lightRoomCollapsed = {};
var lightCardCollapsedByKey = {};
var lightBrightnessDebounceById = {};
var lightCmdInFlightById = {};
var lightWiringByKey = {};
var lightWiringFetchInFlightByKey = {};
var lightWiringFetchTsByKey = {};
var lightWiringStaleMs = 5 * 60 * 1000;
var lightControlsLocked = false;
var lightWiringLoaded = false;
var lightWiringConfigured = null;
var LIGHT_WIRING_OPTIONS = [
    { type: '2wire-dim', label: '2-wire Dimmable (single)', terminals: 'V+ / CH1', channels: 1, uiMode: 'single' },
    { type: '2wire-cct-tied', label: '2-wire CCT (tied warm/cool)', terminals: 'V+ / CH1 (CW+WW)', channels: 1, uiMode: 'single' },
    { type: '3wire-cct', label: '3-wire CCT (warm + cool)', terminals: 'V+ / CH1 (CW) / CH2 (WW)', channels: 2, uiMode: 'cct' },
    { type: '4wire-rgb', label: '4-wire RGB', terminals: 'V+ / CH1 (R) / CH2 (G) / CH3 (B)', channels: 3, uiMode: 'rgb' },
    { type: '5wire-rgbw', label: '5-wire RGBW', terminals: 'V+ / CH1 (R) / CH2 (G) / CH3 (B) / CH4 (W)', channels: 4, uiMode: 'rgbw' },
    { type: '6wire-rgbcw', label: '6-wire RGB + CW + WW', terminals: 'V+ / CH1 (R) / CH2 (G) / CH3 (B) / CH4 (CW) / CH5 (WW)', channels: 5, uiMode: 'rgbcw' },
    { type: 'generic-6ch', label: 'Generic multi-channel (5 outputs)', terminals: 'V+ / CH1 / CH2 / CH3 / CH4 / CH5', channels: 5, uiMode: 'multi-channel' }
];
applyCachedPeers();
var refreshInFlight = false;
var lastManualRefreshTs = 0;
var refreshCooldownMs = 5000;
var refreshStatusTimerId = null;
function isPeerStale(lastSeen) {
    if (!lastSeen) return true;
    return (Date.now() - lastSeen) > PEER_STALE_MS;
}
function getLightCacheKey(target) {
    var name = (target.device_name || target.host || "unknown").toLowerCase();
    var room = (target.room || "unknown").toLowerCase();
    var role = (target.role || "light").toLowerCase();
    return role + "|" + name + "|" + room;
}
function getLightWiringOption(type) {
    return LIGHT_WIRING_OPTIONS.find(function(opt){ return opt.type === type; }) || null;
}
function normalizeLightWiring(data) {
    if (!data || !data.type) {
        var fallback = getLightWiringOption('2wire-dim') || LIGHT_WIRING_OPTIONS[0];
        return Object.assign({}, fallback, { version: 1, configured: false });
    }
    var option = getLightWiringOption(data.type) || getLightWiringOption('2wire-dim') || LIGHT_WIRING_OPTIONS[0];
    return {
        type: option.type,
        label: data.label || option.label,
        terminals: data.terminals || option.terminals,
        channels: typeof data.channels === 'number' ? data.channels : option.channels,
        uiMode: data.ui_mode || option.uiMode,
        version: data.version || 1,
        configured: (data.configured !== undefined) ? !!data.configured : true
    };
}
function applyLightWiringToCard(card, wiring) {
    if (!card || !wiring) return;
    var wiringSummary = card.querySelector('.light-wiring-summary');
    var wiringTerminals = card.querySelector('.light-wiring-terminals');
    var brightnessLabel = card.querySelector('.light-brightness-label');
    var wiringBadge = card.querySelector('.light-wiring-badge');
    if (wiringSummary) wiringSummary.textContent = wiring.label || 'Unknown';
    if (wiringTerminals) wiringTerminals.textContent = wiring.terminals || '-';
    if (brightnessLabel) {
        brightnessLabel.textContent = (wiring.channels && wiring.channels > 1) ? 'Master' : 'Brightness';
    }
    if (wiringBadge) wiringBadge.textContent = wiring.label || wiring.type || 'Wiring';
}
function getLightWiringForTarget(targetId) {
    var cacheKey = lightCacheKeyById[targetId] || targetId;
    return lightWiringByKey[cacheKey] || null;
}
function updateLightWiringDetails(wiring) {
    var terminalsEl = document.getElementById('light-wiring-terminals');
    var channelsEl = document.getElementById('light-wiring-channels');
    if (terminalsEl) terminalsEl.textContent = wiring.terminals || '-';
    if (channelsEl) channelsEl.textContent = (typeof wiring.channels === 'number') ? String(wiring.channels) : '-';
}
function setLightWiringStatus(message, isError) {
    var el = document.getElementById('light-wiring-status');
    if (!el) return;
    el.textContent = message || '';
    el.classList.toggle('error', !!isError);
}
function populateLightWiringSelect(selectedType) {
    var select = document.getElementById('light-wiring-select');
    if (!select) return;
    select.innerHTML = '';
    LIGHT_WIRING_OPTIONS.forEach(function(opt) {
        var optionEl = document.createElement('option');
        optionEl.value = opt.type;
        optionEl.textContent = opt.label;
        select.appendChild(optionEl);
    });
    if (selectedType) select.value = selectedType;
    select.onchange = function() {
        var chosen = getLightWiringOption(select.value);
        if (chosen) {
            updateLightWiringDetails(chosen);
        }
    };
}
function populateLightWiringGateSelect(selectedType) {
    var select = document.getElementById('light-wiring-gate-select');
    if (!select) return;
    select.innerHTML = '';
    LIGHT_WIRING_OPTIONS.forEach(function(opt) {
        var optionEl = document.createElement('option');
        optionEl.value = opt.type;
        optionEl.textContent = opt.label;
        select.appendChild(optionEl);
    });
    if (selectedType) select.value = selectedType;
    select.onchange = function() {
        var chosen = getLightWiringOption(select.value);
        if (chosen) {
            updateLightWiringGateDetails(chosen);
        }
    };
}
function loadLightWiring() {
    populateLightWiringSelect();
    setLightWiringStatus('');
    fetch('/rpc/Light.Wiring')
        .then(function(resp){ return resp.json(); })
        .then(function(res){
            var wiring = normalizeLightWiring(res);
            lightWiringConfigured = wiring.configured;
            populateLightWiringSelect(wiring.type);
            updateLightWiringDetails(wiring);
            lightTargets.forEach(function(t) {
                if (t.isLocal) {
                    var key = lightCacheKeyById[t.id] || getLightCacheKey(t);
                    lightWiringByKey[key] = wiring;
                    var card = document.querySelector('.light-card--device[data-id="' + t.id + '"]');
                    if (card) applyLightWiringToCard(card, wiring);
                }
            });
            lightWiringLoaded = true;
            updateLightWiringGate(wiring);
        })
        .catch(function(){
            setLightWiringStatus('Failed to load wiring', true);
        });
}
function saveLightWiring() {
    var select = document.getElementById('light-wiring-select');
    if (!select) return;
    var type = select.value;
    setLightWiringStatus('Saving...');
    fetch('/rpc/Light.Wiring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: type })
    })
        .then(function(resp){ return resp.json(); })
        .then(function(res){
            var wiring = normalizeLightWiring(res);
            lightWiringConfigured = true;
            setLightWiringStatus('Saved');
            populateLightWiringSelect(wiring.type);
            updateLightWiringDetails(wiring);
            var cacheKey = getLightCacheKey({ device_name: 'local', room: 'local', role: 'light' });
            lightWiringByKey[cacheKey] = wiring;
            lightTargets.forEach(function(t) {
                if (t.isLocal) {
                    var key = lightCacheKeyById[t.id] || getLightCacheKey(t);
                    lightWiringByKey[key] = wiring;
                    var card = document.querySelector('.light-card--device[data-id="' + t.id + '"]');
                    if (card) applyLightWiringToCard(card, wiring);
                }
            });
            updateLightWiringGate(wiring);
        })
        .catch(function(){
            setLightWiringStatus('Save failed', true);
        });
}
function updateLightWiringGateDetails(wiring) {
    var terminalsEl = document.getElementById('light-wiring-gate-terminals');
    var channelsEl = document.getElementById('light-wiring-gate-channels');
    if (terminalsEl) terminalsEl.textContent = wiring.terminals || '-';
    if (channelsEl) {
        var count = (typeof wiring.channels === 'number') ? (wiring.channels + 1) : '-';
        channelsEl.textContent = count === '-' ? '-' : (count + "-wire");
    }
}
function setLightWiringGateStatus(message, isError) {
    var el = document.getElementById('light-wiring-gate-status');
    if (!el) return;
    el.textContent = message || '';
    el.classList.toggle('error', !!isError);
}
function updateLightWiringGate(wiring) {
    var gate = document.getElementById('light-wiring-gate');
    if (!gate) return;
    var localTarget = lightTargets.find(function(t){ return t.isLocal; });
    var configured = wiring ? wiring.configured : true;
    if (lightWiringConfigured !== null) {
        configured = lightWiringConfigured;
    }
    var shouldGate = !!localTarget && configured === false;
    lightControlsLocked = shouldGate;
    gate.classList.toggle('hidden', !shouldGate);
    if (shouldGate) {
        populateLightWiringGateSelect(wiring.type);
        updateLightWiringGateDetails(wiring);
    } else {
        setLightWiringGateStatus('');
    }
    renderLightRooms();
}
function saveLightWiringGate() {
    var select = document.getElementById('light-wiring-gate-select');
    if (!select) return;
    var type = select.value;
    setLightWiringGateStatus('Saving...');
    fetch('/rpc/Light.Wiring', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: type })
    })
        .then(function(resp){ return resp.json(); })
        .then(function(res){
            var wiring = normalizeLightWiring(res);
            wiring.configured = true;
            lightWiringConfigured = true;
            setLightWiringGateStatus('Saved');
            updateLightWiringGate(wiring);
            populateLightWiringSelect(wiring.type);
            updateLightWiringDetails(wiring);
            lightTargets.forEach(function(t) {
                if (t.isLocal) {
                    var key = lightCacheKeyById[t.id] || getLightCacheKey(t);
                    lightWiringByKey[key] = wiring;
                }
            });
        })
        .catch(function(){
            setLightWiringGateStatus('Save failed', true);
        });
}
function ensureLightWiring(target) {
    if (!target) return;
    var cacheKey = lightCacheKeyById[target.id] || getLightCacheKey(target);
    var lastFetch = lightWiringFetchTsByKey[cacheKey] || 0;
    if (lightWiringByKey[cacheKey] && (Date.now() - lastFetch) < lightWiringStaleMs) return;
    if (lightWiringFetchInFlightByKey[cacheKey]) return;
    lightWiringFetchInFlightByKey[cacheKey] = true;
    var base = getLightBaseUrl(target);
    fetch(base + '/rpc/Light.Wiring')
        .then(function(resp){ return resp.json(); })
        .then(function(res){
            var wiring = normalizeLightWiring(res);
            lightWiringByKey[cacheKey] = wiring;
            lightWiringFetchTsByKey[cacheKey] = Date.now();
            var card = document.querySelector('.light-card--device[data-id="' + target.id + '"]');
            if (!card && cacheKey) {
                card = document.querySelector('.light-card--device[data-cache-key="' + cacheKey + '"]');
            }
            if (card) applyLightWiringToCard(card, wiring);
        })
        .catch(function(){})
        .finally(function(){
            lightWiringFetchInFlightByKey[cacheKey] = false;
        });
}
function stepBrightness(value, direction) {
    var current = isNaN(value) ? 0 : value;
    if (direction > 0) {
        if (current >= 100) return 100;
        if (current % 10 === 0) return Math.min(100, current + 10);
        return Math.min(100, Math.ceil(current / 10) * 10);
    }
    if (current <= 0) return 0;
    if (current % 10 === 0) return Math.max(0, current - 10);
    return Math.max(0, Math.floor(current / 10) * 10);
}
function applyBrightnessStep(targetId, slider, values, direction) {
    if (!slider) return;
    var current = parseInt(slider.value || "0", 10);
    var next = stepBrightness(current, direction);
    slider.value = String(next);
    if (values && values.length) {
        values.forEach(function(el){ el.textContent = next + "%"; });
    }
    updateLightStepDisabled(slider.closest('.light-card--device'), next, false);
    sendLightBrightness(targetId, next);
}
function updateLightStepDisabled(card, brightness, isOffline) {
    if (!card) return;
    var down = card.querySelector('.light-brightness-step--down');
    var up = card.querySelector('.light-brightness-step--up');
    var value = typeof brightness === 'number' ? brightness : 0;
    if (down) down.disabled = !!isOffline || value <= 0;
    if (up) up.disabled = !!isOffline || value >= 100;
}
function queueLightBrightnessSend(targetId, value) {
    if (!isRoleAvailable('light')) return;
    if (lightBrightnessDebounceById[targetId]) {
        clearTimeout(lightBrightnessDebounceById[targetId]);
    }
    lightBrightnessDebounceById[targetId] = setTimeout(function() {
        lightBrightnessDebounceById[targetId] = null;
        sendLightBrightness(targetId, value);
    }, 160);
}
function updateLightStatusPill() {
    var pill = document.getElementById('light-status-pill');
    if (!pill) return;
    if (currentModule !== 'light' || !lightTargets.length) {
        pill.classList.add('hidden');
        return;
    }
    var countEl = document.getElementById('light-pill-count');
    var roomsEl = document.getElementById('light-pill-rooms');
    var dotEl = document.getElementById('light-pill-dot');
    var now = Date.now();
    var online = 0;
    var rooms = {};
    lightTargets.forEach(function(t) {
        var cacheKey = lightCacheKeyById[t.id] || getLightCacheKey(t);
        var lastSeen = lightLastSeenById[cacheKey] || t.last_seen || 0;
        var isOnline = lastSeen && (now - lastSeen) <= lightOfflineThresholdMs;
        if (isOnline) online += 1;
        rooms[(t.room || "Unknown").toLowerCase()] = true;
    });
    var total = lightTargets.length;
    var roomCount = Object.keys(rooms).length;
    if (countEl) countEl.textContent = "Lights " + online + "/" + total;
    if (roomsEl) roomsEl.textContent = "Rooms " + roomCount;
    if (dotEl) dotEl.classList.toggle('is-warning', online < total);
    pill.classList.remove('hidden');
}
function getLightRoomSummary(room) {
    var roomTargets = lightTargets.filter(function(t){ return (t.room || "Unknown") === room; });
    var states = roomTargets.map(function(t) {
        var cacheKey = lightCacheKeyById[t.id] || getLightCacheKey(t);
        return (lightLastKnownStateById[cacheKey] || "").toLowerCase();
    });
    var allOn = states.length > 0 && states.every(function(s){ return s === 'on'; });
    var allOff = states.length > 0 && states.every(function(s){ return s === 'off'; });
    return { allOn: allOn, allOff: allOff };
}
function updateLightRoomActionStates() {
    var groups = document.querySelectorAll('.light-room-group');
    groups.forEach(function(group) {
        var room = group.dataset.room;
        if (!room) return;
        var summary = getLightRoomSummary(room);
        var allOnBtn = group.querySelector('.light-room-action[data-action="all-on"]');
        var allOffBtn = group.querySelector('.light-room-action[data-action="all-off"]');
        if (allOnBtn) allOnBtn.disabled = lightControlsLocked || summary.allOn;
        if (allOffBtn) allOffBtn.disabled = lightControlsLocked || summary.allOff;
    });
}
var runningPreset = null; // {slot, headTargetMs, footTargetMs}
var prevHeadSec = 0;
var prevFootSec = 0;
var lastHeadMoveTs = 0;
var lastFootMoveTs = 0;
var motionTimerId = null; // auto-stop for manual motions
var lastHeadActive = false;
var lastFootActive = false;
var motionCmds = ["HEAD_UP","HEAD_DOWN","FOOT_UP","FOOT_DOWN","ALL_UP","ALL_DOWN"];
var lastHeadDir = "STOPPED";
var lastFootDir = "STOPPED";
var prevRelayHeadDir = "STOPPED";
var prevRelayFootDir = "STOPPED";
var optoPins = [35, 36, 37, 38];
var lastOptoStates = [1, 1, 1, 1];
function getBedBaseUrl() {
    if (!currentBedTargetId || !bedTargetsById[currentBedTargetId]) return '';
    var target = bedTargetsById[currentBedTargetId];
    if (target.isLocal || !target.host) return '';
    if (target.host.startsWith('http://') || target.host.startsWith('https://')) return target.host;
    return 'http://' + target.host;
}

function getLightBaseUrl(target) {
    if (!target || !target.host || target.isLocal) return '';
    if (target.host.startsWith('http://') || target.host.startsWith('https://')) return target.host;
    return 'http://' + target.host;
}
function isMotionCommand(cmd) {
    return motionCmds.indexOf(cmd) !== -1;
}

function computeRemainingMs(cmd) {
    var headMaxMs = headMaxSec * 1000;
    var footMaxMs = footMaxSec * 1000;
    var remMs = 0;
    if (cmd === "HEAD_UP") remMs = Math.max(0, headMaxMs - currentLiveHeadMs);
    else if (cmd === "HEAD_DOWN") remMs = Math.max(0, currentLiveHeadMs);
    else if (cmd === "FOOT_UP") remMs = Math.max(0, footMaxMs - currentLiveFootMs);
    else if (cmd === "FOOT_DOWN") remMs = Math.max(0, currentLiveFootMs);
    else if (cmd === "ALL_UP") remMs = Math.max(Math.max(0, headMaxMs - currentLiveHeadMs), Math.max(0, footMaxMs - currentLiveFootMs));
    else if (cmd === "ALL_DOWN") remMs = Math.max(Math.max(0, currentLiveHeadMs), Math.max(0, footMaxMs - currentLiveFootMs));
    return remMs;
}

var headMaxSec = 28;
var footMaxSec = 43;
const SVG_VIEWBOX_TRAVEL_HEIGHT = 108; 
const FRAME_Y_POSITION = 140; 
const MATTRESS_Y_BASE = 116; 
const HEAD_X_START = 0;
const HEAD_X_END = 120;
const GAP_X_START = 120;
const GAP_X_END = 170;
const FOOT_TRIANGLE_X_START = 170;
const FOOT_TRIANGLE_X_END = 260; 
const FOOT_BAR_X_START = 260;
const FOOT_BAR_X_END = 350; 

const PRESET_DEFAULTS = {
    'zg': { head: 10000, foot: 40000, label: "Zero G" },
    'snore': { head: 10000, foot: 0, label: "Anti-Snore" },
    'legs': { head: 0, foot: 43000, label: "Legs Up" },
    'p1': { head: 0, foot: 0, label: "P1" },
    'p2': { head: 0, foot: 0, label: "P2" }
};
const PRESET_CMD_MAP = {
    "ZERO_G": "zg",
    "ANTI_SNORE": "snore",
    "LEGS_UP": "legs",
    "P1": "p1",
    "P2": "p2",
    "FLAT": "flat",
    "MAX": "max"
};

function formatBootTime(timestamp) {
    try {
        var date = new Date(timestamp * 1000);
        var options = {
            month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', hour12: true
        };
        return date.toLocaleString(undefined, options);
    } catch (e) {
        console.error("Error formatting date:", e);
        return "Unknown";
    }
}

function formatDuration(totalSeconds) {
    try {
        var days = Math.floor(totalSeconds / 86400);
        totalSeconds %= 86400;
        var hours = Math.floor(totalSeconds / 3600);
        totalSeconds %= 3600;
        var minutes = Math.floor(totalSeconds / 60);
        var seconds = Math.floor(totalSeconds % 60);
        var parts = [];
        if (days > 0) parts.push(days + "d");
        if (hours > 0 || parts.length) parts.push(hours + "h");
        if (minutes > 0 || parts.length) parts.push(minutes + "m");
        parts.push(seconds + "s");
        return parts.join("");
    } catch (e) {
        return "0s";
    }
}

function showOfflineOverlay() {
    if (currentModule === 'light') return;
    var overlay = document.getElementById('offline-overlay');
    if (overlay) {
        overlay.classList.remove('hidden');
        offlineShown = true;
        var lastEl = document.getElementById('offline-last-connected');
        if (lastEl) lastEl.textContent = lastConnectedText ? ("Last connected: " + lastConnectedText) : "";
    }
    updateBedSummaryStatus(false);
}
function hideOfflineOverlay() {
    var overlay = document.getElementById('offline-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        offlineShown = false;
    }
    updateBedSummaryStatus(true);
}
function syncOfflineOverlay() {
    if (currentModule === 'light') {
        hideOfflineOverlay();
        return;
    }
    if (offlineShown) {
        showOfflineOverlay();
    }
}
function checkOffline() {
    if (offlineShown) return;
    if (currentModule === 'light') return;
    var delta = Date.now() - lastStatusOkTs;
    if (delta > offlineThresholdMs) {
        showOfflineOverlay();
    }
}

function calculateIconPoints(headPos, footPos) {
    var base_y = 14; 
    var travel_y = 10; 
    var h_end = 10;
    var g_start = 10;
    var g_end = 14;
    var f_tri_start = 14;
    var f_tri_end = 20;
    var f_bar_start = 20;
    var f_bar_end = 24;
    var headPercent = (headPos / (headMaxSec * 1000)) * 100;
    var footPercent = (footPos / (footMaxSec * 1000)) * 100;
    headPercent = Math.max(0, Math.min(100, headPercent));
    footPercent = Math.max(0, Math.min(100, footPercent));
    var headY = base_y - (travel_y * (headPercent / 100));
    var footY = base_y - (travel_y * (footPercent / 100) * 0.5);
    var points = '0,' + headY + ' ' + h_end + ',' + base_y + ' ' + g_start + ',' + base_y + ' ' + g_end + ',' + base_y + ' ' + f_tri_start + ',' + base_y + ' ' + f_tri_end + ',' + footY + ' ' + f_bar_start + ',' + footY + ' ' + f_bar_end + ',' + footY;
    return points;
}

function updatePresetButton(slot, headPos, footPos, label) {
    var btnLabelEl, iconLineEl;
    var defaultLabel = slot.toUpperCase(); 
    if (slot === 'p1') { btnLabelEl = document.getElementById('p1-label-text'); iconLineEl = document.getElementById('p1-icon-line'); }
    else if (slot === 'p2') { btnLabelEl = document.getElementById('p2-label-text'); iconLineEl = document.getElementById('p2-icon-line'); }
    else if (slot === 'zg') { btnLabelEl = document.getElementById('zg-label-text'); iconLineEl = document.getElementById('zg-icon-line'); }
    else if (slot === 'snore') { btnLabelEl = document.getElementById('snore-label-text'); iconLineEl = document.getElementById('snore-icon-line'); }
    else if (slot === 'legs') { btnLabelEl = document.getElementById('legs-label-text'); iconLineEl = document.getElementById('legs-icon-line'); }
    else { return; }
    if (!btnLabelEl || !iconLineEl) return;
    label = (label || defaultLabel); 
    btnLabelEl.textContent = label;
    var points = calculateIconPoints(headPos || 0, footPos || 0);
    iconLineEl.setAttribute('points', points);
    if (!presetData[slot]) presetData[slot] = {};
    presetData[slot].label = label;
    presetData[slot].head = headPos || 0;
    presetData[slot].foot = footPos || 0;
}

function updateStatusDisplay(data) { 
    var statusEl1 = document.getElementById("status-line-1");
    var statusEl2 = document.getElementById("status-line-2"); 

    lastStatusOkTs = Date.now();
    lastConnectedText = new Date(lastStatusOkTs).toLocaleString();
    hideOfflineOverlay();
    updateBedSummaryStatus(true);

    if (typeof data.headMax === 'number') headMaxSec = data.headMax;
    if (typeof data.footMax === 'number') footMaxSec = data.footMax;
    updateLimitInputs(false);
    if (typeof window.setTravelLimits === 'function') {
        window.setTravelLimits(headMaxSec, footMaxSec);
    }

    var formattedTime = formatBootTime(data.bootTime);
    var formattedDuration = formatDuration(data.uptime); 
    if (statusEl1) statusEl1.textContent = "";
    var durText = document.getElementById("status-duration-text");
    if (durText) durText.textContent = formattedDuration;
    
    var headPosNum = parseFloat(data.headPos) || 0;
    var footPosNum = parseFloat(data.footPos) || 0;
    if (typeof data.headDir === 'string') lastHeadDir = data.headDir;
    if (typeof data.footDir === 'string') lastFootDir = data.footDir;
    currentLiveHeadMs = headPosNum * 1000;
    currentLiveFootMs = footPosNum * 1000;
    var nowTs = Date.now();
    var headDelta = Math.abs(headPosNum - prevHeadSec);
    var footDelta = Math.abs(footPosNum - prevFootSec);
    var headMoving = headDelta > 0.01; // ~10ms movement delta
    var footMoving = footDelta > 0.01;
    if (headMoving) lastHeadMoveTs = nowTs;
    if (footMoving) lastFootMoveTs = nowTs;
    prevHeadSec = headPosNum;
    prevFootSec = footPosNum;

    var headActive = headMoving || (nowTs - lastHeadMoveTs < 700);
    var footActive = footMoving || (nowTs - lastFootMoveTs < 700);
    lastHeadActive = headActive;
    lastFootActive = footActive;

    if (typeof window.updateBedVisualizer === 'function') {
        window.updateBedVisualizer(headPosNum, footPosNum, headActive, footActive);
    }
    updateBedSummaryFromStatus(data);
    var optoValues = [data.opto1, data.opto2, data.opto3, data.opto4];
    for (var i = 0; i < optoValues.length; i++) {
        if (typeof optoValues[i] !== 'number') continue;
        if (lastOptoStates[i] === 1 && optoValues[i] === 0) {
            console.log("Opto GPIO " + optoPins[i] + " active (remote press)");
        }
        lastOptoStates[i] = optoValues[i];
    }

    if (runningPreset) {
        var toleranceMs = 200; // allow small drift
        var headMs = currentLiveHeadMs;
        var footMs = currentLiveFootMs;
        var headDone = Math.abs(headMs - runningPreset.headTargetMs) <= toleranceMs;
        var footDone = Math.abs(footMs - runningPreset.footTargetMs) <= toleranceMs;
        if (headDone && footDone) {
            clearRunningPresets();
            setStopHighlight(false);
            clearMotionHighlight();
            runningPreset = null;
        }
    }
}

function clearRunningPresets() {
    var allPresets = document.querySelectorAll('.preset-btn.btn-running');
    for (var i = 0; i < allPresets.length; i++) {
        allPresets[i].classList.remove('btn-running');
    }
    runningPreset = null;
}

function setStopHighlight(on) {
    if (!stopBtnEl) return;
    if (on) stopBtnEl.classList.add('btn-running');
    else stopBtnEl.classList.remove('btn-running');
}

function setMotionHighlight(btn, cmd) {
    if (activeMotionBtn && activeMotionBtn !== btn) {
        activeMotionBtn.classList.remove('btn-active-motion');
    }
    activeMotionBtn = btn;
    activeMotionCmd = cmd || null;
    if (activeMotionBtn) activeMotionBtn.classList.add('btn-active-motion');
}

function clearMotionHighlight() {
    if (activeMotionBtn) {
        activeMotionBtn.classList.remove('btn-active-motion');
        activeMotionBtn = null;
        activeMotionCmd = null;
    }
}

function handlePressStart(cmd, btnEl, source) {
    var now = Date.now();
    if (source === 'mouse' && lastPointerType === 'touch' && (now - lastPointerTime) < duplicatePointerWindowMs) {
        return; // ignore synthetic mouse after touch
    }
    lastPointerType = source || '';
    lastPointerTime = now;
    // Toggle: if same button pressed while active, issue STOP and return
    if (activeMotionBtn && btnEl && activeMotionBtn === btnEl) {
        stopCmd(true);
        holdActive = false;
        return;
    }
    holdPressStartTs = Date.now();
    holdActive = true;
    var isMotion = isMotionCommand(cmd);
    if (!isMotion) setStopHighlight(true);
    if (btnEl) setMotionHighlight(btnEl, cmd);
    logUiEvent("UI pressStart cmd=" + cmd + " source=" + (source||""));
    sendCmd(cmd, btnEl);
}

function handlePressEnd(source) {
    var now = Date.now();
    if (source === 'mouse' && lastPointerType === 'touch' && (now - lastPointerTime) < duplicatePointerWindowMs) {
        return; // ignore synthetic mouse after touch
    }
    if (!holdActive) return;
    var dur = now - holdPressStartTs;
    holdActive = false;
    if (dur >= holdThresholdMs) {
        stopCmd(true);
    } else {
        // Single tap on motion: ensure stop pulsing
        if (activeMotionBtn) setStopHighlight(true);
        if (activeMotionCmd && isMotionCommand(activeMotionCmd)) {
            if (motionTimerId) { clearTimeout(motionTimerId); motionTimerId = null; }
            var rem = computeRemainingMs(activeMotionCmd);
            var bufferMs = 1500;
            if (rem > 0) {
                motionTimerId = setTimeout(function() { stopCmd(false); }, rem + bufferMs);
            } else {
                motionTimerId = setTimeout(function() { stopCmd(false); }, 200);
            }
        }
    }
    logUiEvent("UI pressEnd duration=" + dur + "ms");
}

function sendCmd(cmd, btnElement, label, extraData) {
    console.log("Sent: " + cmd);
    var presetCmds = ["ZERO_G", "FLAT", "ANTI_SNORE", "LEGS_UP", "P1", "P2", "MAX"];
    var isPreset = presetCmds.indexOf(cmd) > -1;

    // Toggle behavior: if a preset is already running and pressed again, stop
    if (isPreset && btnElement && btnElement.classList.contains('btn-running')) {
        stopCmd(true);
        return;
    }

    clearRunningPresets(); 
    if (motionTimerId) { clearTimeout(motionTimerId); motionTimerId = null; }
    var motionCmd = isMotionCommand(cmd);
    if (cmd !== "STOP") {
        if (!motionCmd || !holdActive) setStopHighlight(true);
        if (btnElement) setMotionHighlight(btnElement, cmd);
    }

    if (cmd !== "STOP" && !cmd.startsWith('FLAT') && !cmd.startsWith('SET_') && !cmd.startsWith('RESET_') &&    
        !cmd.startsWith('ZERO_G') && !cmd.startsWith('ANTI_SNORE') && !cmd.startsWith('LEGS_UP') && !cmd.startsWith('P1') && !cmd.startsWith('P2') &&
        !cmd.startsWith('MAX')) { 
        pressStartTime = Date.now();
        activeCommand = cmd;
    }

    if (btnElement) {
        btnElement.classList.add('btn-running'); 
        if (isPreset) {
            var slot = PRESET_CMD_MAP[cmd] || cmd.toLowerCase();
            var headT = 0, footT = 0;
            if (presetData[slot]) {
                headT = presetData[slot].head || 0;
                footT = presetData[slot].foot || 0;
            } else if (slot === 'flat') {
                headT = 0; footT = 0;
            } else if (slot === 'max') {
                headT = headMaxSec * 1000;
                footT = footMaxSec * 1000;
            }
            runningPreset = { slot: slot, headTargetMs: headT, footTargetMs: footT };
        }
    }
    
    var body = { cmd: cmd };
    if (label !== undefined) body.label = label;
    if (extraData) { Object.assign(body, extraData); }
    
    var base = getBedBaseUrl();
    fetch(base + '/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        var result = status.result || status;
        updateStatusDisplay(result);

        var slotToUpdate = null;
        if (result.saved_pos) slotToUpdate = result.saved_pos;
        if (result.saved_label) slotToUpdate = result.saved_label;
        if (result.reset) slotToUpdate = result.reset;

        if (slotToUpdate) {
            updatePresetButton(slotToUpdate, result[slotToUpdate+'_head'], result[slotToUpdate+'_foot'], result[slotToUpdate+'_label']);
            updateModalDropdown();
        }

        if (isPreset) {
            var maxWait = parseInt(result.maxWait) || 0;
            if (maxWait > 0) {
                var waitMs = maxWait + 1500;
                if (presetTimerId) clearTimeout(presetTimerId);
                presetTimerId = setTimeout(function() { stopCmd(false); }, waitMs);
            } else {
                clearRunningPresets();
            }
        }
    })
    .catch(function(error) {
        console.error("Fetch error for " + cmd + ":", error);
        clearRunningPresets(); 
        runningPreset = null;
        setStopHighlight(false);
    });
}

function stopCmd(isManualPress) {
    if (presetTimerId) { clearTimeout(presetTimerId); presetTimerId = null; }
    if (motionTimerId) { clearTimeout(motionTimerId); motionTimerId = null; }
    clearRunningPresets();
    setStopHighlight(false);
    clearMotionHighlight();
    if (relayLogEnabled) logUiEvent("UI STOP reason=" + (isManualPress ? "manual" : "auto"));

    if (pressStartTime !== 0 && activeCommand !== "") {
        pressStartTime = 0;
        activeCommand = "";
    }
    var base = getBedBaseUrl();
    fetch(base + '/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'ContentType': 'application/json' },
        body: JSON.stringify({ cmd: 'STOP' }) 
    })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        var result = status.result || status; 
        updateStatusDisplay(result);
    });
}

function logUiAndMotion() {
    if (!relayLogEnabled) return;
    var headState = lastHeadActive ? "moving" : "stopped";
    var footState = lastFootActive ? "moving" : "stopped";
    // Only log when relays are active
    if (lastHeadDir !== "STOPPED" || lastFootDir !== "STOPPED") {
        var motionState = activeMotionBtn ? (activeMotionBtn.id || "motion") : "idle";
        var stopState = (stopBtnEl && stopBtnEl.classList.contains('btn-running')) ? "on" : "off";
        var msg = "UI H=" + headState + " F=" + footState + " motion=" + motionState + " stop=" + stopState +
                  " | RELAY head=" + lastHeadDir + " foot=" + lastFootDir;
        logUiEvent(msg);
    } else {
        // If relays just transitioned to stopped, log once
        if (prevRelayHeadDir !== "STOPPED" || prevRelayFootDir !== "STOPPED") {
            logUiEvent("UI stop; RELAY head=STOPPED foot=STOPPED");
        }
    }
    prevRelayHeadDir = lastHeadDir;
    prevRelayFootDir = lastFootDir;
}

var isFirstPoll = true; 
function pollStatus() {
    if (!isRoleAvailable('bed')) return;
    if (!currentBedTargetId || !bedTargetsById[currentBedTargetId]) return;
    checkOffline();
    var base = getBedBaseUrl();
    fetch(base + '/rpc/Bed.Status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        var result = status.result || status; 
        if (result) {
            updateStatusDisplay(result);
            if (isFirstPoll) {
                presetData = {
                    zg: { head: result.zg_head, foot: result.zg_foot, label: result.zg_label },
                    snore: { head: result.snore_head, foot: result.snore_foot, label: result.snore_label },
                    legs: { head: result.legs_head, foot: result.legs_foot, label: result.legs_label },
                    p1: { head: result.p1_head, foot: result.p1_foot, label: result.p1_label },
                    p2: { head: result.p2_head, foot: result.p2_foot, label: result.p2_label }
                };
                updatePresetButton('zg', result.zg_head, result.zg_foot, result.zg_label);
                updatePresetButton('snore', result.snore_head, result.snore_foot, result.snore_label);
                updatePresetButton('legs', result.legs_head, result.legs_foot, result.legs_label);
                updatePresetButton('p1', result.p1_head, result.p1_foot, result.p1_label);
                updatePresetButton('p2', result.p2_head, result.p2_foot, result.p2_label);
                updateModalDropdown();
                isFirstPoll = false;
            }
        }
    })
    .catch(function(err) {
        console.error("Status poll failed", err);
        checkOffline();
    });
}

function updateModalDropdown() {
    var select = document.getElementById('preset-select');
    if (!select) return;
    select.options[0].text = presetData.zg.label || 'Zero G';
    select.options[1].text = presetData.snore.label || 'Anti-Snore';
    select.options[2].text = presetData.legs.label || 'Legs Up';
    select.options[3].text = presetData.p1.label || 'P1';
    select.options[4].text = presetData.p2.label || 'P2';
    onModalDropdownChange();
    var styleSel = document.getElementById('style-select');
    if (styleSel) styleSel.value = currentStyle;
}

function setModalSections(sections) {
    var cards = document.querySelectorAll('.settings-card');
    var allowAll = !Array.isArray(sections) || sections.length === 0;
    cards.forEach(function(card){
        var section = card.dataset.section;
        if (allowAll || !section) {
            card.classList.remove('is-hidden');
            return;
        }
        var show = sections.indexOf(section) !== -1;
        card.classList.toggle('is-hidden', !show);
    });
}

function toggleSettingsMenu() {
    var menu = document.getElementById('bed-settings-dropdown');
    if (!menu) return;
    menu.classList.toggle('open');
}

function closeSettingsMenu() {
    var menu = document.getElementById('bed-settings-dropdown');
    if (!menu) return;
    menu.classList.remove('open');
}

function toggleLightSettingsMenu() {
    var menu = document.getElementById('light-settings-dropdown');
    if (!menu) return;
    menu.classList.toggle('open');
}

function closeLightSettingsMenu() {
    var menu = document.getElementById('light-settings-dropdown');
    if (!menu) return;
    menu.classList.remove('open');
}

function openSetModal(sections, title) {
    var modal = document.getElementById('set-modal');
    if (!modal) return;
    closeSettingsMenu();
    closeLightSettingsMenu();
    var titleEl = modal.querySelector('.settings-title');
    if (titleEl) titleEl.textContent = title || 'Settings';
    setModalSections(sections);
    if (!sections || sections.indexOf('presets') !== -1) {
        updateModalDropdown();
        onModalDropdownChange();
    }
    if (!sections || sections.indexOf('limits') !== -1) {
        updateLimitInputs(true);
    }
    if (!sections || sections.indexOf('labels') !== -1) {
        loadDeviceLabels();
    }
    if (!sections || sections.indexOf('wiring') !== -1) {
        loadLightWiring();
    }
    modal.style.display = 'flex';
}
function closeSetModal() {
    var modal = document.getElementById('set-modal');
    if (modal) modal.style.display = 'none';
}

function setLabelStatus(message, isError) {
    var el = document.getElementById('label-status');
    if (!el) return;
    el.textContent = message || '';
    el.classList.toggle('error', !!isError);
}

function setBrandTitle(name) {
    var titleEl = document.getElementById('brand-title');
    if (!titleEl) return;
    if (name && name.toLowerCase() === 'homeyantric') {
        titleEl.innerHTML = '<span class="brand-line brand-home">Home</span><span class="brand-line brand-yantric">Yantric</span>';
    } else if (name) {
        titleEl.textContent = name;
    }
}

function loadDeviceLabels() {
    fetch('/rpc/System.Labels')
        .then(function(resp){ return resp.json(); })
        .then(function(res){
            var deviceInput = document.getElementById('label-device-input');
            var roomInput = document.getElementById('label-room-input');
            if (deviceInput) deviceInput.value = res.device_name || '';
            if (roomInput) roomInput.value = res.room || '';
            setLabelStatus('');
        })
        .catch(function(){
            setLabelStatus('Failed to load labels', true);
        });
}

function saveDeviceLabels() {
    var deviceInput = document.getElementById('label-device-input');
    var roomInput = document.getElementById('label-room-input');
    var payload = {
        device_name: deviceInput ? deviceInput.value.trim() : "",
        room: roomInput ? roomInput.value.trim() : ""
    };
    fetch('/rpc/System.Labels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(function(resp){ return resp.json(); })
        .then(function(){
            setLabelStatus('Saved');
            refreshPeersInternal({ force: true });
        })
        .catch(function(){
            setLabelStatus('Save failed', true);
        });
}

function resetDeviceLabels() {
    fetch('/rpc/System.Labels', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_name: "", room: "" })
    })
        .then(function(resp){ return resp.json(); })
        .then(function(){
            setLabelStatus('Reset');
            loadDeviceLabels();
            refreshPeersInternal({ force: true });
        })
        .catch(function(){
            setLabelStatus('Reset failed', true);
        });
}

window.saveDeviceLabels = saveDeviceLabels;
window.resetDeviceLabels = resetDeviceLabels;
window.saveLightWiring = saveLightWiring;
window.saveLightWiringGate = saveLightWiringGate;
function onModalDropdownChange() {
    var select = document.getElementById('preset-select');
    modalCurrentSlot = select.value; 
    var data = presetData[modalCurrentSlot];
    if (data) updateModalButtonStates();
}
function onModalInputChange() { updateModalButtonStates(); }

function updateModalButtonStates() {
    var slot = modalCurrentSlot;
    var data = presetData[slot];
    var defaults = PRESET_DEFAULTS[slot];
    var labelInput = document.getElementById('preset-label-input');
    var modalPosText = document.getElementById('modal-pos-text');
    var saveLabelBtn = document.getElementById('modal-save-label-btn');
    var resetLabelBtn = document.getElementById('modal-reset-label-btn');
    var savePosBtn = document.getElementById('modal-save-pos-btn');
    var resetPosBtn = document.getElementById('modal-reset-pos-btn');

    if (!data || !defaults || !labelInput) return;

    var currentInputText = labelInput.value;
    var savedLabel = data.label;
    var defaultLabel = defaults.label;
    var savedHeadSec = (data.head / 1000).toFixed(0);
    var savedFootSec = (data.foot / 1000).toFixed(0);
    var liveHeadSec = (currentLiveHeadMs / 1000).toFixed(0);
    var liveFootSec = (currentLiveFootMs / 1000).toFixed(0);

    modalPosText.innerHTML = 'Head: ' + savedHeadSec + 's &rarr; ' + liveHeadSec + 's, ' + 'Foot: ' + savedFootSec + 's &rarr; ' + liveFootSec + 's';
    saveLabelBtn.disabled = (currentInputText === savedLabel || currentInputText.length === 0);
    resetLabelBtn.disabled = (savedLabel === defaultLabel);
    var isSamePos = (data.head === currentLiveHeadMs && data.foot === currentLiveFootMs);
    savePosBtn.disabled = isSamePos;
    var isDefaultPos = (data.head === defaults.head && data.foot === defaults.foot);
    resetPosBtn.disabled = isDefaultPos;
    resetLabelBtn.innerHTML = 'Reset to "' + defaultLabel + '"';
    resetPosBtn.innerHTML = 'Reset to H:' + (defaults.head / 1000) + 's, F:' + (defaults.foot / 1000) + 's';
}

function savePresetPos() {
    var slot = document.getElementById('preset-select').value;
    sendCmd('SET_' + slot.toUpperCase() + '_POS', null);
    closeSetModal();
}
function savePresetLabel() {
    var slot = document.getElementById('preset-select').value;
    var labelInput = document.getElementById('preset-label-input');
    var label = labelInput.value; 
    if (!label) { showCustomAlert("Please type a new label first."); return; }
    sendCmd('SET_' + slot.toUpperCase() + '_LABEL', null, label);
    onModalDropdownChange();
}
function resetPresetPos() {
    var slot = document.getElementById('preset-select').value;
    showCustomConfirm("Reset POSITION for this preset?", function(isConfirmed) {
        if (isConfirmed) { sendCmd('RESET_' + slot.toUpperCase() + '_POS'); closeSetModal(); }
    });
}
function resetPresetLabel() {
    var slot = document.getElementById('preset-select').value;
    showCustomConfirm("Reset LABEL for this preset?", function(isConfirmed) {
        if (isConfirmed) { sendCmd('RESET_' + slot.toUpperCase() + '_LABEL'); closeSetModal(); }
    });
}

function updateLimitInputs(force) {
    var headInput = document.getElementById('limit-head-input');
    var footInput = document.getElementById('limit-foot-input');
    if (headInput && (force || document.activeElement !== headInput)) headInput.value = Math.round(headMaxSec);
    if (footInput && (force || document.activeElement !== footInput)) footInput.value = Math.round(footMaxSec);
}

function saveLimits() {
    var headInput = document.getElementById('limit-head-input');
    var footInput = document.getElementById('limit-foot-input');
    if (!headInput || !footInput) return;
    var hVal = parseFloat(headInput.value);
    var fVal = parseFloat(footInput.value);
    if (isNaN(hVal) || isNaN(fVal)) { showCustomAlert("Please enter numeric values for limits."); return; }
    hVal = Math.max(5, Math.min(60, hVal));
    fVal = Math.max(5, Math.min(60, fVal));
    headInput.value = hVal;
    footInput.value = fVal;
    sendCmd('SET_LIMITS', null, null, { headMax: hVal, footMax: fVal });
    closeSetModal();
}

function setOtaStatus(msg) {
    var status = document.getElementById('ota-status');
    if (status) status.textContent = msg;
}

function setOtaProgress(pct) {
    var bar = document.getElementById('ota-progress-bar');
    if (bar) bar.style.width = Math.max(0, Math.min(100, pct)) + '%';
}

function onOtaFileChange() {
    var input = document.getElementById('ota-file-input');
    if (!input) return;
    setOtaProgress(0);
    if (input.files && input.files.length > 0) {
        var f = input.files[0];
        var kb = Math.round(f.size / 1024);
        setOtaStatus('Selected: ' + f.name + ' (' + kb + ' KB)');
    } else {
        setOtaStatus('Choose a .bin firmware file.');
    }
}

function uploadFirmware() {
    var input = document.getElementById('ota-file-input');
    var btn = document.getElementById('ota-upload-btn');
    if (!input || !btn) return;
    if (!input.files || input.files.length === 0) {
        setOtaStatus('Please choose a .bin file first.');
        return;
    }
    var file = input.files[0];
    setOtaProgress(0);
    setOtaStatus('Uploading...');
    btn.disabled = true;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/rpc/Bed.OTA', true);
    xhr.setRequestHeader('Content-Type', 'application/octet-stream');
    xhr.upload.onprogress = function (e) {
        if (e.lengthComputable) {
            var pct = Math.round((e.loaded / e.total) * 100);
            setOtaProgress(pct);
            setOtaStatus('Uploading... ' + pct + '%');
        }
    };
    xhr.onload = function () {
        if (xhr.status === 200) {
            setOtaProgress(100);
            setOtaStatus('Upload complete, rebooting...');
            setTimeout(function() { closeSetModal(); }, 500);
        } else {
            setOtaStatus('Error: ' + xhr.status);
            btn.disabled = false;
        }
    };
    xhr.onerror = function () {
        setOtaStatus('Upload failed (device may be rebooting)');
        btn.disabled = false;
    };
    xhr.send(file);
}

// NEW: Reset Network Function
function resetNetwork() {
    showCustomConfirm("Reset WiFi settings and Reboot? You will need to re-connect to 'Elev8-Setup'.", function(isConfirmed) {
        if (isConfirmed) {
            sendCmd('RESET_NETWORK');
            closeSetModal();
            showCustomAlert("Rebooting... Please connect to the 'Elev8-Setup' WiFi hotspot.");
        }
    });
}

// --- STYLE SWITCHING ---
function applyStyle(style) {
    var body = document.body;
    body.classList.remove('style-a', 'style-b', 'style-c');
    body.classList.add(style);
    currentStyle = style;
    localStorage.setItem('uiStyle', style);
    var styleSel = document.getElementById('style-select');
    if (styleSel) styleSel.value = style;
    // Force immediate repaint/resize adjustments if needed
    resizeDynamicButtons();
}

function onStyleChange() {
    var styleSel = document.getElementById('style-select');
    if (styleSel) applyStyle(styleSel.value);
}

function populateBrandSelect(brands, currentKey) {
    var sel = document.getElementById('brand-select');
    if (!sel || !brands) return;
    sel.innerHTML = '';
    Object.keys(brands).forEach(function(key) {
        var opt = document.createElement('option');
        opt.value = key;
        opt.textContent = brands[key].name || key;
        if (key === currentKey) opt.selected = true;
        sel.appendChild(opt);
    });
}

function applyBrand(key) {
    currentBrandKey = key;
    localStorage.setItem('brandKey', key);
    var brand = (brandingData && brandingData.brands && brandingData.brands[key]) || null;
    if (brand) {
        document.title = brand.name || document.title;
        setBrandTitle(brand.name);
    }
    var sel = document.getElementById('brand-select');
    if (sel) sel.value = key;
}

function onBrandChange() {
    var sel = document.getElementById('brand-select');
    if (!sel) return;
    applyBrand(sel.value);
}
document.addEventListener('DOMContentLoaded', function() {
    var retryBtn = document.getElementById('offline-retry-btn');
    if (retryBtn) retryBtn.addEventListener('click', function() { pollStatus(); });
    stopBtnEl = document.getElementById('stop-btn-main');

    fetch('/branding.json')
        .then(function(resp) { return resp.json(); })
        .then(function(data) {
            brandingData = data;
            var defaultKey = localStorage.getItem('brandKey') || data.defaultBrand || 'homeyantric';
            populateBrandSelect(data.brands, defaultKey);
            applyBrand(defaultKey);
        })
        .catch(function() {
            applyBrand(currentBrandKey);
        });

    var saved = localStorage.getItem('uiStyle') || 'style-b';
    applyStyle(saved);
    var main = document.getElementById('main-container');
    if (main) main.classList.remove('hidden');
    var overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.classList.add('hidden');
    if (typeof window.updateBedVisualizer === 'function') {
        window.updateBedVisualizer(0, 0);
    }

    // Register service worker for PWA install/offline
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(function(err) {
            console.error('SW registration failed', err);
        });
    }
});

function showCustomAlert(message) {
    document.getElementById('alert-message').textContent = message;
    document.getElementById('alert-modal').style.display = 'flex';
}
function closeCustomAlert() { document.getElementById('alert-modal').style.display = 'none'; }
var confirmCallback = null;
function showCustomConfirm(message, callback) {
    document.getElementById('confirm-message').textContent = message;
    confirmCallback = callback;
    document.getElementById('confirm-modal').style.display = 'flex';
}
function closeCustomConfirm(isConfirmed) {
    document.getElementById('confirm-modal').style.display = 'none';
    if (confirmCallback) confirmCallback(isConfirmed);
    confirmCallback = null;
}

function resizeDynamicButtons() { 
    try {
        // For Style C keep fixed sizing
        if (document.body.classList.contains('style-c')) return;
        let H = window.innerHeight;
        let rockerRow = document.getElementById('rocker-row'); 
        if (!rockerRow) return; 
        let Z_pixels = rockerRow.getBoundingClientRect().bottom;
        let remainingSpace = H - Z_pixels - 10; 
        let targetHeight = remainingSpace * 0.25;
        let clampedHeight = Math.max(70, Math.min(targetHeight, 220)); 
        let presetButtons = document.querySelectorAll('.row-3-btn button');
        presetButtons.forEach(function(button) { button.style.minHeight = clampedHeight + 'px'; });
    } catch (e) {}
}

window.addEventListener('load', resizeDynamicButtons);
window.addEventListener('resize', resizeDynamicButtons);
window.addEventListener('load', function() {
    loadBedSummaryState();
    updateBedTargetLabel();
    applyCachedPeers();
    if (peerList.length) {
        logUiEvent("Peers (cached): beds=" + bedTargets.length + " lights=" + lightTargets.length);
    }
    document.addEventListener('click', function(evt) {
        var menu = document.getElementById('bed-settings-dropdown');
        var wrapper = document.querySelector('.bed-settings-menu');
        if (menu && wrapper && !wrapper.contains(evt.target)) {
            menu.classList.remove('open');
        }
        var lightMenu = document.getElementById('light-settings-dropdown');
        var lightWrapper = document.querySelector('.light-settings-menu');
        if (lightMenu && lightWrapper && !lightWrapper.contains(evt.target)) {
            lightMenu.classList.remove('open');
        }
    });
});
setInterval(pollStatus, 1000); 
pollStatus();
setInterval(refreshPeersInternal, 15000);

// --- MODULE SWITCHING (Bed) ---
function switchModule(mod) {
    setActiveModule(mod);
}

function updateTabVisibility() {
    var bedPanel = document.getElementById('bed-tab');
    var lightPanel = document.getElementById('light-tab');
    var bedPill = document.getElementById('bed-status-pill');
    var lightPill = document.getElementById('light-status-pill');
    var bedSettingsMenu = document.getElementById('bed-settings-menu');
    var lightSettingsMenu = document.getElementById('light-settings-menu-top');
    var showBed = currentModule.startsWith('bed:') && bedTargets.length > 0;
    var showLight = currentModule === 'light' && lightTargets.length > 0;
    if (bedPanel) {
        bedPanel.classList.toggle('hidden', !showBed);
        bedPanel.classList.toggle('active', showBed);
    }
    if (lightPanel) {
        lightPanel.classList.toggle('hidden', !showLight);
        lightPanel.classList.toggle('active', showLight);
    }
    if (bedPill) bedPill.classList.toggle('hidden', !showBed);
    if (lightPill) lightPill.classList.toggle('hidden', !showLight);
    if (bedSettingsMenu) bedSettingsMenu.classList.toggle('hidden', !showBed);
    if (lightSettingsMenu) lightSettingsMenu.classList.toggle('hidden', !showLight);
    if (!showBed) closeSettingsMenu();
    if (!showLight) closeLightSettingsMenu();
    syncOfflineOverlay();
    renderTabs();
}

function updateLightCardState(targetId, state, detail, brightness, opts) {
    opts = opts || {};
    var cacheKey = lightCacheKeyById[targetId] || targetId;
    var card = document.querySelector('.light-card--device[data-id="' + targetId + '"]');
    if (!card && cacheKey) {
        card = document.querySelector('.light-card--device[data-cache-key="' + cacheKey + '"]');
        if (card) {
            card.dataset.id = targetId;
        }
    }
    if (!card) return;
    if (card.dataset.cacheKey) {
        cacheKey = card.dataset.cacheKey;
    }
    var statusLine = card.querySelector('.light-status-line');
    var statusDetail = card.querySelector('.light-status-detail');
    var toggleBtn = card.querySelector('.light-toggle-btn');
    var brightnessSlider = card.querySelector('.light-brightness-slider');
    var brightnessSteps = card.querySelectorAll('.light-brightness-step');
    var brightnessValues = card.querySelectorAll('.light-brightness-value');
    var lastSeenEl = card.querySelector('.light-last-seen');
    var isInFlight = !!lightCmdInFlightById[cacheKey] || !!lightCmdInFlightById[targetId];
    if (state) {
        lightLastKnownStateById[cacheKey] = state;
    }
    if (state) {
        lightLastKnownStateById[cacheKey] = state;
    }
    if (!opts.skipLastSeen && detail !== 'Error') {
        lightLastSeenById[cacheKey] = Date.now();
    }
    var effectiveState = state || lightLastKnownStateById[cacheKey] || "";
    var isOn = effectiveState.toLowerCase() === 'on';
    var lastSeen = lightLastSeenById[cacheKey];
    var ageMs = lastSeen ? (Date.now() - lastSeen) : null;
    var isOffline = ageMs !== null && ageMs > lightOfflineThresholdMs;
    var isStale = ageMs !== null && ageMs > PEER_STALE_MS;
    if (statusLine) {
        statusLine.classList.toggle('on', !isOffline && isOn);
        statusLine.classList.toggle('off', !isOffline && !isOn);
        statusLine.classList.toggle('offline', isOffline);
        if (isOffline) {
            statusLine.textContent = 'Light Offline';
        } else if (isStale) {
            statusLine.textContent = 'Light Stale';
        } else {
            statusLine.textContent = effectiveState ? ('Light ' + effectiveState) : 'Ready';
        }
    }
    if (statusDetail) {
        if (isOffline) {
            var lastState = lightLastKnownStateById[cacheKey];
            statusDetail.textContent = lastState ? ('Last state: ' + lastState) : 'Reconnecting...';
        } else if (isStale) {
            statusDetail.textContent = detail || 'Awaiting refresh...';
        } else {
            statusDetail.textContent = detail || (effectiveState || 'Unknown');
        }
    }
    if (toggleBtn) {
        toggleBtn.classList.toggle('is-on', !isOffline && isOn);
        toggleBtn.disabled = isOffline || isInFlight || lightControlsLocked;
        var textEl = toggleBtn.querySelector('.light-toggle-text');
        if (textEl) textEl.textContent = isOffline ? 'Offline' : (effectiveState ? (isOn ? 'Turn Off' : 'Turn On') : 'Toggle');
    }
    if (typeof brightness === 'number') {
        if (brightnessSlider) brightnessSlider.value = String(brightness);
        if (brightnessValues && brightnessValues.length) {
            brightnessValues.forEach(function(el){ el.textContent = brightness + "%"; });
        }
    }
    if (brightnessSlider) brightnessSlider.disabled = isOffline || lightControlsLocked;
    if (brightnessSteps && brightnessSteps.length) {
        brightnessSteps.forEach(function(btn){ btn.disabled = isOffline || lightControlsLocked; });
    }
    if (typeof brightness === 'number') {
        updateLightStepDisabled(card, brightness, isOffline || lightControlsLocked);
    }
    if (card) card.classList.toggle('is-offline', isOffline);
    if (lastSeenEl) {
        if (!lastSeen) {
            lastSeenEl.textContent = 'Never';
            lastSeenEl.classList.remove('is-stale');
        } else {
            var ageSec = Math.floor(ageMs / 1000);
            var label = (ageSec < 5) ? 'Just now' : (ageSec < 60 ? (ageSec + "s ago") : (Math.floor(ageSec / 60) + "m ago"));
            lastSeenEl.textContent = label;
            lastSeenEl.classList.toggle('is-stale', ageMs > lightOfflineThresholdMs);
        }
    }
    updateLightStatusPill();
    updateLightRoomActionStates();
}

function sendLightCmd(cmd, targetId) {
    if (!isRoleAvailable('light')) return;
    var target = lightTargetsById[targetId];
    if (!target) return;
    var base = getLightBaseUrl(target);
    fetch(base + '/rpc/Light.Command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cmd: cmd })
    })
    .then(function(resp) { return resp.json(); })
    .then(function(res) {
        lightCmdInFlightById[targetId] = false;
        updateLightCardState(targetId, res.state || '', res.state || 'OK', res.brightness);
    })
    .catch(function(err) {
        lightCmdInFlightById[targetId] = false;
        updateLightCardState(targetId, '', 'Error');
        console.error('Light cmd error', err);
    });
}

function sendLightBrightness(targetId, value) {
    if (!isRoleAvailable('light')) return;
    var target = lightTargetsById[targetId];
    if (!target) return;
    var base = getLightBaseUrl(target);
    fetch(base + '/rpc/Light.Brightness', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brightness: value })
    })
    .then(function(resp) { return resp.json(); })
    .then(function(res) {
        updateLightCardState(targetId, res.state || '', res.state || 'OK', res.brightness);
    })
    .catch(function(err) {
        updateLightCardState(targetId, '', 'Error');
        console.error('Light brightness error', err);
    });
}

function pollLightStatus() {
    if (!isRoleAvailable('light')) return;
    lightTargets.forEach(function(target) {
        var base = getLightBaseUrl(target);
        var controller = new AbortController();
        var timeoutId = setTimeout(function(){ controller.abort(); }, lightStatusTimeoutMs);
        fetch(base + '/rpc/Light.Status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}', signal: controller.signal })
            .then(function(resp) { return resp.json(); })
            .then(function(res) {
                clearTimeout(timeoutId);
                var cacheKey = lightCacheKeyById[target.id] || getLightCacheKey(target);
                var incomingState = (res.state || '').toLowerCase();
                var lastState = (lightLastKnownStateById[cacheKey] || '').toLowerCase();
                if (incomingState) {
                    if (incomingState === lastState) {
                        lightStateStreakById[cacheKey] = (lightStateStreakById[cacheKey] || 0) + 1;
                    } else {
                        lightStateStreakById[cacheKey] = 1;
                    }
                    if (incomingState === 'off' && lastState === 'on' && lightStateStreakById[cacheKey] === 1) {
                        updateLightCardState(target.id, lastState, 'Confirming...', res.brightness, { skipLastSeen: true });
                        return;
                    }
                }
                updateLightCardState(target.id, res.state || '', res.state || 'Ready', res.brightness);
            })
            .catch(function(err) {
                clearTimeout(timeoutId);
                var cacheKey = lightCacheKeyById[target.id] || target.id;
                var lastState = lightLastKnownStateById[cacheKey] || '';
                updateLightCardState(target.id, lastState, 'Reconnecting...', undefined, { skipLastSeen: true });
                if (err && err.name === 'AbortError') {
                    return;
                }
                console.error('Light status error', err);
            });
    });
}

lightPollTimer = setInterval(pollLightStatus, 2000);

// Periodic log of motor/UI state
setInterval(logUiAndMotion, 1000);

// Initial tab visibility based on enabled roles (after DOM ready)
document.addEventListener('DOMContentLoaded', function() {
    refreshPeersInternal();
    updateTabVisibility();
    if (hasLocalRole('light') && !lightWiringLoaded) {
        loadLightWiring();
    }
});
