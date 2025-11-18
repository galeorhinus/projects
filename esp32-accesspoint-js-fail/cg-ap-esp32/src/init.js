load('api_config.js');
load('api_events.js');
load('api_http.js');
load('api_rpc.js');
load('api_timer.js');
load('api_wifi.js');

print('--- init.js: Starting BedController setup script ---');

let AP_SSID = Cfg.get('wifi.ap.ssid') || 'BedController-Setup';
let AP_PASS = Cfg.get('wifi.ap.pass') || '12345678';
let HTML_FILE = 'app.html';

// --- Setup Access Point ---
print('init.js: Setting up Access Point SSID:', AP_SSID);
Cfg.set({ wifi: { ap: { enable: true, ssid: AP_SSID, pass: AP_PASS } } });
Cfg.save();
print('init.js: Access Point configuration applied.');

// --- Monitor Wi-Fi events ---
Event.addGroupHandler(Net.EVENT_GRP, function(ev, evdata, arg) {
  if (ev === Net.STATUS_DISCONNECTED) {
    print('Wi-Fi: Disconnected');
  } else if (ev === Net.STATUS_CONNECTING) {
    print('Wi-Fi: Connecting...');
  } else if (ev === Net.STATUS_CONNECTED) {
    print('Wi-Fi: Connected, waiting for IP...');
  } else if (ev === Net.STATUS_GOT_IP) {
    print('Wi-Fi: Got IP:', Cfg.get('wifi.sta.ip'));
  }
}, null);

// --- Captive portal redirect ---
HTTPServer.registerEndpoint('/', function(req, res) {
  print('HTTP: Captive portal root hit, redirecting to /app.html');
  res.sendRedirect('/app.html');
});

HTTPServer.registerEndpoint('/generate_204', function(req, res) {
  // Android captive portal check URL
  print('HTTP: Android captive portal check, redirecting to /app.html');
  res.sendRedirect('/app.html');
});

HTTPServer.registerEndpoint('/fwlink', function(req, res) {
  // Windows captive portal check URL
  print('HTTP: Windows captive portal check, redirecting to /app.html');
  res.sendRedirect('/app.html');
});

// --- Serve main setup page ---
HTTPServer.registerEndpoint('/app.html', function(req, res) {
  print('HTTP: Serving app.html');
  let html = File.read(HTML_FILE);
  if (html) {
    res.send(200, html, 'text/html');
  } else {
    res.send(404, 'app.html not found');
  }
});

// --- RPC endpoint to save Wi-Fi credentials ---
RPC.addHandler('SaveWifi', function(args) {
  print('RPC: SaveWifi called with args:', JSON.stringify(args));

  if (!args || !args.ssid || !args.pass) {
    print('RPC: Missing SSID or password');
    return { success: false, error: 'Missing ssid or pass' };
  }

  let ok = Cfg.set({
    wifi: {
      sta: { ssid: args.ssid, pass: args.pass, enable: true },
      ap: { enable: false }
    }
  });

  print('RPC: Cfg.set() result:', ok);
  if (ok) {
    Cfg.save();
    print('RPC: Wi-Fi credentials saved, rebooting in 2 seconds...');
    Sys.reboot(2000);
  }

  return { success: ok };
});

print('init.js: Initialization complete. Awaiting connections...');
