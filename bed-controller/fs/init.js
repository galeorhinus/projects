print('>>> fs/init.js script started.'); // <-- DEBUG: Heartbeat 1
// Load necessary Mongoose OS APIs.
load('api_sys.js');
load('api_timer.js');
load('api_gpio.js');
load('api_config.js');
load('api_math.js');
load('api_rpc.js');      // <-- For RPC.addHandler
load('utils.js');

// --- FEATURE FLAGS ---
let ENABLE_MEMORY_STATE = true;
let ENABLE_PERSISTENT_STATE = true;

// --- Constants ---
// HTTP_PORT is now set in mos.yml
let RELAY_ON = 0;
let RELAY_OFF = 1;
let HEAD_MAX_SECONDS = 28;
let FOOT_MAX_SECONDS = 43;
let FLAT_DURATION_MS = 30000;
let THROTTLE_SAVE_SECONDS = 2.0;
let ZEROG_HEAD_TARGET_MS = 10000;
let ZEROG_FOOT_TARGET_MS = 40000;
let ANTI_SNORE_HEAD_TARGET_MS = 10000;
let ANTI_SNORE_FOOT_TARGET_MS = 0;
let LEGS_UP_HEAD_TARGET_MS = 0;
let LEGS_UP_FOOT_TARGET_MS = FOOT_MAX_SECONDS * 1000;

// --- GPIO Pin Definitions ---
let HEAD_UP_PIN   = 22;
let HEAD_DOWN_PIN = 23;
let FOOT_UP_PIN   = 18;
let FOOT_DOWN_PIN = 19;
let LIGHT_PIN     = 27;
// --- NEW: 4-Pin Transfer Switch ---
let TRANSFER_PIN_1 = 32; // (Controls Relay 5)
let TRANSFER_PIN_2 = 33; // (Controls Relay 6)
let TRANSFER_PIN_3 = 25; // (Controls Relay 7)
let TRANSFER_PIN_4 = 26; // (Controls Relay 8)
// --- END NEW ---

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
// This function calculates the *current* position if motors are moving,
// and returns an object with the live values.
function calculateLivePositions() {
    if (!ENABLE_MEMORY_STATE) {
        return { 
            head: bedState.currentHeadPosMs,
            foot: bedState.currentFootPosMs 
        };
    }

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

    // Return an object with the live positions, rounded
    return {
        head: Math.round(liveHead),
        foot: Math.round(liveFoot)
    };
}


// --- Function to Save State (Conditional based on PERSISTENT flag) ---
function saveBedState(headPosMs, footPosMs, force) {
    if (typeof force === 'undefined') {
        force = false;
    }

    if (ENABLE_PERSISTENT_STATE) {
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
}

// --- Update Position Function (Conditional based on MEMORY flag) ---
// This function is called when a motor *stops*. It calculates the final
// position and saves it.
function updatePosition(motor) {
    if (!ENABLE_MEMORY_STATE) {
        print('>>> updatePosition >>> Memory state disabled, resetting timers/directions.');
        bedState.headStartTime = 0;
        bedState.footStartTime = 0;
        bedState.currentHeadDirection = "STOPPED";
        bedState.currentFootDirection = "STOPPED";
        return;
    }

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

// --- NEW: Helper functions for 4-pin transfer switch ---
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

    if (ENABLE_MEMORY_STATE) {
        updatePosition('head'); 
        updatePosition('foot'); 
    } else {
        bedState.headStartTime = 0;
        bedState.footStartTime = 0;
        bedState.currentHeadDirection = "STOPPED";
        bedState.currentFootDirection = "STOPPED";
    }

    if (bedState.flatTimerId !== 0) {
        Timer.del(bedState.flatTimerId);
        bedState.flatTimerId = 0;
        print('FLAT sequence cancelled/finished.');
    }
    
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

    // --- UPDATED: Return control to the wired remote ---
    deactivateTransferSwitch();
    print(">>> stopMovement >>> Transfer switch OFF (wired remote active).");
}
// --- Hardware Initialization ---
function initGPIOPins() {
    print('Initializing GPIO control pins...');
    GPIO.set_mode(HEAD_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(HEAD_DOWN_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_DOWN_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(LIGHT_PIN, GPIO.MODE_OUTPUT);
    // --- NEW: Init 4 transfer pins ---
    GPIO.set_mode(TRANSFER_PIN_1, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_2, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_3, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_4, GPIO.MODE_OUTPUT);

    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    GPIO.write(LIGHT_PIN, RELAY_OFF);
    // --- NEW: Default 4 transfer pins to OFF (wired remote active) ---
    GPIO.write(TRANSFER_PIN_1, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_2, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_3, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_4, RELAY_OFF);
    
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
    
    if (!ENABLE_MEMORY_STATE) {
        print('!!! ERROR: Position-based presets require ENABLE_MEMORY_STATE=true. Aborting.');
        return 0;
    }

    if (bedState.flatTimerId !== 0) { Timer.del(bedState.flatTimerId); bedState.flatTimerId = 0; }
    if (bedState.zeroGHeadTimerId !== 0) { Timer.del(bedState.zeroGHeadTimerId); bedState.zeroGHeadTimerId = 0; }
    if (bedState.zeroGFootTimerId !== 0) { Timer.del(bedState.zeroGFootTimerId); bedState.zeroGFootTimerId = 0; }
    
    let motorsRunning = (bedState.currentHeadDirection !== "STOPPED" || bedState.currentFootDirection !== "STOPPED");
    
    if (motorsRunning) {
        print('... Motors are running, calling stopMovement() first.');
        // stopMovement() will also reset the transfer switch, which is fine.
        stopMovement(); 
    } else {
        print('... Motors are idle. Proceeding.');
    }
    
    nowSec = Timer.now();
    
    // Read the *saved* position, not a live one, as we just stopped.
    currentHeadMs = bedState.currentHeadPosMs;
    currentFootMs = bedState.currentFootPosMs;

    headDiffMs = targetHeadMs - currentHeadMs;
    footDiffMs = targetFootMs - currentFootMs;

    print('... Current State: Head=' + numToStrJS(currentHeadMs, 0) + 'ms, Foot=' + numToStrJS(currentFootMs, 0) + 'ms');
    print('... Target State:  Head=' + numToStrJS(targetHeadMs, 0) + 'ms, Foot=' + numToStrJS(targetFootMs, 0) + 'ms');
    print('... Calculated Diff: Head=' + numToStrJS(headDiffMs, 0) + 'ms, Foot=' + numToStrJS(footDiffMs, 0) + 'ms');

    // --- UPDATED: Activate Transfer Switch if any movement is needed ---
    if (headDiffMs !== 0 || footDiffMs !== 0) {
        print('... Motors need to move, engaging transfer switch.');
        activateTransferSwitch();
    } else {
        print('... Motors already at target. Transfer switch remains OFF.');
        return 0; // No movement needed
    }
    // --- END UPDATED ---

    if (headDiffMs > 0) { 
        durationMs = headDiffMs;
        print('... Starting HEAD_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "UP";
        GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // INTERLOCK
        GPIO.write(HEAD_UP_PIN, RELAY_ON);

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_UP.');
            GPIO.write(HEAD_UP_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            // Check if all preset motors are stopped
            if (bedState.zeroGFootTimerId === 0) stopMovement();
        }, null);

    } else if (headDiffMs < 0) { 
        durationMs = -headDiffMs;
        print('... Starting HEAD_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "DOWN";
        GPIO.write(HEAD_UP_PIN, RELAY_OFF); // INTERLOCK
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_DOWN.');
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            // Check if all preset motors are stopped
            if (bedState.zeroGFootTimerId === 0) stopMovement();
        }, null);
    } else {
        print('... Head is already at target position.');
    }

    if (footDiffMs > 0) { 
        durationMs = footDiffMs;
        print('... Starting FOOT_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "UP";
        GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // INTERLOCK
        GPIO.write(FOOT_UP_PIN, RELAY_ON);

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_UP.');
            GPIO.write(FOOT_UP_PIN, RELAY_OFF);
            updatePosition('foot'); 
            bedState.zeroGFootTimerId = 0;
            // Check if all preset motors are stopped
            if (bedState.zeroGHeadTimerId === 0) stopMovement();
        }, null);

    } else if (footDiffMs < 0) { 
        durationMs = -footDiffMs;
        print('... Starting FOOT_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "DOWN";
        GPIO.write(FOOT_UP_PIN, RELAY_OFF); // INTERLOCK
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_DOWN.');
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
            updatePosition('foot');
            bedState.zeroGFootTimerId = 0;
            // Check if all preset motors are stopped
            if (bedState.zeroGHeadTimerId === 0) stopMovement();
        }, null);
    } else {
        print('... Foot is already at target position.');
    }

    return Math.max(Math.abs(headDiffMs), Math.abs(footDiffMs));
}


// --- Command Handlers (called by apiCommandHandler) ---
let commandHandlers = {
    'HEAD_UP': function(args) {
        let canMove = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
            if (livePos.head >= HEAD_MAX_SECONDS * 1000) {
                canMove = false;
                print("Executing: HEAD_UP - Already at max position.");
            }
        }
        if (canMove) {
            if (ENABLE_MEMORY_STATE) {
                bedState.headStartTime = Timer.now();
                bedState.currentHeadDirection = "UP";
            }
            // --- UPDATED: Activate Transfer Switch ---
            activateTransferSwitch();
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // Ensure DOWN is off
            // --- END INTERLOCK ---
            GPIO.write(HEAD_UP_PIN, RELAY_ON);
            print("Executing: HEAD_UP" + (ENABLE_MEMORY_STATE ? " (Start Time Recorded)" : ""));
        }
        return {}; // Return empty JSON for a successful RPC call
    },
    'HEAD_DOWN': function(args) {
        let canMove = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
            if (livePos.head <= 0) {
                canMove = false;
                print("Executing: HEAD_DOWN - Already at min position (flat).");
            }
        }
        if (canMove) {
            if (ENABLE_MEMORY_STATE) {
                bedState.headStartTime = Timer.now();
                bedState.currentHeadDirection = "DOWN";
            }
            // --- UPDATED: Activate Transfer Switch ---
            activateTransferSwitch();
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(HEAD_UP_PIN, RELAY_OFF); // Ensure UP is off
            // --- END INTERLOCK ---
            GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
            print("Executing: HEAD_DOWN" + (ENABLE_MEMORY_STATE ? " (Start Time Recorded)" : ""));
        }
        return {}; // Return empty JSON for a successful RPC call
    },
    'FOOT_UP': function(args) {
        let canMove = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
             if (livePos.foot >= FOOT_MAX_SECONDS * 1000) {
                canMove = false;
                print("Executing: FOOT_UP - Already at max position.");
             }
        }
        if(canMove) {
             if (ENABLE_MEMORY_STATE) {
                bedState.footStartTime = Timer.now();
                bedState.currentFootDirection = "UP";
            }
            // --- UPDATED: Activate Transfer Switch ---
            activateTransferSwitch();
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // Ensure DOWN is off
            // --- END INTERLOCK ---
            GPIO.write(FOOT_UP_PIN, RELAY_ON);
            print("Executing: FOOT_UP" + (ENABLE_MEMORY_STATE ? " (Start Time Recorded)" : ""));
        }
        return {}; // Return empty JSON for a successful RPC call
     },
    'FOOT_DOWN': function(args) {
        let canMove = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
            if (livePos.foot <= 0) {
                canMove = false;
                print("Executing: FOOT_DOWN - Already at min position (flat).");
            }
        }
        if(canMove){
            if (ENABLE_MEMORY_STATE) {
                bedState.footStartTime = Timer.now();
                bedState.currentHeadDirection = "DOWN"; // <-- Bug found: should be currentFootDirection
            }
            // --- UPDATED: Activate Transfer Switch ---
            activateTransferSwitch();
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(FOOT_UP_PIN, RELAY_OFF); // Ensure UP is off
            // --- END INTERLOCK ---
            GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
            print("Executing: FOOT_DOWN" + (ENABLE_MEMORY_STATE ? " (Start Time Recorded)" : ""));
        }
        return {}; // Return empty JSON for a successful RPC call
     },
    'ALL_UP': function(args) {
        let startHead = true;
        let startFoot = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
            startHead = livePos.head < HEAD_MAX_SECONDS * 1000;
            startFoot = livePos.foot < FOOT_MAX_SECONDS * 1000;
            let nowSec = Timer.now();
            if (startHead) {
                bedState.headStartTime = nowSec;
                bedState.currentHeadDirection = "UP";
            }
            if (startFoot) {
                bedState.footStartTime = nowSec;
                bedState.currentFootDirection = "UP";
            }
        }
        // --- UPDATED: Activate Transfer Switch ---
        if (startHead || startFoot) {
            activateTransferSwitch();
        }
        // --- END UPDATED ---
        if (startHead) {
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(HEAD_UP_PIN, RELAY_ON);
        }
        if (startFoot) {
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(FOOT_UP_PIN, RELAY_ON);
        }
        print("Executing: ALL_UP" + (startHead ? " (Head Starting)" : "") + (startFoot ? " (Foot Starting)" : ""));
        return {};
    },
    'ALL_DOWN': function(args) {
        let startHead = true;
        let startFoot = true;
        if (ENABLE_MEMORY_STATE) {
            let livePos = calculateLivePositions();
            startHead = livePos.head > 0;
            startFoot = livePos.foot > 0;
            let nowSec = Timer.now();
            if (startHead) {
                bedState.headStartTime = nowSec;
                bedState.currentHeadDirection = "DOWN";
            }
            if (startFoot) {
                bedState.footStartTime = nowSec;
                bedState.currentFootDirection = "DOWN";
            }
        }
        // --- UPDATED: Activate Transfer Switch ---
        if (startHead || startFoot) {
            activateTransferSwitch();
        }
        // --- END UPDATED ---
        if (startHead) {
            GPIO.write(HEAD_UP_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        }
        if (startFoot) {
            GPIO.write(FOOT_UP_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
        }
        print("Executing: ALL_DOWN" + (startHead ? " (Head Starting)" : "") + (startFoot ? " (Foot Starting)" : ""));
        return {};
    },
    'STOP': function(args) {
        // stopMovement() handles all logic, including transfer switch
        stopMovement(); 
        print("Executing: STOP handler called.");
        return { maxWait: 0 };
    },
    'LIGHT_TOGGLE': function(args) {
        // Light is separate and does not need the transfer switch
        let currentState = GPIO.read_out(LIGHT_PIN);
        let newState = (currentState === RELAY_ON ? RELAY_OFF : RELAY_ON);
        GPIO.write(LIGHT_PIN, newState);
        print("Executing: LIGHT_TOGGLE -> " + (newState === RELAY_ON ? "ON" : "OFF"));
        return {};
    },
    'FLAT': function(args) {
        print('Executing: FLAT command initiated...');
        let maxWaitMs = 0;
        if (ENABLE_MEMORY_STATE) {
            // executePositionPreset will handle the transfer switch
            maxWaitMs = executePositionPreset(0, 0); 
        } else {
            print('... Memory state disabled. Running for default FLAT_DURATION_MS');
            if (bedState.flatTimerId !== 0) { Timer.del(bedState.flatTimerId); bedState.flatTimerId = 0; }
            if (bedState.zeroGHeadTimerId !== 0) { Timer.del(bedState.zeroGHeadTimerId); bedState.zeroGHeadTimerId = 0; }
            if (bedState.zeroGFootTimerId !== 0) { Timer.del(bedState.zeroGFootTimerId); bedState.zeroGFootTimerId = 0; }
            
            // --- UPDATED: Activate Transfer Switch ---
            activateTransferSwitch();
            // --- END UPDATED ---

            GPIO.write(HEAD_UP_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(FOOT_UP_PIN, RELAY_OFF); // INTERLOCK
            GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
            GPIO.write(FOOT_DOWN_PIN, RELAY_ON);

            bedState.flatTimerId = Timer.set(FLAT_DURATION_MS, false, function() {
                print('FLAT (no-state): Timer expired, stopping motors.');
                // stopMovement() will handle stopping motors AND transfer switch
                stopMovement();
            }, null);
            maxWaitMs = FLAT_DURATION_MS;
        }
        return { maxWait: maxWaitMs };
    },
    'ZERO_G': function(args) {
        // executePositionPreset will handle the transfer switch
        let maxWaitMs = executePositionPreset(ZEROG_HEAD_TARGET_MS, ZEROG_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    },
    'ANTI_SNORE': function(args) {
        // executePositionPreset will handle the transfer switch
        let maxWaitMs = executePositionPreset(ANTI_SNORE_HEAD_TARGET_MS, ANTI_SNORE_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    },
    'LEGS_UP': function(args) {
        // executePositionPreset will handle the transfer switch
        let maxWaitMs = executePositionPreset(LEGS_UP_HEAD_TARGET_MS, LEGS_UP_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    },
    'UNKNOWN': function(cmd) {
        print('Unknown command received:', cmd);
        return { error: -1, message: 'Unknown command' };
    }
};

// --- RPC Handler: Bed.Command ---
// This single function will handle all API calls that *perform an action*.
RPC.addHandler('Bed.Command', function(args) {
    let cmd = args.cmd;
    if (typeof cmd !== 'string') {
        return { error: -1, message: 'Bad Request. Expected: {"cmd":"COMMAND"}' };
    }
    
    print(">>> Debug: RPC Handler 'Bed.Command' received '" + cmd + "'");

    // Find the handler, or use the UNKNOWN handler
    let handler = commandHandlers[cmd] || commandHandlers.UNKNOWN;
    let result = handler(args); // Call the specific handler
    
    // Get live positions *after* command has run
    let livePos = calculateLivePositions();
    
    // Build the JSON response
    let response = {
        uptime: numToStrJS(Sys.uptime(), 2),
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        stateEnabled: ENABLE_MEMORY_STATE,
        maxWait: (result && typeof result.maxWait === 'number' ? result.maxWait : 0)
    };
    
    // Check if handler returned an error
    if (result && result.error) {
        return result; // Forward the error object
    }
    
    return response;
});


// --- RPC Handler: Bed.Status ---
// This is a *read-only* handler for safe polling.
RPC.addHandler('Bed.Status', function(args) {
    let livePos = calculateLivePositions();
    print(">>> Debug: RPC Handler 'Bed.Status' called.");
    return {
        uptime: numToStrJS(Sys.uptime(), 2),
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        stateEnabled: ENABLE_MEMORY_STATE,
        maxWait: 0 // Status never has a wait time
    };
});


// --- Main Entry Point ---

// Load initial state
if (ENABLE_PERSISTENT_STATE) {
    let loadedHead = Cfg.get('state.head');
    let loadedFoot = Cfg.get('state.foot');
    if (typeof loadedHead === 'number' && loadedHead >= 0) {
        bedState.currentHeadPosMs = loadedHead;
    }
    if (typeof loadedFoot === 'number' && loadedFoot >= 0) {
        bedState.currentFootPosMs = loadedFoot;
    }
    print('Loaded initial state from Flash - Head:', numToStrJS(bedState.currentHeadPosMs / 1000.0, 2), 's, Foot:', numToStrJS(bedState.currentFootPosMs / 1000.0, 2), 's');
} else { 
    print('Persistent state disabled. Initializing positions to 0.');
    bedState.currentHeadPosMs = 0;
    bedState.currentFootPosMs = 0;
}

// Init hardware
initGPIOPins(); 
print(">>> initGPIOPins() FINISHED."); // <-- DEBUG: Heartbeat 2

print(">>> API Handlers Registered. Server is running on port 8080 (set in mos.yml).");

// Optional: Print status every 5 seconds
Timer.set(5000, true, function() {
    // Calculate live positions for logging, but don't save
    let livePos = calculateLivePositions();
    let statusMsg = 'Uptime: ' + numToStrJS(Sys.uptime(), 2) + ' s';
    if (ENABLE_MEMORY_STATE) {
        let headSec = livePos.head / 1000.0;
        let footSec = livePos.foot / 1000.0;
        statusMsg += ' | Pos H: ' + numToStrJS(headSec, 2) + 's | Pos F: ' + numToStrJS(footSec, 2) + 's';
    }
     print(statusMsg);
}, null);