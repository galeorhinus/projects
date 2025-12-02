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

const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;
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
        var hours = Math.floor(totalSeconds / 3600);
        totalSeconds %= 3600;
        var minutes = Math.floor(totalSeconds / 60);
        var seconds = Math.floor(totalSeconds % 60);
        var hh = String(hours).padStart(2, '0');
        var mm = String(minutes).padStart(2, '0');
        var ss = String(seconds).padStart(2, '0');
        return hh + ":" + mm + ":" + ss;
    } catch (e) {
        return "00:00:00";
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
    var headPercent = (headPos / (HEAD_MAX_SEC * 1000)) * 100;
    var footPercent = (footPos / (FOOT_MAX_SEC * 1000)) * 100;
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
    if (!statusEl1 || !statusEl2) return;

    var formattedTime = formatBootTime(data.bootTime);
    var formattedDuration = formatDuration(data.uptime); 
    statusEl1.textContent = "Up since: " + formattedTime;
    statusEl2.textContent = "Duration: " + formattedDuration;
    
    var headPosNum = parseFloat(data.headPos) || 0;
    var footPosNum = parseFloat(data.footPos) || 0;
    currentLiveHeadMs = headPosNum * 1000;
    currentLiveFootMs = footPosNum * 1000;
    if (typeof window.updateBedVisualizer === 'function') {
        window.updateBedVisualizer(headPosNum, footPosNum);
    }
}

function clearRunningPresets() {
    var allPresets = document.querySelectorAll('.preset-btn.btn-running');
    for (var i = 0; i < allPresets.length; i++) {
        allPresets[i].classList.remove('btn-running');
    }
}

function sendCmd(cmd, btnElement, label) {
    console.log("Sent: " + cmd);
    var presetCmds = ["ZERO_G", "FLAT", "ANTI_SNORE", "LEGS_UP", "P1", "P2", "MAX"];
    var isPreset = presetCmds.indexOf(cmd) > -1;

    // Toggle behavior: if a preset is already running and pressed again, stop
    if (isPreset && btnElement && btnElement.classList.contains('btn-running')) {
        stopCmd(true);
        return;
    }

    clearRunningPresets(); 

    if (cmd !== "STOP" && !cmd.startsWith('FLAT') && !cmd.startsWith('SET_') && !cmd.startsWith('RESET_') &&    
        !cmd.startsWith('ZERO_G') && !cmd.startsWith('ANTI_SNORE') && !cmd.startsWith('LEGS_UP') && !cmd.startsWith('P1') && !cmd.startsWith('P2') &&
        !cmd.startsWith('MAX')) { 
        pressStartTime = Date.now();
        activeCommand = cmd;
    }

    if (btnElement) {
        btnElement.classList.add('btn-running'); 
    }
    
    var body = { cmd: cmd };
    if (label !== undefined) body.label = label;
    
    fetch('/rpc/Bed.Command', {
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
    });
}

function stopCmd(isManualPress) {
    if (presetTimerId) { clearTimeout(presetTimerId); presetTimerId = null; }
    clearRunningPresets();

    if (pressStartTime !== 0 && activeCommand !== "") {
        pressStartTime = 0;
        activeCommand = "";
    }
    fetch('/rpc/Bed.Command', {
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

var isFirstPoll = true; 
function pollStatus() {
    fetch('/rpc/Bed.Status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        var result = status.result || status; 
        if (result && result.bootTime) {
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

function openSetModal() {
    var modal = document.getElementById('set-modal');
    if (modal) { updateModalDropdown(); onModalDropdownChange(); modal.style.display = 'flex'; }
}
function closeSetModal() {
    var modal = document.getElementById('set-modal');
    if (modal) modal.style.display = 'none';
}
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
        var titleEl = document.getElementById('brand-title');
        if (titleEl && brand.name) titleEl.textContent = brand.name;
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
setInterval(pollStatus, 1000); 
pollStatus();
