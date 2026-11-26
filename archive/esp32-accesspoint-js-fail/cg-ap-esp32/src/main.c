#include "mgos.h"
#include "mongoose.h"              // MG_EV_HTTP_REQUEST, struct http_message
#include "mgos_http_server.h"      // mgos_register_http_endpoint
#include "mgos_config.h"           // mgos_sys_config_*
#include "mgos_system.h"           // mgos_system_restart

static void reboot_cb(void *arg) {
  (void) arg;
  mgos_system_restart();
}

// POST /api/setup  { "ssid":"...", "pass":"..." }
// - Keep AP enabled
// - Enable STA
// - Save + reboot (AP returns, device also joins STA)
static void setup_handler(struct mg_connection *nc, int ev, void *ev_data, void *user_data) {
  (void) user_data;
  if (ev != MG_EV_HTTP_REQUEST) return;

  struct http_message *hm = (struct http_message *) ev_data;
  char *ssid = NULL, *pass = NULL;

  if (json_scanf(hm->body.p, hm->body.len, "{ssid:%Q, pass:%Q}", &ssid, &pass) != 2 || ssid == NULL) {
    mg_http_send_error(nc, 400, "Missing ssid/pass");
    free(ssid); free(pass);
    return;
  }

  // Leave AP enabled for now
  mgos_sys_config_set_wifi_ap_enable(true);

  // Enable STA with provided creds
  mgos_sys_config_set_wifi_sta_enable(true);
  mgos_sys_config_set_wifi_sta_ssid(ssid);
  mgos_sys_config_set_wifi_sta_pass(pass ? pass : "");

  // Mark “provisioned” so index.html can decide what to show
  FILE *fp = fopen("/provisioned", "w");
  if (fp != NULL) { fputs("1\n", fp); fclose(fp); }

  bool saved = mgos_sys_config_save(&mgos_sys_config, false /* try_once */, NULL);

  const char *msg = saved ? "Saved. Rebooting with AP+STA..." : "Config save failed";
  mg_printf(nc,
            "HTTP/1.1 %s\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: %d\r\n"
            "Connection: close\r\n\r\n%s",
            saved ? "200 OK" : "500 Internal Server Error",
            (int) strlen(msg), msg);

  free(ssid);
  free(pass);

  if (saved) mgos_set_timer(800 /* ms */, 0 /* oneshot */, reboot_cb, NULL);
}

// POST /api/finalize  { "turnOffAp": true }
// - Turn AP off (optional), save, reboot (STA-only)
static void finalize_handler(struct mg_connection *nc, int ev, void *ev_data, void *user_data) {
  (void) user_data;
  if (ev != MG_EV_HTTP_REQUEST) return;
  struct http_message *hm = (struct http_message *) ev_data;

  bool turn_off_ap = false;
  json_scanf(hm->body.p, hm->body.len, "{turnOffAp:%B}", &turn_off_ap);

  if (turn_off_ap) mgos_sys_config_set_wifi_ap_enable(false);

  bool saved = mgos_sys_config_save(&mgos_sys_config, false, NULL);
  const char *msg = saved ? "Finalized. Rebooting..." : "Finalize save failed";
  mg_printf(nc,
            "HTTP/1.1 %s\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: %d\r\n"
            "Connection: close\r\n\r\n%s",
            saved ? "200 OK" : "500 Internal Server Error",
            (int) strlen(msg), msg);

  if (saved) mgos_set_timer(600, 0, reboot_cb, NULL);
}

enum mgos_app_init_result mgos_app_init(void) {
  mgos_register_http_endpoint("/api/setup", setup_handler, NULL);
  mgos_register_http_endpoint("/api/finalize", finalize_handler, NULL);
  return MGOS_APP_INIT_SUCCESS;
}
