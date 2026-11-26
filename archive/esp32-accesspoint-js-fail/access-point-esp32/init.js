// Load all C-level APIs
load('api_timer.js');
load('api_wifi.js');
load('api_config.js');
load('api_rpc.js');
load('api_sys.js');
load('api_http.js');

print('--- init.js script loaded! ---');

// --- 1. Define the RPC Handler ---
RPC.addHandler('My.SaveWifi', function(args) {
  print('Received Wi-Fi credentials:', JSON.stringify(args));
  Cfg.set({wifi: { sta: { enable: true, ssid: args.ssid, pass: args.pass }}}, true);
  Cfg.set({wifi: {ap: {enable: false}}}, true);
  print('New credentials saved. Rebooting in 3 seconds...');
  Sys.reboot(3000);
  return { status: 'ok', message: 'Credentials saved. Device is rebooting.' };
});

// --- 2. Set the 1-second timer for boot logic ---
Timer.set(1000, false /* do not repeat */, function() {
  print('--- 1-second timer elapsed, running main logic ---');

  let ip = Cfg.get('wifi.sta.ip');
  print('Current Wi-Fi IP:', ip); 

  if (ip) {
    // --- WE ARE CONNECTED ---
    print('Wi-Fi is connected. Serving main application.');
    // *** THE FIX ***
    // Change the server's root AND default file
    Cfg.set({http: {
      document_root: '/fs_app',
      default_file: 'app.html'
    }}, true /* save */); // Save this new config
    
  } else {
    // --- NOT CONNECTED ---
    print('Wi-Fi not connected. Starting setup portal in AP mode.');
    // *** THE FIX ***
    // Ensure the server is pointed at the setup files
    Cfg.set({http: {
      document_root: '/fs_setup',
      default_file: 'setup.html'
    }}, true /* save */); // Save this config

    let ap_is_enabled = Cfg.get('wifi.ap.enable');
    if (ap_is_enabled) {
      print('AP is already running. No changes made.');
      print('Connect to SSID: ' + Cfg.get('wifi.ap.ssid') + ' at http://' + Cfg.get('wifi.ap.ip'));
    } else {
      // This will only run on the very first boot
      print('AP is not running. Enabling AP and saving config...');
      let apSSID = Cfg.get('wifi.ap.ssid');
      let apPass = Cfg.get('wifi.ap.pass');
      let apIP = Cfg.get('wifi.ap.ip');

      let apConfig = {
        ssid: apSSID,
        pass: apPass,
        ip: apIP,
        netmask: '255.255.255.0',
        gw: apIP,
        enable: true
      };
      // This Cfg.set() will save and trigger ONE reboot, which is OK.
      Cfg.set({wifi: {ap: apConfig}}, true /* save */);
      print('AP config saved. Device will reboot into AP mode.');
    }
  }
}, null);

print('--- init.js script finished loading. Timer is set. ---');