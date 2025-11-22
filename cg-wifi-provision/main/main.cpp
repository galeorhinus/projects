// main.cpp

#include <string>
#include <cstring>

extern "C" {
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"

#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_mac.h"

#include "lwip/inet.h"
#include "lwip/sockets.h"

#include "esp_http_server.h"
#include "mdns.h"

#include "cJSON.h"
}

static const char *TAG = "HomeYantric";

// Wi-Fi event bits
static EventGroupHandle_t wifi_event_group;
static const int WIFI_CONNECTED_BIT = BIT0;

struct AppState {
    bool provisioning_done = false;
    bool wifi_connected = false;
    std::string sta_ip_str;
    std::string mdns_host_str;
    std::string ap_ip_str = "192.168.4.1";
    bool wifi_error = false;
    std::string wifi_error_reason;
    int wifi_retry_count = 0;
    const int WIFI_MAX_RETRY = 5;
};
static AppState app_state;


// Forward declarations
static void start_softap();
static void start_dns_captive_portal();
static void start_http_server();
static void start_sta_connect(const char *ssid, const char *password);
static void init_mdns_hostname();

// HTTP handler forward declarations
static esp_err_t root_get_handler(httpd_req_t *req);
static esp_err_t scan_get_handler(httpd_req_t *req);
static esp_err_t wifi_post_handler(httpd_req_t *req);
static esp_err_t status_get_handler(httpd_req_t *req);
static esp_err_t app_get_handler(httpd_req_t *req);
static esp_err_t captive_catchall_handler(httpd_req_t *req);
static esp_err_t reset_wifi_handler(httpd_req_t *req);
static esp_err_t close_ap_handler(httpd_req_t *req);   // NEW

static httpd_handle_t start_webserver();

// -------------------- HTML (with logo) --------------------


static const char *HOMEYANTRIC_APP_HTML = R"HTML(
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>HomeYantric • Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      margin:0;
      background:#0b1220;
      color:#e6eefb;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    }
    .wrap {
      max-width:640px;
      margin: 40px auto;
      padding: 24px;
      background:#141d2f;
      border-radius:20px;
      box-shadow:0 10px 30px rgba(0,0,0,.4);
    }
    h1 {
      margin-top:0;
      font-size:28px;
      background:linear-gradient(135deg,#38bdf8,#a855f7);
      -webkit-background-clip:text;
      -webkit-text-fill-color:transparent;
    }
    p { color:#9ca3af; }
    .logo {
      width:48px;
      height:48px;
      margin-bottom:16px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <!-- Logo -->
    <svg class="logo" viewBox="0 0 40 40">
        <defs>
          <linearGradient id="hyGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8"/>
            <stop offset="100%" stop-color="#a855f7"/>
          </linearGradient>
        </defs>
        <rect x="4" y="4" width="32" height="32" rx="10" ry="10" fill="url(#hyGrad2)"/>
        <path d="M13 26V14h3v4h8v-4h3v12h-3v-5h-8v5z" fill="#0b1120"/>
    </svg>

    <h1>Welcome to HomeYantric</h1>

    <p>Your device is connected to Wi-Fi and fully provisioned.</p>

    <p>This is where your app UI will go — controls, status, device info, sliders, buttons, etc.</p>

    <p>To add features here, just let me know what you want the dashboard to do.</p>
  </div>
</body>
</html>
)HTML";

static const char *HOMEYANTRIC_HTML = R"HTML(
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>HomeYantric • Wi-Fi Setup</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    body {
      margin:0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:#050816;
      color:#e5e7eb;
    }
    .wrap {
      max-width: 420px;
      margin: 6vh auto;
      padding: 24px 20px 32px;
      background:#020617;
      border-radius:18px;
      box-shadow:0 18px 40px rgba(0,0,0,.6);
    }
    .logo-row {
      display:flex;
      align-items:center;
      gap:12px;
      margin-bottom:20px;
    }
    .logo-text-main {
      font-weight:700;
      font-size:1.25rem;
      letter-spacing:0.04em;
    }
    .logo-text-sub {
      font-size:0.75rem;
      color:#9ca3af;
      text-transform:uppercase;
      letter-spacing:0.18em;
    }
    .card-title {
      font-size:1.1rem;
      margin-bottom:6px;
      font-weight:600;
    }
    .card-sub {
      font-size:0.85rem;
      color:#9ca3af;
      margin-bottom:16px;
    }
    button, select, input {
      font:inherit;
    }
    .btn {
      border:none;
      padding:10px 14px;
      border-radius:999px;
      cursor:pointer;
      background:linear-gradient(135deg, #38bdf8, #a855f7);
      color:white;
      font-weight:600;
      font-size:0.9rem;
      display:inline-flex;
      align-items:center;
      gap:6px;
    }
    .btn:disabled {
      opacity:.5;
      cursor:default;
    }
    .field {
      margin-bottom:14px;
    }
    label {
      display:block;
      font-size:0.8rem;
      margin-bottom:4px;
      color:#9ca3af;
    }
    input[type=text], input[type=password], select {
      width:100%;
      padding:8px 10px;
      border-radius:10px;
      border:1px solid #1f2937;
      background:#020617;
      color:#e5e7eb;
      box-sizing:border-box;
    }
    .status {
      margin-top:14px;
      font-size:0.8rem;
      color:#9ca3af;
    }
    .links {
      margin-top:12px;
      font-size:0.86rem;
    }
    .links a {
      color:#38bdf8;
      word-break:break-all;
    }
    .badge {
      display:inline-block;
      padding:2px 8px;
      border-radius:999px;
      background:rgba(56,189,248,.12);
      color:#7dd3fc;
      font-size:0.7rem;
      margin-bottom:10px;
      text-transform:uppercase;
      letter-spacing:0.15em;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="logo-row">
      <!-- HomeYantric Logo (inline SVG) -->
      <svg width="40" height="40" viewBox="0 0 40 40" aria-hidden="true">
        <defs>
          <linearGradient id="hyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#38bdf8"/>
            <stop offset="100%" stop-color="#a855f7"/>
          </linearGradient>
        </defs>
        <rect x="4" y="4" width="32" height="32" rx="10" ry="10" fill="url(#hyGrad)"/>
        <path d="M13 26V14h3v4h8v-4h3v12h-3v-5h-8v5z" fill="#0b1120"/>
      </svg>
      <div>
        <div class="logo-text-main">HomeYantric</div>
        <div class="logo-text-sub">Wi-Fi Setup</div>
      </div>
    </div>

    <div class="badge">Step 1 • Connect</div>
    <div class="card-title">Connect to your home Wi-Fi</div>
    <div class="card-sub">
      This device is broadcasting <strong>HomeYantric-Setup</strong>. You’re connected to it now.
      Choose your home network and enter its password.
    </div>

    <div class="field">
      <label for="ssidSelect">Available networks</label>
      <select id="ssidSelect">
        <option value="">Scan networks…</option>
      </select>
    </div>

    <div class="field">
      <label for="ssidManual">Or enter network name</label>
      <input id="ssidManual" type="text" placeholder="Hidden SSID or custom name" />
    </div>

    <div class="field">
      <label for="password">Wi-Fi password</label>
      <input id="password" type="password" autocomplete="current-password" />
      <label style="display:flex;align-items:center;gap:6px;margin-top:6px;font-size:0.8rem;color:#9ca3af;">
        <input id="showPass" type="checkbox" style="width:auto;margin:0;">
        <span>Show password</span>
      </label>
    </div>

    <button class="btn" id="connectBtn">
      <span id="btnLabel">Connect to Wi-Fi</span>
    </button>

    <div class="status" id="statusText">Not connected yet.</div>
    <div class="links" id="linksBox" style="display:none;">
      <div>Once your phone rejoins your normal Wi-Fi, use one of these:</div>
      <div>mDNS: <a id="mdnsLink" href="#" target="_blank"></a></div>
      <div>IP: <a id="ipLink" href="#" target="_blank"></a></div>
    </div>

    <!-- NEW: Disconnect AP button + status -->
    <button class="btn" id="closeApBtn"
            style="margin-top:10px;display:none;background:#111827;border:1px solid #4b5563;">
      Disconnect Setup Wi-Fi
    </button>
    <div class="status" id="closeApStatus"></div>

    <hr style="margin:20px 0;border:none;border-top:1px solid #111827;">

    <div style="font-size:0.8rem;color:#9ca3af;margin-bottom:8px;">
      Having trouble or want to start over?
    </div>
    <button class="btn" id="resetWifiBtn" style="background:#111827;border:1px solid #374151;">
      Reset Wi-Fi & Restart
    </button>
    <div class="status" id="resetStatus"></div>

  </div>

<script>
  const ssidSelect = document.getElementById('ssidSelect');
  const ssidManual = document.getElementById('ssidManual');
  const passwordEl = document.getElementById('password');
  const connectBtn = document.getElementById('connectBtn');
  const btnLabel = document.getElementById('btnLabel');
  const statusText = document.getElementById('statusText');
  const linksBox = document.getElementById('linksBox');
  const mdnsLink = document.getElementById('mdnsLink');
  const ipLink = document.getElementById('ipLink');
  const resetWifiBtn = document.getElementById('resetWifiBtn');
  const resetStatus  = document.getElementById('resetStatus');
  const showPass = document.getElementById('showPass');

  const closeApBtn    = document.getElementById('closeApBtn');    // NEW
  const closeApStatus = document.getElementById('closeApStatus'); // NEW

  if (showPass) {
    showPass.addEventListener('change', (e) => {
      passwordEl.type = e.target.checked ? 'text' : 'password';
    });
  }

  if (resetWifiBtn) {
    resetWifiBtn.addEventListener('click', () => {
      if (!confirm('Reset Wi-Fi settings and restart the device?')) return;

      resetWifiBtn.disabled = true;
      resetStatus.textContent = 'Resetting Wi-Fi and restarting…';

      fetch('/reset_wifi', { method: 'POST' })
        .then(r => r.json())
        .then(j => {
          resetStatus.textContent = 'Device is restarting. Reconnect to "HomeYantric-Setup" in about 10–15 seconds.';
        })
        .catch(e => {
          resetStatus.textContent = 'Failed to send reset command: ' + e;
          resetWifiBtn.disabled = false;
        });
    });
  }

  // NEW: close AP button logic
  if (closeApBtn) {
    closeApBtn.addEventListener('click', () => {
      if (!confirm('Disconnect the HomeYantric-Setup Wi-Fi now? Your phone will likely switch back to your home network.')) {
        return;
      }

      closeApBtn.disabled = true;
      closeApStatus.textContent =
        'Closing setup Wi-Fi… your phone may disconnect from this network in a few seconds.';

      fetch('/close_ap', { method: 'POST' })
        .then(r => r.json())
        .then(j => {
          closeApStatus.textContent =
            'Setup Wi-Fi is closing. Reconnect your phone to your home Wi-Fi and use the links above.';
        })
        .catch(e => {
          closeApStatus.textContent = 'Failed to request AP close: ' + e;
          closeApBtn.disabled = false;
        });
    });
  }

  function scanNetworks() {
    fetch('/scan')
      .then(r => r.json())
      .then(list => {
        ssidSelect.innerHTML = '<option value="">Choose a network…</option>';
        list.forEach(item => {
          const opt = document.createElement('option');
          opt.value = item.ssid;
          opt.textContent = item.ssid + ' (' + item.rssi + ' dBm)';
          ssidSelect.appendChild(opt);
        });
      })
      .catch(e => {
        statusText.textContent = 'Scan failed: ' + e;
      });
  }

  ssidSelect.addEventListener('focus', () => {
    if (ssidSelect.options.length <= 1) scanNetworks();
  });

  connectBtn.addEventListener('click', () => {
    const chosen = ssidSelect.value.trim();
    const manual = ssidManual.value.trim();
    const ssid = manual || chosen;
    const password = passwordEl.value;

    if (!ssid) {
      statusText.textContent = 'Please choose or enter a network name.';
      return;
    }

    statusText.textContent = 'Sending Wi-Fi credentials…';
    connectBtn.disabled = true;
    btnLabel.textContent = 'Connecting…';

    fetch('/wifi', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ssid, password})
    }).then(r => r.json())
      .then(j => {
        statusText.textContent = 'Connecting to "' + ssid + '"…';
        pollStatus();
      })
      .catch(e => {
        statusText.textContent = 'Error sending credentials: ' + e;
        connectBtn.disabled = false;
        btnLabel.textContent = 'Connect to Wi-Fi';
      });
  });

  function pollStatus() {
    fetch('/status')
      .then(r => r.json())
      .then(j => {
        if (j.state === 'connected') {
          statusText.textContent = 'Connected! You can now reconnect your phone to your normal Wi-Fi.';
          linksBox.style.display = '';
          if (j.mdns) {
            mdnsLink.textContent = 'http://' + j.mdns + '.local';
            mdnsLink.href = 'http://' + j.mdns + '.local';
          }
          if (j.ip) {
            ipLink.textContent = 'http://' + j.ip;
            ipLink.href = 'http://' + j.ip;
          }
          connectBtn.disabled = true;
          btnLabel.textContent = 'Connected';

          // NEW: show AP disconnect button once connected
          if (closeApBtn) {
            closeApBtn.style.display = '';
            closeApStatus.textContent =
              'Optionally disconnect "HomeYantric-Setup" so your phone switches back to your home Wi-Fi.';
          }
        } else if (j.state === 'error') {
          statusText.textContent = 'Failed to connect: ' + (j.reason || 'unknown error');
          connectBtn.disabled = false;
          btnLabel.textContent = 'Connect to Wi-Fi';
        } else {
          setTimeout(pollStatus, 1500);
        }
      })
      .catch(() => setTimeout(pollStatus, 2000));
  }
</script>
</body>
</html>
)HTML";

// -------------------- Wi-Fi + Events --------------------

extern "C" void wifi_event_handler(void *arg,
                                   esp_event_base_t event_base,
                                   int32_t event_id,
                                   void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        ESP_LOGI(TAG, "STA start -> connecting…");
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        auto* disc = (wifi_event_sta_disconnected_t*)event_data;
        app_state.wifi_connected = false;
        xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);

        app_state.wifi_retry_count++;
        ESP_LOGW(TAG, "STA disconnected, reason=%d, retry=%d", disc->reason, app_state.wifi_retry_count);

        // Optionally generate a human-readable reason
        app_state.wifi_error_reason.clear();
        switch (disc->reason) {
            case WIFI_REASON_AUTH_FAIL:
            case WIFI_REASON_HANDSHAKE_TIMEOUT:
                app_state.wifi_error_reason = "Authentication failed (check password)";
                break;
            case WIFI_REASON_NO_AP_FOUND:
                app_state.wifi_error_reason = "Network not found";
                break;
            default:
                app_state.wifi_error_reason = "Wi-Fi disconnected (reason " + std::to_string(disc->reason) + ")";
                break;
        }

        if (app_state.wifi_retry_count < app_state.WIFI_MAX_RETRY) {
            app_state.wifi_error = false;
            ESP_LOGI(TAG, "Retrying Wi-Fi…");
            esp_wifi_connect();
        } else {
            app_state.wifi_error = true;
            ESP_LOGW(TAG, "Too many Wi-Fi failures, staying in provisioning mode");
            // NOTE: we keep AP + DNS running, so the user can try again via the portal.
        }
    }
    else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        auto* event = (ip_event_got_ip_t*)event_data;
        char ip[16];
        inet_ntoa_r(event->ip_info.ip.addr, ip, sizeof(ip));
        app_state.sta_ip_str = ip;

        ESP_LOGI(TAG, "Got IP: %s", ip);
        app_state.wifi_connected = true;
        app_state.wifi_error = false;
        app_state.wifi_error_reason.clear();
        app_state.wifi_retry_count = 0;

        app_state.provisioning_done = true;
        xEventGroupSetBits(wifi_event_group, WIFI_CONNECTED_BIT);

        init_mdns_hostname();
    }
}

// SoftAP "HomeYantric-Setup"
static void start_softap()
{
    esp_netif_t *ap_netif = esp_netif_create_default_wifi_ap();

    // optionally read actual IP of AP netif
    esp_netif_ip_info_t ip_info;
    if (esp_netif_get_ip_info(ap_netif, &ip_info) == ESP_OK) {
        char ip[16];
        inet_ntoa_r(ip_info.ip.addr, ip, sizeof(ip));
        app_state.ap_ip_str = ip;
    }

    wifi_config_t wifi_ap_config = {};
    strcpy((char *)wifi_ap_config.ap.ssid, "HomeYantric-Setup");
    wifi_ap_config.ap.ssid_len = strlen("HomeYantric-Setup");
    wifi_ap_config.ap.max_connection = 4;
    wifi_ap_config.ap.authmode = WIFI_AUTH_OPEN;  // or WPA2 with password

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_APSTA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_AP, &wifi_ap_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "SoftAP started, SSID: HomeYantric-Setup, IP: %s", app_state.ap_ip_str.c_str());
}

// mDNS hostname homeyantric-XXXX.local
static void init_mdns_hostname()
{
    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);

    char host[32];
    snprintf(host, sizeof(host), "homeyantric-%02x%02x", mac[4], mac[5]);
    app_state.mdns_host_str = host;

    mdns_init();
    mdns_hostname_set(host);
    mdns_instance_name_set("HomeYantric Device");

    mdns_txt_item_t serviceTxtData[] = {
        {"board", "esp32-wrover"},
        {"app", "homeyantric"}
    };
    mdns_service_add("HomeYantric Web", "_http", "_tcp", 80, serviceTxtData, 2);

    ESP_LOGI(TAG, "mDNS hostname set to: %s.local", host);
}

// Connect STA with provided credentials
static void start_sta_connect(const char *ssid, const char *password)
{
    wifi_config_t wifi_sta_config = {};
    strncpy((char *)wifi_sta_config.sta.ssid, ssid, sizeof(wifi_sta_config.sta.ssid));
    strncpy((char *)wifi_sta_config.sta.password, password, sizeof(wifi_sta_config.sta.password));

    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_sta_config)); 

    app_state.wifi_connected = false;
    app_state.wifi_error = false;
    app_state.wifi_error_reason.clear();
    app_state.wifi_retry_count = 0;

    xEventGroupClearBits(wifi_event_group, WIFI_CONNECTED_BIT);

    ESP_LOGI(TAG, "Starting STA connect to SSID='%s'", ssid);
    ESP_ERROR_CHECK(esp_wifi_connect());
}

// -------------------- Captive Portal DNS --------------------

static void dns_server_task(void *pvParameters)
{
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
    if (sock < 0) {
        ESP_LOGE(TAG, "DNS socket failed");
        vTaskDelete(NULL);
        return;
    }

    struct sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(53);

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        ESP_LOGE(TAG, "DNS bind failed");
        close(sock);
        vTaskDelete(NULL);
        return;
    }

    ESP_LOGI(TAG, "DNS captive portal server started");

    uint8_t rx_buf[512];

    while (true) {
        struct sockaddr_in source_addr{};
        socklen_t socklen = sizeof(source_addr);
        int len = recvfrom(sock, rx_buf, sizeof(rx_buf), 0,
                           (struct sockaddr *)&source_addr, &socklen);
        if (len <= 0) continue;

        uint8_t tx_buf[512];
        if (len > (int)sizeof(tx_buf)) len = sizeof(tx_buf);

        memcpy(tx_buf, rx_buf, len);

        // Response flags
        tx_buf[2] |= 0x80;   // QR = 1 (response)
        tx_buf[3] |= 0x80;   // RA = 1
        tx_buf[7] = 1;       // ANCOUNT = 1 (low byte)

        int pos = 12;
        while (pos < len && tx_buf[pos] != 0) {
            pos += tx_buf[pos] + 1;
        }
        pos += 5; // null + QTYPE + QCLASS

        if (pos + 16 > (int)sizeof(tx_buf)) continue;

        // Answer: pointer to name
        tx_buf[pos++] = 0xC0;
        tx_buf[pos++] = 0x0C;
        // TYPE A
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x01;
        // CLASS IN
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x01;
        // TTL
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x3C; // 60s
        // RDLENGTH = 4
        tx_buf[pos++] = 0x00;
        tx_buf[pos++] = 0x04;

        // AP IP
        uint8_t ip[4] = {192, 168, 4, 1};
        // If you want dynamic from ap_ip_str, parse it here.
        memcpy(&tx_buf[pos], ip, 4);
        pos += 4;

        sendto(sock, tx_buf, pos, 0, (struct sockaddr *)&source_addr, socklen);
    }

    close(sock);
    vTaskDelete(NULL);
}

static void start_dns_captive_portal()
{
    xTaskCreate(&dns_server_task, "dns_server_task", 4096, NULL, 5, NULL);
}

// -------------------- HTTP Server + Handlers --------------------


static esp_err_t root_get_handler(httpd_req_t *req)
{
    if (app_state.provisioning_done) {
        httpd_resp_set_type(req, "text/html");
        return httpd_resp_send(req, HOMEYANTRIC_APP_HTML, HTTPD_RESP_USE_STRLEN);
    } else {
        httpd_resp_set_type(req, "text/html");
        return httpd_resp_send(req, HOMEYANTRIC_HTML, HTTPD_RESP_USE_STRLEN);
    }
}


static esp_err_t scan_get_handler(httpd_req_t *req)
{
    wifi_scan_config_t scan_config = {};
    scan_config.show_hidden = true;
    esp_wifi_scan_start(&scan_config, true);

    uint16_t ap_num = 0;
    esp_wifi_scan_get_ap_num(&ap_num);

    wifi_ap_record_t *ap_records =
        (wifi_ap_record_t *)malloc(sizeof(wifi_ap_record_t) * ap_num);
    esp_wifi_scan_get_ap_records(&ap_num, ap_records);

    std::string json = "[";
    for (int i = 0; i < ap_num; ++i) {
        char ssid[33] = {0};
        memcpy(ssid, ap_records[i].ssid, 32);
        char entry[160];
        snprintf(entry, sizeof(entry),
                 "%s{\"ssid\":\"%s\",\"rssi\":%d}",
                 (i == 0 ? "" : ","),
                 ssid,
                 ap_records[i].rssi);
        json += entry;
    }
    json += "]";

    free(ap_records);

    httpd_resp_set_type(req, "application/json");
    return httpd_resp_sendstr(req, json.c_str());
}

static esp_err_t reset_wifi_handler(httpd_req_t *req)
{
    ESP_LOGW(TAG, "Received reset Wi-Fi request");

    esp_err_t err = esp_wifi_stop();
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "esp_wifi_stop failed: %s", esp_err_to_name(err));
    }

    err = esp_wifi_restore();
    if (err != ESP_OK) {
        ESP_LOGW(TAG, "esp_wifi_restore failed: %s", esp_err_to_name(err));
    }

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(root);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);

    vTaskDelay(pdMS_TO_TICKS(200));

    ESP_LOGW(TAG, "Restarting after Wi-Fi reset");
    esp_restart();

    return ESP_OK;
}

// NEW: close_ap_handler
static esp_err_t close_ap_handler(httpd_req_t *req)
{
    ESP_LOGI(TAG, "Received request to close AP (HomeYantric-Setup)");

    wifi_mode_t mode;
    esp_err_t err = esp_wifi_get_mode(&mode);
    if (err == ESP_OK && (mode == WIFI_MODE_APSTA || mode == WIFI_MODE_AP)) {
        err = esp_wifi_set_mode(WIFI_MODE_STA);
        if (err != ESP_OK) {
            ESP_LOGW(TAG, "esp_wifi_set_mode(STA) failed: %s", esp_err_to_name(err));
        } else {
            ESP_LOGI(TAG, "AP mode disabled, STA only now");
        }
    } else {
        ESP_LOGI(TAG, "AP is already disabled or mode=%d", (int)mode);
    }

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(root);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);

    return ESP_OK;
}

static esp_err_t wifi_post_handler(httpd_req_t *req)
{
    char buf[256];
    int len = httpd_req_recv(req, buf, sizeof(buf) - 1);
    if (len <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "No body");
        return ESP_FAIL;
    }
    buf[len] = 0;

    cJSON *root = cJSON_Parse(buf);
    if (!root) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Invalid JSON");
        return ESP_FAIL;
    }

    const cJSON *ssid = cJSON_GetObjectItem(root, "ssid");
    const cJSON *password = cJSON_GetObjectItem(root, "password");
    if (!cJSON_IsString(ssid) || !ssid->valuestring) {
        cJSON_Delete(root);
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Missing ssid");
        return ESP_FAIL;
    }

    const char *ssid_str = ssid->valuestring;
    const char *pass_str = (cJSON_IsString(password) && password->valuestring)
                           ? password->valuestring : "";

    ESP_LOGI(TAG, "Received Wi-Fi credentials: ssid='%s'", ssid_str);

    start_sta_connect(ssid_str, pass_str);

    cJSON *resp = cJSON_CreateObject();
    cJSON_AddStringToObject(resp, "status", "ok");
    char *resp_str = cJSON_PrintUnformatted(resp);

    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(resp);
    cJSON_Delete(root);

    return ESP_OK;
}

static esp_err_t status_get_handler(httpd_req_t *req)
{
    cJSON *root = cJSON_CreateObject();

    if (app_state.wifi_connected) {
        cJSON_AddStringToObject(root, "state", "connected");
        cJSON_AddStringToObject(root, "ip", app_state.sta_ip_str.c_str());
        cJSON_AddStringToObject(root, "mdns", app_state.mdns_host_str.c_str());
    } else if (app_state.wifi_error) {
        cJSON_AddStringToObject(root, "state", "error");
        if (!app_state.wifi_error_reason.empty()) {
            cJSON_AddStringToObject(root, "reason", app_state.wifi_error_reason.c_str());
        }
    } else {
        cJSON_AddStringToObject(root, "state", "connecting");
    }

    char *resp_str = cJSON_PrintUnformatted(root);
    httpd_resp_set_type(req, "application/json");
    httpd_resp_sendstr(req, resp_str);

    cJSON_free(resp_str);
    cJSON_Delete(root);
    return ESP_OK;
}

static esp_err_t captive_catchall_handler(httpd_req_t *req)
{
    return root_get_handler(req);
}

static httpd_handle_t start_webserver()
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.server_port = 80;
    config.max_uri_handlers = 16;
    config.uri_match_fn = httpd_uri_match_wildcard;  // allow "/*" matching

    httpd_handle_t server = nullptr;

    if (httpd_start(&server, &config) == ESP_OK)
    {
        // ---------- Primary Provisioning Endpoints ----------
        static httpd_uri_t root_uri = {
            .uri       = "/",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t scan_uri = {
            .uri       = "/scan",
            .method    = HTTP_GET,
            .handler   = scan_get_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t wifi_uri = {
            .uri       = "/wifi",
            .method    = HTTP_POST,
            .handler   = wifi_post_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t status_uri = {
            .uri       = "/status",
            .method    = HTTP_GET,
            .handler   = status_get_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t reset_wifi_uri = {
            .uri       = "/reset_wifi",
            .method    = HTTP_POST,
            .handler   = reset_wifi_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t close_ap_uri = {      // NEW
            .uri       = "/close_ap",
            .method    = HTTP_POST,
            .handler   = close_ap_handler,
            .user_ctx  = NULL
        };

        static httpd_uri_t app_uri = {
            .uri       = "/app",
            .method    = HTTP_GET,
            .handler   = app_get_handler,
            .user_ctx  = NULL
        };

        httpd_register_uri_handler(server, &app_uri);
        httpd_register_uri_handler(server, &root_uri);
        httpd_register_uri_handler(server, &scan_uri);
        httpd_register_uri_handler(server, &wifi_uri);
        httpd_register_uri_handler(server, &status_uri);
        httpd_register_uri_handler(server, &reset_wifi_uri);
        httpd_register_uri_handler(server, &close_ap_uri);

        // ---------- Captive Portal Detection URLs ----------
        static httpd_uri_t apple_captive_uri = {
            .uri       = "/hotspot-detect.html",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &apple_captive_uri);

        static httpd_uri_t android_generate_204 = {
            .uri       = "/generate_204",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &android_generate_204);

        static httpd_uri_t android_gen_204 = {
            .uri       = "/gen_204",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &android_gen_204);

        static httpd_uri_t windows_ncsi = {
            .uri       = "/ncsi.txt",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &windows_ncsi);

        static httpd_uri_t windows_connecttest = {
            .uri       = "/connecttest.txt",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &windows_connecttest);

        static httpd_uri_t firefox_canonical = {
            .uri       = "/canonical.html",
            .method    = HTTP_GET,
            .handler   = root_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &firefox_canonical);

        // ---------- Fallback Catch-All ----------
        static httpd_uri_t catchall_uri = {
            .uri       = "/*",
            .method    = HTTP_GET,
            .handler   = captive_catchall_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &catchall_uri);
    }

    return server;
}

static void start_http_server()
{
    start_webserver();
}

// -------------------- app_main --------------------

extern "C" void app_main(void)
{
    // NVS (for Wi-Fi and future credentials)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ESP_ERROR_CHECK(nvs_flash_init());
    }

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifi_event_group = xEventGroupCreate();

    esp_netif_create_default_wifi_sta();  // STA netif
    // AP netif created in start_softap()

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID,
        &wifi_event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP,
        &wifi_event_handler, NULL, NULL));

    start_softap();
    start_http_server();
    start_dns_captive_portal();

    ESP_LOGI(TAG, "HomeYantric provisioning started (ESP32-WROVER)");
}

static esp_err_t app_get_handler(httpd_req_t *req)
{
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, HOMEYANTRIC_APP_HTML, HTTPD_RESP_USE_STRLEN);
}
