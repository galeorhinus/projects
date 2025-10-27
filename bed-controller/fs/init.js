// Load necessary Mongoose OS APIs. These objects are made global.
load('api_sys.js');      // Sys.uptime(), Sys.usleep()
load('api_timer.js');    // Timer.set(), Timer.now(), Timer.del()
load('api_net.js');      // Net.serve() and networking events
load('api_gpio.js');     // GPIO.set_mode(), GPIO.write(), GPIO.read_out()
// api_config.js and api_math.js removed as state saving is removed

// --- Constants ---
let HTTP_PORT = 8080;
let MAX_BUFFER_SIZE = 100;

let RELAY_ON = 0;
let RELAY_OFF = 1;

let HEAD_MAX_SECONDS = 28; // Max time head takes to go fully up/down
let FOOT_MAX_SECONDS = 43; // Max time foot takes to go fully up/down
let FLAT_DURATION_MS = 30000; // Run down motors for 30 seconds for FLAT
let ZEROG_DURATION_MS = 15000; // Run up motors for 15 seconds for ZERO_G

// --- GPIO Pin Definitions ---
let HEAD_UP_PIN   = 22;
let HEAD_DOWN_PIN = 23;
let FOOT_UP_PIN   = 18;
let FOOT_DOWN_PIN = 19;
// Removed ALL_UP_PIN and ALL_DOWN_PIN as they are not needed
let LIGHT_PIN     = 27;

// --- State Variables (Simplified - only timer IDs for presets) ---
let flatTimerId = 0; // Single timer ID for FLAT sequence
let zeroGTimerId = 0; // Single timer ID for ZERO_G sequence

// --- Helper for Number-to-String Conversion (FROZEN VERSION v1.0) ---
function numToStrJS(num) {
    if (num === 0) return "0";
    let is_negative = false;
    if (num < 0) {
        is_negative = true;
        num = -num;
    }

    // chr() is a global MJS function that converts ASCII code to character.
    // Ensure the fallback matches the original working version
    if (typeof chr === 'undefined') { return String(num); } // Using String() as per v1.0

    let result = "";
    // Handle potential floating point values by flooring before loop
    // Convert float to int before processing digits
    let intNum = 0;
    if (num > 0) { // Avoid Math.floor on 0 or negative
        intNum = Math.floor(num);
    }

    while (intNum > 0) {
        let digit = intNum % 10;
        result = chr(digit + 48) + result; // 48 is ASCII for '0'
        intNum = Math.floor(intNum / 10);
    }

    if (is_negative) {
        result = chr(45) + result; // 45 is ASCII for '-'
    }
    // Handle cases where the integer part was 0 but there was a fractional part (unlikely for uptime/length)
    if (result === "" && !is_negative && num > 0) return "0";

    return result;
}
// --- END OF FROZEN numToStrJS ---


// --- Hardware Initialization ---
function initGPIOPins() {
    print('Initializing GPIO control pins...');
    GPIO.set_mode(HEAD_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(HEAD_DOWN_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_UP_PIN, GPIO.MODE_OUTPUT);
    GPIO.set_mode(FOOT_DOWN_PIN, GPIO.MODE_OUTPUT);
    // Removed ALL_UP_PIN and ALL_DOWN_PIN setup
    GPIO.set_mode(LIGHT_PIN, GPIO.MODE_OUTPUT);

    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    // Removed ALL_UP_PIN and ALL_DOWN_PIN init write
    GPIO.write(LIGHT_PIN, RELAY_OFF);
    print('GPIO pins initialized to OFF state.');
}

// --- Simplified Stop Function ---
// Stops all motor relays and cancels any running preset timers
function stopMovement() {
    GPIO.write(HEAD_UP_PIN, RELAY_OFF);
    GPIO.write(HEAD_DOWN_PIN, RELAY_OFF);
    GPIO.write(FOOT_UP_PIN, RELAY_OFF);
    GPIO.write(FOOT_DOWN_PIN, RELAY_OFF);
    // Removed ALL_UP_PIN and ALL_DOWN_PIN writes

    // Cancel any running preset timers
    if (flatTimerId !== 0) {
        Timer.del(flatTimerId);
        flatTimerId = 0;
        print('FLAT sequence cancelled by STOP.');
    }
    if (zeroGTimerId !== 0) {
        Timer.del(zeroGTimerId);
        zeroGTimerId = 0;
        print('ZERO_G sequence cancelled by STOP.');
    }

    print('Command: STOP executed (All Motor Relays OFF)');
}

// --- Command Execution (Simplified) ---
function executeCommand(cmd) {

    // Always stop previous motor movements first
    stopMovement();

    // --- Handle Movement Start Commands ---
    if (cmd === 'HEAD_UP') {
        GPIO.write(HEAD_UP_PIN, RELAY_ON);
        print("Executing: HEAD_UP");
    } else if (cmd === 'HEAD_DOWN') {
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        print("Executing: HEAD_DOWN");
    } else if (cmd === 'FOOT_UP') {
        GPIO.write(FOOT_UP_PIN, RELAY_ON);
        print("Executing: FOOT_UP");
    } else if (cmd === 'FOOT_DOWN') {
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
        print("Executing: FOOT_DOWN");
    } else if (cmd === 'ALL_UP') {
        // *** UPDATED: Activate Head and Foot Up simultaneously ***
        GPIO.write(HEAD_UP_PIN, RELAY_ON);
        GPIO.write(FOOT_UP_PIN, RELAY_ON);
        print("Executing: ALL_UP (activating Head Up + Foot Up pins)");
    } else if (cmd === 'ALL_DOWN') {
         // *** UPDATED: Activate Head and Foot Down simultaneously ***
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);
        print("Executing: ALL_DOWN (activating Head Down + Foot Down pins)");

    // --- Handle Stop Command ---
    } else if (cmd === 'STOP') {
        // stopMovement() was already called at the start
        print("Executing: STOP");

    // --- Handle Light Command ---
    } else if (cmd === 'LIGHT_TOGGLE') {
        let currentState = GPIO.read_out(LIGHT_PIN);
        let newState = (currentState === RELAY_ON ? RELAY_OFF : RELAY_ON);
        GPIO.write(LIGHT_PIN, newState);
        print("Executing: LIGHT_TOGGLE -> " + (newState === RELAY_ON ? "ON" : "OFF"));

    // --- Handle Preset Commands (Simple Timed Logic) ---
    } else if (cmd === 'FLAT') {
        print('Executing: FLAT command initiated (run down ' + numToStrJS(FLAT_DURATION_MS / 1000) + 's).');
        // Activate both down relays
        GPIO.write(HEAD_DOWN_PIN, RELAY_ON);
        GPIO.write(FOOT_DOWN_PIN, RELAY_ON);

        // Set a timer to stop them after the duration
        flatTimerId = Timer.set(FLAT_DURATION_MS, false /* one-shot */, function() {
            print('FLAT: Timer expired, stopping motors.');
            stopMovement(); // Stop all motors
            flatTimerId = 0; // Clear the timer ID
        }, null);

    } else if (cmd === 'ZERO_G') {
        print('Executing: ZERO_G command initiated (run up ' + numToStrJS(ZEROG_DURATION_MS / 1000) + 's).');
        // Activate both up relays
        GPIO.write(HEAD_UP_PIN, RELAY_ON);
        GPIO.write(FOOT_UP_PIN, RELAY_ON);

        // Set a timer to stop them
        zeroGTimerId = Timer.set(ZEROG_DURATION_MS, false /* one-shot */, function() {
            print('ZERO_G: Timer expired, stopping motors.');
            stopMovement(); // Stop all motors
            zeroGTimerId = 0; // Clear the timer ID
        }, null);

    } else {
        print('Unknown command received:', cmd);
    }
}


// --- HTML Page Generation ---
function buildHtmlPage() {
    let html = '';
    html += '<html><head><title>Bed Controller</title>';
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">';
    html += '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">';
    html += '<style>';
    html += 'body { font-family: sans-serif; margin: 0; background-color: #1f2937; color: #f9fafb; display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding-top: 20px; }';
    html += '.container { width: 90%; max-width: 400px; }';
    html += 'h1 { text-align: center; color: #e5e7eb; margin-bottom: 20px; }';
    html += '.btn-group { display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px; }';
    html += '.row { display: flex; justify-content: space-between; gap: 15px; }';
    html += 'button { flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 20px 10px; font-size: 16px; border: none; border-radius: 8px; cursor: pointer; transition: background-color 0.15s, transform 0.1s; user-select: none; -webkit-user-select: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }';
    html += 'button i { font-size: 1.1em; }';
    html += 'button:active { transform: scale(0.97); box-shadow: 0 2px 3px rgba(0,0,0,0.1); }';
    html += '.control-btn { background-color: #3b82f6; color: white; }';
    html += '.control-btn:hover { background-color: #2563eb; }';
    html += '.stop-btn { background-color: #ef4444; color: white; font-weight: bold;}';
    html += '.stop-btn:hover { background-color: #dc2626; }';
    html += '.preset-btn { background-color: #f59e0b; color: white; }';
    html += '.preset-btn:hover { background-color: #d97706; }';
    html += '.all-btn { background-color: #10b981; color: white; }'; // Style for All Up/Down
    html += '.all-btn:hover { background-color: #059669; }';
    html += '.light-btn { background-color: #8b5cf6; color: white; }'; // Style for Light
    html += '.light-btn:hover { background-color: #7c3aed; }';
    html += '.status { text-align: center; margin-top: 20px; font-size: 14px; color: #a1a1aa; }';
    html += '</style></head><body><div class="container"><h1><i class="fas fa-bed"></i> Bed Control</h1>';
    html += '<div class="btn-group">';

    // --- Button Layout with Icons ---
    html += '<div class="row">';
    html += '<button class="control-btn" ontouchstart="sendCmd(\'HEAD_UP\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'HEAD_UP\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-arrow-up"></i> Head Up</button>';
    html += '<button class="control-btn" ontouchstart="sendCmd(\'HEAD_DOWN\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'HEAD_DOWN\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-arrow-down"></i> Head Down</button>';
    html += '</div>';
    html += '<div class="row">';
    html += '<button class="control-btn" ontouchstart="sendCmd(\'FOOT_UP\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'FOOT_UP\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-arrow-up"></i> Foot Up</button>';
    html += '<button class="control-btn" ontouchstart="sendCmd(\'FOOT_DOWN\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'FOOT_DOWN\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-arrow-down"></i> Foot Down</button>';
    html += '</div>';
    // --- All Up / All Down Buttons ---
    html += '<div class="row">';
    html += '<button class="all-btn" ontouchstart="sendCmd(\'ALL_UP\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'ALL_UP\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-angles-up"></i> All Up</button>';
    html += '<button class="all-btn" ontouchstart="sendCmd(\'ALL_DOWN\')" ontouchend="sendCmd(\'STOP\')" onmousedown="sendCmd(\'ALL_DOWN\')" onmouseup="sendCmd(\'STOP\')"><i class="fas fa-angles-down"></i> All Down</button>';
    html += '</div>';
    // --- STOP Button ---
    html += '<div class="row">';
    html += '<button class="stop-btn" style="flex-grow: 2;" onclick="sendCmd(\'STOP\')"><i class="fas fa-stop-circle"></i> STOP ALL MOTORS</button>';
    html += '</div>';
    // --- Light Button ---
    html += '<div class="row">';
    html += '<button class="light-btn" style="flex-grow: 2;" onclick="sendCmd(\'LIGHT_TOGGLE\')"><i class="fas fa-lightbulb"></i> Toggle Light</button>';
    html += '</div>';
    // --- Presets ---
    html += '<div class="row">';
    html += '<button class="preset-btn" onclick="sendCmd(\'FLAT\')"><i class="fas fa-minus"></i> Flat</button>';
    html += '<button class="preset-btn" onclick="sendCmd(\'ZERO_G\')"><i class="fas fa-rocket"></i> Zero G</button>';
    html += '</div>';
    html += '</div>'; // end btn-group

    // --- Simplified Status ---
    // Removed ALL_UP/ALL_DOWN pins from status
    html += '<div class="status">Uptime: ' + numToStrJS(Sys.uptime()) + 's | Pins: H:' + numToStrJS(HEAD_UP_PIN)+','+numToStrJS(HEAD_DOWN_PIN) + ' F:'+numToStrJS(FOOT_UP_PIN)+','+numToStrJS(FOOT_DOWN_PIN) + ' L:'+numToStrJS(LIGHT_PIN) + '</div>';
    html += '</div>'; // end container
    html += '<script>';
    html += 'function sendCmd(cmd) {';
    html += '  var xhr = new XMLHttpRequest();';
    html += '  xhr.open("GET", "/?cmd=" + cmd, true);';
    html += '  xhr.send();';
    html += '  console.log("Sent: " + cmd);';
    // No reload needed for simple timed presets or momentary controls
    html += '}';
    html += '</script>';
    html += '</body></html>';
    return html;
}
// --- END HTML ---


// --- Main Entry Point ---

initGPIOPins(); // Initialize hardware pins

// Start an HTTP server
Net.serve({
    addr: 'tcp://:' + numToStrJS(HTTP_PORT),
    onconnect: function(conn) { print('HTTP Connection from', Net.ctos(conn, false, true, true)); },
    onclose: function(conn) { print('HTTP connection closed'); },
    ondata: function(conn, data) {
      // print('Raw ondata:', data.length, 'bytes'); // Optional: Verbose

      if (data.indexOf('GET /?cmd=') === 0) {
          let uriStart = data.indexOf('GET /?cmd=') + 10;
          let uriEnd = data.indexOf(' ', uriStart);
          if (uriEnd === -1) {
              uriEnd = data.indexOf('\r', uriStart);
              if (uriEnd === -1) uriEnd = data.indexOf('\n', uriStart);
              if (uriEnd === -1) uriEnd = data.length;
          }
          let cmd = data.slice(uriStart, uriEnd);

          // print("Raw Command Extracted: '" + cmd + "'"); // Optional Debug
          if (cmd.slice(0, 1) === ' ') { cmd = cmd.slice(1); }
          if (cmd.slice(cmd.length - 1) === ' ') { cmd = cmd.slice(0, cmd.length - 1); }
          // print("Trimmed Command Extracted: '" + cmd + "'"); // Optional Debug

          executeCommand(cmd);
          let okResponse = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK';
          Net.send(conn, okResponse);

      } else if (data.indexOf('GET / ') === 0) {
          let htmlContent = buildHtmlPage();
          let htmlLength = numToStrJS(htmlContent.length);
          let response = 'HTTP/1.1 200 OK\r\n' +
                         'Content-Type: text/html\r\n' +
                         'Content-Length: ' + htmlLength + '\r\n' +
                         'Connection: close\r\n\r\n' +
                         htmlContent;
          Net.send(conn, response);

      } else if (data.length > 0) {
          let notFoundMsg = 'Not Found';
          let notFoundLength = numToStrJS(notFoundMsg.length);
          let response = 'HTTP/1.1 404 Not Found\r\n' +
                         'Content-Type: text/plain\r\n' +
                         'Content-Length: ' + notFoundLength + '\r\n' +
                         'Connection: close\r\n\r\n' +
                         notFoundMsg;
          Net.send(conn, response);
      }
      Net.discard(conn, data.length);
      Net.close(conn);
    }
});

// Optional: Print system uptime every 5 seconds
Timer.set(5000, true, function() {
  // Simplified print, no position tracking
  print('Uptime:', numToStrJS(Sys.uptime()), 's');
}, null);

