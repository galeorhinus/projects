// --- Client-side JavaScript ---

var pressStartTime = 0;
var activeCommand = "";
var presetTimerId = null; // Timer for preset final status check

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
        const date = new Date(timestamp * 1000);
        const options = {
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
        let hours = Math.floor(totalSeconds / 3600);
        totalSeconds %= 3600;
        let minutes = Math.floor(totalSeconds / 60);
        let seconds = Math.floor(totalSeconds % 60);

        let hh = String(hours).padStart(2, '0');
        let mm = String(minutes).padStart(2, '0');
        let ss = String(seconds).padStart(2, '0');
        
        return hh + ":" + mm + ":" + ss;
    } catch (e) {
        console.error("Error formatting duration:", e);
        return "00:00:00";
    }
}

// --- Calculate points string for a preset icon ---
function calculateIconPoints(headPos, footPos) {
    const base_y = 14; 
    const travel_y = 10; 
    const h_end = 10;
    const g_start = 10;
    const g_end = 14;
    const f_tri_start = 14;
    const f_tri_end = 20;
    const f_bar_start = 20;
    const f_bar_end = 24;

    let headPercent = (headPos / (HEAD_MAX_SEC * 1000)) * 100;
    let footPercent = (footPos / (FOOT_MAX_SEC * 1000)) * 100;
    
    headPercent = Math.max(0, Math.min(100, headPercent));
    footPercent = Math.max(0, Math.min(100, footPercent));

    let headY = base_y - (travel_y * (headPercent / 100));
    let footY = base_y - (travel_y * (footPercent / 100) * 0.5); // Scaled 50%

    let points = 
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
    let btnLabelEl, iconLineEl;
    let defaultLabel = slot.toUpperCase(); 

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

    btnLabelEl.textContent = (label || defaultLabel);
    let points = calculateIconPoints(headPos || 0, footPos || 0);
    iconLineEl.setAttribute('points', points);
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

    let formattedTime = formatBootTime(data.bootTime);
    let formattedDuration = formatDuration(data.uptime); 
    
    statusEl1.textContent = "Up since: " + formattedTime;
    statusEl2.textContent = "Duration: " + formattedDuration;
    
    let headPosNum = 0;
    let footPosNum = 0;
    let headPercent = 0;
    let footPercent = 0;
    
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

    let headSeconds = headPosNum.toFixed(0);
    let footSeconds = footPosNum.toFixed(0);

    // Update text position to show seconds
    headPosTextEl.textContent = headSeconds + "s";
    footPosTextEl.textContent = footSeconds + "s";

    // Hide text if position is 0
    headPosTextEl.style.visibility = (headSeconds == 0) ? 'hidden' : 'visible';
    footPosTextEl.style.visibility = (footSeconds == 0) ? 'hidden' : 'visible';

    // --- Calculate SVG Points ---
    let headY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (headPercent / 100));
    let footY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (footPercent / 100) * 0.5);
    
    let points = 
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
    
    let body = { cmd: cmd };
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
        let result = status.result || status;
        console.log("Received immediate status:", JSON.stringify(result));
        
        updateStatusDisplay(result);

        // --- NEW: Check for all 3 save/reset actions ---
        if (result.saved_pos) {
            let slot = result.saved_pos;
            console.log("Updating " + slot + " button icon/label (pos save)");
            updatePresetButton(slot, result[slot+'_head'], result[slot+'_foot'], result[slot+'_label']);
        }
        if (result.saved_label) {
            let slot = result.saved_label;
            console.log("Updating " + slot + " button icon/label (label save)");
            updatePresetButton(slot, result[slot+'_head'], result[slot+'_foot'], result[slot+'_label']);
        }
        if (result.reset) {
            let slot = result.reset;
            console.log("Updating " + slot + " button icon/label (reset)");
            updatePresetButton(slot, result[slot+'_head'], result[slot+'_foot'], result[slot+'_label']);
        }
        // --- END NEW ---

        // Timer logic for all recallable presets
        let presetCmds = ["ZERO_G", "FLAT", "ANTI_SNORE", "LEGS_UP", "P1", "P2"];
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
        let timerToClear = presetTimerId;
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
        let result = status.result || status; 
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
        let result = status.result || status; 
        if (result && result.bootTime) {
            // Always update the main display
            updateStatusDisplay(result);

            // On first poll, init all preset buttons
            if (isFirstPoll) {
                console.log("First poll. Initializing preset buttons.");
                updatePresetButton('zg', result.zg_head, result.zg_foot, result.zg_label);
                updatePresetButton('snore', result.snore_head, result.snore_foot, result.snore_label);
                updatePresetButton('legs', result.legs_head, result.legs_foot, result.legs_label);
                updatePresetButton('p1', result.p1_head, result.p1_foot, result.p1_label);
                updatePresetButton('p2', result.p2_head, result.p2_foot, result.p2_label);
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

// --- Modal Control Functions ---

function openSetModal() {
    let modal = document.getElementById('set-modal');
    if (modal) {
        document.getElementById('preset-label-input').value = '';

        // Read all 5 current labels from main buttons
        let zgLabel = document.getElementById('zg-label-text').textContent;
        let snoreLabel = document.getElementById('snore-label-text').textContent;
        let legsLabel = document.getElementById('legs-label-text').textContent;
        let p1Label = document.getElementById('p1-label-text').textContent;
        let p2Label = document.getElementById('p2-label-text').textContent;

        // Update text on all 5 modal row labels
        document.getElementById('modal-label-zg').textContent = zgLabel;
        document.getElementById('modal-label-snore').textContent = snoreLabel;
        document.getElementById('modal-label-legs').textContent = legsLabel;
        document.getElementById('modal-label-p1').textContent = p1Label;
        document.getElementById('modal-label-p2').textContent = p2Label;
        
        modal.style.display = 'flex';
    }
}

function closeSetModal() {
    let modal = document.getElementById('set-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// slot is 'zg', 'snore', 'legs', 'p1', or 'p2'
function savePresetPos(slot) {
    let cmd = 'SET_' + slot.toUpperCase() + '_POS'; // e.g., SET_ZG_POS
    sendCmd(cmd, null);
    // Don't close modal, user might want to do more
}

function savePresetLabel(slot) {
    let labelInput = document.getElementById('preset-label-input');
    let label = labelInput.value; 
    
    // Don't save if the label is empty
    if (!label) {
        alert("Please type a new label in the text box first.");
        return;
    }
    
    let cmd = 'SET_' + slot.toUpperCase() + '_LABEL'; // e.g., SET_ZG_LABEL
    sendCmd(cmd, null, label);
    labelInput.value = ''; // Clear input
    // Don't close modal, but we should update the label in the modal
    document.getElementById('modal-label-' + slot).textContent = label;
}

function resetPreset(slot) {
    let labelEl = document.getElementById('modal-label-' + slot);
    let label = labelEl ? labelEl.textContent : slot.toUpperCase();
    
    if (confirm("Are you sure you want to reset '" + label + "' to its factory default?")) {
        let cmd = 'RESET_' + slot.toUpperCase(); // e.g., RESET_ZG
        sendCmd(cmd);
        // Don't close modal, but update the label in the modal
        // We have to guess the default, JS doesn't know it.
        // The server response will update the *main* button, 
        // so we'll just close and let the user re-open.
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