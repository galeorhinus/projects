#include "mgos.h"
#include "mongoose.h"              // v6 API: MG_EV_HTTP_REQUEST, struct http_message
#include "mgos_http_server.h"      // mgos_register_http_endpoint
#include "mgos_config.h"           // mgos_sys_config_*
#include "mgos_system.h"           // mgos_system_restart

static void reboot_cb(void *arg) {
  (void) arg;
  mgos_system_restart();           // noreturn
}

static bool write_file(const char *path, const char *data) {
  FILE *fp = fopen(path, "w");
  if (fp == NULL) return false;
  bool ok = (fputs(data ? data : "", fp) >= 0);
  fclose(fp);
  return ok;
}

static bool file_exists(const char *path) {
  FILE *fp = fopen(path, "r");
  if (fp == NULL) return false;
  fclose(fp);
  return true;
}

// POST /api/setup  body: {"ssid":"...", "pass":"..."}
static void setup_handler(struct mg_connection *nc, int ev, void *ev_data, void *user_data) {
  (void) user_data;
  if (ev != MG_EV_HTTP_REQUEST) return;

  struct http_message *hm = (struct http_message *) ev_data;
  char *ssid = NULL, *pass = NULL;

  int parsed = json_scanf(hm->body.p, hm->body.len, "{ssid:%Q, pass:%Q}", &ssid, &pass);
  if (parsed < 1 || ssid == NULL || *ssid == '\0') {
    mg_http_send_error(nc, 400, "Missing ssid/pass");
    free(ssid); free(pass);
    return;
  }

  // Apply runtime config
  mgos_sys_config_set_wifi_sta_enable(true);
  mgos_sys_config_set_wifi_sta_ssid(ssid);
  mgos_sys_config_set_wifi_sta_pass(pass ? pass : "");
  mgos_sys_config_set_wifi_ap_enable(false);

  // Persist (conf9.json)
  bool saved = mgos_sys_config_save(&mgos_sys_config, false /* try_once */, NULL);

  // If saved, drop the provisioning marker
  bool marked = false;
  if (saved) marked = write_file("/provisioned", "1\n");

  const char *msg = (saved && marked) ? "Saved. Rebooting..." :
                    (!saved ? "Config save failed" : "Marker write failed");
  int code = (saved && marked) ? 200 : 500;

  mg_printf(nc,
            "HTTP/1.1 %d %s\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: %d\r\n"
            "Connection: close\r\n\r\n%s",
            code, (code == 200 ? "OK" : "Internal Server Error"),
            (int) strlen(msg), msg);

  free(ssid);
  free(pass);

  if (code == 200) {
    // Reboot shortly so the page can show the response
    mgos_set_timer(1500, 0 /* oneshot */, reboot_cb, NULL);
  }
}

// GET /provisioned  -> 200 if file exists, else 404
static void provisioned_handler(struct mg_connection *nc, int ev, void *ev_data, void *user_data) {
  (void) user_data;
  if (ev != MG_EV_HTTP_REQUEST) return;

  if (file_exists("/provisioned")) {
    const char *body = "1\n";
    mg_printf(nc,
              "HTTP/1.1 200 OK\r\n"
              "Content-Type: text/plain\r\n"
              "Content-Length: %d\r\n"
              "Cache-Control: no-store\r\n"
              "Connection: close\r\n\r\n%s",
              (int) strlen(body), body);
  } else {
    mg_http_send_error(nc, 404, "Not Provisioned");
  }
}

enum mgos_app_init_result mgos_app_init(void) {
  // IMPORTANT: do NOT create /provisioned here.
  mgos_register_http_endpoint("/api/setup", setup_handler, NULL);
  mgos_register_http_endpoint("/provisioned", provisioned_handler, NULL);
  return MGOS_APP_INIT_SUCCESS;
}
