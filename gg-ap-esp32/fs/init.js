// --- Load all necessary APIs at the absolute top ---
load('api_timer.js');     
load('api_rpc.js');       
load('api_config.js');    
load('api_sys.js');       
load('api_events.js');    
load('api_net.js');       
load('api_wifi.js');      

print('--- init.js script loaded! (Using rpc-service-wifi) ---');

// --- 1. Define RPC Handlers ---

// This handler is called by index.html to save credentials
RPC.addHandler('My.SaveWifi', function(args) {
  print('Received Wi-Fi credentials: ' + JSON.stringify(args));
  
  // 1. Set STA config
  Cfg.set({wifi: { sta: { enable: true, ssid: args.ssid, pass: args.pass }}}, true);
  
  // 2. We NO LONGER disable the AP. We want AP+STA mode.
  //    We also ensure the default file is index.html for polling.
  Cfg.set({http: {default_file: 'index.html'}}, true);
  
  print('New credentials saved. Rebooting in 3 seconds (AP will remain ON)...');
  Sys.reboot(3000); 
  return { status: 'ok', message: 'Credentials saved. Device is rebooting.' };
});

// *** NO 'My.GetStatus' NEEDED ***
// We will now use the built-in "Wifi.GetStatus" RPC call,
// which is provided by the 'rpc-service-wifi' library.
// Our 'fs/index.html' file will call this directly.


// --- 2. Event Handlers ---
// We keep these for logging, but they are no longer critical
// as 'Wifi.GetStatus' handles this logic internally.

Event.addHandler(Net.STATUS_GOT_IP, function(ev, evdata, ud) {
  print('*** Net Event: GOT_IP. (Handled by Wifi.GetStatus). ***');
}, null);

Event.addHandler(Net.STATUS_DISCONNECTED, function(ev, evdata, ud) {
  print('*** Net Event: DISCONNECTED from STA Network. ***');
}, null);


// --- 3. Timer Logic (AP+STA version) ---
// This logic remains the same, to handle the first-boot AP setup.
Timer.set(200, false, function() {
  
  print('--- Initial State Check Running (200ms delay) ---');

  let sta_ssid = Cfg.get('wifi.sta.ssid');
  let ap_is_enabled = Cfg.get('wifi.ap.enable');
  
  print('Current Wi-Fi SSID from Cfg: ' + (sta_ssid ? sta_ssid : 'undefined')); 

  if (!sta_ssid && !ap_is_enabled) {
    // --- First Boot (Neither STA nor AP is on) ---
    print('First Boot: No STA SSID and AP is off. Enabling AP...');
    
    let apConfig = {
      ssid: Cfg.get('wifi.ap.ssid'),
      pass: Cfg.get('wifi.ap.pass'),
      ip: Cfg.get('wifi.ap.ip'),
      netmask: '255.255.255.0',
      gw: Cfg.get('wifi.ap.ip'),
      enable: true
    };
    
    // Set AP config, ensure we serve index.html, and reboot
    Cfg.set({wifi: {ap: apConfig}}, true);
    Cfg.set({http: {default_file: 'index.html'}}, true);
    print('AP config saved. Device will reboot into AP mode.');
    Sys.reboot(100);
    
  } else if (!sta_ssid && ap_is_enabled) {
    // --- AP Mode (Setup Portal is Active) ---
    print('Timer: AP mode. Waiting for user setup on index.html.');
    print('Connect to SSID: ' + Cfg.get('wifi.ap.ssid') + ' at http://' + Cfg.get('wifi.ap.ip'));
    
  } else if (sta_ssid) {
    // --- AP+STA Mode (Configured) ---
    print('Timer: AP+STA mode detected (SSID: ' + sta_ssid + ').');
    print('AP is running. STA is attempting to connect...');
  }

}, null);

print('--- init.js script finished loading. Handlers are set. ---');