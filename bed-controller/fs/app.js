// --- Client-side JavaScript ---

var pressStartTime = 0;
var activeCommand = "";
var presetTimerId = null; // Timer for preset final status check
var presetData = {}; // NEW: Cache for preset data

// --- Max position constants (from init.js) ---
const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;

// --- SVG Coordinate Constants ---
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


// --- Format boot timestamp ---
function formatBootTime(timestamp) {
    try {
        var date = new Date(timestamp * 1000);
        var options = {
            month: 'short', 
            day: 'numeric', 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true
        };
        return date.toLocaleString(undefined, options);
    } catch (e) {
        console.error("Error formatting date:", e);
        return "Unknown";
    }
}

// --- Format duration in seconds to HH:MM:SS ---
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
        console.error("Error formatting duration:", e);
        return "00:00:00";
    }
}

// --- Calculate points string for a preset icon ---
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
    var footY = base_y - (travel_y * (footPercent / 100) * 0.5); // Scaled 50%

    var points = 
        '0,' + headY + ' ' +         // 1. Head top-left
        h_end + ',' + base_y + ' ' + // 2. Head bottom-right
        g_start + ',' + base_y + ' ' + // 3. Gap start
        g_end + ',' + base_y + ' ' +   // 4. Gap end
        f_tri_start + ',' + base_y + ' ' + // 5. Foot tri start
        f_tri_end + ',' + footY + ' ' +  // 6. Foot tri top-right
        f_bar_start + ',' + footY + ' ' +// 7. Foot bar start
        f_bar_end + ',' + footY;         // 8. Foot bar end
        
    return points;
}

// --- Update a specific preset button's icon and label ---
function updatePresetButton(slot, headPos, footPos, label) {
    var btnLabelEl, iconLineEl;
    var defaultLabel = slot.toUpperCase(); 

    if (slot === 'p1') {
        btnLabelEl = document.getElementById('p1-label-text');
        iconLineEl = document.getElementById('p1-icon-line');
    } else if (slot === 'p2') {
        btnLabelEl = document.getElementById('p2-label-text');
        iconLineEl = document.getElementById('p2-icon-line');
    } else if (slot === 'zg') {
        btnLabelEl = document.getElementById('zg-label-text');
        iconLineEl = document.getElementById('zg-icon-line');
    } else if (slot === 'snore') {
        btnLabelEl = document.getElementById('snore-label-text');
        iconLineEl = document.getElementById('snore-icon-line');
    } else if (slot === 'legs') {
        btnLabelEl = document.getElementById('legs-label-text');
        iconLineEl = document.getElementById('legs-icon-line');
    } else {
        return; 
    }

    if (!btnLabelEl || !iconLineEl) {
        console.error("updatePresetButton: Could not find elements for slot: " + slot);
        return;
    }
    
    label = (label || defaultLabel); 
    btnLabelEl.textContent = label;
    
    var points = calculateIconPoints(headPos || 0, footPos || 0);
    iconLineEl.setAttribute('points', points);

    // Update the global cache
    if (!presetData[slot]) presetData[slot] = {};
    presetData[slot].label = label;
    presetData[slot].head = headPos || 0;
    presetData[slot].foot = footPos || 0;
}


// --- Update status display ---
function updateStatusDisplay(data) { 
    var statusEl1 = document.getElementById("status-line-1");
    var statusEl2 = document.getElementById("status-line-2"); 
    
    var headPosTextEl = document.getElementById("head-pos-text"); 
    var footPosTextEl = document.getElementById("foot-pos-text"); 
    var headPosContainerEl = document.getElementById("head-pos-text-container"); 
    var footPosContainerEl = document.getElementById("foot-pos-text-container"); 

    var mattressLineEl = document.getElementById("mattress-line"); 

    if (!statusEl1 || !statusEl2 || !headPosTextEl || !footPosTextEl || !mattressLineEl || !headPosContainerEl || !footPosContainerEl) {
        console.error("A UI element is missing!");
        return;
    }

    var formattedTime = formatBootTime(data.bootTime);
    var formattedDuration = formatDuration(data.uptime); 
    
    statusEl1.textContent = "Up since: " + formattedTime;
    statusEl2.textContent = "Duration: " + formattedDuration;
    
    var headPosNum = 0;
    var footPosNum = 0;
    var headPercent = 0;
    var footPercent = 0;
    
    try {
        headPosNum = parseFloat(data.headPos) || 0;
        footPosNum = parseFloat(data.footPos) || 0;

        headPercent = (headPosNum / HEAD_MAX_SEC) * 100;
        footPercent = (footPosNum / FOOT_MAX_SEC) * 100;

        headPercent = Math.max(0, Math.min(100, headPercent));
        footPercent = Math.max(0, Math.min(100, footPercent));

    } catch (e) {
        console.error("Error calculating percentages:", e);
    }

    var headSeconds = headPosNum.toFixed(0);
    var footSeconds = footPosNum.toFixed(0);

    // Update text position to show seconds
    headPosTextEl.textContent = headSeconds + "s";
    footPosTextEl.textContent = footSeconds + "s";

    // Hide text if position is 0
    headPosTextEl.style.visibility = (headSeconds == 0) ? 'hidden' : 'visible';
    footPosTextEl.style.visibility = (footSeconds == 0) ? 'hidden' : 'visible';

    // --- Calculate SVG Points ---
    var headY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (headPercent / 100));
    var footY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (footPercent / 100) * 0.5);
    
    var points = 
        HEAD_X_START + ',' + headY + ' ' +           // 1. Head top-left
        HEAD_X_END + ',' + MATTRESS_Y_BASE + ' ' +   // 2. Head bottom-right
        GAP_X_START + ',' + MATTRESS_Y_BASE + ' ' +  // 3. Gap start (same point)
        GAP_X_END + ',' + MATTRESS_Y_BASE + ' ' +    // 4. Gap end
        FOOT_TRIANGLE_X_START + ',' + MATTRESS_Y_BASE + ' ' + // 5. Foot tri start (same point)
        FOOT_TRIANGLE_X_END + ',' + footY + ' ' +    // 6. Foot tri top-right
        FOOT_BAR_X_START + ',' + footY + ' ' +       // 7. Foot bar start (same point)
        FOOT_BAR_X_END + ',' + footY;                // 8. Foot bar end
    
    mattressLineEl.setAttribute('points', points);

    // Update Y position of text
    headPosContainerEl.setAttribute('y', headY - 10);
    footPosContainerEl.setAttribute('y', footY - 10);
}

// --- Helper to clear all running preset buttons ---
function clearRunningPresets() {
    var allPresets = document.querySelectorAll('.preset-btn.btn-running');
    for (var i = 0; i < allPresets.length; i++) {
        allPresets[i].classList.remove('btn-running');
    }
}

// --- Send RPC Command ---
function sendCmd(cmd, btnElement, label) {
    console.log("Sent: " + cmd);

    if (cmd !== "STOP" && cmd !== "LIGHT_TOGGLE" && !cmd.startsWith('FLAT') && !cmd.startsWith('SET_') && !cmd.startsWith('RESET_') &&
        !cmd.startsWith('ZERO_G') && !cmd.startsWith('ANTI_SNORE') && !cmd.startsWith('LEGS_UP') && !cmd.startsWith('P1') && !cmd.startsWith('P2')) {
        pressStartTime = Date.now();
        activeCommand = cmd;
    }

    if (btnElement) {
        clearRunningPresets(); 
        btnElement.classList.add('btn-running'); 
    }
    
    var body = { cmd: cmd };
    if (label !== undefined) {
        body.label = label;
    }
    
    fetch('/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(function(status) {
        var result = status.result || status;
        console.log("Received immediate status:", JSON.stringify(result));
        
        updateStatusDisplay(result);

        // --- NEW: Check for all 3 save/reset actions ---
        var slotToUpdate = null;
        if (result.saved_pos) { slotToUpdate = result.saved_pos; }
        if (result.saved_label) { slotToUpdate = result.saved_label; }
        if (result.reset) { slotToUpdate = result.reset; }

        if (slotToUpdate) {
            console.log("Updating " + slotToUpdate + " button icon/label");
            
            // Handle single slot update
            updatePresetButton(slotToUpdate, result[slotToUpdate+'_head'], result[slotToUpdate+'_foot'], result[slotToUpdate+'_label']);
            // Update the modal dropdown to reflect the change
            updateModalDropdown();
        }
        // --- END NEW ---

        // Timer logic for all recallable presets
        var presetCmds = ["ZERO_G", "FLAT", "ANTI_SNORE", "LEGS_UP", "P1", "P2"];
        if (presetCmds.indexOf(cmd) > -1) {
            var maxWait = parseInt(result.maxWait) || 0;
            if (maxWait > 0) {
                var waitMs = maxWait + 1500;
                console.log(cmd + ": Setting timer to fetch final status in " + (waitMs / 1000) + "s");
                
                if (presetTimerId) clearTimeout(presetTimerId);
                
                presetTimerId = setTimeout(function() {
                    stopCmd(false); 
                }, waitMs);
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

// --- Stop Command / Status Fetch ---
function stopCmd(isManualPress) {
    if (presetTimerId) {
        var timerToClear = presetTimerId;
        clearTimeout(presetTimerId);
        presetTimerId = null;
        console.log("Clearing preset timer (" + timerToClear + ") due to STOP command.");
    }
    clearRunningPresets();

    if (pressStartTime !== 0 && activeCommand !== "") {
        var duration = (Date.now() - pressStartTime);
        console.log(activeCommand + " button released after ~" + duration + " ms.");
        pressStartTime = 0;
        activeCommand = "";
    }

    var logMsg = isManualPress ? "STOP (Manual Button Press)" : "STOP (Preset Timer Finished)";
    console.log("Sent: " + logMsg);

    fetch('/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'ContentType': 'application/json' },
        body: JSON.stringify({ cmd: 'STOP' }) 
    })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        var result = status.result || status; 
        console.log("Received status update:", JSON.stringify(result));
        updateStatusDisplay(result);
    })
    .catch(function(error) {
        console.error("Fetch error for STOP:", error);
    });
}

// --- Status Polling Function ---
var isFirstPoll = true; 

function pollStatus() {
    fetch('/rpc/Bed.Status', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}) 
    })
    .then(function(response) {
        if (!response.ok) {
            if (response.status !== 404) {
                console.error('Poll status: ' + response.statusText);
            }
            throw new Error('Poll response was not ok');
        }
        return response.json();
    })
    .then(function(status) {
        var result = status.result || status; 
        if (result && result.bootTime) {
            // Always update the main display
            updateStatusDisplay(result);

            // On first poll, init all preset buttons
            if (isFirstPoll) {
                console.log("First poll. Initializing preset buttons.");
                // Store preset data globally
                presetData = {
                    zg: { head: result.zg_head, foot: result.zg_foot, label: result.zg_label },
                    snore: { head: result.snore_head, foot: result.snore_foot, label: result.snore_label },
                    legs: { head: result.legs_head, foot: result.legs_foot, label: result.legs_label },
                    p1: { head: result.p1_head, foot: result.p1_foot, label: result.p1_label },
                    p2: { head: result.p2_head, foot: result.p2_foot, label: result.p2_label }
                };
                
                // Update all buttons
                updatePresetButton('zg', result.zg_head, result.zg_foot, result.zg_label);
                updatePresetButton('snore', result.snore_head, result.snore_foot, result.snore_label);
                updatePresetButton('legs', result.legs_head, result.legs_foot, result.legs_label);
                updatePresetButton('p1', result.p1_head, result.p1_foot, result.p1_label);
                updatePresetButton('p2', result.p2_head, result.p2_foot, result.p2_label);
                
                // Populate the modal dropdown
                updateModalDropdown();

                isFirstPoll = false; // Only run this once
            }
        }
    })
    .catch(function(error) {
        if (error.message !== 'Poll response was not ok') {
            console.error("Poll error:", error);
        }
    });
}

// --- NEW: Helper to update modal dropdown options ---
function updateModalDropdown() {
    var select = document.getElementById('preset-select');
    
    if (!select) {
        console.error("Modal dropdown element #preset-select not found.");
        return;
    }
    
    // Get the currently saved data from our cache
    select.options[0].text = presetData.zg.label || 'Zero G';
    select.options[1].text = presetData.snore.label || 'Anti-Snore';
    select.options[2].text = presetData.legs.label || 'Legs Up';
    select.options[3].text = presetData.p1.label || 'P1';
    select.options[4].text = presetData.p2.label || 'P2';
    
    // Trigger the change event to update the modal content for the first selected item
    onModalDropdownChange();
}

// --- Modal Control Functions ---
function openSetModal() {
    var modal = document.getElementById('set-modal');
    if (modal) {
        // Update the dropdown labels based on current main UI state
        updateModalDropdown();
        // Trigger the onchange event to load the currently selected preset's data
        onModalDropdownChange();
        modal.style.display = 'flex';
    }
}

function closeSetModal() {
    var modal = document.getElementById('set-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// --- Called when dropdown changes ---
function onModalDropdownChange() {
    var select = document.getElementById('preset-select');
    var modalPosText = document.getElementById('modal-pos-text');
    var slot = select.value; 
    var data = presetData[slot];
    
    if (data && modalPosText) {
        // Update label input box
        document.getElementById('preset-label-input').value = data.label;
        // Update position display text
        var headSec = (data.head / 1000).toFixed(0);
        var footSec = (data.foot / 1000).toFixed(0);
        modalPosText.textContent = 'Head: ' + headSec + 's, Foot: ' + footSec + 's';
    }
}

// --- Modal action buttons ---
function savePresetPos() {
    var slot = document.getElementById('preset-select').value;
    var cmd = 'SET_' + slot.toUpperCase() + '_POS'; // e.g., SET_ZG_POS
    sendCmd(cmd, null);
    closeSetModal();
}

function savePresetLabel() {
    var slot = document.getElementById('preset-select').value;
    var labelInput = document.getElementById('preset-label-input');
    var label = labelInput.value; 
    
    if (!label) {
        alert("Please type a new label in the text box first.");
        return;
    }
    
    var cmd = 'SET_' + slot.toUpperCase() + '_LABEL'; // e.g., SET_ZG_LABEL
    sendCmd(cmd, null, label);
    // Don't close, just clear the input
    labelInput.value = '';
}

function resetPresetPos() {
    var slot = document.getElementById('preset-select').value;
    var label = presetData[slot] ? presetData[slot].label : slot.toUpperCase();
    
    if (confirm("Are you sure you want to reset the POSITION for '" + label + "' to its factory default?")) {
        var cmd = 'RESET_' + slot.toUpperCase() + '_POS'; 
        sendCmd(cmd);
        closeSetModal();
    }
}

function resetPresetLabel() {
    var slot = document.getElementById('preset-select').value;
    var label = presetData[slot] ? presetData[slot].label : slot.toUpperCase();
    
    if (confirm("Are you sure you want to reset the LABEL for '" + label + "' to its factory default?")) {
        var cmd = 'RESET_' + slot.toUpperCase() + '_LABEL';
        sendCmd(cmd);
        closeSetModal();
    }
}


// --- Start Polling ---
try {
    pollStatus(); // Poll immediately on load
    setInterval(pollStatus, 1000); 
} catch (e) {
    console.error("Failed to start polling:", e);
}