print('>>> fs/init.js script started.'); // <-- DEBUG: Heartbeat 1
// Load necessary Mongoose OS APIs.
load('api_sys.js');
load('api_timer.js');
load('api_gpio.js');
load('api_config.js');
load('api_math.js');
load('api_rpc.js');      // <-- For RPC.addHandler
load('utils.js');

// --- Constants ---
// HTTP_PORT is now set in mos.yml
let RELAY_ON = 0;
let RELAY_OFF = 1;
let HEAD_MAX_SECONDS = 28;
let FOOT_MAX_SECONDS = 43;
let FLAT_DURATION_MS = 30000; // This is now only a fallback for FLAT
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
// This function is called when a motor *stops*. It calculates the final
// position and saves it.
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

    // Update position unconditionally
    updatePosition('head'); 
    updatePosition('foot'); 

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

    // --- NEW: Deactivate transfer switch after stopping ---
    deactivateTransferSwitch();
}
// --- Hardware Initialization ---
function initGPIOPins() {
    print('Initializing GPIO control pins...');
    // Motor Pins
    GPIO.set_mode(HEAD_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(HEAD_DOWN_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_DOWN_PIN, GPIO.MODE_OUTPUT);
    // Light Pin
    GPIO.set_mode(LIGHT_PIN, GPIO.MODE_OUTPUT);
    // --- NEW: Transfer Switch Pins ---
    GPIO.set_mode(TRANSFER_PIN_1, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_2, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_3, GPIO.MODE_OUTPUT);
    GPIO.set_mode(TRANSFER_PIN_4, GPIO.MODE_OUTPUT);
    // --- END NEW ---

    // Set pins to the OFF state initially
    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    GPIO.write(LIGHT_PIN, RELAY_OFF);
    // --- NEW: Set transfer switch to OFF (wired remote active) ---
    GPIO.write(TRANSFER_PIN_1, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_2, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_3, RELAY_OFF);
    GPIO.write(TRANSFER_PIN_4, RELAY_OFF);
    // --- END NEW ---
    
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
    let willMove = false; // --- NEW: Flag to track if movement is needed ---

    print('Executing: Position-based PRESET command initiated...');
    
    // Stop any in-progress preset timers
    if (bedState.flatTimerId !== 0) { Timer.del(bedState.flatTimerId); bedState.flatTimerId = 0; }
    if (bedState.zeroGHeadTimerId !== 0) { Timer.del(bedState.zeroGHeadTimerId); bedState.zeroGHeadTimerId = 0; }
    if (bedState.zeroGFootTimerId !== 0) { Timer.del(bedState.zeroGFootTimerId); bedState.zeroGFootTimerId = 0; }
    
    let motorsRunning = (bedState.currentHeadDirection !== "STOPPED" || bedState.currentFootDirection !== "STOPPED");
    
    if (motorsRunning) {
        print('... Motors are running, calling stopMovement() first.');
        // stopMovement() will also deactivate transfer switch. This is OK.
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

    // --- 2. Execute Head Movement ---
    if (headDiffMs > 0) { 
        durationMs = headDiffMs;
        print('... Starting HEAD_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "UP";
        GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // Interlock
        GPIO.write(HEAD_UP_PIN, RELAY_ON);
        willMove = true;

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_UP.');
            GPIO.write(HEAD_UP_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            // If foot is also done, deactivate transfer switch
            if (bedState.zeroGFootTimerId === 0) deactivateTransferSwitch();
        }, null);

    } else if (headDiffMs < 0) { 
        durationMs = -headDiffMs;
        print('... Starting HEAD_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.headStartTime = nowSec;
        bedState.currentHeadDirection = "DOWN";
        GPIO.write(HEAD_UP_PIN, RELAY_OFF); // Interlock
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        willMove = true;

        bedState.zeroGHeadTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Head timer finished, stopping HEAD_DOWN.');
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
            updatePosition('head'); 
            bedState.zeroGHeadTimerId = 0;
            if (bedState.zeroGFootTimerId === 0) deactivateTransferSwitch();
        }, null);
    } else {
        print('... Head is already at target position.');
    }

    // --- 3. Execute Foot Movement ---
    if (footDiffMs > 0) { 
        durationMs = footDiffMs;
        print('... Starting FOOT_UP for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "UP";
        GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // Interlock
        GPIO.write(FOOT_UP_PIN, RELAY_ON);
        willMove = true;

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_UP.');
            GPIO.write(FOOT_UP_PIN, RELAY_OFF);
            updatePosition('foot'); 
            bedState.zeroGFootTimerId = 0;
            if (bedState.zeroGHeadTimerId === 0) deactivateTransferSwitch();
        }, null);

    } else if (footDiffMs < 0) { 
        durationMs = -footDiffMs;
        print('... Starting FOOT_DOWN for ' + numToStrJS(durationMs, 0) + 'ms');
        bedState.footStartTime = nowSec;
        bedState.currentFootDirection = "DOWN";
        GPIO.write(FOOT_UP_PIN, RELAY_OFF); // Interlock
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
        willMove = true;

        bedState.zeroGFootTimerId = Timer.set(durationMs, false, function() {
            print('PRESET: Foot timer finished, stopping FOOT_DOWN.');
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
            updatePosition('foot');
            bedState.zeroGFootTimerId = 0;
            if (bedState.zeroGHeadTimerId === 0) deactivateTransferSwitch();
        }, null);
    } else {
        print('... Foot is already at target position.');
    }

    // --- NEW: Activate transfer switch only if we are moving ---
    if (willMove) {
        activateTransferSwitch();
    }

    return Math.max(Math.abs(headDiffMs), Math.abs(footDiffMs));
}


// --- RPC Command Handler (for actions) ---
let commandHandlers = {
    'HEAD_UP': function(args) {
        let canMove = true;
        let livePos = calculateLivePositions();
        if (livePos.head >= HEAD_MAX_SECONDS * 1000) {
            canMove = false;
            print("Executing: HEAD_UP - Already at max position.");
        }
        if (canMove) {
            activateTransferSwitch(); // <-- NEW: Activate switch
            bedState.headStartTime = Timer.now();
            bedState.currentHeadDirection = "UP";
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // Ensure DOWN is off
            // --- END INTERLOCK ---
            GPIO.write(HEAD_UP_PIN, RELAY_ON);
            print("Executing: HEAD_UP (Start Time Recorded)");
        }
        return {}; // Return empty JSON for a successful RPC call
    },
    'HEAD_DOWN': function(args) {
        let canMove = true;
        let livePos = calculateLivePositions();
        if (livePos.head <= 0) {
            canMove = false;
            print("Executing: HEAD_DOWN - Already at min position (flat).");
        }
        if (canMove) {
            activateTransferSwitch(); // <-- NEW: Activate switch
            bedState.headStartTime = Timer.now();
            bedState.currentHeadDirection = "DOWN";
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(HEAD_UP_PIN, RELAY_OFF); // Ensure UP is off
            // --- END INTERLOCK ---
            GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
            print("Executing: HEAD_DOWN (Start Time Recorded)");
        }
        return {}; // Return empty JSON for a successful RPC call
    },
    'FOOT_UP': function(args) {
        let canMove = true;
        let livePos = calculateLivePositions();
         if (livePos.foot >= FOOT_MAX_SECONDS * 1000) {
            canMove = false;
            print("Executing: FOOT_UP - Already at max position.");
         }
        if(canMove) {
            activateTransferSwitch(); // <-- NEW: Activate switch
            bedState.footStartTime = Timer.now();
            bedState.currentFootDirection = "UP";
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // Ensure DOWN is off
            // --- END INTERLOCK ---
            GPIO.write(FOOT_UP_PIN, RELAY_ON);
            print("Executing: FOOT_UP (Start Time Recorded)");
        }
        return {}; // Return empty JSON for a successful RPC call
     },
    'FOOT_DOWN': function(args) {
        let canMove = true;
        let livePos = calculateLivePositions();
        if (livePos.foot <= 0) {
            canMove = false;
            print("Executing: FOOT_DOWN - Already at min position (flat).");
        }
        if(canMove){
            activateTransferSwitch(); // <-- NEW: Activate switch
            bedState.footStartTime = Timer.now();
            bedState.currentFootDirection = "DOWN";
            // --- SOFTWARE INTERLOCK ---
            GPIO.write(FOOT_UP_PIN, RELAY_OFF); // Ensure UP is off
            // --- END INTERLOCK ---
            GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
            print("Executing: FOOT_DOWN (Start Time Recorded)");
        }
        return {}; // Return empty JSON for a successful RPC call
     },
     'ALL_UP': function(args) {
        let startHead = true;
        let startFoot = true;
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
        
        if (startHead || startFoot) {
            activateTransferSwitch(); // <-- NEW: Activate switch
            if (startHead) {
                GPIO.write(HEAD_DOWN_PIN, RELAY_OFF); // Interlock
                GPIO.write(HEAD_UP_PIN, RELAY_ON);
            }
            if (startFoot) {
                GPIO.write(FOOT_DOWN_PIN, RELAY_OFF); // Interlock
                GPIO.write(FOOT_UP_PIN, RELAY_ON);
            }
        }
        print("Executing: ALL_UP" + (startHead ? " (Head Starting)" : "") + (startFoot ? " (Foot Starting)" : ""));
        return {};
    },
    'ALL_DOWN': function(args) {
        let startHead = true;
        let startFoot = true;
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

        if (startHead || startFoot) {
            activateTransferSwitch(); // <-- NEW: Activate switch
            if (startHead) {
                GPIO.write(HEAD_UP_PIN, RELAY_OFF); // Interlock
                GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
            }
            if (startFoot) {
                GPIO.write(FOOT_UP_PIN, RELAY_OFF); // Interlock
                GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
            }
        }
        print("Executing: ALL_DOWN" + (startHead ? " (Head Starting)" : "") + (startFoot ? " (Foot Starting)" : ""));
        return {};
    },
    'STOP': function(args) {
        stopMovement();
        print("Executing: STOP handler called.");
        return { maxWait: 0 };
    },
    'LIGHT_TOGGLE': function(args) {
        let currentState = GPIO.read_out(LIGHT_PIN);
        let newState = (currentState === RELAY_ON ? RELAY_OFF : RELAY_ON);
        GPIO.write(LIGHT_PIN, newState);
        print("Executing: LIGHT_TOGGLE -> " + (newState === RELAY_ON ? "ON" : "OFF"));
        return {};
    },
    'FLAT': function(args) {
        print('Executing: FLAT command initiated...');
        let maxWaitMs = executePositionPreset(0, 0); 
        return { maxWait: maxWaitMs };
    },
    'ZERO_G': function(args) {
        let maxWaitMs = executePositionPreset(ZEROG_HEAD_TARGET_MS, ZEROG_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    },
    'ANTI_SNORE': function(args) {
        let maxWaitMs = executePositionPreset(ANTI_SNORE_HEAD_TARGET_MS, ANTI_SNORE_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    },
    'LEGS_UP': function(args) {
        let maxWaitMs = executePositionPreset(LEGS_UP_HEAD_TARGET_MS, LEGS_UP_FOOT_TARGET_MS);
        return { maxWait: maxWaitMs };
    }
};

// --- RPC Handler Wrapper ---
// This single function will handle all API calls from the 'Bed.Command' endpoint.
RPC.addHandler('Bed.Command', function(args) {
    let cmd = args.cmd;
    if (typeof cmd !== 'string' || typeof commandHandlers[cmd] !== 'function') {
        return { error: -1, message: 'Bad or Unknown Command' };
    }
    
    print(">>> Debug: RPC Handler 'Bed.Command' received '" + cmd + "'");

    // Run the specific command handler
    let result = commandHandlers[cmd](args);
    
    // Get live positions *after* command has run
    let livePos = calculateLivePositions();
    let bootTime = Timer.now() - Sys.uptime();
    
    // Build the JSON response
    let response = {
        bootTime: bootTime, // Send boot timestamp
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        maxWait: (result && typeof result.maxWait === 'number' ? result.maxWait : 0)
    };
    
    return response;
});

// --- RPC Handler for STATUS polling ---
// This is a separate, safe, read-only command.
RPC.addHandler('Bed.Status', function(args) {
    let livePos = calculateLivePositions();
    let bootTime = Timer.now() - Sys.uptime();
    print(">>> Debug: RPC Handler 'Bed.Status' called.");
    return {
        bootTime: bootTime, // Send boot timestamp
        headPos: numToStrJS(livePos.head / 1000.0, 2),
        footPos: numToStrJS(livePos.foot / 1000.0, 2),
        maxWait: 0 // Status never has a wait time
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
print('>>> initGPIOPins() FINISHED.'); // <-- DEBUG: Heartbeat 2

print(">>> API Handlers Registered. Server is running on port 8080 (set in mos.yml).");

// Optional: Print status every 5 seconds
Timer.set(5000, true, function() {
    // Calculate live positions for logging, but don't save
    let livePos = calculateLivePositions();
    let statusMsg = 'Uptime: ' + numToStrJS(Sys.uptime(), 2) + ' s';
    let headSec = livePos.head / 1000.0;
    let footSec = livePos.foot / 1000.0;
    statusMsg += ' | Pos H: ' + numToStrJS(headSec, 2) + 's | Pos F: ' + numToStrJS(footSec, 2) + 's';
    print(statusMsg);
}, null);