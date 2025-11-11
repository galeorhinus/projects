// init.js — minimal AP onboarding bootstrap (no FFI, no HTTP handlers here)
load('api_config.js');
load('api_wifi.js');
load('api_timer.js');
load('api_sys.js');

print('=== Minimal init.js (AP bootstrap) ===');

// ---- 1) Decide AP/STA state -------------------------------------------------
// If STA is already enabled in config, do nothing special here (let it boot).
// Otherwise, enable AP with our onboarding SSID/pass so user can join.
let staEnabled = Cfg.get('wifi.sta.enable');
if (!staEnabled) {
  // Use your chosen onboarding SSID/pass
  let apSsid = Cfg.get('wifi.ap.ssid') || 'BedController-Setup';
  let apPass = Cfg.get('wifi.ap.pass') || '12345678';

  // Apply config and persist it (Cfg.set saves when 2nd arg is true)
  let ok = Cfg.set({
    wifi: {
      ap:  { enable: true, ssid: apSsid, pass: apPass },
      sta: { enable: false }
    }
  }, true);
  print('Cfg.set returned:', ok ? 'true' : 'false');

  if (ok) print('WiFi config applied; AP will start automatically.');
} else {
  print('STA already enabled in config; keeping existing WiFi settings.');
}

// ---- 2) Informative logs once the AP stack is up ----------------------------
// Give ESP a moment to bring AP up, then show the IP and onboarding URL.
Timer.set(3000 /* ms */, 0 /* oneshot */, function() {
  // Older builds may not have Wifi.ap.getIP(); fall back to common default.
  let ip = (Wifi.ap && Wifi.ap.getIP) ? Wifi.ap.getIP() : '192.168.4.1';
  print('Connect to your AP and open http://' + ip + '/');

  // Optional: point explicitly to your page if you serve /app.html
  // print('Or go directly to http://' + ip + '/index.html');
}, null);

// ---- 3) Optional: after user submits creds, the C endpoint should:
//   - set wifi.sta.ssid / wifi.sta.pass, wifi.sta.enable=true, wifi.ap.enable=false
//   - save config and reboot.
// Nothing else is needed here in JS. The device will come back up on STA.
