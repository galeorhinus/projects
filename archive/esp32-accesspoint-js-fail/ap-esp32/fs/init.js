// --- Load all necessary APIs at the absolute top (for handler definition) ---
load('api_timer.js');     
load('api_rpc.js');       
load('api_config.js');    
load('api_sys.js');       
load('api_events.js');    
load('api_net.js');       
load('api_wifi.js');      

print('--- init.js script loaded! (API defined globally) ---');

// --- 1. Define the RPC Handler (Handles the initial configuration save) ---
RPC.addHandler('My.SaveWifi', function(args) {
  print('Received Wi-Fi credentials: ' + JSON.stringify(args));
  
  // 1. Set STA config
  Cfg.set({wifi: { sta: { enable: true, ssid: args.ssid, pass: args.pass }}}, true);
  // 2. Set AP to be disabled on next boot
  Cfg.set({wifi: {ap: {enable: false}}}, true);
  // 3. Set http default file back to 'index.html' (for future provisioning attempts)
  Cfg.set({http: {default_file: 'index.html'}}, true);
  
  print('New credentials saved. Rebooting in 3 seconds...');
  Sys.reboot(3000); 
  return { status: 'ok', message: 'Credentials saved. Device is rebooting.' };
});

// --- 2. Event Handler (The sole source of truth for STA state transition) ---

// On successful IP acquisition, switch to app.html via reboot.
Event.addHandler(Net.STATUS_GOT_IP, function(ev, evdata, ud) {
  print('*** Net Event: GOT_IP - Device Connected ***');
  
  if (Cfg.get('http.default_file') !== 'app.html') {
    print('Switching from index.html to app.html...');
    Cfg.set({http: {default_file: 'app.html'}}, true);
    Sys.reboot(100); // Quick reboot to load new config/page
  }
}, null);

// On disconnection/Wi-Fi loss, switch back to index.html/setup mode.
Event.addHandler(Net.STATUS_DISCONNECTED, function(ev, evdata, ud) {
  print('*** Net Event: DISCONNECTED ***');
  
  if (Cfg.get('http.default_file') !== 'index.html') {
     print('Wi-Fi lost. Switching to index.html and rebooting...');
     Cfg.set({http: {default_file: 'index.html'}}, true);
     Sys.reboot(100);
  }
}, null);


// --- 3. Timer Logic (Only for First Boot AP Setup) ---
// This runs once quickly to ensure the initial AP state is set if no config exists.
Timer.set(100, false, function() {
  
  print('--- Initial State Check Running (100ms delay) ---');

  let ip = Cfg.get('wifi.sta.ip');
  let ap_is_enabled = Cfg.get('wifi.ap.enable');
  
  print('Current Wi-Fi IP from Cfg: ' + (ip ? ip : 'undefined')); 

  if (!ip && !ap_is_enabled) {
    // --- First Boot (Neither STA nor AP is on) ---
    print('First Boot: Enabling AP and saving config...');
    
    let apConfig = {
      ssid: Cfg.get('wifi.ap.ssid'),
      pass: Cfg.get('wifi.ap.pass'),
      ip: Cfg.get('wifi.ap.ip'),
      netmask: '255.255.255.0',
      gw: Cfg.get('wifi.ap.ip'),
      enable: true
    };
    
    // Set AP config and reboot to AP mode
    Cfg.set({wifi: {ap: apConfig}}, true);
    print('AP config saved. Device will reboot into AP mode.');
    Sys.reboot(100);
    
  } else if (ap_is_enabled && !ip) {
    // --- AP Mode (Setup Portal is Active) ---
    print('Timer: AP is already running. Serving index.html.');
    print('Connect to SSID: ' + Cfg.get('wifi.ap.ssid') + ' at http://' + Cfg.get('wifi.ap.ip'));
  } else if (ip) {
    // --- STA Mode (Connected) ---
    print('Timer: STA mode detected. Event handler will manage state.');
  }

}, null);

print('--- init.js script finished loading. Handlers are set. ---');