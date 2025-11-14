print('>>> fs/init.js script started.'); // DEBUG: Heartbeat 1
// Load necessary Mongoose OS APIs.
load('api_sys.js');
load('api_timer.js');
load('api_gpio.js');
load('api_config.js');
load('api_math.js');
load('api_rpc.js');      // For RPC.addHandler
load('utils.js');

// --- Constants ---
let RELAY_ON = 0;
let RELAY_OFF = 1;
let HEAD_MAX_SECONDS = 28;
let FOOT_MAX_SECONDS = 43;
let THROTTLE_SAVE_SECONDS = 2.0;
let SYNC_EXTRA_MS = 10000; // NEW: 10s buffer for FLAT/MAX re-sync

let DEBUG = false;

// --- FACTORY DEFAULTS (Used for Reset, defined outside functions for MJS stability) ---
let PRESET_DEFAULTS = {
    'zg': { head: 10000, foot: 40000, label: "Zero G" },
    'snore': { head: 10000, foot: 0, label: "Anti-Snore" },
    'legs': { head: 0, foot: 43000, label: "Legs Up" },
    'p1': { head: 0, foot: 0, label: "P1" },
    'p2': { head: 0, foot: 0, label: "P2" }
};
// --- END FACTORY DEFAULTS ---


// --- GPIO Pin Definitions ---
let HEAD_UP_PIN   = 22;
let HEAD_DOWN_PIN = 23;
let FOOT_UP_PIN   = 18;
let FOOT_DOWN_PIN = 19;
let TRANSFER_PIN_1 = 32;
let TRANSFER_PIN_2 = 33;
let TRANSFER_PIN_3 = 25;
let TRANSFER_PIN_4 = 26;

// --- State Variables ---
let bedState = {
    flatTimerId: 0,
    zeroGHeadTimerId: 0,
    zeroGFootTimerId: 0,
    currentHeadPosMs: 0,
    currentFootPosMs: 0,
    headStartTime: 0,
    footStartTime: 0,
    currentHeadDirection: "STOPPED",
    currentFootDirection: "STOPPED"
};

let lastSaveTime = 0;

// --- Helper: Calculate Live Position ---
function calculateLivePositions() {
    let now = Timer.now();
    let liveHead = bedState.currentHeadPosMs;
    let liveFoot = bedState.currentFootPosMs;
    let maxHeadMs = HEAD_MAX_SECONDS * 1000;
    let maxFootMs = FOOT_MAX_SECONDS * 1000;

    if (bedState.headStartTime !== 0 && bedState.currentHeadDirection !== "STOPPED") {
        let elapsedMs = (now - bedState.headStartTime) * 1000;
        if (bedState.currentHeadDirection === "UP") {
            liveHead += elapsedMs;
        } else if (bedState.currentHeadDirection === "DOWN") {
            liveHead -= elapsedMs;
        }
        liveHead = Math.max(0, Math.min(maxHeadMs, liveHead));
    }
    
    if (bedState.footStartTime !== 0 && bedState.currentFootDirection !== "STOPPED") {
        let elapsedMs = (now - bedState.footStartTime) * 1000;
        if (bedState.currentFootDirection === "UP") {
            liveFoot += elapsedMs;
        } else if (bedState.currentFootDirection === "DOWN") {
            liveFoot -= elapsedMs;
        }
        liveFoot = Math.max(0, Math.min(maxFootMs, liveFoot));
    }

    return {
        head: Math.round(liveHead),
        foot: Math.round(liveFoot)
    };
}


// --- Function to Save State ---
function saveBedState(headPosMs, footPosMs, force) {
    if (typeof force === 'undefined') {
        force = false;
    }

    let now = Timer.now();
    if (force !== true && (now - lastSaveTime < THROTTLE_SAVE_SECONDS)) {
        print('... Throttling flash save. (Time since last save: ' + numToStrJS(now - lastSaveTime, 2) + 's)');
        return;
    }
    let headSec = headPosMs / 1000.0;
    let footSec = footPosMs / 1000.0;
    print('Attempting to save state to Flash: Head=' + numToStrJS(headSec, 2) + 's, Foot=' + numToStrJS(footSec, 2) + 's');
    Cfg.set({state: {head: headPosMs, foot: footPosMs}});
    print('... Cfg.set called.');
    lastSaveTime = now;
}

// --- Update Position Function ---
function updatePosition(motor) {
    let now = Timer.now();
    print('>>> updatePosition (' + motor + ') >>> Current Time: ' + numToStrJS(now, 2) + ' s');
    let stateChanged = false;

    if (motor === 'head') {
        print('>>> updatePosition >>> Checking Head. StartTime: ' + numToStrJS(bedState.headStartTime, 2) + ' s | Direction: ' + bedState.currentHeadDirection);
        if (bedState.headStartTime !== 0 && bedState.currentHeadDirection !== "STOPPED") {
            let elapsedSec = now - bedState.headStartTime;
            let elapsedMs = elapsedSec * 1000; 
            let oldPosMs = bedState.currentHeadPosMs; 
            let newPosMs = oldPosMs;

            print('>>> updatePosition >>> Head Elapsed Time:', numToStrJS(elapsedSec, 2), 's (', numToStrJS(elapsedMs, 0), 'ms)');

            if (bedState.currentHeadDirection === "UP") {
                newPosMs += elapsedMs;
            } else if (bedState.currentHeadDirection === "DOWN") {
                newPosMs -= elapsedMs;
            }

            print('>>> updatePosition >>> Head Calculated New Position (ms):', numToStrJS(newPosMs, 0));

            let maxHeadMs = HEAD_MAX_SECONDS * 1000;
            newPosMs = Math.max(0, Math.min(maxHeadMs, newPosMs));
            newPosMs = Math.round(newPosMs); 

            print('>>> updatePosition >>> Head Clamped & Rounded New Position (ms):', numToStrJS(newPosMs, 0));
            print('>>> updatePosition >>> Head moved for ~' + numToStrJS(elapsedSec, 2) + 's. New cumulative position: ' + numToStrJS(newPosMs / 1000.0, 2) + 's');

            if (newPosMs !== oldPosMs) {
                bedState.currentHeadPosMs = newPosMs;
                stateChanged = true;
            }
            bedState.headStartTime = 0; 
            bedState.currentHeadDirection = "STOPPED";
            print('>>> updatePosition >>> Head movement processed. StartTime reset.');
            
            if (stateChanged) {
                print('>>> updatePosition (head) >>> State changed, calling saveBedState.');
                saveBedState(bedState.currentHeadPosMs, bedState.currentFootPosMs); 
            }
        }
    } 

    if (motor === 'foot') {
        print('>>> updatePosition >>> Checking Foot. StartTime: ' + numToStrJS(bedState.footStartTime, 2) + ' s | Direction: ' + bedState.currentFootDirection);
        if (bedState.footStartTime !== 0 && bedState.currentFootDirection !== "STOPPED") {
            let elapsedSec = now - bedState.footStartTime;
            let elapsedMs = elapsedSec * 1000; 
            let oldPosMs = bedState.currentFootPosMs; 
            let newPosMs = oldPosMs;

            print('>>> updatePosition >>> Foot Elapsed Time:', numToStrJS(elapsedSec, 2), 's (', numToStrJS(elapsedMs, 0), 'ms)');

            if (bedState.currentFootDirection === "UP") {
                newPosMs += elapsedMs;
            } else if (bedState.currentFootDirection === "DOWN") {
                newPosMs -= elapsedMs;
            }

            print('>>> updatePosition >>> Foot Calculated New Position (ms):', numToStrJS(newPosMs, 0));

            let maxFootMs = FOOT_MAX_SECONDS * 1000;
            newPosMs = Math.max(0, Math.min(maxFootMs, newPosMs));
            newPosMs = Math.round(newPosMs); 

            print('>>> updatePosition >>> Foot Clamped & Rounded New Position (ms):', numToStrJS(newPosMs, 0));
            print('>>> updatePosition >>> Foot moved for ~' + numToStrJS(elapsedSec, 2) + 's. New cumulative position: ' + numToStrJS(newPosMs / 1000.0, 2) + 's');

            if (newPosMs !== oldPosMs) {
                bedState.currentFootPosMs = newPosMs;
                stateChanged = true;
            }
            bedState.footStartTime = 0; 
            bedState.currentFootDirection = "STOPPED";
            print('>>> updatePosition >>> Foot movement processed. StartTime reset.');
            
            if (stateChanged) {
                print('>>> updatePosition (foot) >>> State changed, calling saveBedState.');
                saveBedState(bedState.currentHeadPosMs, bedState.currentFootPosMs); 
            }
        }
    } 

    if (!stateChanged) {
        print('>>> updatePosition (' + motor + ') >>> State did not change.');
    }
    print('>>> updatePosition (' + motor + ') >>> Exiting');
}

// --- Helper functions for 4-pin transfer switch ---
function activateTransferSwitch() {
    print(">>> Activating Transfer Switch (ESP32 control)...");
    GPIO.write(TRANSFER_PIN_1, RELAY_ON);
    GPIO.write(TRANSFER_PIN_2, RELAY_ON);
    GPIO.write(TRANSFER_PIN_3, RELAY_ON);
    GPIO.write(TRANSFER_PIN_4, RELAY_ON);
}

function deactivateTransferSwitch() {
    print(">>> Deactivating Transfer Switch (Wired remote control)...");
    GPIO.write(TRANSFER_PIN_1, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_2, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_3, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_4, RELAY_OFF);
}
// --- END NEW ---


// --- Stop Function ---
function stopMovement() {
    print('>>> Entering stopMovement()');

    print(">>> stopMovement >>> Turning OFF HEAD_UP_PIN (" + numToStrJS(HEAD_UP_PIN, 0) + ")");
    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    print(">>> stopMovement >>> Turning OFF HEAD_DOWN_PIN (" + numToStrJS(HEAD_DOWN_PIN, 0) + ")");
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    print(">>> stopMovement >>> Turning OFF FOOT_UP_PIN (" + numToStrJS(FOOT_UP_PIN, 0) + ")");
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    print(">>> stopMovement >>> Turning OFF FOOT_DOWN_PIN (" + numToStrJS(FOOT_DOWN_PIN, 0) + ")");
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    print('... All motor relays turned OFF');

    updatePosition('head'); 
    updatePosition('foot'); 

    if (bedState.flatTimerId !== 0) {
        Timer.del(bedState.flatTimerId);
        bedState.flatTimerId = 0;
        print('FLAT sequence cancelled/finished.');
    }

    // if (bedState.maxTimerId !== 0) {
    //     Timer.del(bedState.maxTimerId);
    //     bedState.maxTimerId = 0;
    //     print('MAX sequence cancelled/finished.');
    // }

    if (bedState.zeroGHeadTimerId !== 0) {
        Timer.del(bedState.zeroGHeadTimerId);
        bedState.zeroGHeadTimerId = 0;
        print('ZERO_G Head sequence cancelled.');
    }
    if (bedState.zeroGFootTimerId !== 0) {
        Timer.del(bedState.zeroGFootTimerId);
        bedState.zeroGFootTimerId = 0;
        print('ZERO_G Foot sequence cancelled.');
    }

    // --- NEW: Return control to wired remote ---
    deactivateTransferSwitch();
}

// --- Hardware Initialization ---
function initGPIOPins() {
    print('Initializing GPIO control pins...');
    GPIO.set_mode(HEAD_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(HEAD_DOWN_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_DOWN_PIN, GPIO.MODE_OUTPUT);
    // --- NEW: Init 4 transfer pins ---
    GPIO.set_mode(TRANSFER_PIN_1, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_2, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_3, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_4, GPIO.MODE_OUTPUT);

    // Set motor pins to the OFF state
    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    
    // --- NEW: Set transfer pins to OFF (wired remote active) ---
    deactivateTransferSwitch();
    
    print('GPIO pins initialized to OFF state.');
}


// --- Generic "Go-To-Position" Preset Function ---
function executePositionPreset(targetHeadMs, targetFootMs) {
    let nowSec = 0;
    let currentHeadMs = 0;
    let currentFootMs = 0;
    let headDiffMs = 0;
    let footDiffMs = 0;
    let durationMs = 0;

    print('Executing: Position-based PRESET command initiated...');
    
    if (bedState.flatTimerId !== 0) { Timer.del(bedState.flatTimerId); bedState.flatTimerId = 0; }
    if (bedState.zeroGHeadTimerId !== 0) { Timer.del(bedState.zeroGHeadTimerId); bedState.zeroGHeadTimerId = 0; }
    if (bedState.zeroGFootTimerId !== 0) { Timer.del(bedState.zeroGFootTimerId); bedState.zeroGFootTimerId = 0; }
    
    let motorsRunning = (bedState.currentHeadDirection !== "STOPPED" || bedState.currentFootDirection !== "STOPPED");
    
    if (motorsRunning) {
        print('... Motors are running, calling stopMovement() first.');
        stopMovement(); 
    } else {
        print('... Motors are idle. Proceeding.');
    }
    
    nowSec = Timer.now();
    
    currentHeadMs = bedState.currentHeadPosMs;
    currentFootMs = bedState.currentFootPosMs;

    headDiffMs = targetHeadMs - currentHeadMs;
    footDiffMs = targetFootMs - currentFootMs;

    print('... Current State: Head=' + numToStrJS(currentHeadMs, 0) + 'ms, Foot=' + numToStrJS(currentFootMs, 0) + 'ms');
    print('... Target State:  Head=' + numToStrJS(targetHeadMs, 0) + 'ms, Foot=' + numToStrJS(targetFootMs, 0) + 'ms');
    print('... Calculated Diff: Head=' + numToStrJS(headDiffMs, 0) + 'ms, Foot=' + numToStrJS(footDiffMs, 0) + 'ms');

    // --- NEW: Add buffer for FLAT/MAX commands ---
    let headDurationMs = Math.abs(headDiffMs);
    let footDurationMs = Math.abs(footDiffMs);
    
    let isMaxCmd = (targetHeadMs === (HEAD_MAX_SECONDS * 1000)) && (targetFootMs === (FOOT_MAX_SECONDS * 1000));
    let isFlatCmd = (targetHeadMs === 0) && (targetFootMs === 0);

    if (isMaxCmd || isFlatCmd) {
        print('... FLAT/MAX command detected. Adding ' + numToStrJS(SYNC_EXTRA_MS, 0) + 'ms re-sync buffer.');
        // Only add buffer if motor needs to run
        if (headDurationMs > 0) { 
            headDurationMs += SYNC_EXTRA_MS;
        }
        if (footDurationMs > 0) { 
            footDurationMs += SYNC_EXTRA_MS;
        }
    }
    // --- END NEW ---

    if (headDiffMs !== 0 || footDiffMs !== 0) {
        activateTransferSwitch();
    } else {
        print('... Already at target position. No movement needed.');
        return 0; // No wait time
    }

    if (headDiffMs > 0) { 
        durationMs = headDurationMs; // Use new buffered duration
        print('... Starting HEAD_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "UP";
        GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // Interlock
        GPIO.write(HEAD_UP_PIN, RELAY_ON);

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_UP.');
            GPIO.write(HEAD_UP_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            if (bedState.zeroGFootTimerId === 0) stopMovement();
        }, null);

    } else if (headDiffMs < 0) { 
        durationMs = headDurationMs; // Use new buffered duration
        print('... Starting HEAD_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "DOWN";
        GPIO.write(HEAD_UP_PIN, RELAY_OFF); // Interlock
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_DOWN.');
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            if (bedState.zeroGFootTimerId === 0) stopMovement();
        }, null);
    } else {
        print('... Head is already at target position.');
    }

    if (footDiffMs > 0) { 
        durationMs = footDurationMs; // Use new buffered duration
        print('... Starting FOOT_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "UP";
        GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // Interlock
        GPIO.write(FOOT_UP_PIN, RELAY_ON);

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_UP.');
            GPIO.write(FOOT_UP_PIN, RELAY_OFF);
            updatePosition('foot'); 
            bedState.zeroGFootTimerId = 0;
            if (bedState.zeroGHeadTimerId === 0) stopMovement();
        }, null);

    } else if (footDiffMs < 0) { 
        durationMs = footDurationMs; // Use new buffered duration
        print('... Starting FOOT_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "DOWN";
        GPIO.write(FOOT_UP_PIN, RELAY_OFF); // Interlock
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_DOWN.');
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
            updatePosition('foot');
            bedState.zeroGFootTimerId = 0;
            if (bedState.zeroGHeadTimerId === 0) stopMovement();
        }, null);
    } else {
        print('... Foot is already at target position.');
    }

    return Math.max(headDurationMs, footDurationMs); // Return the longest duration
}

// --- NEW: Helper function to save a preset position ---
function savePresetPos(slot) {
    stopMovement(); // Get stable positions
    let head = bedState.currentHeadPosMs;
    let foot = bedState.currentFootPosMs;
    print('Saving ' + slot + ' Position. Head: ' + numToStrJS(head, 0) + ', Foot: ' + numToStrJS(foot, 0));
    
    let configToSave = { state: {} };
    configToSave.state[slot + '_head'] = head;
    configToSave.state[slot + '_foot'] = foot;
    Cfg.set(configToSave);
    
    let response = { saved_pos: slot };
    response[slot + '_head'] = head;
    response[slot + '_foot'] = foot;
    response[slot + '_label'] = Cfg.get('state.' + slot + '_label'); // Send back existing label
    return response;
}

// --- NEW: Helper function to save a preset label ---
function savePresetLabel(slot, args) {
    let label = (args && typeof args.label === 'string' && args.label) ? args.label : slot.toUpperCase();
    print('Saving ' + slot + ' Label: ' + label);

    let configToSave = { state: {} };
    configToSave.state[slot + '_label'] = label;
    Cfg.set(configToSave);
    
    let response = { saved_label: slot };
    response[slot + '_head'] = Cfg.get('state.' + slot + '_head'); // Send back existing position
    response[slot + '_foot'] = Cfg.get('state.' + slot + '_foot');
    response[slot + '_label'] = label;
    return response;
}

// --- NEW: Helper function to reset a preset ---
// slot: 'p1', 'p2', 'zg', 'snore', 'legs'
// defaults: object { head: H, foot: F, label: L }
function resetPreset(slot, defaults) {
    print('Resetting ' + slot + ' to defaults...');
    
    let configToSave = { state: {} };
    configToSave.state[slot + '_head'] = defaults.head;
    configToSave.state[slot + '_foot'] = defaults.foot;
    configToSave.state[slot + '_label'] = defaults.label;
    Cfg.set(configToSave);
    
    let response = { reset: slot };
    response[slot + '_head'] = defaults.head;
    response[slot + '_foot'] = defaults.foot;
    response[slot + '_label'] = defaults.label;
    return response;
}

// --- RPC: Command Handlers (as a map) ---
let commandHandlers = {

    'HEAD_UP': function(args) {
        let livePos = calculateLivePositions();
        let atMax = (livePos.head >= HEAD_MAX_SECONDS * 1000);

        if (atMax) {
            print("Executing: HEAD_UP - At max limit. Activating relay for re-sync.");
        } else {
            bedState.headStartTime = Timer.now(); // <-- Only start timer if NOT at max
            bedState.currentHeadDirection = "UP";
            print("Executing: HEAD_UP (Start Time Recorded)");
        }
        
        activateTransferSwitch(); 
        GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); 
        GPIO.write(HEAD_UP_PIN, RELAY_ON); // <-- Always activate
        
        return {}; 
    },
    'HEAD_DOWN': function(args) {
        let livePos = calculateLivePositions();
        let atMin = (livePos.head <= 0);

        if (atMin) {
            print("Executing: HEAD_DOWN - At min limit. Activating relay for re-sync.");
        } else {
            bedState.headStartTime = Timer.now(); // <-- Only start timer if NOT at min
            bedState.currentHeadDirection = "DOWN";
            print("Executing: HEAD_DOWN (Start Time Recorded)");
        }

        activateTransferSwitch(); 
        GPIO.write(HEAD_UP_PIN, RELAY_OFF); 
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON); // <-- Always activate

        return {};
    },
    'FOOT_UP': function(args) {
        let livePos = calculateLivePositions();
        let atMax = (livePos.foot >= FOOT_MAX_SECONDS * 1000);
        
        if (atMax) {
            print("Executing: FOOT_UP - At max limit. Activating relay for re-sync.");
        } else {
            bedState.footStartTime = Timer.now(); // <-- Only start timer if NOT at max
            bedState.currentFootDirection = "UP";
            print("Executing: FOOT_UP (Start Time Recorded)");
        }

        activateTransferSwitch(); 
        GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); 
        GPIO.write(FOOT_UP_PIN, RELAY_ON); // <-- Always activate
        
        return {};
    },
    'FOOT_DOWN': function(args) {
        let livePos = calculateLivePositions();
        let atMin = (livePos.foot <= 0);

        if (atMin) {
            print("Executing: FOOT_DOWN - At min limit. Activating relay for re-sync.");
        } else {
            bedState.footStartTime = Timer.now(); // <-- Only start timer if NOT at min
            bedState.currentFootDirection = "DOWN";
            print("Executing: FOOT_DOWN (Start Time Recorded)");
        }
        
        activateTransferSwitch(); 
        GPIO.write(FOOT_UP_PIN, RELAY_OFF); 
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON); // <-- Always activate
        
        return {};
    },

    'ALL_UP': function(args) {
        let livePos = calculateLivePositions();
        let atHeadMax = (livePos.head >= HEAD_MAX_SECONDS * 1000);
        let atFootMax = (livePos.foot >= FOOT_MAX_SECONDS * 1000);
        let nowSec = Timer.now();
        let logMsg = "Executing: ALL_UP";

        activateTransferSwitch(); 

        if (atHeadMax) {
            logMsg += " (Head @ Max, re-syncing)";
        } else {
            bedState.headStartTime = nowSec;
            bedState.currentHeadDirection = "UP";
            logMsg += " (Head Starting)";
        }
        
        if (atFootMax) {
            logMsg += " (Foot @ Max, re-syncing)";
        } else {
            bedState.footStartTime = nowSec;
            bedState.currentFootDirection = "UP";
            logMsg += " (Foot Starting)";
        }

        // Always activate relays
        GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); 
        GPIO.write(HEAD_UP_PIN, RELAY_ON);
        GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); 
        GPIO.write(FOOT_UP_PIN, RELAY_ON);
        
        print(logMsg);
        return {};
    },
    'ALL_DOWN': function(args) {
        let livePos = calculateLivePositions();
        let atHeadMin = (livePos.head <= 0);
        let atFootMin = (livePos.foot <= 0);
        let nowSec = Timer.now();
        let logMsg = "Executing: ALL_DOWN";

        activateTransferSwitch(); 

        if (atHeadMin) {
            logMsg += " (Head @ Min, re-syncing)";
        } else {
            bedState.headStartTime = nowSec;
            bedState.currentHeadDirection = "DOWN";
            logMsg += " (Head Starting)";
        }
        
        if (atFootMin) {
            logMsg += " (Foot @ Min, re-syncing)";
        } else {
            bedState.footStartTime = nowSec;
            bedState.currentFootDirection = "DOWN";
            logMsg += " (Foot Starting)";
        }

        // Always activate relays
        GPIO.write(HEAD_UP_PIN, RELAY_OFF); 
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        GPIO.write(FOOT_UP_PIN, RELAY_OFF); 
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);

        print(logMsg);
        return {};
    },
    'STOP': function(args) {
        stopMovement();
        print("Executing: STOP handler called.");
        return { maxWait: 0 };
    },    
    // --- Preset Recall Handlers ---
    'FLAT': function(args) {
        print('Executing: FLAT command initiated...');
        let maxWaitMs = executePositionPreset(0, 0); 
        return { maxWait: maxWaitMs };
    },
    // --- NEW: MAX Command ---
    'MAX': function(args) {
        print('Executing: MAX command initiated...');
        let maxWaitMs = executePositionPreset(HEAD_MAX_SECONDS * 1000, FOOT_MAX_SECONDS * 1000); 
        return { maxWait: maxWaitMs };
    },
    'ZERO_G': function(args) {
        let head = Cfg.get('state.zg_head');
        let foot = Cfg.get('state.zg_foot');
        print('Executing: Preset ' + Cfg.get('state.zg_label') + ' -> H:' + numToStrJS(head, 0) + ' F:' + numToStrJS(foot, 0));
        let maxWaitMs = executePositionPreset(head, foot);
        return { maxWait: maxWaitMs };
    },
    'ANTI_SNORE': function(args) {
        let head = Cfg.get('state.snore_head');
        let foot = Cfg.get('state.snore_foot');
        print('Executing: Preset ' + Cfg.get('state.snore_label') + ' -> H:' + numToStrJS(head, 0) + ' F:' + numToStrJS(foot, 0));
        let maxWaitMs = executePositionPreset(head, foot);
        return { maxWait: maxWaitMs };
    },
    'LEGS_UP': function(args) {
        let head = Cfg.get('state.legs_head');
        let foot = Cfg.get('state.legs_foot');
        print('Executing: Preset ' + Cfg.get('state.legs_label') + ' -> H:' + numToStrJS(head, 0) + ' F:' + numToStrJS(foot, 0));
        let maxWaitMs = executePositionPreset(head, foot);
        return { maxWait: maxWaitMs };
    },
    'P1': function(args) {
        let head = Cfg.get('state.p1_head');
        let foot = Cfg.get('state.p1_foot');
        print('Executing: Preset ' + Cfg.get('state.p1_label') + ' -> H:' + numToStrJS(head, 0) + ' F:' + numToStrJS(foot, 0));
        let maxWaitMs = executePositionPreset(head, foot);
        return { maxWait: maxWaitMs };
    },
    'P2': function(args) {
        let head = Cfg.get('state.p2_head');
        let foot = Cfg.get('state.p2_foot');
        print('Executing: Preset ' + Cfg.get('state.p2_label') + ' -> H:' + numToStrJS(head, 0) + ' F:' + numToStrJS(foot, 0));
        let maxWaitMs = executePositionPreset(head, foot);
        return { maxWait: maxWaitMs };
    },

    // --- Preset Save Handlers ---
    'SET_P1_POS': function(args) { return savePresetPos('p1'); },
    'SET_P2_POS': function(args) { return savePresetPos('p2'); },
    'SET_ZG_POS': function(args) { return savePresetPos('zg'); },
    'SET_SNORE_POS': function(args) { return savePresetPos('snore'); },
    'SET_LEGS_POS': function(args) { return savePresetPos('legs'); },

    'SET_P1_LABEL': function(args) { return savePresetLabel('p1', args); },
    'SET_P2_LABEL': function(args) { return savePresetLabel('p2', args); },
    'SET_ZG_LABEL': function(args) { return savePresetLabel('zg', args); },
    'SET_SNORE_LABEL': function(args) { return savePresetLabel('snore', args); },
    'SET_LEGS_LABEL': function(args) { return savePresetLabel('legs', args); },
    
    // --- Preset Reset Handlers ---
    'RESET_P1': function(args) { 
        return resetPreset('p1', { head: 0, foot: 0, label: "P1" }); 
    },
    'RESET_P2': function(args) { 
        return resetPreset('p2', { head: 0, foot: 0, label: "P2" }); 
    },
    'RESET_ZG': function(args) { 
        return resetPreset('zg', { head: 10000, foot: 40000, label: "Zero G" }); 
    },
    'RESET_SNORE': function(args) { 
        return resetPreset('snore', { head: 10000, foot: 0, label: "Anti-Snore" }); 
    },
    'RESET_LEGS': function(args) { 
        return resetPreset('legs', { head: 0, foot: 43000, label: "Legs Up" }); 
    },

    'UNKNOWN': function(cmd) {
        print('Unknown command received:', cmd);
        return { error: -1, message: 'Unknown command' };
    }
};

// --- RPC Handler: Bed.Command ---
RPC.addHandler('Bed.Command', function(args) {
    let cmd = args.cmd;
    if (typeof cmd !== 'string') {
        return { error: -1, message: 'Bad Request. Expected: {"cmd":"COMMAND"}' };
    }
    
    if(DEBUG) {
        print(">>> Debug: RPC Handler 'Bed.Command' received '" + cmd + "'");
    }

    let handler = commandHandlers[cmd] || commandHandlers.UNKNOWN;
    let result = handler(args); // Pass all args (for label)
    
    let livePos = calculateLivePositions();
    let now = Timer.now();
    
    // Build the base response
    let response = {
        bootTime: numToStrJS(now - Sys.uptime(), 0),
        uptime: numToStrJS(Sys.uptime(), 0),
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        maxWait: (result && typeof result.maxWait === 'number' ? result.maxWait : 0)
    };

    // --- NEW: Check for all new response types ---
    if (result && result.saved_pos) {
        let slot = result.saved_pos;
        response.saved_pos = slot;
        response[slot + '_head'] = result[slot + '_head'];
        response[slot + '_foot'] = result[slot + '_foot'];
        response[slot + '_label'] = result[slot + '_label'];
    }
    if (result && result.saved_label) {
        let slot = result.saved_label;
        response.saved_label = slot;
        response[slot + '_head'] = result[slot + '_head'];
        response[slot + '_foot'] = result[slot + '_foot'];
        response[slot + '_label'] = result[slot + '_label'];
    }
    if (result && result.reset) {
        let slot = result.reset;
        response.reset = slot;
        response[slot + '_head'] = result[slot + '_head'];
        response[slot + '_foot'] = result[slot + '_foot'];
        response[slot + '_label'] = result[slot + '_label'];
    }
    // --- END NEW ---
    
    if (result && result.error) {
        return result; // Forward the error object
    }
    
    return response;
});


// --- RPC Handler: Bed.Status ---
RPC.addHandler('Bed.Status', function(args) {
    let livePos = calculateLivePositions();
    let now = Timer.now();
    print(">>> Debug: RPC Handler 'Bed.Status' called.");
    
    // On status poll, we return LIVE data + ALL SAVED PRESET data
    return {
        bootTime: numToStrJS(now - Sys.uptime(), 0),
        uptime: numToStrJS(Sys.uptime(), 0),
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        maxWait: 0, 
        
        p1_head: Cfg.get('state.p1_head'),
        p1_foot: Cfg.get('state.p1_foot'),
        p1_label: Cfg.get('state.p1_label'),
        
        p2_head: Cfg.get('state.p2_head'),
        p2_foot: Cfg.get('state.p2_foot'),
        p2_label: Cfg.get('state.p2_label'),

        zg_head: Cfg.get('state.zg_head'),
        zg_foot: Cfg.get('state.zg_foot'),
        zg_label: Cfg.get('state.zg_label'),

        snore_head: Cfg.get('state.snore_head'),
        snore_foot: Cfg.get('state.snore_foot'),
        snore_label: Cfg.get('state.snore_label'),

        legs_head: Cfg.get('state.legs_head'),
        legs_foot: Cfg.get('state.legs_foot'),
        legs_label: Cfg.get('state.legs_label')
    };
});


// --- Main Entry Point ---

// Load initial state
let loadedHead = Cfg.get('state.head');
let loadedFoot = Cfg.get('state.foot');
if (typeof loadedHead === 'number' && loadedHead >= 0) {
    bedState.currentHeadPosMs = loadedHead;
}
if (typeof loadedFoot === 'number' && loadedFoot >= 0) {
    bedState.currentFootPosMs = loadedFoot;
}
print('Loaded initial state from Flash - Head:', numToStrJS(bedState.currentHeadPosMs / 1000.0, 2), 's, Foot:', numToStrJS(bedState.currentFootPosMs / 1000.0, 2), 's');

// Init hardware
initGPIOPins(); 
print(">>> initGPIOPins() FINISHED."); // <-- DEBUG: Heartbeat 2

print(">>> RPC Handlers for 'Bed.Command' and 'Bed.Status' registered.");
print(">>> Server is running (port set in mos.yml, e.g., 8080).");

// Optional: Print status every 5 seconds
Timer.set(5000, true, function() {
    let livePos = calculateLivePositions();
    let statusMsg = 'Uptime: ' + numToStrJS(Sys.uptime(), 2) + ' s';
    let headSec = livePos.head / 1000.0;
    let footSec = livePos.foot / 1000.0;
    statusMsg += ' | Pos H: ' + numToStrJS(headSec, 2) + 's | Pos F: ' + numToStrJS(footSec, 2) + 's';
    print(statusMsg);
}, null);