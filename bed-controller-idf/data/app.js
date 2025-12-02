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

const HEAD_NODE_VERTICAL_TRAVEL = MATTRESS_Y_BASE - 8;
const FOOT_NODE_VERTICAL_TRAVEL = HEAD_NODE_VERTICAL_TRAVEL * 0.5;
const HEAD_LENGTH = 121;
const FIXED_LENGTH = 51;
const FOOT1_LENGTH = 80;
const FOOT2_LENGTH = 80;
const HEAD_TO_FIXED_GAP = 6;
const FIXED_TO_FOOT1_GAP = 6;
const FOOT1_TO_FOOT2_GAP = 6;
const ELEMENT_THICKNESS = 12;
const ELEMENT_RADIUS = 4;
const VANISHING_POINT_X = 169;
const VANISHING_POINT_Y = -60;
const VANISH_LINE_FRACTION = 0.3;
const VANISH_ELEMENT_THICKNESS = 12;
const VANISH_ELEMENT_RADIUS = 4;
const SHOW_CONNECTORS = false;

const BED_BASE_POINTS = [
    { x: 0, y: 126 },
    { x: 350, y: 126 },
    { x: 350, y: 132 },
    { x: 324, y: 132 },
    { x: 324, y: 151 },
    { x: 316, y: 151 },
    { x: 316, y: 132 },
    { x: 244, y: 132 },
    { x: 244, y: 151 },
    { x: 236, y: 151 },
    { x: 236, y: 132 },
    { x: 114, y: 132 },
    { x: 114, y: 151 },
    { x: 106, y: 151 },
    { x: 106, y: 132 },
    { x: 34, y: 132 },
    { x: 34, y: 151 },
    { x: 26, y: 151 },
    { x: 26, y: 132 },
    { x: 0, y: 132 }
];

const BED_TOP_PAIRS = [
    [0, 1],
    [5, 6],
    [9, 10],
    [11, 12],
    [15, 16]
];

const HEAD_NODE_START_X = 0;
const HEAD_NODE_END_X = HEAD_NODE_START_X + HEAD_LENGTH;
const FIXED_NODE_START_X = HEAD_NODE_END_X + HEAD_TO_FIXED_GAP;
const FIXED_NODE_END_X = FIXED_NODE_START_X + FIXED_LENGTH;
const FOOT1_NODE_START_X = FIXED_NODE_END_X + FIXED_TO_FOOT1_GAP;
const FOOT1_NODE_END_X = FOOT1_NODE_START_X + FOOT1_LENGTH;
const FOOT2_NODE_START_X = FOOT1_NODE_END_X + FOOT1_TO_FOOT2_GAP;
const FOOT2_NODE_END_X = FOOT2_NODE_START_X + FOOT2_LENGTH;

const MATTRESS_ELEMENT_IDS = [
    'mattress-element-0',
    'mattress-element-1',
    'mattress-element-2',
    'mattress-element-3'
];
const VANISH_ELEMENT_IDS = [
    'vanish-element-0',
    'vanish-element-1',
    'vanish-element-2',
    'vanish-element-3'
];
const VANISH_TOP_IDS = [
    'vanish-top-0',
    'vanish-top-1',
    'vanish-top-2',
    'vanish-top-3'
];
const VANISH_CONNECTOR_IDS = [
    'vanish-connector-0',
    'vanish-connector-1',
    'vanish-connector-2',
    'vanish-connector-3',
    'vanish-connector-4',
    'vanish-connector-5',
    'vanish-connector-6',
    'vanish-connector-7'
];

var visualizerRefs = null;

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

function clampVisualizer(val, min, max) {
    return Math.max(min, Math.min(max, val));
}

function polygonCentroid(points) {
    var area = 0;
    var cx = 0;
    var cy = 0;
    for (var i = 0, len = points.length; i < len; i++) {
        var j = (i + 1) % len;
        var cross = (points[i].x * points[j].y) - (points[j].x * points[i].y);
        area += cross;
        cx += (points[i].x + points[j].x) * cross;
        cy += (points[i].y + points[j].y) * cross;
    }
    area = area / 2;
    if (!area) {
        return { x: points[0].x, y: points[0].y };
    }
    cx = cx / (6 * area);
    cy = cy / (6 * area);
    return { x: cx, y: cy };
}

function mapToVanish(point) {
    return {
        x: point.x + ((VANISHING_POINT_X - point.x) * VANISH_LINE_FRACTION),
        y: point.y + ((VANISHING_POINT_Y - point.y) * VANISH_LINE_FRACTION)
    };
}

function setPolygonPoints(el, points) {
    if (!el) return;
    var pts = points.map(function(p) { return p.x + ',' + p.y; }).join(' ');
    el.setAttribute('points', pts);
}

function getVisualizerRefs() {
    if (visualizerRefs) return visualizerRefs;
    visualizerRefs = {
        mattressElements: MATTRESS_ELEMENT_IDS.map(function(id) { return document.getElementById(id); }),
        vanishElements: VANISH_ELEMENT_IDS.map(function(id) { return document.getElementById(id); }),
        vanishTops: VANISH_TOP_IDS.map(function(id) { return document.getElementById(id); }),
        vanishConnectors: VANISH_CONNECTOR_IDS.map(function(id) { return document.getElementById(id); }),
        bedTopEls: [
            document.getElementById('bed-top'),
            document.getElementById('bed-top-1'),
            document.getElementById('bed-top-2'),
            document.getElementById('bed-top-3'),
            document.getElementById('bed-top-4')
        ],
        bedBaseEl: document.getElementById('bed-base'),
        vanishBedBaseEl: document.getElementById('vanish-bed-base'),
        headPosText: document.getElementById('head-pos-text'),
        footPosText: document.getElementById('foot-pos-text'),
        headPosContainer: document.getElementById('head-pos-text-container'),
        footPosContainer: document.getElementById('foot-pos-text-container')
    };
    return visualizerRefs;
}

function calculateVisualizerNodes(headPosSec, footPosSec) {
    var headPercent = clampVisualizer((headPosSec / HEAD_MAX_SEC) * 100, 0, 100);
    var footPercent = clampVisualizer((footPosSec / FOOT_MAX_SEC) * 100, 0, 100);
    var headTargetY = MATTRESS_Y_BASE - (HEAD_NODE_VERTICAL_TRAVEL * (headPercent / 100));
    var headTheta = Math.atan2(MATTRESS_Y_BASE - headTargetY, HEAD_LENGTH);
    var headNodeX = HEAD_NODE_END_X - (HEAD_LENGTH * Math.cos(headTheta));
    var headNodeY = MATTRESS_Y_BASE - (HEAD_LENGTH * Math.sin(headTheta));

    var footTargetY = MATTRESS_Y_BASE - (FOOT_NODE_VERTICAL_TRAVEL * (footPercent / 100));
    var footTheta = Math.atan2(MATTRESS_Y_BASE - footTargetY, FOOT1_LENGTH);
    var foot1EndX = FOOT1_NODE_START_X + (FOOT1_LENGTH * Math.cos(footTheta));
    var foot1EndY = MATTRESS_Y_BASE - (FOOT1_LENGTH * Math.sin(footTheta));
    var footDeltaX = foot1EndX - FOOT1_NODE_END_X;
    var footDeltaY = foot1EndY - MATTRESS_Y_BASE;
    var foot2StartX = FOOT2_NODE_START_X + footDeltaX;
    var foot2EndX = FOOT2_NODE_END_X + footDeltaX;
    var foot2Y = MATTRESS_Y_BASE + footDeltaY;

    var nodes = [
        { x: headNodeX, y: headNodeY },
        { x: HEAD_NODE_END_X, y: MATTRESS_Y_BASE },
        { x: FIXED_NODE_START_X, y: MATTRESS_Y_BASE },
        { x: FIXED_NODE_END_X, y: MATTRESS_Y_BASE },
        { x: FOOT1_NODE_START_X, y: MATTRESS_Y_BASE },
        { x: foot1EndX, y: foot1EndY },
        { x: foot2StartX, y: foot2Y },
        { x: foot2EndX, y: foot2Y }
    ];
    return { headY: headNodeY, footY: foot1EndY, nodes: nodes };
}

function updateBedPolygons(bedBaseEl, vanishBedBaseEl, bedTopEls) {
    setPolygonPoints(bedBaseEl, BED_BASE_POINTS);
    setPolygonPoints(vanishBedBaseEl, BED_BASE_POINTS.map(mapToVanish));
    bedTopEls.forEach(function(el, idx) {
        if (!el) return;
        var pair = BED_TOP_PAIRS[idx];
        var a = BED_BASE_POINTS[pair[0]];
        var b = BED_BASE_POINTS[pair[1]];
        var va = mapToVanish(a);
        var vb = mapToVanish(b);
        setPolygonPoints(el, [a, b, vb, va]);
    });
}

function updateMattressRects(nodes, mattressElements) {
    var elementNodePairs = [
        [0, 1],
        [2, 3],
        [4, 5],
        [6, 7]
    ];
    elementNodePairs.forEach(function(pair, index) {
        var element = mattressElements[index];
        if (!element) return;
        var start = nodes[pair[0]];
        var end = nodes[pair[1]];
        var dx = end.x - start.x;
        var dy = end.y - start.y;
        var length = Math.sqrt((dx * dx) + (dy * dy));
        var angle = Math.atan2(dy, dx) * (180 / Math.PI);
        element.setAttribute('x', start.x);
        element.setAttribute('y', start.y - (ELEMENT_THICKNESS / 2));
        element.setAttribute('width', length);
        element.setAttribute('height', ELEMENT_THICKNESS);
        element.setAttribute('rx', ELEMENT_RADIUS);
        element.setAttribute('ry', ELEMENT_RADIUS);
        element.setAttribute('transform', 'rotate(' + angle + ' ' + start.x + ' ' + start.y + ')');
    });
}

function updateVanishRects(vanishNodes, vanishElements) {
    var vanishPairs = [
        [0, 1],
        [2, 3],
        [4, 5],
        [6, 7]
    ];
    vanishPairs.forEach(function(pair, index) {
        var element = vanishElements[index];
        if (!element) return;
        var start = vanishNodes[pair[0]];
        var end = vanishNodes[pair[1]];
        if (!start || !end) return;
        var dx = end.x - start.x;
        var dy = end.y - start.y;
        var length = Math.sqrt((dx * dx) + (dy * dy));
        var angle = Math.atan2(dy, dx) * (180 / Math.PI);
        element.setAttribute('x', start.x);
        element.setAttribute('y', start.y - (VANISH_ELEMENT_THICKNESS / 2));
        element.setAttribute('width', length);
        element.setAttribute('height', VANISH_ELEMENT_THICKNESS);
        element.setAttribute('rx', VANISH_ELEMENT_RADIUS);
        element.setAttribute('ry', VANISH_ELEMENT_RADIUS);
        element.setAttribute('transform', 'rotate(' + angle + ' ' + start.x + ' ' + start.y + ')');
    });
}

function updateVanishTops(vals, vanishNodes, vanishTops, headPosContainerEl, footPosContainerEl) {
    var topLift = 0;
    var topPairs = [
        [0, 1],
        [2, 3],
        [4, 5],
        [6, 7]
    ];
    topPairs.forEach(function(pair, index) {
        var poly = vanishTops[index];
        if (!poly) return;
        var nStart = vals.nodes[pair[0]];
        var nEnd = vals.nodes[pair[1]];
        var vStart = vanishNodes[pair[0]];
        var vEnd = vanishNodes[pair[1]];
        var lifted = [
            { x: nStart.x, y: nStart.y - topLift },
            { x: vStart.x, y: vStart.y - topLift },
            { x: vEnd.x, y: vEnd.y - topLift },
            { x: nEnd.x, y: nEnd.y - topLift }
        ];
        setPolygonPoints(poly, lifted);
        var centroid = polygonCentroid(lifted);
        if (index === 0 && headPosContainerEl) {
            headPosContainerEl.setAttribute('x', centroid.x - 7);
            headPosContainerEl.setAttribute('y', centroid.y - 12);
        }
        if (index === 3 && footPosContainerEl) {
            footPosContainerEl.setAttribute('x', centroid.x - 43);
            footPosContainerEl.setAttribute('y', centroid.y - 12);
        }
    });
}

function updateConnectors(vals, vanishNodes, connectors) {
    vanishNodes.forEach(function(vNode, index) {
        var connector = connectors[index];
        if (!connector) return;
        connector.style.display = SHOW_CONNECTORS ? 'inline' : 'none';
        var baseNode = vals.nodes[index];
        connector.setAttribute('x1', baseNode.x);
        connector.setAttribute('y1', baseNode.y - (ELEMENT_THICKNESS / 6));
        connector.setAttribute('x2', vNode.x);
        connector.setAttribute('y2', vNode.y - (ELEMENT_THICKNESS / 6));
    });
}

function updateBedVisualizer(headSec, footSec) {
    var refs = getVisualizerRefs();
    if (!refs) return;
    updateBedPolygons(refs.bedBaseEl, refs.vanishBedBaseEl, refs.bedTopEls);

    var vals = calculateVisualizerNodes(headSec, footSec);
    var vanishNodes = vals.nodes.map(mapToVanish);

    updateMattressRects(vals.nodes, refs.mattressElements);
    updateVanishRects(vanishNodes, refs.vanishElements);
    updateConnectors(vals, vanishNodes, refs.vanishConnectors);
    updateVanishTops(vals, vanishNodes, refs.vanishTops, refs.headPosContainer, refs.footPosContainer);

    if (refs.headPosText && refs.footPosText) {
        refs.headPosText.textContent = headSec.toFixed(0) + "s";
        refs.footPosText.textContent = footSec.toFixed(0) + "s";
        refs.headPosText.style.visibility = headSec > 0 ? 'visible' : 'hidden';
        refs.footPosText.style.visibility = footSec > 0 ? 'visible' : 'hidden';
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
    updateBedVisualizer(headPosNum, footPosNum);
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
    updateBedVisualizer(0, 0);

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
