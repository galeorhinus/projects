/* clang-format off */
/*
 * Generated file - do not edit.
 * Command: /mongoose-os/tools/mgos_gen_config.py --c_name=mgos_config --c_global_name=mgos_sys_config --dest_dir=/data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_612452169/build/gen/ /mongoose-os/src/mgos_debug_udp_config.yaml /data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_612452169/build/gen/mos_conf_schema.yml
 */

#pragma once

#include <stdbool.h>

#include "common/mg_str.h"

#include "mgos_config_util.h"

#ifdef __cplusplus
extern "C" {
#endif


/* debug type struct mgos_config_debug */
struct mgos_config_debug {
  const char * udp_log_addr;
  int udp_log_level;
  int mbedtls_level;
  int level;
  const char * file_level;
  int event_level;
  int stdout_uart;
  int stderr_uart;
  int factory_reset_gpio;
  const char * mg_mgr_hexdump_file;
};
const struct mgos_conf_entry *mgos_config_debug_get_schema(void);
void mgos_config_debug_set_defaults(struct mgos_config_debug *cfg);
static inline bool mgos_config_debug_parse(struct mg_str json, struct mgos_config_debug *cfg) {
  mgos_config_debug_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_debug_get_schema(), cfg);
}
bool mgos_config_debug_parse_f(const char *fname, struct mgos_config_debug *cfg);
static inline bool mgos_config_debug_emit(const struct mgos_config_debug *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_debug_get_schema(), pretty, out);
}
static inline bool mgos_config_debug_emit_f(const struct mgos_config_debug *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_debug_get_schema(), pretty, fname);
}
static inline bool mgos_config_debug_copy(const struct mgos_config_debug *src, struct mgos_config_debug *dst) {
  return mgos_conf_copy(mgos_config_debug_get_schema(), src, dst);
}
static inline void mgos_config_debug_free(struct mgos_config_debug *cfg) {
  return mgos_conf_free(mgos_config_debug_get_schema(), cfg);
}

/* device type struct mgos_config_device */
struct mgos_config_device {
  const char * id;
  const char * license;
  const char * mac;
  const char * public_key;
  const char * sn;
};
const struct mgos_conf_entry *mgos_config_device_get_schema(void);
void mgos_config_device_set_defaults(struct mgos_config_device *cfg);
static inline bool mgos_config_device_parse(struct mg_str json, struct mgos_config_device *cfg) {
  mgos_config_device_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_device_get_schema(), cfg);
}
bool mgos_config_device_parse_f(const char *fname, struct mgos_config_device *cfg);
static inline bool mgos_config_device_emit(const struct mgos_config_device *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_device_get_schema(), pretty, out);
}
static inline bool mgos_config_device_emit_f(const struct mgos_config_device *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_device_get_schema(), pretty, fname);
}
static inline bool mgos_config_device_copy(const struct mgos_config_device *src, struct mgos_config_device *dst) {
  return mgos_conf_copy(mgos_config_device_get_schema(), src, dst);
}
static inline void mgos_config_device_free(struct mgos_config_device *cfg) {
  return mgos_conf_free(mgos_config_device_get_schema(), cfg);
}

/* sys type struct mgos_config_sys */
struct mgos_config_sys {
  const char * tz_spec;
  int wdt_timeout;
  const char * pref_ota_lib;
};
const struct mgos_conf_entry *mgos_config_sys_get_schema(void);
void mgos_config_sys_set_defaults(struct mgos_config_sys *cfg);
static inline bool mgos_config_sys_parse(struct mg_str json, struct mgos_config_sys *cfg) {
  mgos_config_sys_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_sys_get_schema(), cfg);
}
bool mgos_config_sys_parse_f(const char *fname, struct mgos_config_sys *cfg);
static inline bool mgos_config_sys_emit(const struct mgos_config_sys *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_sys_get_schema(), pretty, out);
}
static inline bool mgos_config_sys_emit_f(const struct mgos_config_sys *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_sys_get_schema(), pretty, fname);
}
static inline bool mgos_config_sys_copy(const struct mgos_config_sys *src, struct mgos_config_sys *dst) {
  return mgos_conf_copy(mgos_config_sys_get_schema(), src, dst);
}
static inline void mgos_config_sys_free(struct mgos_config_sys *cfg) {
  return mgos_conf_free(mgos_config_sys_get_schema(), cfg);
}

/* dns_sd type struct mgos_config_dns_sd */
struct mgos_config_dns_sd {
  int enable;
  int adv_only;
  const char * host_name;
  const char * txt;
};
const struct mgos_conf_entry *mgos_config_dns_sd_get_schema(void);
void mgos_config_dns_sd_set_defaults(struct mgos_config_dns_sd *cfg);
static inline bool mgos_config_dns_sd_parse(struct mg_str json, struct mgos_config_dns_sd *cfg) {
  mgos_config_dns_sd_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_dns_sd_get_schema(), cfg);
}
bool mgos_config_dns_sd_parse_f(const char *fname, struct mgos_config_dns_sd *cfg);
static inline bool mgos_config_dns_sd_emit(const struct mgos_config_dns_sd *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_dns_sd_get_schema(), pretty, out);
}
static inline bool mgos_config_dns_sd_emit_f(const struct mgos_config_dns_sd *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_dns_sd_get_schema(), pretty, fname);
}
static inline bool mgos_config_dns_sd_copy(const struct mgos_config_dns_sd *src, struct mgos_config_dns_sd *dst) {
  return mgos_conf_copy(mgos_config_dns_sd_get_schema(), src, dst);
}
static inline void mgos_config_dns_sd_free(struct mgos_config_dns_sd *cfg) {
  return mgos_conf_free(mgos_config_dns_sd_get_schema(), cfg);
}

/* http type struct mgos_config_http */
struct mgos_config_http {
  int enable;
  const char * listen_addr;
  const char * document_root;
  const char * index_files;
  const char * ssl_cert;
  const char * ssl_key;
  const char * ssl_ca_cert;
  const char * upload_acl;
  const char * hidden_files;
  const char * auth_domain;
  const char * auth_file;
  int auth_algo;
  const char * extra_headers;
};
const struct mgos_conf_entry *mgos_config_http_get_schema(void);
void mgos_config_http_set_defaults(struct mgos_config_http *cfg);
static inline bool mgos_config_http_parse(struct mg_str json, struct mgos_config_http *cfg) {
  mgos_config_http_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_http_get_schema(), cfg);
}
bool mgos_config_http_parse_f(const char *fname, struct mgos_config_http *cfg);
static inline bool mgos_config_http_emit(const struct mgos_config_http *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_http_get_schema(), pretty, out);
}
static inline bool mgos_config_http_emit_f(const struct mgos_config_http *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_http_get_schema(), pretty, fname);
}
static inline bool mgos_config_http_copy(const struct mgos_config_http *src, struct mgos_config_http *dst) {
  return mgos_conf_copy(mgos_config_http_get_schema(), src, dst);
}
static inline void mgos_config_http_free(struct mgos_config_http *cfg) {
  return mgos_conf_free(mgos_config_http_get_schema(), cfg);
}

/* mjs type struct mgos_config_mjs */
struct mgos_config_mjs {
  int generate_jsc;
};
const struct mgos_conf_entry *mgos_config_mjs_get_schema(void);
void mgos_config_mjs_set_defaults(struct mgos_config_mjs *cfg);
static inline bool mgos_config_mjs_parse(struct mg_str json, struct mgos_config_mjs *cfg) {
  mgos_config_mjs_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_mjs_get_schema(), cfg);
}
bool mgos_config_mjs_parse_f(const char *fname, struct mgos_config_mjs *cfg);
static inline bool mgos_config_mjs_emit(const struct mgos_config_mjs *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_mjs_get_schema(), pretty, out);
}
static inline bool mgos_config_mjs_emit_f(const struct mgos_config_mjs *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_mjs_get_schema(), pretty, fname);
}
static inline bool mgos_config_mjs_copy(const struct mgos_config_mjs *src, struct mgos_config_mjs *dst) {
  return mgos_conf_copy(mgos_config_mjs_get_schema(), src, dst);
}
static inline void mgos_config_mjs_free(struct mgos_config_mjs *cfg) {
  return mgos_conf_free(mgos_config_mjs_get_schema(), cfg);
}

/* update type struct mgos_config_update */
struct mgos_config_update {
  int timeout;
  int commit_timeout;
  const char * key0;
  const char * key1;
  const char * key2;
  const char * key3;
  const char * key4;
  const char * key5;
  const char * key6;
  const char * key7;
  int sig_req_mask;
  const char * url;
  int interval;
  const char * extra_http_headers;
  const char * ssl_ca_file;
  const char * ssl_client_cert_file;
  const char * ssl_server_name;
  int enable_post;
};
const struct mgos_conf_entry *mgos_config_update_get_schema(void);
void mgos_config_update_set_defaults(struct mgos_config_update *cfg);
static inline bool mgos_config_update_parse(struct mg_str json, struct mgos_config_update *cfg) {
  mgos_config_update_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_update_get_schema(), cfg);
}
bool mgos_config_update_parse_f(const char *fname, struct mgos_config_update *cfg);
static inline bool mgos_config_update_emit(const struct mgos_config_update *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_update_get_schema(), pretty, out);
}
static inline bool mgos_config_update_emit_f(const struct mgos_config_update *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_update_get_schema(), pretty, fname);
}
static inline bool mgos_config_update_copy(const struct mgos_config_update *src, struct mgos_config_update *dst) {
  return mgos_conf_copy(mgos_config_update_get_schema(), src, dst);
}
static inline void mgos_config_update_free(struct mgos_config_update *cfg) {
  return mgos_conf_free(mgos_config_update_get_schema(), cfg);
}

/* rpc.uart type struct mgos_config_rpc_uart */
struct mgos_config_rpc_uart {
  int uart_no;
  int baud_rate;
  const char * fc_type;
  const char * dst;
  int enable;
  int no_delay;
  int rx_buf_size;
  int tx_buf_size;
};
const struct mgos_conf_entry *mgos_config_rpc_uart_get_schema(void);
void mgos_config_rpc_uart_set_defaults(struct mgos_config_rpc_uart *cfg);
static inline bool mgos_config_rpc_uart_parse(struct mg_str json, struct mgos_config_rpc_uart *cfg) {
  mgos_config_rpc_uart_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_rpc_uart_get_schema(), cfg);
}
bool mgos_config_rpc_uart_parse_f(const char *fname, struct mgos_config_rpc_uart *cfg);
static inline bool mgos_config_rpc_uart_emit(const struct mgos_config_rpc_uart *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_rpc_uart_get_schema(), pretty, out);
}
static inline bool mgos_config_rpc_uart_emit_f(const struct mgos_config_rpc_uart *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_rpc_uart_get_schema(), pretty, fname);
}
static inline bool mgos_config_rpc_uart_copy(const struct mgos_config_rpc_uart *src, struct mgos_config_rpc_uart *dst) {
  return mgos_conf_copy(mgos_config_rpc_uart_get_schema(), src, dst);
}
static inline void mgos_config_rpc_uart_free(struct mgos_config_rpc_uart *cfg) {
  return mgos_conf_free(mgos_config_rpc_uart_get_schema(), cfg);
}

/* rpc type struct mgos_config_rpc */
struct mgos_config_rpc {
  int enable;
  int http_enable;
  int service_sys_enable;
  int max_frame_size;
  int max_queue_length;
  int max_non_persistent_channels;
  int default_out_channel_idle_close_timeout;
  const char * acl;
  const char * acl_file;
  const char * auth_domain;
  const char * auth_file;
  int auth_algo;
  struct mgos_config_rpc_uart uart;
};
const struct mgos_conf_entry *mgos_config_rpc_get_schema(void);
void mgos_config_rpc_set_defaults(struct mgos_config_rpc *cfg);
static inline bool mgos_config_rpc_parse(struct mg_str json, struct mgos_config_rpc *cfg) {
  mgos_config_rpc_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_rpc_get_schema(), cfg);
}
bool mgos_config_rpc_parse_f(const char *fname, struct mgos_config_rpc *cfg);
static inline bool mgos_config_rpc_emit(const struct mgos_config_rpc *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_rpc_get_schema(), pretty, out);
}
static inline bool mgos_config_rpc_emit_f(const struct mgos_config_rpc *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_rpc_get_schema(), pretty, fname);
}
static inline bool mgos_config_rpc_copy(const struct mgos_config_rpc *src, struct mgos_config_rpc *dst) {
  return mgos_conf_copy(mgos_config_rpc_get_schema(), src, dst);
}
static inline void mgos_config_rpc_free(struct mgos_config_rpc *cfg) {
  return mgos_conf_free(mgos_config_rpc_get_schema(), cfg);
}

/* wifi.ap type struct mgos_config_wifi_ap */
struct mgos_config_wifi_ap {
  int enable;
  const char * ssid;
  const char * pass;
  int hidden;
  int channel;
  int max_connections;
  const char * ip;
  const char * netmask;
  const char * gw;
  const char * dhcp_start;
  const char * dhcp_end;
  int trigger_on_gpio;
  int disable_after;
  const char * hostname;
  int bandwidth_20mhz;
  const char * protocol;
};
const struct mgos_conf_entry *mgos_config_wifi_ap_get_schema(void);
void mgos_config_wifi_ap_set_defaults(struct mgos_config_wifi_ap *cfg);
static inline bool mgos_config_wifi_ap_parse(struct mg_str json, struct mgos_config_wifi_ap *cfg) {
  mgos_config_wifi_ap_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_wifi_ap_get_schema(), cfg);
}
bool mgos_config_wifi_ap_parse_f(const char *fname, struct mgos_config_wifi_ap *cfg);
static inline bool mgos_config_wifi_ap_emit(const struct mgos_config_wifi_ap *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_wifi_ap_get_schema(), pretty, out);
}
static inline bool mgos_config_wifi_ap_emit_f(const struct mgos_config_wifi_ap *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_wifi_ap_get_schema(), pretty, fname);
}
static inline bool mgos_config_wifi_ap_copy(const struct mgos_config_wifi_ap *src, struct mgos_config_wifi_ap *dst) {
  return mgos_conf_copy(mgos_config_wifi_ap_get_schema(), src, dst);
}
static inline void mgos_config_wifi_ap_free(struct mgos_config_wifi_ap *cfg) {
  return mgos_conf_free(mgos_config_wifi_ap_get_schema(), cfg);
}

/* wifi.sta type struct mgos_config_wifi_sta */
struct mgos_config_wifi_sta {
  int enable;
  const char * ssid;
  const char * pass;
  const char * bssid;
  int channel;
  const char * last_bssid;
  int last_channel;
  const char * user;
  const char * anon_identity;
  const char * cert;
  const char * key;
  const char * ca_cert;
  const char * ip;
  const char * netmask;
  const char * gw;
  const char * nameserver;
  const char * dhcp_hostname;
  const char * protocol;
  int listen_interval_ms;
};
const struct mgos_conf_entry *mgos_config_wifi_sta_get_schema(void);
void mgos_config_wifi_sta_set_defaults(struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta_parse(struct mg_str json, struct mgos_config_wifi_sta *cfg) {
  mgos_config_wifi_sta_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_wifi_sta_get_schema(), cfg);
}
bool mgos_config_wifi_sta_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta_emit(const struct mgos_config_wifi_sta *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_wifi_sta_get_schema(), pretty, out);
}
static inline bool mgos_config_wifi_sta_emit_f(const struct mgos_config_wifi_sta *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_wifi_sta_get_schema(), pretty, fname);
}
static inline bool mgos_config_wifi_sta_copy(const struct mgos_config_wifi_sta *src, struct mgos_config_wifi_sta *dst) {
  return mgos_conf_copy(mgos_config_wifi_sta_get_schema(), src, dst);
}
static inline void mgos_config_wifi_sta_free(struct mgos_config_wifi_sta *cfg) {
  return mgos_conf_free(mgos_config_wifi_sta_get_schema(), cfg);
}

/* wifi.sta1 type struct mgos_config_wifi_sta */
const struct mgos_conf_entry *mgos_config_wifi_sta1_get_schema(void);
void mgos_config_wifi_sta1_set_defaults(struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta1_parse(struct mg_str json, struct mgos_config_wifi_sta *cfg) {
  mgos_config_wifi_sta1_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_wifi_sta1_get_schema(), cfg);
}
bool mgos_config_wifi_sta1_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta1_emit(const struct mgos_config_wifi_sta *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_wifi_sta1_get_schema(), pretty, out);
}
static inline bool mgos_config_wifi_sta1_emit_f(const struct mgos_config_wifi_sta *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_wifi_sta1_get_schema(), pretty, fname);
}
static inline bool mgos_config_wifi_sta1_copy(const struct mgos_config_wifi_sta *src, struct mgos_config_wifi_sta *dst) {
  return mgos_conf_copy(mgos_config_wifi_sta1_get_schema(), src, dst);
}
static inline void mgos_config_wifi_sta1_free(struct mgos_config_wifi_sta *cfg) {
  return mgos_conf_free(mgos_config_wifi_sta1_get_schema(), cfg);
}

/* wifi.sta2 type struct mgos_config_wifi_sta */
const struct mgos_conf_entry *mgos_config_wifi_sta2_get_schema(void);
void mgos_config_wifi_sta2_set_defaults(struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta2_parse(struct mg_str json, struct mgos_config_wifi_sta *cfg) {
  mgos_config_wifi_sta2_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_wifi_sta2_get_schema(), cfg);
}
bool mgos_config_wifi_sta2_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg);
static inline bool mgos_config_wifi_sta2_emit(const struct mgos_config_wifi_sta *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_wifi_sta2_get_schema(), pretty, out);
}
static inline bool mgos_config_wifi_sta2_emit_f(const struct mgos_config_wifi_sta *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_wifi_sta2_get_schema(), pretty, fname);
}
static inline bool mgos_config_wifi_sta2_copy(const struct mgos_config_wifi_sta *src, struct mgos_config_wifi_sta *dst) {
  return mgos_conf_copy(mgos_config_wifi_sta2_get_schema(), src, dst);
}
static inline void mgos_config_wifi_sta2_free(struct mgos_config_wifi_sta *cfg) {
  return mgos_conf_free(mgos_config_wifi_sta2_get_schema(), cfg);
}

/* wifi type struct mgos_config_wifi */
struct mgos_config_wifi {
  struct mgos_config_wifi_ap ap;
  struct mgos_config_wifi_sta sta;
  struct mgos_config_wifi_sta sta1;
  struct mgos_config_wifi_sta sta2;
  int sta_rssi_thr;
  int sta_connect_timeout;
  int sta_roam_rssi_thr;
  int sta_roam_interval;
  int sta_ps_mode;
};
const struct mgos_conf_entry *mgos_config_wifi_get_schema(void);
void mgos_config_wifi_set_defaults(struct mgos_config_wifi *cfg);
static inline bool mgos_config_wifi_parse(struct mg_str json, struct mgos_config_wifi *cfg) {
  mgos_config_wifi_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_wifi_get_schema(), cfg);
}
bool mgos_config_wifi_parse_f(const char *fname, struct mgos_config_wifi *cfg);
static inline bool mgos_config_wifi_emit(const struct mgos_config_wifi *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_wifi_get_schema(), pretty, out);
}
static inline bool mgos_config_wifi_emit_f(const struct mgos_config_wifi *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_wifi_get_schema(), pretty, fname);
}
static inline bool mgos_config_wifi_copy(const struct mgos_config_wifi *src, struct mgos_config_wifi *dst) {
  return mgos_conf_copy(mgos_config_wifi_get_schema(), src, dst);
}
static inline void mgos_config_wifi_free(struct mgos_config_wifi *cfg) {
  return mgos_conf_free(mgos_config_wifi_get_schema(), cfg);
}

/* sntp type struct mgos_config_sntp */
struct mgos_config_sntp {
  int enable;
  const char * server;
  int use_dhcp_ntp_server;
  int retry_min;
  int retry_max;
  int update_interval;
};
const struct mgos_conf_entry *mgos_config_sntp_get_schema(void);
void mgos_config_sntp_set_defaults(struct mgos_config_sntp *cfg);
static inline bool mgos_config_sntp_parse(struct mg_str json, struct mgos_config_sntp *cfg) {
  mgos_config_sntp_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_sntp_get_schema(), cfg);
}
bool mgos_config_sntp_parse_f(const char *fname, struct mgos_config_sntp *cfg);
static inline bool mgos_config_sntp_emit(const struct mgos_config_sntp *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_sntp_get_schema(), pretty, out);
}
static inline bool mgos_config_sntp_emit_f(const struct mgos_config_sntp *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_sntp_get_schema(), pretty, fname);
}
static inline bool mgos_config_sntp_copy(const struct mgos_config_sntp *src, struct mgos_config_sntp *dst) {
  return mgos_conf_copy(mgos_config_sntp_get_schema(), src, dst);
}
static inline void mgos_config_sntp_free(struct mgos_config_sntp *cfg) {
  return mgos_conf_free(mgos_config_sntp_get_schema(), cfg);
}

/* app type struct mgos_config_app */
struct mgos_config_app {
  const char * name;
};
const struct mgos_conf_entry *mgos_config_app_get_schema(void);
void mgos_config_app_set_defaults(struct mgos_config_app *cfg);
static inline bool mgos_config_app_parse(struct mg_str json, struct mgos_config_app *cfg) {
  mgos_config_app_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_app_get_schema(), cfg);
}
bool mgos_config_app_parse_f(const char *fname, struct mgos_config_app *cfg);
static inline bool mgos_config_app_emit(const struct mgos_config_app *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_app_get_schema(), pretty, out);
}
static inline bool mgos_config_app_emit_f(const struct mgos_config_app *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_app_get_schema(), pretty, fname);
}
static inline bool mgos_config_app_copy(const struct mgos_config_app *src, struct mgos_config_app *dst) {
  return mgos_conf_copy(mgos_config_app_get_schema(), src, dst);
}
static inline void mgos_config_app_free(struct mgos_config_app *cfg) {
  return mgos_conf_free(mgos_config_app_get_schema(), cfg);
}

/* <root> type struct mgos_config */
struct mgos_config {
  struct mgos_config_debug debug;
  struct mgos_config_device device;
  struct mgos_config_sys sys;
  const char * conf_acl;
  struct mgos_config_dns_sd dns_sd;
  struct mgos_config_http http;
  struct mgos_config_mjs mjs;
  struct mgos_config_update update;
  struct mgos_config_rpc rpc;
  struct mgos_config_wifi wifi;
  struct mgos_config_sntp sntp;
  struct mgos_config_app app;
};
const struct mgos_conf_entry *mgos_config_get_schema(void);
void mgos_config_set_defaults(struct mgos_config *cfg);
static inline bool mgos_config_parse(struct mg_str json, struct mgos_config *cfg) {
  mgos_config_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_get_schema(), cfg);
}
bool mgos_config_parse_f(const char *fname, struct mgos_config *cfg);
static inline bool mgos_config_emit(const struct mgos_config *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_get_schema(), pretty, out);
}
static inline bool mgos_config_emit_f(const struct mgos_config *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_get_schema(), pretty, fname);
}
static inline bool mgos_config_copy(const struct mgos_config *src, struct mgos_config *dst) {
  return mgos_conf_copy(mgos_config_get_schema(), src, dst);
}
static inline void mgos_config_free(struct mgos_config *cfg) {
  return mgos_conf_free(mgos_config_get_schema(), cfg);
}

extern struct mgos_config mgos_sys_config;

/* debug */
#define MGOS_CONFIG_HAVE_DEBUG
#define MGOS_SYS_CONFIG_HAVE_DEBUG
const struct mgos_config_debug *mgos_config_get_debug(const struct mgos_config *cfg);
static inline const struct mgos_config_debug *mgos_sys_config_get_debug(void) { return mgos_config_get_debug(&mgos_sys_config); }

/* debug.udp_log_addr */
#define MGOS_CONFIG_HAVE_DEBUG_UDP_LOG_ADDR
#define MGOS_SYS_CONFIG_HAVE_DEBUG_UDP_LOG_ADDR
const char * mgos_config_get_debug_udp_log_addr(const struct mgos_config *cfg);
const char * mgos_config_get_default_debug_udp_log_addr(void);
static inline const char * mgos_sys_config_get_debug_udp_log_addr(void) { return mgos_config_get_debug_udp_log_addr(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_debug_udp_log_addr(void) { return mgos_config_get_default_debug_udp_log_addr(); }
void mgos_config_set_debug_udp_log_addr(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_debug_udp_log_addr(const char * v) { mgos_config_set_debug_udp_log_addr(&mgos_sys_config, v); }

/* debug.udp_log_level */
#define MGOS_CONFIG_HAVE_DEBUG_UDP_LOG_LEVEL
#define MGOS_SYS_CONFIG_HAVE_DEBUG_UDP_LOG_LEVEL
int mgos_config_get_debug_udp_log_level(const struct mgos_config *cfg);
int mgos_config_get_default_debug_udp_log_level(void);
static inline int mgos_sys_config_get_debug_udp_log_level(void) { return mgos_config_get_debug_udp_log_level(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_udp_log_level(void) { return mgos_config_get_default_debug_udp_log_level(); }
void mgos_config_set_debug_udp_log_level(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_udp_log_level(int v) { mgos_config_set_debug_udp_log_level(&mgos_sys_config, v); }

/* debug.mbedtls_level */
#define MGOS_CONFIG_HAVE_DEBUG_MBEDTLS_LEVEL
#define MGOS_SYS_CONFIG_HAVE_DEBUG_MBEDTLS_LEVEL
int mgos_config_get_debug_mbedtls_level(const struct mgos_config *cfg);
int mgos_config_get_default_debug_mbedtls_level(void);
static inline int mgos_sys_config_get_debug_mbedtls_level(void) { return mgos_config_get_debug_mbedtls_level(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_mbedtls_level(void) { return mgos_config_get_default_debug_mbedtls_level(); }
void mgos_config_set_debug_mbedtls_level(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_mbedtls_level(int v) { mgos_config_set_debug_mbedtls_level(&mgos_sys_config, v); }

/* debug.level */
#define MGOS_CONFIG_HAVE_DEBUG_LEVEL
#define MGOS_SYS_CONFIG_HAVE_DEBUG_LEVEL
int mgos_config_get_debug_level(const struct mgos_config *cfg);
int mgos_config_get_default_debug_level(void);
static inline int mgos_sys_config_get_debug_level(void) { return mgos_config_get_debug_level(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_level(void) { return mgos_config_get_default_debug_level(); }
void mgos_config_set_debug_level(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_level(int v) { mgos_config_set_debug_level(&mgos_sys_config, v); }

/* debug.file_level */
#define MGOS_CONFIG_HAVE_DEBUG_FILE_LEVEL
#define MGOS_SYS_CONFIG_HAVE_DEBUG_FILE_LEVEL
const char * mgos_config_get_debug_file_level(const struct mgos_config *cfg);
const char * mgos_config_get_default_debug_file_level(void);
static inline const char * mgos_sys_config_get_debug_file_level(void) { return mgos_config_get_debug_file_level(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_debug_file_level(void) { return mgos_config_get_default_debug_file_level(); }
void mgos_config_set_debug_file_level(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_debug_file_level(const char * v) { mgos_config_set_debug_file_level(&mgos_sys_config, v); }

/* debug.event_level */
#define MGOS_CONFIG_HAVE_DEBUG_EVENT_LEVEL
#define MGOS_SYS_CONFIG_HAVE_DEBUG_EVENT_LEVEL
int mgos_config_get_debug_event_level(const struct mgos_config *cfg);
int mgos_config_get_default_debug_event_level(void);
static inline int mgos_sys_config_get_debug_event_level(void) { return mgos_config_get_debug_event_level(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_event_level(void) { return mgos_config_get_default_debug_event_level(); }
void mgos_config_set_debug_event_level(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_event_level(int v) { mgos_config_set_debug_event_level(&mgos_sys_config, v); }

/* debug.stdout_uart */
#define MGOS_CONFIG_HAVE_DEBUG_STDOUT_UART
#define MGOS_SYS_CONFIG_HAVE_DEBUG_STDOUT_UART
int mgos_config_get_debug_stdout_uart(const struct mgos_config *cfg);
int mgos_config_get_default_debug_stdout_uart(void);
static inline int mgos_sys_config_get_debug_stdout_uart(void) { return mgos_config_get_debug_stdout_uart(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_stdout_uart(void) { return mgos_config_get_default_debug_stdout_uart(); }
void mgos_config_set_debug_stdout_uart(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_stdout_uart(int v) { mgos_config_set_debug_stdout_uart(&mgos_sys_config, v); }

/* debug.stderr_uart */
#define MGOS_CONFIG_HAVE_DEBUG_STDERR_UART
#define MGOS_SYS_CONFIG_HAVE_DEBUG_STDERR_UART
int mgos_config_get_debug_stderr_uart(const struct mgos_config *cfg);
int mgos_config_get_default_debug_stderr_uart(void);
static inline int mgos_sys_config_get_debug_stderr_uart(void) { return mgos_config_get_debug_stderr_uart(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_stderr_uart(void) { return mgos_config_get_default_debug_stderr_uart(); }
void mgos_config_set_debug_stderr_uart(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_stderr_uart(int v) { mgos_config_set_debug_stderr_uart(&mgos_sys_config, v); }

/* debug.factory_reset_gpio */
#define MGOS_CONFIG_HAVE_DEBUG_FACTORY_RESET_GPIO
#define MGOS_SYS_CONFIG_HAVE_DEBUG_FACTORY_RESET_GPIO
int mgos_config_get_debug_factory_reset_gpio(const struct mgos_config *cfg);
int mgos_config_get_default_debug_factory_reset_gpio(void);
static inline int mgos_sys_config_get_debug_factory_reset_gpio(void) { return mgos_config_get_debug_factory_reset_gpio(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_debug_factory_reset_gpio(void) { return mgos_config_get_default_debug_factory_reset_gpio(); }
void mgos_config_set_debug_factory_reset_gpio(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_debug_factory_reset_gpio(int v) { mgos_config_set_debug_factory_reset_gpio(&mgos_sys_config, v); }

/* debug.mg_mgr_hexdump_file */
#define MGOS_CONFIG_HAVE_DEBUG_MG_MGR_HEXDUMP_FILE
#define MGOS_SYS_CONFIG_HAVE_DEBUG_MG_MGR_HEXDUMP_FILE
const char * mgos_config_get_debug_mg_mgr_hexdump_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_debug_mg_mgr_hexdump_file(void);
static inline const char * mgos_sys_config_get_debug_mg_mgr_hexdump_file(void) { return mgos_config_get_debug_mg_mgr_hexdump_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_debug_mg_mgr_hexdump_file(void) { return mgos_config_get_default_debug_mg_mgr_hexdump_file(); }
void mgos_config_set_debug_mg_mgr_hexdump_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_debug_mg_mgr_hexdump_file(const char * v) { mgos_config_set_debug_mg_mgr_hexdump_file(&mgos_sys_config, v); }

/* device */
#define MGOS_CONFIG_HAVE_DEVICE
#define MGOS_SYS_CONFIG_HAVE_DEVICE
const struct mgos_config_device *mgos_config_get_device(const struct mgos_config *cfg);
static inline const struct mgos_config_device *mgos_sys_config_get_device(void) { return mgos_config_get_device(&mgos_sys_config); }

/* device.id */
#define MGOS_CONFIG_HAVE_DEVICE_ID
#define MGOS_SYS_CONFIG_HAVE_DEVICE_ID
const char * mgos_config_get_device_id(const struct mgos_config *cfg);
const char * mgos_config_get_default_device_id(void);
static inline const char * mgos_sys_config_get_device_id(void) { return mgos_config_get_device_id(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_device_id(void) { return mgos_config_get_default_device_id(); }
void mgos_config_set_device_id(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_device_id(const char * v) { mgos_config_set_device_id(&mgos_sys_config, v); }

/* device.license */
#define MGOS_CONFIG_HAVE_DEVICE_LICENSE
#define MGOS_SYS_CONFIG_HAVE_DEVICE_LICENSE
const char * mgos_config_get_device_license(const struct mgos_config *cfg);
const char * mgos_config_get_default_device_license(void);
static inline const char * mgos_sys_config_get_device_license(void) { return mgos_config_get_device_license(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_device_license(void) { return mgos_config_get_default_device_license(); }
void mgos_config_set_device_license(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_device_license(const char * v) { mgos_config_set_device_license(&mgos_sys_config, v); }

/* device.mac */
#define MGOS_CONFIG_HAVE_DEVICE_MAC
#define MGOS_SYS_CONFIG_HAVE_DEVICE_MAC
const char * mgos_config_get_device_mac(const struct mgos_config *cfg);
const char * mgos_config_get_default_device_mac(void);
static inline const char * mgos_sys_config_get_device_mac(void) { return mgos_config_get_device_mac(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_device_mac(void) { return mgos_config_get_default_device_mac(); }
void mgos_config_set_device_mac(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_device_mac(const char * v) { mgos_config_set_device_mac(&mgos_sys_config, v); }

/* device.public_key */
#define MGOS_CONFIG_HAVE_DEVICE_PUBLIC_KEY
#define MGOS_SYS_CONFIG_HAVE_DEVICE_PUBLIC_KEY
const char * mgos_config_get_device_public_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_device_public_key(void);
static inline const char * mgos_sys_config_get_device_public_key(void) { return mgos_config_get_device_public_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_device_public_key(void) { return mgos_config_get_default_device_public_key(); }
void mgos_config_set_device_public_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_device_public_key(const char * v) { mgos_config_set_device_public_key(&mgos_sys_config, v); }

/* device.sn */
#define MGOS_CONFIG_HAVE_DEVICE_SN
#define MGOS_SYS_CONFIG_HAVE_DEVICE_SN
const char * mgos_config_get_device_sn(const struct mgos_config *cfg);
const char * mgos_config_get_default_device_sn(void);
static inline const char * mgos_sys_config_get_device_sn(void) { return mgos_config_get_device_sn(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_device_sn(void) { return mgos_config_get_default_device_sn(); }
void mgos_config_set_device_sn(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_device_sn(const char * v) { mgos_config_set_device_sn(&mgos_sys_config, v); }

/* sys */
#define MGOS_CONFIG_HAVE_SYS
#define MGOS_SYS_CONFIG_HAVE_SYS
const struct mgos_config_sys *mgos_config_get_sys(const struct mgos_config *cfg);
static inline const struct mgos_config_sys *mgos_sys_config_get_sys(void) { return mgos_config_get_sys(&mgos_sys_config); }

/* sys.tz_spec */
#define MGOS_CONFIG_HAVE_SYS_TZ_SPEC
#define MGOS_SYS_CONFIG_HAVE_SYS_TZ_SPEC
const char * mgos_config_get_sys_tz_spec(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_tz_spec(void);
static inline const char * mgos_sys_config_get_sys_tz_spec(void) { return mgos_config_get_sys_tz_spec(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_tz_spec(void) { return mgos_config_get_default_sys_tz_spec(); }
void mgos_config_set_sys_tz_spec(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_tz_spec(const char * v) { mgos_config_set_sys_tz_spec(&mgos_sys_config, v); }

/* sys.wdt_timeout */
#define MGOS_CONFIG_HAVE_SYS_WDT_TIMEOUT
#define MGOS_SYS_CONFIG_HAVE_SYS_WDT_TIMEOUT
int mgos_config_get_sys_wdt_timeout(const struct mgos_config *cfg);
int mgos_config_get_default_sys_wdt_timeout(void);
static inline int mgos_sys_config_get_sys_wdt_timeout(void) { return mgos_config_get_sys_wdt_timeout(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sys_wdt_timeout(void) { return mgos_config_get_default_sys_wdt_timeout(); }
void mgos_config_set_sys_wdt_timeout(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sys_wdt_timeout(int v) { mgos_config_set_sys_wdt_timeout(&mgos_sys_config, v); }

/* sys.pref_ota_lib */
#define MGOS_CONFIG_HAVE_SYS_PREF_OTA_LIB
#define MGOS_SYS_CONFIG_HAVE_SYS_PREF_OTA_LIB
const char * mgos_config_get_sys_pref_ota_lib(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_pref_ota_lib(void);
static inline const char * mgos_sys_config_get_sys_pref_ota_lib(void) { return mgos_config_get_sys_pref_ota_lib(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_pref_ota_lib(void) { return mgos_config_get_default_sys_pref_ota_lib(); }
void mgos_config_set_sys_pref_ota_lib(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_pref_ota_lib(const char * v) { mgos_config_set_sys_pref_ota_lib(&mgos_sys_config, v); }

/* conf_acl */
#define MGOS_CONFIG_HAVE_CONF_ACL
#define MGOS_SYS_CONFIG_HAVE_CONF_ACL
const char * mgos_config_get_conf_acl(const struct mgos_config *cfg);
const char * mgos_config_get_default_conf_acl(void);
static inline const char * mgos_sys_config_get_conf_acl(void) { return mgos_config_get_conf_acl(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_conf_acl(void) { return mgos_config_get_default_conf_acl(); }
void mgos_config_set_conf_acl(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_conf_acl(const char * v) { mgos_config_set_conf_acl(&mgos_sys_config, v); }

/* dns_sd */
#define MGOS_CONFIG_HAVE_DNS_SD
#define MGOS_SYS_CONFIG_HAVE_DNS_SD
const struct mgos_config_dns_sd *mgos_config_get_dns_sd(const struct mgos_config *cfg);
static inline const struct mgos_config_dns_sd *mgos_sys_config_get_dns_sd(void) { return mgos_config_get_dns_sd(&mgos_sys_config); }

/* dns_sd.enable */
#define MGOS_CONFIG_HAVE_DNS_SD_ENABLE
#define MGOS_SYS_CONFIG_HAVE_DNS_SD_ENABLE
int mgos_config_get_dns_sd_enable(const struct mgos_config *cfg);
int mgos_config_get_default_dns_sd_enable(void);
static inline int mgos_sys_config_get_dns_sd_enable(void) { return mgos_config_get_dns_sd_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_dns_sd_enable(void) { return mgos_config_get_default_dns_sd_enable(); }
void mgos_config_set_dns_sd_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_dns_sd_enable(int v) { mgos_config_set_dns_sd_enable(&mgos_sys_config, v); }

/* dns_sd.adv_only */
#define MGOS_CONFIG_HAVE_DNS_SD_ADV_ONLY
#define MGOS_SYS_CONFIG_HAVE_DNS_SD_ADV_ONLY
int mgos_config_get_dns_sd_adv_only(const struct mgos_config *cfg);
int mgos_config_get_default_dns_sd_adv_only(void);
static inline int mgos_sys_config_get_dns_sd_adv_only(void) { return mgos_config_get_dns_sd_adv_only(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_dns_sd_adv_only(void) { return mgos_config_get_default_dns_sd_adv_only(); }
void mgos_config_set_dns_sd_adv_only(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_dns_sd_adv_only(int v) { mgos_config_set_dns_sd_adv_only(&mgos_sys_config, v); }

/* dns_sd.host_name */
#define MGOS_CONFIG_HAVE_DNS_SD_HOST_NAME
#define MGOS_SYS_CONFIG_HAVE_DNS_SD_HOST_NAME
const char * mgos_config_get_dns_sd_host_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_dns_sd_host_name(void);
static inline const char * mgos_sys_config_get_dns_sd_host_name(void) { return mgos_config_get_dns_sd_host_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_dns_sd_host_name(void) { return mgos_config_get_default_dns_sd_host_name(); }
void mgos_config_set_dns_sd_host_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_dns_sd_host_name(const char * v) { mgos_config_set_dns_sd_host_name(&mgos_sys_config, v); }

/* dns_sd.txt */
#define MGOS_CONFIG_HAVE_DNS_SD_TXT
#define MGOS_SYS_CONFIG_HAVE_DNS_SD_TXT
const char * mgos_config_get_dns_sd_txt(const struct mgos_config *cfg);
const char * mgos_config_get_default_dns_sd_txt(void);
static inline const char * mgos_sys_config_get_dns_sd_txt(void) { return mgos_config_get_dns_sd_txt(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_dns_sd_txt(void) { return mgos_config_get_default_dns_sd_txt(); }
void mgos_config_set_dns_sd_txt(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_dns_sd_txt(const char * v) { mgos_config_set_dns_sd_txt(&mgos_sys_config, v); }

/* http */
#define MGOS_CONFIG_HAVE_HTTP
#define MGOS_SYS_CONFIG_HAVE_HTTP
const struct mgos_config_http *mgos_config_get_http(const struct mgos_config *cfg);
static inline const struct mgos_config_http *mgos_sys_config_get_http(void) { return mgos_config_get_http(&mgos_sys_config); }

/* http.enable */
#define MGOS_CONFIG_HAVE_HTTP_ENABLE
#define MGOS_SYS_CONFIG_HAVE_HTTP_ENABLE
int mgos_config_get_http_enable(const struct mgos_config *cfg);
int mgos_config_get_default_http_enable(void);
static inline int mgos_sys_config_get_http_enable(void) { return mgos_config_get_http_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_http_enable(void) { return mgos_config_get_default_http_enable(); }
void mgos_config_set_http_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_http_enable(int v) { mgos_config_set_http_enable(&mgos_sys_config, v); }

/* http.listen_addr */
#define MGOS_CONFIG_HAVE_HTTP_LISTEN_ADDR
#define MGOS_SYS_CONFIG_HAVE_HTTP_LISTEN_ADDR
const char * mgos_config_get_http_listen_addr(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_listen_addr(void);
static inline const char * mgos_sys_config_get_http_listen_addr(void) { return mgos_config_get_http_listen_addr(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_listen_addr(void) { return mgos_config_get_default_http_listen_addr(); }
void mgos_config_set_http_listen_addr(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_listen_addr(const char * v) { mgos_config_set_http_listen_addr(&mgos_sys_config, v); }

/* http.document_root */
#define MGOS_CONFIG_HAVE_HTTP_DOCUMENT_ROOT
#define MGOS_SYS_CONFIG_HAVE_HTTP_DOCUMENT_ROOT
const char * mgos_config_get_http_document_root(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_document_root(void);
static inline const char * mgos_sys_config_get_http_document_root(void) { return mgos_config_get_http_document_root(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_document_root(void) { return mgos_config_get_default_http_document_root(); }
void mgos_config_set_http_document_root(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_document_root(const char * v) { mgos_config_set_http_document_root(&mgos_sys_config, v); }

/* http.index_files */
#define MGOS_CONFIG_HAVE_HTTP_INDEX_FILES
#define MGOS_SYS_CONFIG_HAVE_HTTP_INDEX_FILES
const char * mgos_config_get_http_index_files(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_index_files(void);
static inline const char * mgos_sys_config_get_http_index_files(void) { return mgos_config_get_http_index_files(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_index_files(void) { return mgos_config_get_default_http_index_files(); }
void mgos_config_set_http_index_files(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_index_files(const char * v) { mgos_config_set_http_index_files(&mgos_sys_config, v); }

/* http.ssl_cert */
#define MGOS_CONFIG_HAVE_HTTP_SSL_CERT
#define MGOS_SYS_CONFIG_HAVE_HTTP_SSL_CERT
const char * mgos_config_get_http_ssl_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_ssl_cert(void);
static inline const char * mgos_sys_config_get_http_ssl_cert(void) { return mgos_config_get_http_ssl_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_ssl_cert(void) { return mgos_config_get_default_http_ssl_cert(); }
void mgos_config_set_http_ssl_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_ssl_cert(const char * v) { mgos_config_set_http_ssl_cert(&mgos_sys_config, v); }

/* http.ssl_key */
#define MGOS_CONFIG_HAVE_HTTP_SSL_KEY
#define MGOS_SYS_CONFIG_HAVE_HTTP_SSL_KEY
const char * mgos_config_get_http_ssl_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_ssl_key(void);
static inline const char * mgos_sys_config_get_http_ssl_key(void) { return mgos_config_get_http_ssl_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_ssl_key(void) { return mgos_config_get_default_http_ssl_key(); }
void mgos_config_set_http_ssl_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_ssl_key(const char * v) { mgos_config_set_http_ssl_key(&mgos_sys_config, v); }

/* http.ssl_ca_cert */
#define MGOS_CONFIG_HAVE_HTTP_SSL_CA_CERT
#define MGOS_SYS_CONFIG_HAVE_HTTP_SSL_CA_CERT
const char * mgos_config_get_http_ssl_ca_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_ssl_ca_cert(void);
static inline const char * mgos_sys_config_get_http_ssl_ca_cert(void) { return mgos_config_get_http_ssl_ca_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_ssl_ca_cert(void) { return mgos_config_get_default_http_ssl_ca_cert(); }
void mgos_config_set_http_ssl_ca_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_ssl_ca_cert(const char * v) { mgos_config_set_http_ssl_ca_cert(&mgos_sys_config, v); }

/* http.upload_acl */
#define MGOS_CONFIG_HAVE_HTTP_UPLOAD_ACL
#define MGOS_SYS_CONFIG_HAVE_HTTP_UPLOAD_ACL
const char * mgos_config_get_http_upload_acl(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_upload_acl(void);
static inline const char * mgos_sys_config_get_http_upload_acl(void) { return mgos_config_get_http_upload_acl(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_upload_acl(void) { return mgos_config_get_default_http_upload_acl(); }
void mgos_config_set_http_upload_acl(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_upload_acl(const char * v) { mgos_config_set_http_upload_acl(&mgos_sys_config, v); }

/* http.hidden_files */
#define MGOS_CONFIG_HAVE_HTTP_HIDDEN_FILES
#define MGOS_SYS_CONFIG_HAVE_HTTP_HIDDEN_FILES
const char * mgos_config_get_http_hidden_files(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_hidden_files(void);
static inline const char * mgos_sys_config_get_http_hidden_files(void) { return mgos_config_get_http_hidden_files(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_hidden_files(void) { return mgos_config_get_default_http_hidden_files(); }
void mgos_config_set_http_hidden_files(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_hidden_files(const char * v) { mgos_config_set_http_hidden_files(&mgos_sys_config, v); }

/* http.auth_domain */
#define MGOS_CONFIG_HAVE_HTTP_AUTH_DOMAIN
#define MGOS_SYS_CONFIG_HAVE_HTTP_AUTH_DOMAIN
const char * mgos_config_get_http_auth_domain(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_auth_domain(void);
static inline const char * mgos_sys_config_get_http_auth_domain(void) { return mgos_config_get_http_auth_domain(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_auth_domain(void) { return mgos_config_get_default_http_auth_domain(); }
void mgos_config_set_http_auth_domain(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_auth_domain(const char * v) { mgos_config_set_http_auth_domain(&mgos_sys_config, v); }

/* http.auth_file */
#define MGOS_CONFIG_HAVE_HTTP_AUTH_FILE
#define MGOS_SYS_CONFIG_HAVE_HTTP_AUTH_FILE
const char * mgos_config_get_http_auth_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_auth_file(void);
static inline const char * mgos_sys_config_get_http_auth_file(void) { return mgos_config_get_http_auth_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_auth_file(void) { return mgos_config_get_default_http_auth_file(); }
void mgos_config_set_http_auth_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_auth_file(const char * v) { mgos_config_set_http_auth_file(&mgos_sys_config, v); }

/* http.auth_algo */
#define MGOS_CONFIG_HAVE_HTTP_AUTH_ALGO
#define MGOS_SYS_CONFIG_HAVE_HTTP_AUTH_ALGO
int mgos_config_get_http_auth_algo(const struct mgos_config *cfg);
int mgos_config_get_default_http_auth_algo(void);
static inline int mgos_sys_config_get_http_auth_algo(void) { return mgos_config_get_http_auth_algo(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_http_auth_algo(void) { return mgos_config_get_default_http_auth_algo(); }
void mgos_config_set_http_auth_algo(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_http_auth_algo(int v) { mgos_config_set_http_auth_algo(&mgos_sys_config, v); }

/* http.extra_headers */
#define MGOS_CONFIG_HAVE_HTTP_EXTRA_HEADERS
#define MGOS_SYS_CONFIG_HAVE_HTTP_EXTRA_HEADERS
const char * mgos_config_get_http_extra_headers(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_extra_headers(void);
static inline const char * mgos_sys_config_get_http_extra_headers(void) { return mgos_config_get_http_extra_headers(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_extra_headers(void) { return mgos_config_get_default_http_extra_headers(); }
void mgos_config_set_http_extra_headers(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_extra_headers(const char * v) { mgos_config_set_http_extra_headers(&mgos_sys_config, v); }

/* mjs */
#define MGOS_CONFIG_HAVE_MJS
#define MGOS_SYS_CONFIG_HAVE_MJS
const struct mgos_config_mjs *mgos_config_get_mjs(const struct mgos_config *cfg);
static inline const struct mgos_config_mjs *mgos_sys_config_get_mjs(void) { return mgos_config_get_mjs(&mgos_sys_config); }

/* mjs.generate_jsc */
#define MGOS_CONFIG_HAVE_MJS_GENERATE_JSC
#define MGOS_SYS_CONFIG_HAVE_MJS_GENERATE_JSC
int mgos_config_get_mjs_generate_jsc(const struct mgos_config *cfg);
int mgos_config_get_default_mjs_generate_jsc(void);
static inline int mgos_sys_config_get_mjs_generate_jsc(void) { return mgos_config_get_mjs_generate_jsc(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_mjs_generate_jsc(void) { return mgos_config_get_default_mjs_generate_jsc(); }
void mgos_config_set_mjs_generate_jsc(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_mjs_generate_jsc(int v) { mgos_config_set_mjs_generate_jsc(&mgos_sys_config, v); }

/* update */
#define MGOS_CONFIG_HAVE_UPDATE
#define MGOS_SYS_CONFIG_HAVE_UPDATE
const struct mgos_config_update *mgos_config_get_update(const struct mgos_config *cfg);
static inline const struct mgos_config_update *mgos_sys_config_get_update(void) { return mgos_config_get_update(&mgos_sys_config); }

/* update.timeout */
#define MGOS_CONFIG_HAVE_UPDATE_TIMEOUT
#define MGOS_SYS_CONFIG_HAVE_UPDATE_TIMEOUT
int mgos_config_get_update_timeout(const struct mgos_config *cfg);
int mgos_config_get_default_update_timeout(void);
static inline int mgos_sys_config_get_update_timeout(void) { return mgos_config_get_update_timeout(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_update_timeout(void) { return mgos_config_get_default_update_timeout(); }
void mgos_config_set_update_timeout(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_update_timeout(int v) { mgos_config_set_update_timeout(&mgos_sys_config, v); }

/* update.commit_timeout */
#define MGOS_CONFIG_HAVE_UPDATE_COMMIT_TIMEOUT
#define MGOS_SYS_CONFIG_HAVE_UPDATE_COMMIT_TIMEOUT
int mgos_config_get_update_commit_timeout(const struct mgos_config *cfg);
int mgos_config_get_default_update_commit_timeout(void);
static inline int mgos_sys_config_get_update_commit_timeout(void) { return mgos_config_get_update_commit_timeout(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_update_commit_timeout(void) { return mgos_config_get_default_update_commit_timeout(); }
void mgos_config_set_update_commit_timeout(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_update_commit_timeout(int v) { mgos_config_set_update_commit_timeout(&mgos_sys_config, v); }

/* update.key0 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY0
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY0
const char * mgos_config_get_update_key0(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key0(void);
static inline const char * mgos_sys_config_get_update_key0(void) { return mgos_config_get_update_key0(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key0(void) { return mgos_config_get_default_update_key0(); }
void mgos_config_set_update_key0(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key0(const char * v) { mgos_config_set_update_key0(&mgos_sys_config, v); }

/* update.key1 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY1
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY1
const char * mgos_config_get_update_key1(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key1(void);
static inline const char * mgos_sys_config_get_update_key1(void) { return mgos_config_get_update_key1(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key1(void) { return mgos_config_get_default_update_key1(); }
void mgos_config_set_update_key1(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key1(const char * v) { mgos_config_set_update_key1(&mgos_sys_config, v); }

/* update.key2 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY2
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY2
const char * mgos_config_get_update_key2(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key2(void);
static inline const char * mgos_sys_config_get_update_key2(void) { return mgos_config_get_update_key2(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key2(void) { return mgos_config_get_default_update_key2(); }
void mgos_config_set_update_key2(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key2(const char * v) { mgos_config_set_update_key2(&mgos_sys_config, v); }

/* update.key3 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY3
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY3
const char * mgos_config_get_update_key3(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key3(void);
static inline const char * mgos_sys_config_get_update_key3(void) { return mgos_config_get_update_key3(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key3(void) { return mgos_config_get_default_update_key3(); }
void mgos_config_set_update_key3(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key3(const char * v) { mgos_config_set_update_key3(&mgos_sys_config, v); }

/* update.key4 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY4
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY4
const char * mgos_config_get_update_key4(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key4(void);
static inline const char * mgos_sys_config_get_update_key4(void) { return mgos_config_get_update_key4(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key4(void) { return mgos_config_get_default_update_key4(); }
void mgos_config_set_update_key4(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key4(const char * v) { mgos_config_set_update_key4(&mgos_sys_config, v); }

/* update.key5 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY5
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY5
const char * mgos_config_get_update_key5(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key5(void);
static inline const char * mgos_sys_config_get_update_key5(void) { return mgos_config_get_update_key5(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key5(void) { return mgos_config_get_default_update_key5(); }
void mgos_config_set_update_key5(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key5(const char * v) { mgos_config_set_update_key5(&mgos_sys_config, v); }

/* update.key6 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY6
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY6
const char * mgos_config_get_update_key6(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key6(void);
static inline const char * mgos_sys_config_get_update_key6(void) { return mgos_config_get_update_key6(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key6(void) { return mgos_config_get_default_update_key6(); }
void mgos_config_set_update_key6(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key6(const char * v) { mgos_config_set_update_key6(&mgos_sys_config, v); }

/* update.key7 */
#define MGOS_CONFIG_HAVE_UPDATE_KEY7
#define MGOS_SYS_CONFIG_HAVE_UPDATE_KEY7
const char * mgos_config_get_update_key7(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_key7(void);
static inline const char * mgos_sys_config_get_update_key7(void) { return mgos_config_get_update_key7(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_key7(void) { return mgos_config_get_default_update_key7(); }
void mgos_config_set_update_key7(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_key7(const char * v) { mgos_config_set_update_key7(&mgos_sys_config, v); }

/* update.sig_req_mask */
#define MGOS_CONFIG_HAVE_UPDATE_SIG_REQ_MASK
#define MGOS_SYS_CONFIG_HAVE_UPDATE_SIG_REQ_MASK
int mgos_config_get_update_sig_req_mask(const struct mgos_config *cfg);
int mgos_config_get_default_update_sig_req_mask(void);
static inline int mgos_sys_config_get_update_sig_req_mask(void) { return mgos_config_get_update_sig_req_mask(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_update_sig_req_mask(void) { return mgos_config_get_default_update_sig_req_mask(); }
void mgos_config_set_update_sig_req_mask(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_update_sig_req_mask(int v) { mgos_config_set_update_sig_req_mask(&mgos_sys_config, v); }

/* update.url */
#define MGOS_CONFIG_HAVE_UPDATE_URL
#define MGOS_SYS_CONFIG_HAVE_UPDATE_URL
const char * mgos_config_get_update_url(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_url(void);
static inline const char * mgos_sys_config_get_update_url(void) { return mgos_config_get_update_url(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_url(void) { return mgos_config_get_default_update_url(); }
void mgos_config_set_update_url(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_url(const char * v) { mgos_config_set_update_url(&mgos_sys_config, v); }

/* update.interval */
#define MGOS_CONFIG_HAVE_UPDATE_INTERVAL
#define MGOS_SYS_CONFIG_HAVE_UPDATE_INTERVAL
int mgos_config_get_update_interval(const struct mgos_config *cfg);
int mgos_config_get_default_update_interval(void);
static inline int mgos_sys_config_get_update_interval(void) { return mgos_config_get_update_interval(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_update_interval(void) { return mgos_config_get_default_update_interval(); }
void mgos_config_set_update_interval(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_update_interval(int v) { mgos_config_set_update_interval(&mgos_sys_config, v); }

/* update.extra_http_headers */
#define MGOS_CONFIG_HAVE_UPDATE_EXTRA_HTTP_HEADERS
#define MGOS_SYS_CONFIG_HAVE_UPDATE_EXTRA_HTTP_HEADERS
const char * mgos_config_get_update_extra_http_headers(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_extra_http_headers(void);
static inline const char * mgos_sys_config_get_update_extra_http_headers(void) { return mgos_config_get_update_extra_http_headers(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_extra_http_headers(void) { return mgos_config_get_default_update_extra_http_headers(); }
void mgos_config_set_update_extra_http_headers(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_extra_http_headers(const char * v) { mgos_config_set_update_extra_http_headers(&mgos_sys_config, v); }

/* update.ssl_ca_file */
#define MGOS_CONFIG_HAVE_UPDATE_SSL_CA_FILE
#define MGOS_SYS_CONFIG_HAVE_UPDATE_SSL_CA_FILE
const char * mgos_config_get_update_ssl_ca_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_ssl_ca_file(void);
static inline const char * mgos_sys_config_get_update_ssl_ca_file(void) { return mgos_config_get_update_ssl_ca_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_ssl_ca_file(void) { return mgos_config_get_default_update_ssl_ca_file(); }
void mgos_config_set_update_ssl_ca_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_ssl_ca_file(const char * v) { mgos_config_set_update_ssl_ca_file(&mgos_sys_config, v); }

/* update.ssl_client_cert_file */
#define MGOS_CONFIG_HAVE_UPDATE_SSL_CLIENT_CERT_FILE
#define MGOS_SYS_CONFIG_HAVE_UPDATE_SSL_CLIENT_CERT_FILE
const char * mgos_config_get_update_ssl_client_cert_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_ssl_client_cert_file(void);
static inline const char * mgos_sys_config_get_update_ssl_client_cert_file(void) { return mgos_config_get_update_ssl_client_cert_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_ssl_client_cert_file(void) { return mgos_config_get_default_update_ssl_client_cert_file(); }
void mgos_config_set_update_ssl_client_cert_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_ssl_client_cert_file(const char * v) { mgos_config_set_update_ssl_client_cert_file(&mgos_sys_config, v); }

/* update.ssl_server_name */
#define MGOS_CONFIG_HAVE_UPDATE_SSL_SERVER_NAME
#define MGOS_SYS_CONFIG_HAVE_UPDATE_SSL_SERVER_NAME
const char * mgos_config_get_update_ssl_server_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_update_ssl_server_name(void);
static inline const char * mgos_sys_config_get_update_ssl_server_name(void) { return mgos_config_get_update_ssl_server_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_update_ssl_server_name(void) { return mgos_config_get_default_update_ssl_server_name(); }
void mgos_config_set_update_ssl_server_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_update_ssl_server_name(const char * v) { mgos_config_set_update_ssl_server_name(&mgos_sys_config, v); }

/* update.enable_post */
#define MGOS_CONFIG_HAVE_UPDATE_ENABLE_POST
#define MGOS_SYS_CONFIG_HAVE_UPDATE_ENABLE_POST
int mgos_config_get_update_enable_post(const struct mgos_config *cfg);
int mgos_config_get_default_update_enable_post(void);
static inline int mgos_sys_config_get_update_enable_post(void) { return mgos_config_get_update_enable_post(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_update_enable_post(void) { return mgos_config_get_default_update_enable_post(); }
void mgos_config_set_update_enable_post(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_update_enable_post(int v) { mgos_config_set_update_enable_post(&mgos_sys_config, v); }

/* rpc */
#define MGOS_CONFIG_HAVE_RPC
#define MGOS_SYS_CONFIG_HAVE_RPC
const struct mgos_config_rpc *mgos_config_get_rpc(const struct mgos_config *cfg);
static inline const struct mgos_config_rpc *mgos_sys_config_get_rpc(void) { return mgos_config_get_rpc(&mgos_sys_config); }

/* rpc.enable */
#define MGOS_CONFIG_HAVE_RPC_ENABLE
#define MGOS_SYS_CONFIG_HAVE_RPC_ENABLE
int mgos_config_get_rpc_enable(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_enable(void);
static inline int mgos_sys_config_get_rpc_enable(void) { return mgos_config_get_rpc_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_enable(void) { return mgos_config_get_default_rpc_enable(); }
void mgos_config_set_rpc_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_enable(int v) { mgos_config_set_rpc_enable(&mgos_sys_config, v); }

/* rpc.http_enable */
#define MGOS_CONFIG_HAVE_RPC_HTTP_ENABLE
#define MGOS_SYS_CONFIG_HAVE_RPC_HTTP_ENABLE
int mgos_config_get_rpc_http_enable(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_http_enable(void);
static inline int mgos_sys_config_get_rpc_http_enable(void) { return mgos_config_get_rpc_http_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_http_enable(void) { return mgos_config_get_default_rpc_http_enable(); }
void mgos_config_set_rpc_http_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_http_enable(int v) { mgos_config_set_rpc_http_enable(&mgos_sys_config, v); }

/* rpc.service_sys_enable */
#define MGOS_CONFIG_HAVE_RPC_SERVICE_SYS_ENABLE
#define MGOS_SYS_CONFIG_HAVE_RPC_SERVICE_SYS_ENABLE
int mgos_config_get_rpc_service_sys_enable(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_service_sys_enable(void);
static inline int mgos_sys_config_get_rpc_service_sys_enable(void) { return mgos_config_get_rpc_service_sys_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_service_sys_enable(void) { return mgos_config_get_default_rpc_service_sys_enable(); }
void mgos_config_set_rpc_service_sys_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_service_sys_enable(int v) { mgos_config_set_rpc_service_sys_enable(&mgos_sys_config, v); }

/* rpc.max_frame_size */
#define MGOS_CONFIG_HAVE_RPC_MAX_FRAME_SIZE
#define MGOS_SYS_CONFIG_HAVE_RPC_MAX_FRAME_SIZE
int mgos_config_get_rpc_max_frame_size(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_max_frame_size(void);
static inline int mgos_sys_config_get_rpc_max_frame_size(void) { return mgos_config_get_rpc_max_frame_size(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_max_frame_size(void) { return mgos_config_get_default_rpc_max_frame_size(); }
void mgos_config_set_rpc_max_frame_size(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_max_frame_size(int v) { mgos_config_set_rpc_max_frame_size(&mgos_sys_config, v); }

/* rpc.max_queue_length */
#define MGOS_CONFIG_HAVE_RPC_MAX_QUEUE_LENGTH
#define MGOS_SYS_CONFIG_HAVE_RPC_MAX_QUEUE_LENGTH
int mgos_config_get_rpc_max_queue_length(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_max_queue_length(void);
static inline int mgos_sys_config_get_rpc_max_queue_length(void) { return mgos_config_get_rpc_max_queue_length(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_max_queue_length(void) { return mgos_config_get_default_rpc_max_queue_length(); }
void mgos_config_set_rpc_max_queue_length(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_max_queue_length(int v) { mgos_config_set_rpc_max_queue_length(&mgos_sys_config, v); }

/* rpc.max_non_persistent_channels */
#define MGOS_CONFIG_HAVE_RPC_MAX_NON_PERSISTENT_CHANNELS
#define MGOS_SYS_CONFIG_HAVE_RPC_MAX_NON_PERSISTENT_CHANNELS
int mgos_config_get_rpc_max_non_persistent_channels(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_max_non_persistent_channels(void);
static inline int mgos_sys_config_get_rpc_max_non_persistent_channels(void) { return mgos_config_get_rpc_max_non_persistent_channels(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_max_non_persistent_channels(void) { return mgos_config_get_default_rpc_max_non_persistent_channels(); }
void mgos_config_set_rpc_max_non_persistent_channels(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_max_non_persistent_channels(int v) { mgos_config_set_rpc_max_non_persistent_channels(&mgos_sys_config, v); }

/* rpc.default_out_channel_idle_close_timeout */
#define MGOS_CONFIG_HAVE_RPC_DEFAULT_OUT_CHANNEL_IDLE_CLOSE_TIMEOUT
#define MGOS_SYS_CONFIG_HAVE_RPC_DEFAULT_OUT_CHANNEL_IDLE_CLOSE_TIMEOUT
int mgos_config_get_rpc_default_out_channel_idle_close_timeout(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_default_out_channel_idle_close_timeout(void);
static inline int mgos_sys_config_get_rpc_default_out_channel_idle_close_timeout(void) { return mgos_config_get_rpc_default_out_channel_idle_close_timeout(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_default_out_channel_idle_close_timeout(void) { return mgos_config_get_default_rpc_default_out_channel_idle_close_timeout(); }
void mgos_config_set_rpc_default_out_channel_idle_close_timeout(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_default_out_channel_idle_close_timeout(int v) { mgos_config_set_rpc_default_out_channel_idle_close_timeout(&mgos_sys_config, v); }

/* rpc.acl */
#define MGOS_CONFIG_HAVE_RPC_ACL
#define MGOS_SYS_CONFIG_HAVE_RPC_ACL
const char * mgos_config_get_rpc_acl(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_acl(void);
static inline const char * mgos_sys_config_get_rpc_acl(void) { return mgos_config_get_rpc_acl(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_acl(void) { return mgos_config_get_default_rpc_acl(); }
void mgos_config_set_rpc_acl(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_acl(const char * v) { mgos_config_set_rpc_acl(&mgos_sys_config, v); }

/* rpc.acl_file */
#define MGOS_CONFIG_HAVE_RPC_ACL_FILE
#define MGOS_SYS_CONFIG_HAVE_RPC_ACL_FILE
const char * mgos_config_get_rpc_acl_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_acl_file(void);
static inline const char * mgos_sys_config_get_rpc_acl_file(void) { return mgos_config_get_rpc_acl_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_acl_file(void) { return mgos_config_get_default_rpc_acl_file(); }
void mgos_config_set_rpc_acl_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_acl_file(const char * v) { mgos_config_set_rpc_acl_file(&mgos_sys_config, v); }

/* rpc.auth_domain */
#define MGOS_CONFIG_HAVE_RPC_AUTH_DOMAIN
#define MGOS_SYS_CONFIG_HAVE_RPC_AUTH_DOMAIN
const char * mgos_config_get_rpc_auth_domain(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_auth_domain(void);
static inline const char * mgos_sys_config_get_rpc_auth_domain(void) { return mgos_config_get_rpc_auth_domain(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_auth_domain(void) { return mgos_config_get_default_rpc_auth_domain(); }
void mgos_config_set_rpc_auth_domain(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_auth_domain(const char * v) { mgos_config_set_rpc_auth_domain(&mgos_sys_config, v); }

/* rpc.auth_file */
#define MGOS_CONFIG_HAVE_RPC_AUTH_FILE
#define MGOS_SYS_CONFIG_HAVE_RPC_AUTH_FILE
const char * mgos_config_get_rpc_auth_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_auth_file(void);
static inline const char * mgos_sys_config_get_rpc_auth_file(void) { return mgos_config_get_rpc_auth_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_auth_file(void) { return mgos_config_get_default_rpc_auth_file(); }
void mgos_config_set_rpc_auth_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_auth_file(const char * v) { mgos_config_set_rpc_auth_file(&mgos_sys_config, v); }

/* rpc.auth_algo */
#define MGOS_CONFIG_HAVE_RPC_AUTH_ALGO
#define MGOS_SYS_CONFIG_HAVE_RPC_AUTH_ALGO
int mgos_config_get_rpc_auth_algo(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_auth_algo(void);
static inline int mgos_sys_config_get_rpc_auth_algo(void) { return mgos_config_get_rpc_auth_algo(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_auth_algo(void) { return mgos_config_get_default_rpc_auth_algo(); }
void mgos_config_set_rpc_auth_algo(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_auth_algo(int v) { mgos_config_set_rpc_auth_algo(&mgos_sys_config, v); }

/* rpc.uart */
#define MGOS_CONFIG_HAVE_RPC_UART
#define MGOS_SYS_CONFIG_HAVE_RPC_UART
const struct mgos_config_rpc_uart *mgos_config_get_rpc_uart(const struct mgos_config *cfg);
static inline const struct mgos_config_rpc_uart *mgos_sys_config_get_rpc_uart(void) { return mgos_config_get_rpc_uart(&mgos_sys_config); }

/* rpc.uart.uart_no */
#define MGOS_CONFIG_HAVE_RPC_UART_UART_NO
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_UART_NO
int mgos_config_get_rpc_uart_uart_no(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_uart_no(void);
static inline int mgos_sys_config_get_rpc_uart_uart_no(void) { return mgos_config_get_rpc_uart_uart_no(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_uart_no(void) { return mgos_config_get_default_rpc_uart_uart_no(); }
void mgos_config_set_rpc_uart_uart_no(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_uart_no(int v) { mgos_config_set_rpc_uart_uart_no(&mgos_sys_config, v); }

/* rpc.uart.baud_rate */
#define MGOS_CONFIG_HAVE_RPC_UART_BAUD_RATE
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_BAUD_RATE
int mgos_config_get_rpc_uart_baud_rate(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_baud_rate(void);
static inline int mgos_sys_config_get_rpc_uart_baud_rate(void) { return mgos_config_get_rpc_uart_baud_rate(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_baud_rate(void) { return mgos_config_get_default_rpc_uart_baud_rate(); }
void mgos_config_set_rpc_uart_baud_rate(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_baud_rate(int v) { mgos_config_set_rpc_uart_baud_rate(&mgos_sys_config, v); }

/* rpc.uart.fc_type */
#define MGOS_CONFIG_HAVE_RPC_UART_FC_TYPE
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_FC_TYPE
const char * mgos_config_get_rpc_uart_fc_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_uart_fc_type(void);
static inline const char * mgos_sys_config_get_rpc_uart_fc_type(void) { return mgos_config_get_rpc_uart_fc_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_uart_fc_type(void) { return mgos_config_get_default_rpc_uart_fc_type(); }
void mgos_config_set_rpc_uart_fc_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_uart_fc_type(const char * v) { mgos_config_set_rpc_uart_fc_type(&mgos_sys_config, v); }

/* rpc.uart.dst */
#define MGOS_CONFIG_HAVE_RPC_UART_DST
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_DST
const char * mgos_config_get_rpc_uart_dst(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_uart_dst(void);
static inline const char * mgos_sys_config_get_rpc_uart_dst(void) { return mgos_config_get_rpc_uart_dst(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_uart_dst(void) { return mgos_config_get_default_rpc_uart_dst(); }
void mgos_config_set_rpc_uart_dst(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_uart_dst(const char * v) { mgos_config_set_rpc_uart_dst(&mgos_sys_config, v); }

/* rpc.uart.enable */
#define MGOS_CONFIG_HAVE_RPC_UART_ENABLE
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_ENABLE
int mgos_config_get_rpc_uart_enable(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_enable(void);
static inline int mgos_sys_config_get_rpc_uart_enable(void) { return mgos_config_get_rpc_uart_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_enable(void) { return mgos_config_get_default_rpc_uart_enable(); }
void mgos_config_set_rpc_uart_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_enable(int v) { mgos_config_set_rpc_uart_enable(&mgos_sys_config, v); }

/* rpc.uart.no_delay */
#define MGOS_CONFIG_HAVE_RPC_UART_NO_DELAY
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_NO_DELAY
int mgos_config_get_rpc_uart_no_delay(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_no_delay(void);
static inline int mgos_sys_config_get_rpc_uart_no_delay(void) { return mgos_config_get_rpc_uart_no_delay(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_no_delay(void) { return mgos_config_get_default_rpc_uart_no_delay(); }
void mgos_config_set_rpc_uart_no_delay(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_no_delay(int v) { mgos_config_set_rpc_uart_no_delay(&mgos_sys_config, v); }

/* rpc.uart.rx_buf_size */
#define MGOS_CONFIG_HAVE_RPC_UART_RX_BUF_SIZE
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_RX_BUF_SIZE
int mgos_config_get_rpc_uart_rx_buf_size(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_rx_buf_size(void);
static inline int mgos_sys_config_get_rpc_uart_rx_buf_size(void) { return mgos_config_get_rpc_uart_rx_buf_size(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_rx_buf_size(void) { return mgos_config_get_default_rpc_uart_rx_buf_size(); }
void mgos_config_set_rpc_uart_rx_buf_size(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_rx_buf_size(int v) { mgos_config_set_rpc_uart_rx_buf_size(&mgos_sys_config, v); }

/* rpc.uart.tx_buf_size */
#define MGOS_CONFIG_HAVE_RPC_UART_TX_BUF_SIZE
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_TX_BUF_SIZE
int mgos_config_get_rpc_uart_tx_buf_size(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_tx_buf_size(void);
static inline int mgos_sys_config_get_rpc_uart_tx_buf_size(void) { return mgos_config_get_rpc_uart_tx_buf_size(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_tx_buf_size(void) { return mgos_config_get_default_rpc_uart_tx_buf_size(); }
void mgos_config_set_rpc_uart_tx_buf_size(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_tx_buf_size(int v) { mgos_config_set_rpc_uart_tx_buf_size(&mgos_sys_config, v); }

/* wifi */
#define MGOS_CONFIG_HAVE_WIFI
#define MGOS_SYS_CONFIG_HAVE_WIFI
const struct mgos_config_wifi *mgos_config_get_wifi(const struct mgos_config *cfg);
static inline const struct mgos_config_wifi *mgos_sys_config_get_wifi(void) { return mgos_config_get_wifi(&mgos_sys_config); }

/* wifi.ap */
#define MGOS_CONFIG_HAVE_WIFI_AP
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP
const struct mgos_config_wifi_ap *mgos_config_get_wifi_ap(const struct mgos_config *cfg);
static inline const struct mgos_config_wifi_ap *mgos_sys_config_get_wifi_ap(void) { return mgos_config_get_wifi_ap(&mgos_sys_config); }

/* wifi.ap.enable */
#define MGOS_CONFIG_HAVE_WIFI_AP_ENABLE
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_ENABLE
int mgos_config_get_wifi_ap_enable(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_enable(void);
static inline int mgos_sys_config_get_wifi_ap_enable(void) { return mgos_config_get_wifi_ap_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_enable(void) { return mgos_config_get_default_wifi_ap_enable(); }
void mgos_config_set_wifi_ap_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_enable(int v) { mgos_config_set_wifi_ap_enable(&mgos_sys_config, v); }

/* wifi.ap.ssid */
#define MGOS_CONFIG_HAVE_WIFI_AP_SSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_SSID
const char * mgos_config_get_wifi_ap_ssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_ssid(void);
static inline const char * mgos_sys_config_get_wifi_ap_ssid(void) { return mgos_config_get_wifi_ap_ssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_ssid(void) { return mgos_config_get_default_wifi_ap_ssid(); }
void mgos_config_set_wifi_ap_ssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_ssid(const char * v) { mgos_config_set_wifi_ap_ssid(&mgos_sys_config, v); }

/* wifi.ap.pass */
#define MGOS_CONFIG_HAVE_WIFI_AP_PASS
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_PASS
const char * mgos_config_get_wifi_ap_pass(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_pass(void);
static inline const char * mgos_sys_config_get_wifi_ap_pass(void) { return mgos_config_get_wifi_ap_pass(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_pass(void) { return mgos_config_get_default_wifi_ap_pass(); }
void mgos_config_set_wifi_ap_pass(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_pass(const char * v) { mgos_config_set_wifi_ap_pass(&mgos_sys_config, v); }

/* wifi.ap.hidden */
#define MGOS_CONFIG_HAVE_WIFI_AP_HIDDEN
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_HIDDEN
int mgos_config_get_wifi_ap_hidden(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_hidden(void);
static inline int mgos_sys_config_get_wifi_ap_hidden(void) { return mgos_config_get_wifi_ap_hidden(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_hidden(void) { return mgos_config_get_default_wifi_ap_hidden(); }
void mgos_config_set_wifi_ap_hidden(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_hidden(int v) { mgos_config_set_wifi_ap_hidden(&mgos_sys_config, v); }

/* wifi.ap.channel */
#define MGOS_CONFIG_HAVE_WIFI_AP_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_CHANNEL
int mgos_config_get_wifi_ap_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_channel(void);
static inline int mgos_sys_config_get_wifi_ap_channel(void) { return mgos_config_get_wifi_ap_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_channel(void) { return mgos_config_get_default_wifi_ap_channel(); }
void mgos_config_set_wifi_ap_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_channel(int v) { mgos_config_set_wifi_ap_channel(&mgos_sys_config, v); }

/* wifi.ap.max_connections */
#define MGOS_CONFIG_HAVE_WIFI_AP_MAX_CONNECTIONS
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_MAX_CONNECTIONS
int mgos_config_get_wifi_ap_max_connections(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_max_connections(void);
static inline int mgos_sys_config_get_wifi_ap_max_connections(void) { return mgos_config_get_wifi_ap_max_connections(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_max_connections(void) { return mgos_config_get_default_wifi_ap_max_connections(); }
void mgos_config_set_wifi_ap_max_connections(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_max_connections(int v) { mgos_config_set_wifi_ap_max_connections(&mgos_sys_config, v); }

/* wifi.ap.ip */
#define MGOS_CONFIG_HAVE_WIFI_AP_IP
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_IP
const char * mgos_config_get_wifi_ap_ip(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_ip(void);
static inline const char * mgos_sys_config_get_wifi_ap_ip(void) { return mgos_config_get_wifi_ap_ip(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_ip(void) { return mgos_config_get_default_wifi_ap_ip(); }
void mgos_config_set_wifi_ap_ip(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_ip(const char * v) { mgos_config_set_wifi_ap_ip(&mgos_sys_config, v); }

/* wifi.ap.netmask */
#define MGOS_CONFIG_HAVE_WIFI_AP_NETMASK
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_NETMASK
const char * mgos_config_get_wifi_ap_netmask(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_netmask(void);
static inline const char * mgos_sys_config_get_wifi_ap_netmask(void) { return mgos_config_get_wifi_ap_netmask(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_netmask(void) { return mgos_config_get_default_wifi_ap_netmask(); }
void mgos_config_set_wifi_ap_netmask(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_netmask(const char * v) { mgos_config_set_wifi_ap_netmask(&mgos_sys_config, v); }

/* wifi.ap.gw */
#define MGOS_CONFIG_HAVE_WIFI_AP_GW
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_GW
const char * mgos_config_get_wifi_ap_gw(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_gw(void);
static inline const char * mgos_sys_config_get_wifi_ap_gw(void) { return mgos_config_get_wifi_ap_gw(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_gw(void) { return mgos_config_get_default_wifi_ap_gw(); }
void mgos_config_set_wifi_ap_gw(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_gw(const char * v) { mgos_config_set_wifi_ap_gw(&mgos_sys_config, v); }

/* wifi.ap.dhcp_start */
#define MGOS_CONFIG_HAVE_WIFI_AP_DHCP_START
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_DHCP_START
const char * mgos_config_get_wifi_ap_dhcp_start(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_dhcp_start(void);
static inline const char * mgos_sys_config_get_wifi_ap_dhcp_start(void) { return mgos_config_get_wifi_ap_dhcp_start(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_dhcp_start(void) { return mgos_config_get_default_wifi_ap_dhcp_start(); }
void mgos_config_set_wifi_ap_dhcp_start(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_dhcp_start(const char * v) { mgos_config_set_wifi_ap_dhcp_start(&mgos_sys_config, v); }

/* wifi.ap.dhcp_end */
#define MGOS_CONFIG_HAVE_WIFI_AP_DHCP_END
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_DHCP_END
const char * mgos_config_get_wifi_ap_dhcp_end(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_dhcp_end(void);
static inline const char * mgos_sys_config_get_wifi_ap_dhcp_end(void) { return mgos_config_get_wifi_ap_dhcp_end(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_dhcp_end(void) { return mgos_config_get_default_wifi_ap_dhcp_end(); }
void mgos_config_set_wifi_ap_dhcp_end(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_dhcp_end(const char * v) { mgos_config_set_wifi_ap_dhcp_end(&mgos_sys_config, v); }

/* wifi.ap.trigger_on_gpio */
#define MGOS_CONFIG_HAVE_WIFI_AP_TRIGGER_ON_GPIO
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_TRIGGER_ON_GPIO
int mgos_config_get_wifi_ap_trigger_on_gpio(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_trigger_on_gpio(void);
static inline int mgos_sys_config_get_wifi_ap_trigger_on_gpio(void) { return mgos_config_get_wifi_ap_trigger_on_gpio(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_trigger_on_gpio(void) { return mgos_config_get_default_wifi_ap_trigger_on_gpio(); }
void mgos_config_set_wifi_ap_trigger_on_gpio(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_trigger_on_gpio(int v) { mgos_config_set_wifi_ap_trigger_on_gpio(&mgos_sys_config, v); }

/* wifi.ap.disable_after */
#define MGOS_CONFIG_HAVE_WIFI_AP_DISABLE_AFTER
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_DISABLE_AFTER
int mgos_config_get_wifi_ap_disable_after(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_disable_after(void);
static inline int mgos_sys_config_get_wifi_ap_disable_after(void) { return mgos_config_get_wifi_ap_disable_after(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_disable_after(void) { return mgos_config_get_default_wifi_ap_disable_after(); }
void mgos_config_set_wifi_ap_disable_after(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_disable_after(int v) { mgos_config_set_wifi_ap_disable_after(&mgos_sys_config, v); }

/* wifi.ap.hostname */
#define MGOS_CONFIG_HAVE_WIFI_AP_HOSTNAME
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_HOSTNAME
const char * mgos_config_get_wifi_ap_hostname(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_hostname(void);
static inline const char * mgos_sys_config_get_wifi_ap_hostname(void) { return mgos_config_get_wifi_ap_hostname(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_hostname(void) { return mgos_config_get_default_wifi_ap_hostname(); }
void mgos_config_set_wifi_ap_hostname(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_hostname(const char * v) { mgos_config_set_wifi_ap_hostname(&mgos_sys_config, v); }

/* wifi.ap.bandwidth_20mhz */
#define MGOS_CONFIG_HAVE_WIFI_AP_BANDWIDTH_20MHZ
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_BANDWIDTH_20MHZ
int mgos_config_get_wifi_ap_bandwidth_20mhz(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_ap_bandwidth_20mhz(void);
static inline int mgos_sys_config_get_wifi_ap_bandwidth_20mhz(void) { return mgos_config_get_wifi_ap_bandwidth_20mhz(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_ap_bandwidth_20mhz(void) { return mgos_config_get_default_wifi_ap_bandwidth_20mhz(); }
void mgos_config_set_wifi_ap_bandwidth_20mhz(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_ap_bandwidth_20mhz(int v) { mgos_config_set_wifi_ap_bandwidth_20mhz(&mgos_sys_config, v); }

/* wifi.ap.protocol */
#define MGOS_CONFIG_HAVE_WIFI_AP_PROTOCOL
#define MGOS_SYS_CONFIG_HAVE_WIFI_AP_PROTOCOL
const char * mgos_config_get_wifi_ap_protocol(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_ap_protocol(void);
static inline const char * mgos_sys_config_get_wifi_ap_protocol(void) { return mgos_config_get_wifi_ap_protocol(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_ap_protocol(void) { return mgos_config_get_default_wifi_ap_protocol(); }
void mgos_config_set_wifi_ap_protocol(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_ap_protocol(const char * v) { mgos_config_set_wifi_ap_protocol(&mgos_sys_config, v); }

/* wifi.sta */
#define MGOS_CONFIG_HAVE_WIFI_STA
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta(const struct mgos_config *cfg);
static inline const struct mgos_config_wifi_sta *mgos_sys_config_get_wifi_sta(void) { return mgos_config_get_wifi_sta(&mgos_sys_config); }

/* wifi.sta.enable */
#define MGOS_CONFIG_HAVE_WIFI_STA_ENABLE
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_ENABLE
int mgos_config_get_wifi_sta_enable(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_enable(void);
static inline int mgos_sys_config_get_wifi_sta_enable(void) { return mgos_config_get_wifi_sta_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_enable(void) { return mgos_config_get_default_wifi_sta_enable(); }
void mgos_config_set_wifi_sta_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_enable(int v) { mgos_config_set_wifi_sta_enable(&mgos_sys_config, v); }

/* wifi.sta.ssid */
#define MGOS_CONFIG_HAVE_WIFI_STA_SSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_SSID
const char * mgos_config_get_wifi_sta_ssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_ssid(void);
static inline const char * mgos_sys_config_get_wifi_sta_ssid(void) { return mgos_config_get_wifi_sta_ssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_ssid(void) { return mgos_config_get_default_wifi_sta_ssid(); }
void mgos_config_set_wifi_sta_ssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_ssid(const char * v) { mgos_config_set_wifi_sta_ssid(&mgos_sys_config, v); }

/* wifi.sta.pass */
#define MGOS_CONFIG_HAVE_WIFI_STA_PASS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_PASS
const char * mgos_config_get_wifi_sta_pass(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_pass(void);
static inline const char * mgos_sys_config_get_wifi_sta_pass(void) { return mgos_config_get_wifi_sta_pass(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_pass(void) { return mgos_config_get_default_wifi_sta_pass(); }
void mgos_config_set_wifi_sta_pass(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_pass(const char * v) { mgos_config_set_wifi_sta_pass(&mgos_sys_config, v); }

/* wifi.sta.bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_BSSID
const char * mgos_config_get_wifi_sta_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta_bssid(void) { return mgos_config_get_wifi_sta_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_bssid(void) { return mgos_config_get_default_wifi_sta_bssid(); }
void mgos_config_set_wifi_sta_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_bssid(const char * v) { mgos_config_set_wifi_sta_bssid(&mgos_sys_config, v); }

/* wifi.sta.channel */
#define MGOS_CONFIG_HAVE_WIFI_STA_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_CHANNEL
int mgos_config_get_wifi_sta_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_channel(void);
static inline int mgos_sys_config_get_wifi_sta_channel(void) { return mgos_config_get_wifi_sta_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_channel(void) { return mgos_config_get_default_wifi_sta_channel(); }
void mgos_config_set_wifi_sta_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_channel(int v) { mgos_config_set_wifi_sta_channel(&mgos_sys_config, v); }

/* wifi.sta.last_bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA_LAST_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_LAST_BSSID
const char * mgos_config_get_wifi_sta_last_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_last_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta_last_bssid(void) { return mgos_config_get_wifi_sta_last_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_last_bssid(void) { return mgos_config_get_default_wifi_sta_last_bssid(); }
void mgos_config_set_wifi_sta_last_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_last_bssid(const char * v) { mgos_config_set_wifi_sta_last_bssid(&mgos_sys_config, v); }

/* wifi.sta.last_channel */
#define MGOS_CONFIG_HAVE_WIFI_STA_LAST_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_LAST_CHANNEL
int mgos_config_get_wifi_sta_last_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_last_channel(void);
static inline int mgos_sys_config_get_wifi_sta_last_channel(void) { return mgos_config_get_wifi_sta_last_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_last_channel(void) { return mgos_config_get_default_wifi_sta_last_channel(); }
void mgos_config_set_wifi_sta_last_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_last_channel(int v) { mgos_config_set_wifi_sta_last_channel(&mgos_sys_config, v); }

/* wifi.sta.user */
#define MGOS_CONFIG_HAVE_WIFI_STA_USER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_USER
const char * mgos_config_get_wifi_sta_user(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_user(void);
static inline const char * mgos_sys_config_get_wifi_sta_user(void) { return mgos_config_get_wifi_sta_user(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_user(void) { return mgos_config_get_default_wifi_sta_user(); }
void mgos_config_set_wifi_sta_user(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_user(const char * v) { mgos_config_set_wifi_sta_user(&mgos_sys_config, v); }

/* wifi.sta.anon_identity */
#define MGOS_CONFIG_HAVE_WIFI_STA_ANON_IDENTITY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_ANON_IDENTITY
const char * mgos_config_get_wifi_sta_anon_identity(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_anon_identity(void);
static inline const char * mgos_sys_config_get_wifi_sta_anon_identity(void) { return mgos_config_get_wifi_sta_anon_identity(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_anon_identity(void) { return mgos_config_get_default_wifi_sta_anon_identity(); }
void mgos_config_set_wifi_sta_anon_identity(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_anon_identity(const char * v) { mgos_config_set_wifi_sta_anon_identity(&mgos_sys_config, v); }

/* wifi.sta.cert */
#define MGOS_CONFIG_HAVE_WIFI_STA_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_CERT
const char * mgos_config_get_wifi_sta_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta_cert(void) { return mgos_config_get_wifi_sta_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_cert(void) { return mgos_config_get_default_wifi_sta_cert(); }
void mgos_config_set_wifi_sta_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_cert(const char * v) { mgos_config_set_wifi_sta_cert(&mgos_sys_config, v); }

/* wifi.sta.key */
#define MGOS_CONFIG_HAVE_WIFI_STA_KEY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_KEY
const char * mgos_config_get_wifi_sta_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_key(void);
static inline const char * mgos_sys_config_get_wifi_sta_key(void) { return mgos_config_get_wifi_sta_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_key(void) { return mgos_config_get_default_wifi_sta_key(); }
void mgos_config_set_wifi_sta_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_key(const char * v) { mgos_config_set_wifi_sta_key(&mgos_sys_config, v); }

/* wifi.sta.ca_cert */
#define MGOS_CONFIG_HAVE_WIFI_STA_CA_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_CA_CERT
const char * mgos_config_get_wifi_sta_ca_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_ca_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta_ca_cert(void) { return mgos_config_get_wifi_sta_ca_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_ca_cert(void) { return mgos_config_get_default_wifi_sta_ca_cert(); }
void mgos_config_set_wifi_sta_ca_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_ca_cert(const char * v) { mgos_config_set_wifi_sta_ca_cert(&mgos_sys_config, v); }

/* wifi.sta.ip */
#define MGOS_CONFIG_HAVE_WIFI_STA_IP
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_IP
const char * mgos_config_get_wifi_sta_ip(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_ip(void);
static inline const char * mgos_sys_config_get_wifi_sta_ip(void) { return mgos_config_get_wifi_sta_ip(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_ip(void) { return mgos_config_get_default_wifi_sta_ip(); }
void mgos_config_set_wifi_sta_ip(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_ip(const char * v) { mgos_config_set_wifi_sta_ip(&mgos_sys_config, v); }

/* wifi.sta.netmask */
#define MGOS_CONFIG_HAVE_WIFI_STA_NETMASK
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_NETMASK
const char * mgos_config_get_wifi_sta_netmask(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_netmask(void);
static inline const char * mgos_sys_config_get_wifi_sta_netmask(void) { return mgos_config_get_wifi_sta_netmask(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_netmask(void) { return mgos_config_get_default_wifi_sta_netmask(); }
void mgos_config_set_wifi_sta_netmask(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_netmask(const char * v) { mgos_config_set_wifi_sta_netmask(&mgos_sys_config, v); }

/* wifi.sta.gw */
#define MGOS_CONFIG_HAVE_WIFI_STA_GW
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_GW
const char * mgos_config_get_wifi_sta_gw(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_gw(void);
static inline const char * mgos_sys_config_get_wifi_sta_gw(void) { return mgos_config_get_wifi_sta_gw(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_gw(void) { return mgos_config_get_default_wifi_sta_gw(); }
void mgos_config_set_wifi_sta_gw(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_gw(const char * v) { mgos_config_set_wifi_sta_gw(&mgos_sys_config, v); }

/* wifi.sta.nameserver */
#define MGOS_CONFIG_HAVE_WIFI_STA_NAMESERVER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_NAMESERVER
const char * mgos_config_get_wifi_sta_nameserver(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_nameserver(void);
static inline const char * mgos_sys_config_get_wifi_sta_nameserver(void) { return mgos_config_get_wifi_sta_nameserver(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_nameserver(void) { return mgos_config_get_default_wifi_sta_nameserver(); }
void mgos_config_set_wifi_sta_nameserver(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_nameserver(const char * v) { mgos_config_set_wifi_sta_nameserver(&mgos_sys_config, v); }

/* wifi.sta.dhcp_hostname */
#define MGOS_CONFIG_HAVE_WIFI_STA_DHCP_HOSTNAME
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_DHCP_HOSTNAME
const char * mgos_config_get_wifi_sta_dhcp_hostname(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_dhcp_hostname(void);
static inline const char * mgos_sys_config_get_wifi_sta_dhcp_hostname(void) { return mgos_config_get_wifi_sta_dhcp_hostname(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_dhcp_hostname(void) { return mgos_config_get_default_wifi_sta_dhcp_hostname(); }
void mgos_config_set_wifi_sta_dhcp_hostname(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_dhcp_hostname(const char * v) { mgos_config_set_wifi_sta_dhcp_hostname(&mgos_sys_config, v); }

/* wifi.sta.protocol */
#define MGOS_CONFIG_HAVE_WIFI_STA_PROTOCOL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_PROTOCOL
const char * mgos_config_get_wifi_sta_protocol(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta_protocol(void);
static inline const char * mgos_sys_config_get_wifi_sta_protocol(void) { return mgos_config_get_wifi_sta_protocol(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta_protocol(void) { return mgos_config_get_default_wifi_sta_protocol(); }
void mgos_config_set_wifi_sta_protocol(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta_protocol(const char * v) { mgos_config_set_wifi_sta_protocol(&mgos_sys_config, v); }

/* wifi.sta.listen_interval_ms */
#define MGOS_CONFIG_HAVE_WIFI_STA_LISTEN_INTERVAL_MS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_LISTEN_INTERVAL_MS
int mgos_config_get_wifi_sta_listen_interval_ms(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_listen_interval_ms(void);
static inline int mgos_sys_config_get_wifi_sta_listen_interval_ms(void) { return mgos_config_get_wifi_sta_listen_interval_ms(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_listen_interval_ms(void) { return mgos_config_get_default_wifi_sta_listen_interval_ms(); }
void mgos_config_set_wifi_sta_listen_interval_ms(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_listen_interval_ms(int v) { mgos_config_set_wifi_sta_listen_interval_ms(&mgos_sys_config, v); }

/* wifi.sta1 */
#define MGOS_CONFIG_HAVE_WIFI_STA1
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta1(const struct mgos_config *cfg);
static inline const struct mgos_config_wifi_sta *mgos_sys_config_get_wifi_sta1(void) { return mgos_config_get_wifi_sta1(&mgos_sys_config); }

/* wifi.sta1.enable */
#define MGOS_CONFIG_HAVE_WIFI_STA1_ENABLE
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_ENABLE
int mgos_config_get_wifi_sta1_enable(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta1_enable(void);
static inline int mgos_sys_config_get_wifi_sta1_enable(void) { return mgos_config_get_wifi_sta1_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta1_enable(void) { return mgos_config_get_default_wifi_sta1_enable(); }
void mgos_config_set_wifi_sta1_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta1_enable(int v) { mgos_config_set_wifi_sta1_enable(&mgos_sys_config, v); }

/* wifi.sta1.ssid */
#define MGOS_CONFIG_HAVE_WIFI_STA1_SSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_SSID
const char * mgos_config_get_wifi_sta1_ssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_ssid(void);
static inline const char * mgos_sys_config_get_wifi_sta1_ssid(void) { return mgos_config_get_wifi_sta1_ssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_ssid(void) { return mgos_config_get_default_wifi_sta1_ssid(); }
void mgos_config_set_wifi_sta1_ssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_ssid(const char * v) { mgos_config_set_wifi_sta1_ssid(&mgos_sys_config, v); }

/* wifi.sta1.pass */
#define MGOS_CONFIG_HAVE_WIFI_STA1_PASS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_PASS
const char * mgos_config_get_wifi_sta1_pass(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_pass(void);
static inline const char * mgos_sys_config_get_wifi_sta1_pass(void) { return mgos_config_get_wifi_sta1_pass(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_pass(void) { return mgos_config_get_default_wifi_sta1_pass(); }
void mgos_config_set_wifi_sta1_pass(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_pass(const char * v) { mgos_config_set_wifi_sta1_pass(&mgos_sys_config, v); }

/* wifi.sta1.bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA1_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_BSSID
const char * mgos_config_get_wifi_sta1_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta1_bssid(void) { return mgos_config_get_wifi_sta1_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_bssid(void) { return mgos_config_get_default_wifi_sta1_bssid(); }
void mgos_config_set_wifi_sta1_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_bssid(const char * v) { mgos_config_set_wifi_sta1_bssid(&mgos_sys_config, v); }

/* wifi.sta1.channel */
#define MGOS_CONFIG_HAVE_WIFI_STA1_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_CHANNEL
int mgos_config_get_wifi_sta1_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta1_channel(void);
static inline int mgos_sys_config_get_wifi_sta1_channel(void) { return mgos_config_get_wifi_sta1_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta1_channel(void) { return mgos_config_get_default_wifi_sta1_channel(); }
void mgos_config_set_wifi_sta1_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta1_channel(int v) { mgos_config_set_wifi_sta1_channel(&mgos_sys_config, v); }

/* wifi.sta1.last_bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA1_LAST_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_LAST_BSSID
const char * mgos_config_get_wifi_sta1_last_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_last_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta1_last_bssid(void) { return mgos_config_get_wifi_sta1_last_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_last_bssid(void) { return mgos_config_get_default_wifi_sta1_last_bssid(); }
void mgos_config_set_wifi_sta1_last_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_last_bssid(const char * v) { mgos_config_set_wifi_sta1_last_bssid(&mgos_sys_config, v); }

/* wifi.sta1.last_channel */
#define MGOS_CONFIG_HAVE_WIFI_STA1_LAST_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_LAST_CHANNEL
int mgos_config_get_wifi_sta1_last_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta1_last_channel(void);
static inline int mgos_sys_config_get_wifi_sta1_last_channel(void) { return mgos_config_get_wifi_sta1_last_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta1_last_channel(void) { return mgos_config_get_default_wifi_sta1_last_channel(); }
void mgos_config_set_wifi_sta1_last_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta1_last_channel(int v) { mgos_config_set_wifi_sta1_last_channel(&mgos_sys_config, v); }

/* wifi.sta1.user */
#define MGOS_CONFIG_HAVE_WIFI_STA1_USER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_USER
const char * mgos_config_get_wifi_sta1_user(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_user(void);
static inline const char * mgos_sys_config_get_wifi_sta1_user(void) { return mgos_config_get_wifi_sta1_user(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_user(void) { return mgos_config_get_default_wifi_sta1_user(); }
void mgos_config_set_wifi_sta1_user(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_user(const char * v) { mgos_config_set_wifi_sta1_user(&mgos_sys_config, v); }

/* wifi.sta1.anon_identity */
#define MGOS_CONFIG_HAVE_WIFI_STA1_ANON_IDENTITY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_ANON_IDENTITY
const char * mgos_config_get_wifi_sta1_anon_identity(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_anon_identity(void);
static inline const char * mgos_sys_config_get_wifi_sta1_anon_identity(void) { return mgos_config_get_wifi_sta1_anon_identity(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_anon_identity(void) { return mgos_config_get_default_wifi_sta1_anon_identity(); }
void mgos_config_set_wifi_sta1_anon_identity(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_anon_identity(const char * v) { mgos_config_set_wifi_sta1_anon_identity(&mgos_sys_config, v); }

/* wifi.sta1.cert */
#define MGOS_CONFIG_HAVE_WIFI_STA1_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_CERT
const char * mgos_config_get_wifi_sta1_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta1_cert(void) { return mgos_config_get_wifi_sta1_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_cert(void) { return mgos_config_get_default_wifi_sta1_cert(); }
void mgos_config_set_wifi_sta1_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_cert(const char * v) { mgos_config_set_wifi_sta1_cert(&mgos_sys_config, v); }

/* wifi.sta1.key */
#define MGOS_CONFIG_HAVE_WIFI_STA1_KEY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_KEY
const char * mgos_config_get_wifi_sta1_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_key(void);
static inline const char * mgos_sys_config_get_wifi_sta1_key(void) { return mgos_config_get_wifi_sta1_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_key(void) { return mgos_config_get_default_wifi_sta1_key(); }
void mgos_config_set_wifi_sta1_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_key(const char * v) { mgos_config_set_wifi_sta1_key(&mgos_sys_config, v); }

/* wifi.sta1.ca_cert */
#define MGOS_CONFIG_HAVE_WIFI_STA1_CA_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_CA_CERT
const char * mgos_config_get_wifi_sta1_ca_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_ca_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta1_ca_cert(void) { return mgos_config_get_wifi_sta1_ca_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_ca_cert(void) { return mgos_config_get_default_wifi_sta1_ca_cert(); }
void mgos_config_set_wifi_sta1_ca_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_ca_cert(const char * v) { mgos_config_set_wifi_sta1_ca_cert(&mgos_sys_config, v); }

/* wifi.sta1.ip */
#define MGOS_CONFIG_HAVE_WIFI_STA1_IP
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_IP
const char * mgos_config_get_wifi_sta1_ip(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_ip(void);
static inline const char * mgos_sys_config_get_wifi_sta1_ip(void) { return mgos_config_get_wifi_sta1_ip(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_ip(void) { return mgos_config_get_default_wifi_sta1_ip(); }
void mgos_config_set_wifi_sta1_ip(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_ip(const char * v) { mgos_config_set_wifi_sta1_ip(&mgos_sys_config, v); }

/* wifi.sta1.netmask */
#define MGOS_CONFIG_HAVE_WIFI_STA1_NETMASK
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_NETMASK
const char * mgos_config_get_wifi_sta1_netmask(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_netmask(void);
static inline const char * mgos_sys_config_get_wifi_sta1_netmask(void) { return mgos_config_get_wifi_sta1_netmask(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_netmask(void) { return mgos_config_get_default_wifi_sta1_netmask(); }
void mgos_config_set_wifi_sta1_netmask(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_netmask(const char * v) { mgos_config_set_wifi_sta1_netmask(&mgos_sys_config, v); }

/* wifi.sta1.gw */
#define MGOS_CONFIG_HAVE_WIFI_STA1_GW
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_GW
const char * mgos_config_get_wifi_sta1_gw(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_gw(void);
static inline const char * mgos_sys_config_get_wifi_sta1_gw(void) { return mgos_config_get_wifi_sta1_gw(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_gw(void) { return mgos_config_get_default_wifi_sta1_gw(); }
void mgos_config_set_wifi_sta1_gw(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_gw(const char * v) { mgos_config_set_wifi_sta1_gw(&mgos_sys_config, v); }

/* wifi.sta1.nameserver */
#define MGOS_CONFIG_HAVE_WIFI_STA1_NAMESERVER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_NAMESERVER
const char * mgos_config_get_wifi_sta1_nameserver(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_nameserver(void);
static inline const char * mgos_sys_config_get_wifi_sta1_nameserver(void) { return mgos_config_get_wifi_sta1_nameserver(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_nameserver(void) { return mgos_config_get_default_wifi_sta1_nameserver(); }
void mgos_config_set_wifi_sta1_nameserver(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_nameserver(const char * v) { mgos_config_set_wifi_sta1_nameserver(&mgos_sys_config, v); }

/* wifi.sta1.dhcp_hostname */
#define MGOS_CONFIG_HAVE_WIFI_STA1_DHCP_HOSTNAME
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_DHCP_HOSTNAME
const char * mgos_config_get_wifi_sta1_dhcp_hostname(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_dhcp_hostname(void);
static inline const char * mgos_sys_config_get_wifi_sta1_dhcp_hostname(void) { return mgos_config_get_wifi_sta1_dhcp_hostname(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_dhcp_hostname(void) { return mgos_config_get_default_wifi_sta1_dhcp_hostname(); }
void mgos_config_set_wifi_sta1_dhcp_hostname(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_dhcp_hostname(const char * v) { mgos_config_set_wifi_sta1_dhcp_hostname(&mgos_sys_config, v); }

/* wifi.sta1.protocol */
#define MGOS_CONFIG_HAVE_WIFI_STA1_PROTOCOL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_PROTOCOL
const char * mgos_config_get_wifi_sta1_protocol(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta1_protocol(void);
static inline const char * mgos_sys_config_get_wifi_sta1_protocol(void) { return mgos_config_get_wifi_sta1_protocol(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta1_protocol(void) { return mgos_config_get_default_wifi_sta1_protocol(); }
void mgos_config_set_wifi_sta1_protocol(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta1_protocol(const char * v) { mgos_config_set_wifi_sta1_protocol(&mgos_sys_config, v); }

/* wifi.sta1.listen_interval_ms */
#define MGOS_CONFIG_HAVE_WIFI_STA1_LISTEN_INTERVAL_MS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA1_LISTEN_INTERVAL_MS
int mgos_config_get_wifi_sta1_listen_interval_ms(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta1_listen_interval_ms(void);
static inline int mgos_sys_config_get_wifi_sta1_listen_interval_ms(void) { return mgos_config_get_wifi_sta1_listen_interval_ms(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta1_listen_interval_ms(void) { return mgos_config_get_default_wifi_sta1_listen_interval_ms(); }
void mgos_config_set_wifi_sta1_listen_interval_ms(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta1_listen_interval_ms(int v) { mgos_config_set_wifi_sta1_listen_interval_ms(&mgos_sys_config, v); }

/* wifi.sta2 */
#define MGOS_CONFIG_HAVE_WIFI_STA2
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta2(const struct mgos_config *cfg);
static inline const struct mgos_config_wifi_sta *mgos_sys_config_get_wifi_sta2(void) { return mgos_config_get_wifi_sta2(&mgos_sys_config); }

/* wifi.sta2.enable */
#define MGOS_CONFIG_HAVE_WIFI_STA2_ENABLE
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_ENABLE
int mgos_config_get_wifi_sta2_enable(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta2_enable(void);
static inline int mgos_sys_config_get_wifi_sta2_enable(void) { return mgos_config_get_wifi_sta2_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta2_enable(void) { return mgos_config_get_default_wifi_sta2_enable(); }
void mgos_config_set_wifi_sta2_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta2_enable(int v) { mgos_config_set_wifi_sta2_enable(&mgos_sys_config, v); }

/* wifi.sta2.ssid */
#define MGOS_CONFIG_HAVE_WIFI_STA2_SSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_SSID
const char * mgos_config_get_wifi_sta2_ssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_ssid(void);
static inline const char * mgos_sys_config_get_wifi_sta2_ssid(void) { return mgos_config_get_wifi_sta2_ssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_ssid(void) { return mgos_config_get_default_wifi_sta2_ssid(); }
void mgos_config_set_wifi_sta2_ssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_ssid(const char * v) { mgos_config_set_wifi_sta2_ssid(&mgos_sys_config, v); }

/* wifi.sta2.pass */
#define MGOS_CONFIG_HAVE_WIFI_STA2_PASS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_PASS
const char * mgos_config_get_wifi_sta2_pass(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_pass(void);
static inline const char * mgos_sys_config_get_wifi_sta2_pass(void) { return mgos_config_get_wifi_sta2_pass(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_pass(void) { return mgos_config_get_default_wifi_sta2_pass(); }
void mgos_config_set_wifi_sta2_pass(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_pass(const char * v) { mgos_config_set_wifi_sta2_pass(&mgos_sys_config, v); }

/* wifi.sta2.bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA2_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_BSSID
const char * mgos_config_get_wifi_sta2_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta2_bssid(void) { return mgos_config_get_wifi_sta2_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_bssid(void) { return mgos_config_get_default_wifi_sta2_bssid(); }
void mgos_config_set_wifi_sta2_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_bssid(const char * v) { mgos_config_set_wifi_sta2_bssid(&mgos_sys_config, v); }

/* wifi.sta2.channel */
#define MGOS_CONFIG_HAVE_WIFI_STA2_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_CHANNEL
int mgos_config_get_wifi_sta2_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta2_channel(void);
static inline int mgos_sys_config_get_wifi_sta2_channel(void) { return mgos_config_get_wifi_sta2_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta2_channel(void) { return mgos_config_get_default_wifi_sta2_channel(); }
void mgos_config_set_wifi_sta2_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta2_channel(int v) { mgos_config_set_wifi_sta2_channel(&mgos_sys_config, v); }

/* wifi.sta2.last_bssid */
#define MGOS_CONFIG_HAVE_WIFI_STA2_LAST_BSSID
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_LAST_BSSID
const char * mgos_config_get_wifi_sta2_last_bssid(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_last_bssid(void);
static inline const char * mgos_sys_config_get_wifi_sta2_last_bssid(void) { return mgos_config_get_wifi_sta2_last_bssid(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_last_bssid(void) { return mgos_config_get_default_wifi_sta2_last_bssid(); }
void mgos_config_set_wifi_sta2_last_bssid(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_last_bssid(const char * v) { mgos_config_set_wifi_sta2_last_bssid(&mgos_sys_config, v); }

/* wifi.sta2.last_channel */
#define MGOS_CONFIG_HAVE_WIFI_STA2_LAST_CHANNEL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_LAST_CHANNEL
int mgos_config_get_wifi_sta2_last_channel(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta2_last_channel(void);
static inline int mgos_sys_config_get_wifi_sta2_last_channel(void) { return mgos_config_get_wifi_sta2_last_channel(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta2_last_channel(void) { return mgos_config_get_default_wifi_sta2_last_channel(); }
void mgos_config_set_wifi_sta2_last_channel(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta2_last_channel(int v) { mgos_config_set_wifi_sta2_last_channel(&mgos_sys_config, v); }

/* wifi.sta2.user */
#define MGOS_CONFIG_HAVE_WIFI_STA2_USER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_USER
const char * mgos_config_get_wifi_sta2_user(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_user(void);
static inline const char * mgos_sys_config_get_wifi_sta2_user(void) { return mgos_config_get_wifi_sta2_user(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_user(void) { return mgos_config_get_default_wifi_sta2_user(); }
void mgos_config_set_wifi_sta2_user(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_user(const char * v) { mgos_config_set_wifi_sta2_user(&mgos_sys_config, v); }

/* wifi.sta2.anon_identity */
#define MGOS_CONFIG_HAVE_WIFI_STA2_ANON_IDENTITY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_ANON_IDENTITY
const char * mgos_config_get_wifi_sta2_anon_identity(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_anon_identity(void);
static inline const char * mgos_sys_config_get_wifi_sta2_anon_identity(void) { return mgos_config_get_wifi_sta2_anon_identity(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_anon_identity(void) { return mgos_config_get_default_wifi_sta2_anon_identity(); }
void mgos_config_set_wifi_sta2_anon_identity(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_anon_identity(const char * v) { mgos_config_set_wifi_sta2_anon_identity(&mgos_sys_config, v); }

/* wifi.sta2.cert */
#define MGOS_CONFIG_HAVE_WIFI_STA2_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_CERT
const char * mgos_config_get_wifi_sta2_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta2_cert(void) { return mgos_config_get_wifi_sta2_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_cert(void) { return mgos_config_get_default_wifi_sta2_cert(); }
void mgos_config_set_wifi_sta2_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_cert(const char * v) { mgos_config_set_wifi_sta2_cert(&mgos_sys_config, v); }

/* wifi.sta2.key */
#define MGOS_CONFIG_HAVE_WIFI_STA2_KEY
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_KEY
const char * mgos_config_get_wifi_sta2_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_key(void);
static inline const char * mgos_sys_config_get_wifi_sta2_key(void) { return mgos_config_get_wifi_sta2_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_key(void) { return mgos_config_get_default_wifi_sta2_key(); }
void mgos_config_set_wifi_sta2_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_key(const char * v) { mgos_config_set_wifi_sta2_key(&mgos_sys_config, v); }

/* wifi.sta2.ca_cert */
#define MGOS_CONFIG_HAVE_WIFI_STA2_CA_CERT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_CA_CERT
const char * mgos_config_get_wifi_sta2_ca_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_ca_cert(void);
static inline const char * mgos_sys_config_get_wifi_sta2_ca_cert(void) { return mgos_config_get_wifi_sta2_ca_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_ca_cert(void) { return mgos_config_get_default_wifi_sta2_ca_cert(); }
void mgos_config_set_wifi_sta2_ca_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_ca_cert(const char * v) { mgos_config_set_wifi_sta2_ca_cert(&mgos_sys_config, v); }

/* wifi.sta2.ip */
#define MGOS_CONFIG_HAVE_WIFI_STA2_IP
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_IP
const char * mgos_config_get_wifi_sta2_ip(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_ip(void);
static inline const char * mgos_sys_config_get_wifi_sta2_ip(void) { return mgos_config_get_wifi_sta2_ip(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_ip(void) { return mgos_config_get_default_wifi_sta2_ip(); }
void mgos_config_set_wifi_sta2_ip(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_ip(const char * v) { mgos_config_set_wifi_sta2_ip(&mgos_sys_config, v); }

/* wifi.sta2.netmask */
#define MGOS_CONFIG_HAVE_WIFI_STA2_NETMASK
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_NETMASK
const char * mgos_config_get_wifi_sta2_netmask(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_netmask(void);
static inline const char * mgos_sys_config_get_wifi_sta2_netmask(void) { return mgos_config_get_wifi_sta2_netmask(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_netmask(void) { return mgos_config_get_default_wifi_sta2_netmask(); }
void mgos_config_set_wifi_sta2_netmask(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_netmask(const char * v) { mgos_config_set_wifi_sta2_netmask(&mgos_sys_config, v); }

/* wifi.sta2.gw */
#define MGOS_CONFIG_HAVE_WIFI_STA2_GW
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_GW
const char * mgos_config_get_wifi_sta2_gw(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_gw(void);
static inline const char * mgos_sys_config_get_wifi_sta2_gw(void) { return mgos_config_get_wifi_sta2_gw(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_gw(void) { return mgos_config_get_default_wifi_sta2_gw(); }
void mgos_config_set_wifi_sta2_gw(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_gw(const char * v) { mgos_config_set_wifi_sta2_gw(&mgos_sys_config, v); }

/* wifi.sta2.nameserver */
#define MGOS_CONFIG_HAVE_WIFI_STA2_NAMESERVER
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_NAMESERVER
const char * mgos_config_get_wifi_sta2_nameserver(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_nameserver(void);
static inline const char * mgos_sys_config_get_wifi_sta2_nameserver(void) { return mgos_config_get_wifi_sta2_nameserver(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_nameserver(void) { return mgos_config_get_default_wifi_sta2_nameserver(); }
void mgos_config_set_wifi_sta2_nameserver(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_nameserver(const char * v) { mgos_config_set_wifi_sta2_nameserver(&mgos_sys_config, v); }

/* wifi.sta2.dhcp_hostname */
#define MGOS_CONFIG_HAVE_WIFI_STA2_DHCP_HOSTNAME
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_DHCP_HOSTNAME
const char * mgos_config_get_wifi_sta2_dhcp_hostname(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_dhcp_hostname(void);
static inline const char * mgos_sys_config_get_wifi_sta2_dhcp_hostname(void) { return mgos_config_get_wifi_sta2_dhcp_hostname(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_dhcp_hostname(void) { return mgos_config_get_default_wifi_sta2_dhcp_hostname(); }
void mgos_config_set_wifi_sta2_dhcp_hostname(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_dhcp_hostname(const char * v) { mgos_config_set_wifi_sta2_dhcp_hostname(&mgos_sys_config, v); }

/* wifi.sta2.protocol */
#define MGOS_CONFIG_HAVE_WIFI_STA2_PROTOCOL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_PROTOCOL
const char * mgos_config_get_wifi_sta2_protocol(const struct mgos_config *cfg);
const char * mgos_config_get_default_wifi_sta2_protocol(void);
static inline const char * mgos_sys_config_get_wifi_sta2_protocol(void) { return mgos_config_get_wifi_sta2_protocol(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_wifi_sta2_protocol(void) { return mgos_config_get_default_wifi_sta2_protocol(); }
void mgos_config_set_wifi_sta2_protocol(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_wifi_sta2_protocol(const char * v) { mgos_config_set_wifi_sta2_protocol(&mgos_sys_config, v); }

/* wifi.sta2.listen_interval_ms */
#define MGOS_CONFIG_HAVE_WIFI_STA2_LISTEN_INTERVAL_MS
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA2_LISTEN_INTERVAL_MS
int mgos_config_get_wifi_sta2_listen_interval_ms(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta2_listen_interval_ms(void);
static inline int mgos_sys_config_get_wifi_sta2_listen_interval_ms(void) { return mgos_config_get_wifi_sta2_listen_interval_ms(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta2_listen_interval_ms(void) { return mgos_config_get_default_wifi_sta2_listen_interval_ms(); }
void mgos_config_set_wifi_sta2_listen_interval_ms(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta2_listen_interval_ms(int v) { mgos_config_set_wifi_sta2_listen_interval_ms(&mgos_sys_config, v); }

/* wifi.sta_rssi_thr */
#define MGOS_CONFIG_HAVE_WIFI_STA_RSSI_THR
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_RSSI_THR
int mgos_config_get_wifi_sta_rssi_thr(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_rssi_thr(void);
static inline int mgos_sys_config_get_wifi_sta_rssi_thr(void) { return mgos_config_get_wifi_sta_rssi_thr(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_rssi_thr(void) { return mgos_config_get_default_wifi_sta_rssi_thr(); }
void mgos_config_set_wifi_sta_rssi_thr(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_rssi_thr(int v) { mgos_config_set_wifi_sta_rssi_thr(&mgos_sys_config, v); }

/* wifi.sta_connect_timeout */
#define MGOS_CONFIG_HAVE_WIFI_STA_CONNECT_TIMEOUT
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_CONNECT_TIMEOUT
int mgos_config_get_wifi_sta_connect_timeout(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_connect_timeout(void);
static inline int mgos_sys_config_get_wifi_sta_connect_timeout(void) { return mgos_config_get_wifi_sta_connect_timeout(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_connect_timeout(void) { return mgos_config_get_default_wifi_sta_connect_timeout(); }
void mgos_config_set_wifi_sta_connect_timeout(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_connect_timeout(int v) { mgos_config_set_wifi_sta_connect_timeout(&mgos_sys_config, v); }

/* wifi.sta_roam_rssi_thr */
#define MGOS_CONFIG_HAVE_WIFI_STA_ROAM_RSSI_THR
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_ROAM_RSSI_THR
int mgos_config_get_wifi_sta_roam_rssi_thr(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_roam_rssi_thr(void);
static inline int mgos_sys_config_get_wifi_sta_roam_rssi_thr(void) { return mgos_config_get_wifi_sta_roam_rssi_thr(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_roam_rssi_thr(void) { return mgos_config_get_default_wifi_sta_roam_rssi_thr(); }
void mgos_config_set_wifi_sta_roam_rssi_thr(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_roam_rssi_thr(int v) { mgos_config_set_wifi_sta_roam_rssi_thr(&mgos_sys_config, v); }

/* wifi.sta_roam_interval */
#define MGOS_CONFIG_HAVE_WIFI_STA_ROAM_INTERVAL
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_ROAM_INTERVAL
int mgos_config_get_wifi_sta_roam_interval(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_roam_interval(void);
static inline int mgos_sys_config_get_wifi_sta_roam_interval(void) { return mgos_config_get_wifi_sta_roam_interval(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_roam_interval(void) { return mgos_config_get_default_wifi_sta_roam_interval(); }
void mgos_config_set_wifi_sta_roam_interval(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_roam_interval(int v) { mgos_config_set_wifi_sta_roam_interval(&mgos_sys_config, v); }

/* wifi.sta_ps_mode */
#define MGOS_CONFIG_HAVE_WIFI_STA_PS_MODE
#define MGOS_SYS_CONFIG_HAVE_WIFI_STA_PS_MODE
int mgos_config_get_wifi_sta_ps_mode(const struct mgos_config *cfg);
int mgos_config_get_default_wifi_sta_ps_mode(void);
static inline int mgos_sys_config_get_wifi_sta_ps_mode(void) { return mgos_config_get_wifi_sta_ps_mode(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_wifi_sta_ps_mode(void) { return mgos_config_get_default_wifi_sta_ps_mode(); }
void mgos_config_set_wifi_sta_ps_mode(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_wifi_sta_ps_mode(int v) { mgos_config_set_wifi_sta_ps_mode(&mgos_sys_config, v); }

/* sntp */
#define MGOS_CONFIG_HAVE_SNTP
#define MGOS_SYS_CONFIG_HAVE_SNTP
const struct mgos_config_sntp *mgos_config_get_sntp(const struct mgos_config *cfg);
static inline const struct mgos_config_sntp *mgos_sys_config_get_sntp(void) { return mgos_config_get_sntp(&mgos_sys_config); }

/* sntp.enable */
#define MGOS_CONFIG_HAVE_SNTP_ENABLE
#define MGOS_SYS_CONFIG_HAVE_SNTP_ENABLE
int mgos_config_get_sntp_enable(const struct mgos_config *cfg);
int mgos_config_get_default_sntp_enable(void);
static inline int mgos_sys_config_get_sntp_enable(void) { return mgos_config_get_sntp_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sntp_enable(void) { return mgos_config_get_default_sntp_enable(); }
void mgos_config_set_sntp_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sntp_enable(int v) { mgos_config_set_sntp_enable(&mgos_sys_config, v); }

/* sntp.server */
#define MGOS_CONFIG_HAVE_SNTP_SERVER
#define MGOS_SYS_CONFIG_HAVE_SNTP_SERVER
const char * mgos_config_get_sntp_server(const struct mgos_config *cfg);
const char * mgos_config_get_default_sntp_server(void);
static inline const char * mgos_sys_config_get_sntp_server(void) { return mgos_config_get_sntp_server(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sntp_server(void) { return mgos_config_get_default_sntp_server(); }
void mgos_config_set_sntp_server(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sntp_server(const char * v) { mgos_config_set_sntp_server(&mgos_sys_config, v); }

/* sntp.use_dhcp_ntp_server */
#define MGOS_CONFIG_HAVE_SNTP_USE_DHCP_NTP_SERVER
#define MGOS_SYS_CONFIG_HAVE_SNTP_USE_DHCP_NTP_SERVER
int mgos_config_get_sntp_use_dhcp_ntp_server(const struct mgos_config *cfg);
int mgos_config_get_default_sntp_use_dhcp_ntp_server(void);
static inline int mgos_sys_config_get_sntp_use_dhcp_ntp_server(void) { return mgos_config_get_sntp_use_dhcp_ntp_server(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sntp_use_dhcp_ntp_server(void) { return mgos_config_get_default_sntp_use_dhcp_ntp_server(); }
void mgos_config_set_sntp_use_dhcp_ntp_server(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sntp_use_dhcp_ntp_server(int v) { mgos_config_set_sntp_use_dhcp_ntp_server(&mgos_sys_config, v); }

/* sntp.retry_min */
#define MGOS_CONFIG_HAVE_SNTP_RETRY_MIN
#define MGOS_SYS_CONFIG_HAVE_SNTP_RETRY_MIN
int mgos_config_get_sntp_retry_min(const struct mgos_config *cfg);
int mgos_config_get_default_sntp_retry_min(void);
static inline int mgos_sys_config_get_sntp_retry_min(void) { return mgos_config_get_sntp_retry_min(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sntp_retry_min(void) { return mgos_config_get_default_sntp_retry_min(); }
void mgos_config_set_sntp_retry_min(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sntp_retry_min(int v) { mgos_config_set_sntp_retry_min(&mgos_sys_config, v); }

/* sntp.retry_max */
#define MGOS_CONFIG_HAVE_SNTP_RETRY_MAX
#define MGOS_SYS_CONFIG_HAVE_SNTP_RETRY_MAX
int mgos_config_get_sntp_retry_max(const struct mgos_config *cfg);
int mgos_config_get_default_sntp_retry_max(void);
static inline int mgos_sys_config_get_sntp_retry_max(void) { return mgos_config_get_sntp_retry_max(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sntp_retry_max(void) { return mgos_config_get_default_sntp_retry_max(); }
void mgos_config_set_sntp_retry_max(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sntp_retry_max(int v) { mgos_config_set_sntp_retry_max(&mgos_sys_config, v); }

/* sntp.update_interval */
#define MGOS_CONFIG_HAVE_SNTP_UPDATE_INTERVAL
#define MGOS_SYS_CONFIG_HAVE_SNTP_UPDATE_INTERVAL
int mgos_config_get_sntp_update_interval(const struct mgos_config *cfg);
int mgos_config_get_default_sntp_update_interval(void);
static inline int mgos_sys_config_get_sntp_update_interval(void) { return mgos_config_get_sntp_update_interval(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_sntp_update_interval(void) { return mgos_config_get_default_sntp_update_interval(); }
void mgos_config_set_sntp_update_interval(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_sntp_update_interval(int v) { mgos_config_set_sntp_update_interval(&mgos_sys_config, v); }

/* app */
#define MGOS_CONFIG_HAVE_APP
#define MGOS_SYS_CONFIG_HAVE_APP
const struct mgos_config_app *mgos_config_get_app(const struct mgos_config *cfg);
static inline const struct mgos_config_app *mgos_sys_config_get_app(void) { return mgos_config_get_app(&mgos_sys_config); }

/* app.name */
#define MGOS_CONFIG_HAVE_APP_NAME
#define MGOS_SYS_CONFIG_HAVE_APP_NAME
const char * mgos_config_get_app_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_app_name(void);
static inline const char * mgos_sys_config_get_app_name(void) { return mgos_config_get_app_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_app_name(void) { return mgos_config_get_default_app_name(); }
void mgos_config_set_app_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_app_name(const char * v) { mgos_config_set_app_name(&mgos_sys_config, v); }

bool mgos_sys_config_get(const struct mg_str key, struct mg_str *value);
bool mgos_sys_config_set(const struct mg_str key, const struct mg_str value, bool free_strings);

bool mgos_config_is_default_str(const char *s);

/* Backward compatibility. */
const struct mgos_conf_entry *mgos_config_schema(void);

#ifdef __cplusplus
}
#endif
