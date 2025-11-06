// --- Client-side JavaScript ---

var pressStartTime = 0;
var activeCommand = "";
var presetTimerId = null; // Timer for preset final status check

// --- Max position constants (from init.js) ---
const HEAD_MAX_SEC = 28;
const FOOT_MAX_SEC = 43;

// --- SVG Coordinate Constants ---
const SVG_VIEWBOX_TRAVEL_HEIGHT = 108; // The max vertical travel of the mattress
const FRAME_Y_POSITION = 140; // Y coordinate for the gray frame
const MATTRESS_Y_BASE = 116; // Y coordinate for the flat (0%) mattress (140 - 24)

// --- Head Section ---
const HEAD_X_START = 0;
const HEAD_X_END = 120;

// --- Gap ---
const GAP_X_START = 120;
const GAP_X_END = 170;

// --- Foot Section ---
const FOOT_TRIANGLE_X_START = 170;
const FOOT_TRIANGLE_X_END = 260; // 170 + 90
const FOOT_BAR_X_START = 260;
const FOOT_BAR_X_END = 350; // 260 + 90


// --- Format boot timestamp ---
// Converts a UNIX timestamp (in seconds) to "Nov 5, 8:30 PM"
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

// --- NEW: Format duration in seconds to HH:MM:SS ---
function formatDuration(totalSeconds) {
    try {
        let hours = Math.floor(totalSeconds / 3600);
        totalSeconds %= 3600;
        let minutes = Math.floor(totalSeconds / 60);
        let seconds = Math.floor(totalSeconds % 60);

        // Pad with leading zeros
        let hh = String(hours).padStart(2, '0');
        let mm = String(minutes).padStart(2, '0');
        let ss = String(seconds).padStart(2, '0');
        
        return hh + ":" + mm + ":" + ss;
    } catch (e) {
        console.error("Error formatting duration:", e);
        return "00:00:00";
    }
}

// --- Update status display ---
function updateStatusDisplay(bootTime, uptime, headPos, footPos) { 
    var statusEl1 = document.getElementById("status-line-1");
    var statusEl2 = document.getElementById("status-line-2"); 
    
    var headPosTextEl = document.getElementById("head-pos-text"); 
    var footPosTextEl = document.getElementById("foot-pos-text"); 
    var headPosContainerEl = document.getElementById("head-pos-text-container"); 
    var footPosContainerEl = document.getElementById("foot-pos-text-container"); 

    var mattressLineEl = document.getElementById("mattress-line"); 

    if (statusEl1 && statusEl2 && headPosTextEl && footPosTextEl && mattressLineEl && headPosContainerEl && footPosContainerEl) {
        // Format the boot time
        let formattedTime = formatBootTime(bootTime);
        let formattedDuration = formatDuration(uptime); 
        
        statusEl1.textContent = "Up since: " + formattedTime;
        statusEl2.textContent = "Duration: " + formattedDuration;
        
        let headPosNum = 0;
        let footPosNum = 0;
        let headPercent = 0;
        let footPercent = 0;
        
        try {
            headPosNum = parseFloat(headPos) || 0;
            footPosNum = parseFloat(footPos) || 0;

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

        // --- NEW: Hide text if position is 0 ---
        headPosTextEl.style.visibility = (headSeconds == 0) ? 'hidden' : 'visible';
        footPosTextEl.style.visibility = (footSeconds == 0) ? 'hidden' : 'visible';


        // --- Calculate SVG Points ---
        
        let headY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (headPercent / 100));
        let footY = MATTRESS_Y_BASE - (SVG_VIEWBOX_TRAVEL_HEIGHT * (footPercent / 100) * 0.5);
        
        // Set all points for the single mattress polyline
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

        // --- CHANGED: Update Y position of text ---
        headPosContainerEl.setAttribute('y', headY - 10);
        footPosContainerEl.setAttribute('y', footY - 10);
    }
}

// --- Helper to clear all running preset buttons ---
function clearRunningPresets() {
    var allPresets = document.querySelectorAll('.preset-btn.btn-running');
    for (var i = 0; i < allPresets.length; i++) {
        allPresets[i].classList.remove('btn-running');
    }
}

// --- Send RPC Command ---
function sendCmd(cmd, btnElement) {
    console.log("Sent: " + cmd);

    // This is a momentary (hold-down) button
    if (cmd !== "STOP" && cmd !== "LIGHT_TOGGLE" && !cmd.startsWith('FLAT') && !cmd.startsWith('ZERO_G') && !cmd.startsWith('ANTI_SNORE') && !cmd.startsWith('LEGS_UP')) {
        pressStartTime = Date.now();
        activeCommand = cmd;
    }

    // This is a preset (one-click) button
    if (btnElement) {
        clearRunningPresets(); // Clear any other running presets
        btnElement.classList.add('btn-running'); // Set this one as running
    }
    
    // --- Use RPC POST request ---
    fetch('/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cmd: cmd })
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(function(status) {
        // Mongoose OS RPC wraps the actual return value in a "result" object
        let result = status.result || status;
        console.log("Received immediate status:", JSON.stringify(result));
        updateStatusDisplay(result.bootTime, result.uptime, result.headPos, result.footPos);

        // If this was a preset, set a timer to fetch final status
        if (cmd === "ZERO_G" || cmd === "FLAT" || cmd === "ANTI_SNORE" || cmd === "LEGS_UP") {
            var maxWait = parseInt(result.maxWait) || 0;
            if (maxWait > 0) {
                // Use server-provided time + 1.5s buffer
                var waitMs = maxWait + 1500;
                console.log(cmd + ": Setting timer to fetch final status in " + (waitMs / 1000) + "s");
                
                // Clear any old timer before setting a new one
                if (presetTimerId) clearTimeout(presetTimerId);
                
                presetTimerId = setTimeout(function() {
                    stopCmd(false); // Call stopCmd to fetch status (not a manual press)
                }, waitMs);
            } else {
                // No movement, just clear the button
                clearRunningPresets();
            }
        }
    })
    .catch(function(error) {
        console.error("Fetch error for " + cmd + ":", error);
        clearRunningPresets(); // Stop pulsing on error
    });
}

// --- Stop Command / Status Fetch ---
function stopCmd(isManualPress) {
    // Clear any pending preset timer
    if (presetTimerId) {
        let timerToClear = presetTimerId;
        clearTimeout(presetTimerId);
        presetTimerId = null;
        console.log("Clearing preset timer (" + timerToClear + ") due to STOP command.");
    }
    // Clear all pulsing buttons
    clearRunningPresets();

    if (pressStartTime !== 0 && activeCommand !== "") {
        var duration = (Date.now() - pressStartTime);
        console.log(activeCommand + " button released after ~" + duration + " ms.");
        pressStartTime = 0;
        activeCommand = "";
    }

    var logMsg = isManualPress ? "STOP (Manual Button Press)" : "STOP (Preset Timer Finished)";
    console.log("Sent: " + logMsg);

    // --- Use RPC POST request ---
    fetch('/rpc/Bed.Command', {
        method: 'POST',
        headers: { 'ContentType': 'application/json' },
        body: JSON.stringify({ cmd: 'STOP' }) // Always send STOP to stop motors
    })
    .then(function(response) { return response.json(); })
    .then(function(status) {
        let result = status.result || status; // Handle nested result
        console.log("Received status update:", JSON.stringify(result));
        updateStatusDisplay(result.bootTime, result.uptime, result.headPos, result.footPos);
    })
    .catch(function(error) {
        console.error("Fetch error for STOP:", error);
    });
}

// --- Status Polling Function ---
function pollStatus() {
    fetch('/rpc/Bed.Status', { // Use the new, safe STATUS endpoint
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}) // No args needed
    })
    .then(function(response) {
        if (!response.ok) {
            // Don't log 404 for favicon
            if (response.status !== 404) {
                console.error('Poll status: ' + response.statusText);
            }
            throw new Error('Poll response was not ok');
        }
        return response.json();
    })
    .then(function(status) {
        let result = status.result || status; // Handle nested result
        // Only update if the response is valid
        if (result && result.bootTime) {
            updateStatusDisplay(result.bootTime, result.uptime, result.headPos, result.footPos);
        }
    })
    .catch(function(error) {
        // Don't log the "not ok" error again
        if (error.message !== 'Poll response was not ok') {
            console.error("Poll error:", error);
        }
    });
}

// --- Start Polling ---
// Poll immediately on load, then every 1 second
try {
    pollStatus(); 
    setInterval(pollStatus, 1000); 
} catch (e) {
    console.error("Failed to start polling:", e);
}