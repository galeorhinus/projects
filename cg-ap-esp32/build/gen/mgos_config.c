/* clang-format off */
/*
 * Generated file - do not edit.
 * Command: /mongoose-os/tools/mgos_gen_config.py --c_name=mgos_config --c_global_name=mgos_sys_config --dest_dir=/data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_612452169/build/gen/ /mongoose-os/src/mgos_debug_udp_config.yaml /data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_612452169/build/gen/mos_conf_schema.yml
 */

#include "mgos_config.h"

#include <stdbool.h>

#include "common/cs_file.h"

#include "mgos_config_util.h"


/* struct mgos_config */
static const struct mgos_conf_entry mgos_config_schema_[] = {
    {.type = CONF_TYPE_OBJECT, .key = "", .offset = 0, .num_desc = 176},
    {.type = CONF_TYPE_OBJECT, .key = "debug", .offset = offsetof(struct mgos_config, debug), .num_desc = 10},
    {.type = CONF_TYPE_STRING, .key = "udp_log_addr", .offset = offsetof(struct mgos_config, debug.udp_log_addr)},
    {.type = CONF_TYPE_INT, .key = "udp_log_level", .offset = offsetof(struct mgos_config, debug.udp_log_level)},
    {.type = CONF_TYPE_INT, .key = "mbedtls_level", .offset = offsetof(struct mgos_config, debug.mbedtls_level)},
    {.type = CONF_TYPE_INT, .key = "level", .offset = offsetof(struct mgos_config, debug.level)},
    {.type = CONF_TYPE_STRING, .key = "file_level", .offset = offsetof(struct mgos_config, debug.file_level)},
    {.type = CONF_TYPE_INT, .key = "event_level", .offset = offsetof(struct mgos_config, debug.event_level)},
    {.type = CONF_TYPE_INT, .key = "stdout_uart", .offset = offsetof(struct mgos_config, debug.stdout_uart)},
    {.type = CONF_TYPE_INT, .key = "stderr_uart", .offset = offsetof(struct mgos_config, debug.stderr_uart)},
    {.type = CONF_TYPE_INT, .key = "factory_reset_gpio", .offset = offsetof(struct mgos_config, debug.factory_reset_gpio)},
    {.type = CONF_TYPE_STRING, .key = "mg_mgr_hexdump_file", .offset = offsetof(struct mgos_config, debug.mg_mgr_hexdump_file)},
    {.type = CONF_TYPE_OBJECT, .key = "device", .offset = offsetof(struct mgos_config, device), .num_desc = 5},
    {.type = CONF_TYPE_STRING, .key = "id", .offset = offsetof(struct mgos_config, device.id)},
    {.type = CONF_TYPE_STRING, .key = "license", .offset = offsetof(struct mgos_config, device.license)},
    {.type = CONF_TYPE_STRING, .key = "mac", .offset = offsetof(struct mgos_config, device.mac)},
    {.type = CONF_TYPE_STRING, .key = "public_key", .offset = offsetof(struct mgos_config, device.public_key)},
    {.type = CONF_TYPE_STRING, .key = "sn", .offset = offsetof(struct mgos_config, device.sn)},
    {.type = CONF_TYPE_OBJECT, .key = "sys", .offset = offsetof(struct mgos_config, sys), .num_desc = 3},
    {.type = CONF_TYPE_STRING, .key = "tz_spec", .offset = offsetof(struct mgos_config, sys.tz_spec)},
    {.type = CONF_TYPE_INT, .key = "wdt_timeout", .offset = offsetof(struct mgos_config, sys.wdt_timeout)},
    {.type = CONF_TYPE_STRING, .key = "pref_ota_lib", .offset = offsetof(struct mgos_config, sys.pref_ota_lib)},
    {.type = CONF_TYPE_STRING, .key = "conf_acl", .offset = offsetof(struct mgos_config, conf_acl)},
    {.type = CONF_TYPE_OBJECT, .key = "dns_sd", .offset = offsetof(struct mgos_config, dns_sd), .num_desc = 4},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, dns_sd.enable)},
    {.type = CONF_TYPE_BOOL, .key = "adv_only", .offset = offsetof(struct mgos_config, dns_sd.adv_only)},
    {.type = CONF_TYPE_STRING, .key = "host_name", .offset = offsetof(struct mgos_config, dns_sd.host_name)},
    {.type = CONF_TYPE_STRING, .key = "txt", .offset = offsetof(struct mgos_config, dns_sd.txt)},
    {.type = CONF_TYPE_OBJECT, .key = "http", .offset = offsetof(struct mgos_config, http), .num_desc = 13},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, http.enable)},
    {.type = CONF_TYPE_STRING, .key = "listen_addr", .offset = offsetof(struct mgos_config, http.listen_addr)},
    {.type = CONF_TYPE_STRING, .key = "document_root", .offset = offsetof(struct mgos_config, http.document_root)},
    {.type = CONF_TYPE_STRING, .key = "index_files", .offset = offsetof(struct mgos_config, http.index_files)},
    {.type = CONF_TYPE_STRING, .key = "ssl_cert", .offset = offsetof(struct mgos_config, http.ssl_cert)},
    {.type = CONF_TYPE_STRING, .key = "ssl_key", .offset = offsetof(struct mgos_config, http.ssl_key)},
    {.type = CONF_TYPE_STRING, .key = "ssl_ca_cert", .offset = offsetof(struct mgos_config, http.ssl_ca_cert)},
    {.type = CONF_TYPE_STRING, .key = "upload_acl", .offset = offsetof(struct mgos_config, http.upload_acl)},
    {.type = CONF_TYPE_STRING, .key = "hidden_files", .offset = offsetof(struct mgos_config, http.hidden_files)},
    {.type = CONF_TYPE_STRING, .key = "auth_domain", .offset = offsetof(struct mgos_config, http.auth_domain)},
    {.type = CONF_TYPE_STRING, .key = "auth_file", .offset = offsetof(struct mgos_config, http.auth_file)},
    {.type = CONF_TYPE_INT, .key = "auth_algo", .offset = offsetof(struct mgos_config, http.auth_algo)},
    {.type = CONF_TYPE_STRING, .key = "extra_headers", .offset = offsetof(struct mgos_config, http.extra_headers)},
    {.type = CONF_TYPE_OBJECT, .key = "mjs", .offset = offsetof(struct mgos_config, mjs), .num_desc = 1},
    {.type = CONF_TYPE_BOOL, .key = "generate_jsc", .offset = offsetof(struct mgos_config, mjs.generate_jsc)},
    {.type = CONF_TYPE_OBJECT, .key = "update", .offset = offsetof(struct mgos_config, update), .num_desc = 18},
    {.type = CONF_TYPE_INT, .key = "timeout", .offset = offsetof(struct mgos_config, update.timeout)},
    {.type = CONF_TYPE_INT, .key = "commit_timeout", .offset = offsetof(struct mgos_config, update.commit_timeout)},
    {.type = CONF_TYPE_STRING, .key = "key0", .offset = offsetof(struct mgos_config, update.key0)},
    {.type = CONF_TYPE_STRING, .key = "key1", .offset = offsetof(struct mgos_config, update.key1)},
    {.type = CONF_TYPE_STRING, .key = "key2", .offset = offsetof(struct mgos_config, update.key2)},
    {.type = CONF_TYPE_STRING, .key = "key3", .offset = offsetof(struct mgos_config, update.key3)},
    {.type = CONF_TYPE_STRING, .key = "key4", .offset = offsetof(struct mgos_config, update.key4)},
    {.type = CONF_TYPE_STRING, .key = "key5", .offset = offsetof(struct mgos_config, update.key5)},
    {.type = CONF_TYPE_STRING, .key = "key6", .offset = offsetof(struct mgos_config, update.key6)},
    {.type = CONF_TYPE_STRING, .key = "key7", .offset = offsetof(struct mgos_config, update.key7)},
    {.type = CONF_TYPE_INT, .key = "sig_req_mask", .offset = offsetof(struct mgos_config, update.sig_req_mask)},
    {.type = CONF_TYPE_STRING, .key = "url", .offset = offsetof(struct mgos_config, update.url)},
    {.type = CONF_TYPE_INT, .key = "interval", .offset = offsetof(struct mgos_config, update.interval)},
    {.type = CONF_TYPE_STRING, .key = "extra_http_headers", .offset = offsetof(struct mgos_config, update.extra_http_headers)},
    {.type = CONF_TYPE_STRING, .key = "ssl_ca_file", .offset = offsetof(struct mgos_config, update.ssl_ca_file)},
    {.type = CONF_TYPE_STRING, .key = "ssl_client_cert_file", .offset = offsetof(struct mgos_config, update.ssl_client_cert_file)},
    {.type = CONF_TYPE_STRING, .key = "ssl_server_name", .offset = offsetof(struct mgos_config, update.ssl_server_name)},
    {.type = CONF_TYPE_BOOL, .key = "enable_post", .offset = offsetof(struct mgos_config, update.enable_post)},
    {.type = CONF_TYPE_OBJECT, .key = "rpc", .offset = offsetof(struct mgos_config, rpc), .num_desc = 21},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, rpc.enable)},
    {.type = CONF_TYPE_BOOL, .key = "http_enable", .offset = offsetof(struct mgos_config, rpc.http_enable)},
    {.type = CONF_TYPE_BOOL, .key = "service_sys_enable", .offset = offsetof(struct mgos_config, rpc.service_sys_enable)},
    {.type = CONF_TYPE_INT, .key = "max_frame_size", .offset = offsetof(struct mgos_config, rpc.max_frame_size)},
    {.type = CONF_TYPE_INT, .key = "max_queue_length", .offset = offsetof(struct mgos_config, rpc.max_queue_length)},
    {.type = CONF_TYPE_INT, .key = "max_non_persistent_channels", .offset = offsetof(struct mgos_config, rpc.max_non_persistent_channels)},
    {.type = CONF_TYPE_INT, .key = "default_out_channel_idle_close_timeout", .offset = offsetof(struct mgos_config, rpc.default_out_channel_idle_close_timeout)},
    {.type = CONF_TYPE_STRING, .key = "acl", .offset = offsetof(struct mgos_config, rpc.acl)},
    {.type = CONF_TYPE_STRING, .key = "acl_file", .offset = offsetof(struct mgos_config, rpc.acl_file)},
    {.type = CONF_TYPE_STRING, .key = "auth_domain", .offset = offsetof(struct mgos_config, rpc.auth_domain)},
    {.type = CONF_TYPE_STRING, .key = "auth_file", .offset = offsetof(struct mgos_config, rpc.auth_file)},
    {.type = CONF_TYPE_INT, .key = "auth_algo", .offset = offsetof(struct mgos_config, rpc.auth_algo)},
    {.type = CONF_TYPE_OBJECT, .key = "uart", .offset = offsetof(struct mgos_config, rpc.uart), .num_desc = 8},
    {.type = CONF_TYPE_INT, .key = "uart_no", .offset = offsetof(struct mgos_config, rpc.uart.uart_no)},
    {.type = CONF_TYPE_INT, .key = "baud_rate", .offset = offsetof(struct mgos_config, rpc.uart.baud_rate)},
    {.type = CONF_TYPE_STRING, .key = "fc_type", .offset = offsetof(struct mgos_config, rpc.uart.fc_type)},
    {.type = CONF_TYPE_STRING, .key = "dst", .offset = offsetof(struct mgos_config, rpc.uart.dst)},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, rpc.uart.enable)},
    {.type = CONF_TYPE_BOOL, .key = "no_delay", .offset = offsetof(struct mgos_config, rpc.uart.no_delay)},
    {.type = CONF_TYPE_INT, .key = "rx_buf_size", .offset = offsetof(struct mgos_config, rpc.uart.rx_buf_size)},
    {.type = CONF_TYPE_INT, .key = "tx_buf_size", .offset = offsetof(struct mgos_config, rpc.uart.tx_buf_size)},
    {.type = CONF_TYPE_OBJECT, .key = "wifi", .offset = offsetof(struct mgos_config, wifi), .num_desc = 82},
    {.type = CONF_TYPE_OBJECT, .key = "ap", .offset = offsetof(struct mgos_config, wifi.ap), .num_desc = 16},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, wifi.ap.enable)},
    {.type = CONF_TYPE_STRING, .key = "ssid", .offset = offsetof(struct mgos_config, wifi.ap.ssid)},
    {.type = CONF_TYPE_STRING, .key = "pass", .offset = offsetof(struct mgos_config, wifi.ap.pass)},
    {.type = CONF_TYPE_BOOL, .key = "hidden", .offset = offsetof(struct mgos_config, wifi.ap.hidden)},
    {.type = CONF_TYPE_INT, .key = "channel", .offset = offsetof(struct mgos_config, wifi.ap.channel)},
    {.type = CONF_TYPE_INT, .key = "max_connections", .offset = offsetof(struct mgos_config, wifi.ap.max_connections)},
    {.type = CONF_TYPE_STRING, .key = "ip", .offset = offsetof(struct mgos_config, wifi.ap.ip)},
    {.type = CONF_TYPE_STRING, .key = "netmask", .offset = offsetof(struct mgos_config, wifi.ap.netmask)},
    {.type = CONF_TYPE_STRING, .key = "gw", .offset = offsetof(struct mgos_config, wifi.ap.gw)},
    {.type = CONF_TYPE_STRING, .key = "dhcp_start", .offset = offsetof(struct mgos_config, wifi.ap.dhcp_start)},
    {.type = CONF_TYPE_STRING, .key = "dhcp_end", .offset = offsetof(struct mgos_config, wifi.ap.dhcp_end)},
    {.type = CONF_TYPE_INT, .key = "trigger_on_gpio", .offset = offsetof(struct mgos_config, wifi.ap.trigger_on_gpio)},
    {.type = CONF_TYPE_INT, .key = "disable_after", .offset = offsetof(struct mgos_config, wifi.ap.disable_after)},
    {.type = CONF_TYPE_STRING, .key = "hostname", .offset = offsetof(struct mgos_config, wifi.ap.hostname)},
    {.type = CONF_TYPE_BOOL, .key = "bandwidth_20mhz", .offset = offsetof(struct mgos_config, wifi.ap.bandwidth_20mhz)},
    {.type = CONF_TYPE_STRING, .key = "protocol", .offset = offsetof(struct mgos_config, wifi.ap.protocol)},
    {.type = CONF_TYPE_OBJECT, .key = "sta", .offset = offsetof(struct mgos_config, wifi.sta), .num_desc = 19},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, wifi.sta.enable)},
    {.type = CONF_TYPE_STRING, .key = "ssid", .offset = offsetof(struct mgos_config, wifi.sta.ssid)},
    {.type = CONF_TYPE_STRING, .key = "pass", .offset = offsetof(struct mgos_config, wifi.sta.pass)},
    {.type = CONF_TYPE_STRING, .key = "bssid", .offset = offsetof(struct mgos_config, wifi.sta.bssid)},
    {.type = CONF_TYPE_INT, .key = "channel", .offset = offsetof(struct mgos_config, wifi.sta.channel)},
    {.type = CONF_TYPE_STRING, .key = "last_bssid", .offset = offsetof(struct mgos_config, wifi.sta.last_bssid)},
    {.type = CONF_TYPE_INT, .key = "last_channel", .offset = offsetof(struct mgos_config, wifi.sta.last_channel)},
    {.type = CONF_TYPE_STRING, .key = "user", .offset = offsetof(struct mgos_config, wifi.sta.user)},
    {.type = CONF_TYPE_STRING, .key = "anon_identity", .offset = offsetof(struct mgos_config, wifi.sta.anon_identity)},
    {.type = CONF_TYPE_STRING, .key = "cert", .offset = offsetof(struct mgos_config, wifi.sta.cert)},
    {.type = CONF_TYPE_STRING, .key = "key", .offset = offsetof(struct mgos_config, wifi.sta.key)},
    {.type = CONF_TYPE_STRING, .key = "ca_cert", .offset = offsetof(struct mgos_config, wifi.sta.ca_cert)},
    {.type = CONF_TYPE_STRING, .key = "ip", .offset = offsetof(struct mgos_config, wifi.sta.ip)},
    {.type = CONF_TYPE_STRING, .key = "netmask", .offset = offsetof(struct mgos_config, wifi.sta.netmask)},
    {.type = CONF_TYPE_STRING, .key = "gw", .offset = offsetof(struct mgos_config, wifi.sta.gw)},
    {.type = CONF_TYPE_STRING, .key = "nameserver", .offset = offsetof(struct mgos_config, wifi.sta.nameserver)},
    {.type = CONF_TYPE_STRING, .key = "dhcp_hostname", .offset = offsetof(struct mgos_config, wifi.sta.dhcp_hostname)},
    {.type = CONF_TYPE_STRING, .key = "protocol", .offset = offsetof(struct mgos_config, wifi.sta.protocol)},
    {.type = CONF_TYPE_INT, .key = "listen_interval_ms", .offset = offsetof(struct mgos_config, wifi.sta.listen_interval_ms)},
    {.type = CONF_TYPE_OBJECT, .key = "sta1", .offset = offsetof(struct mgos_config, wifi.sta1), .num_desc = 19},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, wifi.sta1.enable)},
    {.type = CONF_TYPE_STRING, .key = "ssid", .offset = offsetof(struct mgos_config, wifi.sta1.ssid)},
    {.type = CONF_TYPE_STRING, .key = "pass", .offset = offsetof(struct mgos_config, wifi.sta1.pass)},
    {.type = CONF_TYPE_STRING, .key = "bssid", .offset = offsetof(struct mgos_config, wifi.sta1.bssid)},
    {.type = CONF_TYPE_INT, .key = "channel", .offset = offsetof(struct mgos_config, wifi.sta1.channel)},
    {.type = CONF_TYPE_STRING, .key = "last_bssid", .offset = offsetof(struct mgos_config, wifi.sta1.last_bssid)},
    {.type = CONF_TYPE_INT, .key = "last_channel", .offset = offsetof(struct mgos_config, wifi.sta1.last_channel)},
    {.type = CONF_TYPE_STRING, .key = "user", .offset = offsetof(struct mgos_config, wifi.sta1.user)},
    {.type = CONF_TYPE_STRING, .key = "anon_identity", .offset = offsetof(struct mgos_config, wifi.sta1.anon_identity)},
    {.type = CONF_TYPE_STRING, .key = "cert", .offset = offsetof(struct mgos_config, wifi.sta1.cert)},
    {.type = CONF_TYPE_STRING, .key = "key", .offset = offsetof(struct mgos_config, wifi.sta1.key)},
    {.type = CONF_TYPE_STRING, .key = "ca_cert", .offset = offsetof(struct mgos_config, wifi.sta1.ca_cert)},
    {.type = CONF_TYPE_STRING, .key = "ip", .offset = offsetof(struct mgos_config, wifi.sta1.ip)},
    {.type = CONF_TYPE_STRING, .key = "netmask", .offset = offsetof(struct mgos_config, wifi.sta1.netmask)},
    {.type = CONF_TYPE_STRING, .key = "gw", .offset = offsetof(struct mgos_config, wifi.sta1.gw)},
    {.type = CONF_TYPE_STRING, .key = "nameserver", .offset = offsetof(struct mgos_config, wifi.sta1.nameserver)},
    {.type = CONF_TYPE_STRING, .key = "dhcp_hostname", .offset = offsetof(struct mgos_config, wifi.sta1.dhcp_hostname)},
    {.type = CONF_TYPE_STRING, .key = "protocol", .offset = offsetof(struct mgos_config, wifi.sta1.protocol)},
    {.type = CONF_TYPE_INT, .key = "listen_interval_ms", .offset = offsetof(struct mgos_config, wifi.sta1.listen_interval_ms)},
    {.type = CONF_TYPE_OBJECT, .key = "sta2", .offset = offsetof(struct mgos_config, wifi.sta2), .num_desc = 19},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, wifi.sta2.enable)},
    {.type = CONF_TYPE_STRING, .key = "ssid", .offset = offsetof(struct mgos_config, wifi.sta2.ssid)},
    {.type = CONF_TYPE_STRING, .key = "pass", .offset = offsetof(struct mgos_config, wifi.sta2.pass)},
    {.type = CONF_TYPE_STRING, .key = "bssid", .offset = offsetof(struct mgos_config, wifi.sta2.bssid)},
    {.type = CONF_TYPE_INT, .key = "channel", .offset = offsetof(struct mgos_config, wifi.sta2.channel)},
    {.type = CONF_TYPE_STRING, .key = "last_bssid", .offset = offsetof(struct mgos_config, wifi.sta2.last_bssid)},
    {.type = CONF_TYPE_INT, .key = "last_channel", .offset = offsetof(struct mgos_config, wifi.sta2.last_channel)},
    {.type = CONF_TYPE_STRING, .key = "user", .offset = offsetof(struct mgos_config, wifi.sta2.user)},
    {.type = CONF_TYPE_STRING, .key = "anon_identity", .offset = offsetof(struct mgos_config, wifi.sta2.anon_identity)},
    {.type = CONF_TYPE_STRING, .key = "cert", .offset = offsetof(struct mgos_config, wifi.sta2.cert)},
    {.type = CONF_TYPE_STRING, .key = "key", .offset = offsetof(struct mgos_config, wifi.sta2.key)},
    {.type = CONF_TYPE_STRING, .key = "ca_cert", .offset = offsetof(struct mgos_config, wifi.sta2.ca_cert)},
    {.type = CONF_TYPE_STRING, .key = "ip", .offset = offsetof(struct mgos_config, wifi.sta2.ip)},
    {.type = CONF_TYPE_STRING, .key = "netmask", .offset = offsetof(struct mgos_config, wifi.sta2.netmask)},
    {.type = CONF_TYPE_STRING, .key = "gw", .offset = offsetof(struct mgos_config, wifi.sta2.gw)},
    {.type = CONF_TYPE_STRING, .key = "nameserver", .offset = offsetof(struct mgos_config, wifi.sta2.nameserver)},
    {.type = CONF_TYPE_STRING, .key = "dhcp_hostname", .offset = offsetof(struct mgos_config, wifi.sta2.dhcp_hostname)},
    {.type = CONF_TYPE_STRING, .key = "protocol", .offset = offsetof(struct mgos_config, wifi.sta2.protocol)},
    {.type = CONF_TYPE_INT, .key = "listen_interval_ms", .offset = offsetof(struct mgos_config, wifi.sta2.listen_interval_ms)},
    {.type = CONF_TYPE_INT, .key = "sta_rssi_thr", .offset = offsetof(struct mgos_config, wifi.sta_rssi_thr)},
    {.type = CONF_TYPE_INT, .key = "sta_connect_timeout", .offset = offsetof(struct mgos_config, wifi.sta_connect_timeout)},
    {.type = CONF_TYPE_INT, .key = "sta_roam_rssi_thr", .offset = offsetof(struct mgos_config, wifi.sta_roam_rssi_thr)},
    {.type = CONF_TYPE_INT, .key = "sta_roam_interval", .offset = offsetof(struct mgos_config, wifi.sta_roam_interval)},
    {.type = CONF_TYPE_INT, .key = "sta_ps_mode", .offset = offsetof(struct mgos_config, wifi.sta_ps_mode)},
    {.type = CONF_TYPE_OBJECT, .key = "sntp", .offset = offsetof(struct mgos_config, sntp), .num_desc = 6},
    {.type = CONF_TYPE_BOOL, .key = "enable", .offset = offsetof(struct mgos_config, sntp.enable)},
    {.type = CONF_TYPE_STRING, .key = "server", .offset = offsetof(struct mgos_config, sntp.server)},
    {.type = CONF_TYPE_BOOL, .key = "use_dhcp_ntp_server", .offset = offsetof(struct mgos_config, sntp.use_dhcp_ntp_server)},
    {.type = CONF_TYPE_INT, .key = "retry_min", .offset = offsetof(struct mgos_config, sntp.retry_min)},
    {.type = CONF_TYPE_INT, .key = "retry_max", .offset = offsetof(struct mgos_config, sntp.retry_max)},
    {.type = CONF_TYPE_INT, .key = "update_interval", .offset = offsetof(struct mgos_config, sntp.update_interval)},
    {.type = CONF_TYPE_OBJECT, .key = "app", .offset = offsetof(struct mgos_config, app), .num_desc = 1},
    {.type = CONF_TYPE_STRING, .key = "name", .offset = offsetof(struct mgos_config, app.name)},
};

/* struct mgos_config_debug */
const struct mgos_conf_entry *mgos_config_debug_get_schema(void) {
  return &mgos_config_schema_[1];
}

void mgos_config_debug_set_defaults(struct mgos_config_debug *cfg) {
  cfg->udp_log_addr = NULL;
  cfg->udp_log_level = 3;
  cfg->mbedtls_level = 1;
  cfg->level = 2;
  cfg->file_level = NULL;
  cfg->event_level = 2;
  cfg->stdout_uart = 0;
  cfg->stderr_uart = 0;
  cfg->factory_reset_gpio = -1;
  cfg->mg_mgr_hexdump_file = NULL;
}
bool mgos_config_debug_parse_f(const char *fname, struct mgos_config_debug *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_debug_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_device */
const struct mgos_conf_entry *mgos_config_device_get_schema(void) {
  return &mgos_config_schema_[12];
}

void mgos_config_device_set_defaults(struct mgos_config_device *cfg) {
  cfg->id = "esp32_??????";
  cfg->license = NULL;
  cfg->mac = NULL;
  cfg->public_key = NULL;
  cfg->sn = NULL;
}
bool mgos_config_device_parse_f(const char *fname, struct mgos_config_device *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_device_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_sys */
const struct mgos_conf_entry *mgos_config_sys_get_schema(void) {
  return &mgos_config_schema_[18];
}

void mgos_config_sys_set_defaults(struct mgos_config_sys *cfg) {
  cfg->tz_spec = NULL;
  cfg->wdt_timeout = 30;
  cfg->pref_ota_lib = NULL;
}
bool mgos_config_sys_parse_f(const char *fname, struct mgos_config_sys *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_sys_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_dns_sd */
const struct mgos_conf_entry *mgos_config_dns_sd_get_schema(void) {
  return &mgos_config_schema_[23];
}

void mgos_config_dns_sd_set_defaults(struct mgos_config_dns_sd *cfg) {
  cfg->enable = true;
  cfg->adv_only = false;
  cfg->host_name = "bedcontroller";
  cfg->txt = NULL;
}
bool mgos_config_dns_sd_parse_f(const char *fname, struct mgos_config_dns_sd *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_dns_sd_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_http */
const struct mgos_conf_entry *mgos_config_http_get_schema(void) {
  return &mgos_config_schema_[28];
}

void mgos_config_http_set_defaults(struct mgos_config_http *cfg) {
  cfg->enable = true;
  cfg->listen_addr = "80";
  cfg->document_root = "/";
  cfg->index_files = NULL;
  cfg->ssl_cert = NULL;
  cfg->ssl_key = NULL;
  cfg->ssl_ca_cert = NULL;
  cfg->upload_acl = "*";
  cfg->hidden_files = NULL;
  cfg->auth_domain = NULL;
  cfg->auth_file = NULL;
  cfg->auth_algo = 0;
  cfg->extra_headers = NULL;
}
bool mgos_config_http_parse_f(const char *fname, struct mgos_config_http *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_http_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_mjs */
const struct mgos_conf_entry *mgos_config_mjs_get_schema(void) {
  return &mgos_config_schema_[42];
}

void mgos_config_mjs_set_defaults(struct mgos_config_mjs *cfg) {
  cfg->generate_jsc = true;
}
bool mgos_config_mjs_parse_f(const char *fname, struct mgos_config_mjs *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_mjs_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_update */
const struct mgos_conf_entry *mgos_config_update_get_schema(void) {
  return &mgos_config_schema_[44];
}

void mgos_config_update_set_defaults(struct mgos_config_update *cfg) {
  cfg->timeout = 600;
  cfg->commit_timeout = 0;
  cfg->key0 = NULL;
  cfg->key1 = NULL;
  cfg->key2 = NULL;
  cfg->key3 = NULL;
  cfg->key4 = NULL;
  cfg->key5 = NULL;
  cfg->key6 = NULL;
  cfg->key7 = NULL;
  cfg->sig_req_mask = -1;
  cfg->url = NULL;
  cfg->interval = 0;
  cfg->extra_http_headers = NULL;
  cfg->ssl_ca_file = "ca.pem";
  cfg->ssl_client_cert_file = NULL;
  cfg->ssl_server_name = NULL;
  cfg->enable_post = true;
}
bool mgos_config_update_parse_f(const char *fname, struct mgos_config_update *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_update_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_rpc_uart */
const struct mgos_conf_entry *mgos_config_rpc_uart_get_schema(void) {
  return &mgos_config_schema_[76];
}

void mgos_config_rpc_uart_set_defaults(struct mgos_config_rpc_uart *cfg) {
  cfg->uart_no = 0;
  cfg->baud_rate = 0;
  cfg->fc_type = NULL;
  cfg->dst = NULL;
  cfg->enable = false;
  cfg->no_delay = false;
  cfg->rx_buf_size = 0;
  cfg->tx_buf_size = 0;
}
bool mgos_config_rpc_uart_parse_f(const char *fname, struct mgos_config_rpc_uart *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_rpc_uart_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_rpc */
const struct mgos_conf_entry *mgos_config_rpc_get_schema(void) {
  return &mgos_config_schema_[63];
}

void mgos_config_rpc_set_defaults(struct mgos_config_rpc *cfg) {
  cfg->enable = true;
  cfg->http_enable = true;
  cfg->service_sys_enable = true;
  cfg->max_frame_size = 4096;
  cfg->max_queue_length = 25;
  cfg->max_non_persistent_channels = 20;
  cfg->default_out_channel_idle_close_timeout = 10;
  cfg->acl = NULL;
  cfg->acl_file = NULL;
  cfg->auth_domain = "RPC";
  cfg->auth_file = NULL;
  cfg->auth_algo = 0;
  mgos_config_rpc_uart_set_defaults(&cfg->uart);
}
bool mgos_config_rpc_parse_f(const char *fname, struct mgos_config_rpc *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_rpc_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_wifi_ap */
const struct mgos_conf_entry *mgos_config_wifi_ap_get_schema(void) {
  return &mgos_config_schema_[86];
}

void mgos_config_wifi_ap_set_defaults(struct mgos_config_wifi_ap *cfg) {
  cfg->enable = false;
  cfg->ssid = NULL;
  cfg->pass = NULL;
  cfg->hidden = false;
  cfg->channel = 6;
  cfg->max_connections = 10;
  cfg->ip = "192.168.4.1";
  cfg->netmask = "255.255.255.0";
  cfg->gw = "192.168.4.1";
  cfg->dhcp_start = "192.168.4.2";
  cfg->dhcp_end = "192.168.4.100";
  cfg->trigger_on_gpio = -1;
  cfg->disable_after = 0;
  cfg->hostname = NULL;
  cfg->bandwidth_20mhz = false;
  cfg->protocol = "BGN";
}
bool mgos_config_wifi_ap_parse_f(const char *fname, struct mgos_config_wifi_ap *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_wifi_ap_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_wifi_sta */
const struct mgos_conf_entry *mgos_config_wifi_sta_get_schema(void) {
  return &mgos_config_schema_[143];
}

void mgos_config_wifi_sta_set_defaults(struct mgos_config_wifi_sta *cfg) {
  cfg->enable = false;
  cfg->ssid = NULL;
  cfg->pass = NULL;
  cfg->bssid = NULL;
  cfg->channel = 0;
  cfg->last_bssid = NULL;
  cfg->last_channel = 0;
  cfg->user = NULL;
  cfg->anon_identity = NULL;
  cfg->cert = NULL;
  cfg->key = NULL;
  cfg->ca_cert = NULL;
  cfg->ip = NULL;
  cfg->netmask = NULL;
  cfg->gw = NULL;
  cfg->nameserver = NULL;
  cfg->dhcp_hostname = NULL;
  cfg->protocol = "BGN";
  cfg->listen_interval_ms = 0;
}
bool mgos_config_wifi_sta_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_wifi_sta_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_wifi_sta */
const struct mgos_conf_entry *mgos_config_wifi_sta1_get_schema(void) {
  return &mgos_config_schema_[143];
}

void mgos_config_wifi_sta1_set_defaults(struct mgos_config_wifi_sta *cfg) {
  cfg->enable = false;
  cfg->ssid = NULL;
  cfg->pass = NULL;
  cfg->bssid = NULL;
  cfg->channel = 0;
  cfg->last_bssid = NULL;
  cfg->last_channel = 0;
  cfg->user = NULL;
  cfg->anon_identity = NULL;
  cfg->cert = NULL;
  cfg->key = NULL;
  cfg->ca_cert = NULL;
  cfg->ip = NULL;
  cfg->netmask = NULL;
  cfg->gw = NULL;
  cfg->nameserver = NULL;
  cfg->dhcp_hostname = NULL;
  cfg->protocol = "BGN";
  cfg->listen_interval_ms = 0;
}
bool mgos_config_wifi_sta1_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_wifi_sta1_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_wifi_sta */
const struct mgos_conf_entry *mgos_config_wifi_sta2_get_schema(void) {
  return &mgos_config_schema_[143];
}

void mgos_config_wifi_sta2_set_defaults(struct mgos_config_wifi_sta *cfg) {
  cfg->enable = false;
  cfg->ssid = NULL;
  cfg->pass = NULL;
  cfg->bssid = NULL;
  cfg->channel = 0;
  cfg->last_bssid = NULL;
  cfg->last_channel = 0;
  cfg->user = NULL;
  cfg->anon_identity = NULL;
  cfg->cert = NULL;
  cfg->key = NULL;
  cfg->ca_cert = NULL;
  cfg->ip = NULL;
  cfg->netmask = NULL;
  cfg->gw = NULL;
  cfg->nameserver = NULL;
  cfg->dhcp_hostname = NULL;
  cfg->protocol = "BGN";
  cfg->listen_interval_ms = 0;
}
bool mgos_config_wifi_sta2_parse_f(const char *fname, struct mgos_config_wifi_sta *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_wifi_sta2_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_wifi */
const struct mgos_conf_entry *mgos_config_wifi_get_schema(void) {
  return &mgos_config_schema_[85];
}

void mgos_config_wifi_set_defaults(struct mgos_config_wifi *cfg) {
  mgos_config_wifi_ap_set_defaults(&cfg->ap);
  mgos_config_wifi_sta_set_defaults(&cfg->sta);
  mgos_config_wifi_sta1_set_defaults(&cfg->sta1);
  mgos_config_wifi_sta2_set_defaults(&cfg->sta2);
  cfg->sta_rssi_thr = -95;
  cfg->sta_connect_timeout = 15;
  cfg->sta_roam_rssi_thr = -80;
  cfg->sta_roam_interval = 0;
  cfg->sta_ps_mode = 0;
}
bool mgos_config_wifi_parse_f(const char *fname, struct mgos_config_wifi *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_wifi_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_sntp */
const struct mgos_conf_entry *mgos_config_sntp_get_schema(void) {
  return &mgos_config_schema_[168];
}

void mgos_config_sntp_set_defaults(struct mgos_config_sntp *cfg) {
  cfg->enable = true;
  cfg->server = "time.google.com";
  cfg->use_dhcp_ntp_server = true;
  cfg->retry_min = 1;
  cfg->retry_max = 30;
  cfg->update_interval = 7200;
}
bool mgos_config_sntp_parse_f(const char *fname, struct mgos_config_sntp *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_sntp_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config_app */
const struct mgos_conf_entry *mgos_config_app_get_schema(void) {
  return &mgos_config_schema_[175];
}

void mgos_config_app_set_defaults(struct mgos_config_app *cfg) {
  cfg->name = NULL;
}
bool mgos_config_app_parse_f(const char *fname, struct mgos_config_app *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_app_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* struct mgos_config */
const struct mgos_conf_entry *mgos_config_get_schema(void) {
  return &mgos_config_schema_[0];
}

void mgos_config_set_defaults(struct mgos_config *cfg) {
  mgos_config_debug_set_defaults(&cfg->debug);
  mgos_config_device_set_defaults(&cfg->device);
  mgos_config_sys_set_defaults(&cfg->sys);
  cfg->conf_acl = "*";
  mgos_config_dns_sd_set_defaults(&cfg->dns_sd);
  mgos_config_http_set_defaults(&cfg->http);
  mgos_config_mjs_set_defaults(&cfg->mjs);
  mgos_config_update_set_defaults(&cfg->update);
  mgos_config_rpc_set_defaults(&cfg->rpc);
  mgos_config_wifi_set_defaults(&cfg->wifi);
  mgos_config_sntp_set_defaults(&cfg->sntp);
  mgos_config_app_set_defaults(&cfg->app);
}
bool mgos_config_parse_f(const char *fname, struct mgos_config *cfg) {
  size_t len;
  char *data = cs_read_file(fname, &len);
  if (data == NULL) return false;
  bool res = mgos_config_parse(mg_mk_str_n(data, len), cfg);
  free(data);
  return res;
}

/* Global instance */
struct mgos_config mgos_sys_config;

/* Accessors */

/* debug */
const struct mgos_config_debug *mgos_config_get_debug(const struct mgos_config *cfg) { return &cfg->debug; }

/* debug.udp_log_addr */
const char * mgos_config_get_debug_udp_log_addr(const struct mgos_config *cfg) { return cfg->debug.udp_log_addr; }
const char * mgos_config_get_default_debug_udp_log_addr(void) { return NULL; }
void mgos_config_set_debug_udp_log_addr(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->debug.udp_log_addr, v); }

/* debug.udp_log_level */
int mgos_config_get_debug_udp_log_level(const struct mgos_config *cfg) { return cfg->debug.udp_log_level; }
int mgos_config_get_default_debug_udp_log_level(void) { return 3; }
void mgos_config_set_debug_udp_log_level(struct mgos_config *cfg, int v) { cfg->debug.udp_log_level = v; }

/* debug.mbedtls_level */
int mgos_config_get_debug_mbedtls_level(const struct mgos_config *cfg) { return cfg->debug.mbedtls_level; }
int mgos_config_get_default_debug_mbedtls_level(void) { return 1; }
void mgos_config_set_debug_mbedtls_level(struct mgos_config *cfg, int v) { cfg->debug.mbedtls_level = v; }

/* debug.level */
int mgos_config_get_debug_level(const struct mgos_config *cfg) { return cfg->debug.level; }
int mgos_config_get_default_debug_level(void) { return 2; }
void mgos_config_set_debug_level(struct mgos_config *cfg, int v) { cfg->debug.level = v; }

/* debug.file_level */
const char * mgos_config_get_debug_file_level(const struct mgos_config *cfg) { return cfg->debug.file_level; }
const char * mgos_config_get_default_debug_file_level(void) { return NULL; }
void mgos_config_set_debug_file_level(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->debug.file_level, v); }

/* debug.event_level */
int mgos_config_get_debug_event_level(const struct mgos_config *cfg) { return cfg->debug.event_level; }
int mgos_config_get_default_debug_event_level(void) { return 2; }
void mgos_config_set_debug_event_level(struct mgos_config *cfg, int v) { cfg->debug.event_level = v; }

/* debug.stdout_uart */
int mgos_config_get_debug_stdout_uart(const struct mgos_config *cfg) { return cfg->debug.stdout_uart; }
int mgos_config_get_default_debug_stdout_uart(void) { return 0; }
void mgos_config_set_debug_stdout_uart(struct mgos_config *cfg, int v) { cfg->debug.stdout_uart = v; }

/* debug.stderr_uart */
int mgos_config_get_debug_stderr_uart(const struct mgos_config *cfg) { return cfg->debug.stderr_uart; }
int mgos_config_get_default_debug_stderr_uart(void) { return 0; }
void mgos_config_set_debug_stderr_uart(struct mgos_config *cfg, int v) { cfg->debug.stderr_uart = v; }

/* debug.factory_reset_gpio */
int mgos_config_get_debug_factory_reset_gpio(const struct mgos_config *cfg) { return cfg->debug.factory_reset_gpio; }
int mgos_config_get_default_debug_factory_reset_gpio(void) { return -1; }
void mgos_config_set_debug_factory_reset_gpio(struct mgos_config *cfg, int v) { cfg->debug.factory_reset_gpio = v; }

/* debug.mg_mgr_hexdump_file */
const char * mgos_config_get_debug_mg_mgr_hexdump_file(const struct mgos_config *cfg) { return cfg->debug.mg_mgr_hexdump_file; }
const char * mgos_config_get_default_debug_mg_mgr_hexdump_file(void) { return NULL; }
void mgos_config_set_debug_mg_mgr_hexdump_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->debug.mg_mgr_hexdump_file, v); }

/* device */
const struct mgos_config_device *mgos_config_get_device(const struct mgos_config *cfg) { return &cfg->device; }

/* device.id */
const char * mgos_config_get_device_id(const struct mgos_config *cfg) { return cfg->device.id; }
const char * mgos_config_get_default_device_id(void) { return "esp32_??????"; }
void mgos_config_set_device_id(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->device.id, v); }

/* device.license */
const char * mgos_config_get_device_license(const struct mgos_config *cfg) { return cfg->device.license; }
const char * mgos_config_get_default_device_license(void) { return NULL; }
void mgos_config_set_device_license(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->device.license, v); }

/* device.mac */
const char * mgos_config_get_device_mac(const struct mgos_config *cfg) { return cfg->device.mac; }
const char * mgos_config_get_default_device_mac(void) { return NULL; }
void mgos_config_set_device_mac(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->device.mac, v); }

/* device.public_key */
const char * mgos_config_get_device_public_key(const struct mgos_config *cfg) { return cfg->device.public_key; }
const char * mgos_config_get_default_device_public_key(void) { return NULL; }
void mgos_config_set_device_public_key(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->device.public_key, v); }

/* device.sn */
const char * mgos_config_get_device_sn(const struct mgos_config *cfg) { return cfg->device.sn; }
const char * mgos_config_get_default_device_sn(void) { return NULL; }
void mgos_config_set_device_sn(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->device.sn, v); }

/* sys */
const struct mgos_config_sys *mgos_config_get_sys(const struct mgos_config *cfg) { return &cfg->sys; }

/* sys.tz_spec */
const char * mgos_config_get_sys_tz_spec(const struct mgos_config *cfg) { return cfg->sys.tz_spec; }
const char * mgos_config_get_default_sys_tz_spec(void) { return NULL; }
void mgos_config_set_sys_tz_spec(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->sys.tz_spec, v); }

/* sys.wdt_timeout */
int mgos_config_get_sys_wdt_timeout(const struct mgos_config *cfg) { return cfg->sys.wdt_timeout; }
int mgos_config_get_default_sys_wdt_timeout(void) { return 30; }
void mgos_config_set_sys_wdt_timeout(struct mgos_config *cfg, int v) { cfg->sys.wdt_timeout = v; }

/* sys.pref_ota_lib */
const char * mgos_config_get_sys_pref_ota_lib(const struct mgos_config *cfg) { return cfg->sys.pref_ota_lib; }
const char * mgos_config_get_default_sys_pref_ota_lib(void) { return NULL; }
void mgos_config_set_sys_pref_ota_lib(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->sys.pref_ota_lib, v); }

/* conf_acl */
const char * mgos_config_get_conf_acl(const struct mgos_config *cfg) { return cfg->conf_acl; }
const char * mgos_config_get_default_conf_acl(void) { return "*"; }
void mgos_config_set_conf_acl(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->conf_acl, v); }

/* dns_sd */
const struct mgos_config_dns_sd *mgos_config_get_dns_sd(const struct mgos_config *cfg) { return &cfg->dns_sd; }

/* dns_sd.enable */
int mgos_config_get_dns_sd_enable(const struct mgos_config *cfg) { return cfg->dns_sd.enable; }
int mgos_config_get_default_dns_sd_enable(void) { return true; }
void mgos_config_set_dns_sd_enable(struct mgos_config *cfg, int v) { cfg->dns_sd.enable = v; }

/* dns_sd.adv_only */
int mgos_config_get_dns_sd_adv_only(const struct mgos_config *cfg) { return cfg->dns_sd.adv_only; }
int mgos_config_get_default_dns_sd_adv_only(void) { return false; }
void mgos_config_set_dns_sd_adv_only(struct mgos_config *cfg, int v) { cfg->dns_sd.adv_only = v; }

/* dns_sd.host_name */
const char * mgos_config_get_dns_sd_host_name(const struct mgos_config *cfg) { return cfg->dns_sd.host_name; }
const char * mgos_config_get_default_dns_sd_host_name(void) { return "bedcontroller"; }
void mgos_config_set_dns_sd_host_name(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->dns_sd.host_name, v); }

/* dns_sd.txt */
const char * mgos_config_get_dns_sd_txt(const struct mgos_config *cfg) { return cfg->dns_sd.txt; }
const char * mgos_config_get_default_dns_sd_txt(void) { return NULL; }
void mgos_config_set_dns_sd_txt(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->dns_sd.txt, v); }

/* http */
const struct mgos_config_http *mgos_config_get_http(const struct mgos_config *cfg) { return &cfg->http; }

/* http.enable */
int mgos_config_get_http_enable(const struct mgos_config *cfg) { return cfg->http.enable; }
int mgos_config_get_default_http_enable(void) { return true; }
void mgos_config_set_http_enable(struct mgos_config *cfg, int v) { cfg->http.enable = v; }

/* http.listen_addr */
const char * mgos_config_get_http_listen_addr(const struct mgos_config *cfg) { return cfg->http.listen_addr; }
const char * mgos_config_get_default_http_listen_addr(void) { return "80"; }
void mgos_config_set_http_listen_addr(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.listen_addr, v); }

/* http.document_root */
const char * mgos_config_get_http_document_root(const struct mgos_config *cfg) { return cfg->http.document_root; }
const char * mgos_config_get_default_http_document_root(void) { return "/"; }
void mgos_config_set_http_document_root(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.document_root, v); }

/* http.index_files */
const char * mgos_config_get_http_index_files(const struct mgos_config *cfg) { return cfg->http.index_files; }
const char * mgos_config_get_default_http_index_files(void) { return NULL; }
void mgos_config_set_http_index_files(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.index_files, v); }

/* http.ssl_cert */
const char * mgos_config_get_http_ssl_cert(const struct mgos_config *cfg) { return cfg->http.ssl_cert; }
const char * mgos_config_get_default_http_ssl_cert(void) { return NULL; }
void mgos_config_set_http_ssl_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.ssl_cert, v); }

/* http.ssl_key */
const char * mgos_config_get_http_ssl_key(const struct mgos_config *cfg) { return cfg->http.ssl_key; }
const char * mgos_config_get_default_http_ssl_key(void) { return NULL; }
void mgos_config_set_http_ssl_key(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.ssl_key, v); }

/* http.ssl_ca_cert */
const char * mgos_config_get_http_ssl_ca_cert(const struct mgos_config *cfg) { return cfg->http.ssl_ca_cert; }
const char * mgos_config_get_default_http_ssl_ca_cert(void) { return NULL; }
void mgos_config_set_http_ssl_ca_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.ssl_ca_cert, v); }

/* http.upload_acl */
const char * mgos_config_get_http_upload_acl(const struct mgos_config *cfg) { return cfg->http.upload_acl; }
const char * mgos_config_get_default_http_upload_acl(void) { return "*"; }
void mgos_config_set_http_upload_acl(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.upload_acl, v); }

/* http.hidden_files */
const char * mgos_config_get_http_hidden_files(const struct mgos_config *cfg) { return cfg->http.hidden_files; }
const char * mgos_config_get_default_http_hidden_files(void) { return NULL; }
void mgos_config_set_http_hidden_files(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.hidden_files, v); }

/* http.auth_domain */
const char * mgos_config_get_http_auth_domain(const struct mgos_config *cfg) { return cfg->http.auth_domain; }
const char * mgos_config_get_default_http_auth_domain(void) { return NULL; }
void mgos_config_set_http_auth_domain(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.auth_domain, v); }

/* http.auth_file */
const char * mgos_config_get_http_auth_file(const struct mgos_config *cfg) { return cfg->http.auth_file; }
const char * mgos_config_get_default_http_auth_file(void) { return NULL; }
void mgos_config_set_http_auth_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.auth_file, v); }

/* http.auth_algo */
int mgos_config_get_http_auth_algo(const struct mgos_config *cfg) { return cfg->http.auth_algo; }
int mgos_config_get_default_http_auth_algo(void) { return 0; }
void mgos_config_set_http_auth_algo(struct mgos_config *cfg, int v) { cfg->http.auth_algo = v; }

/* http.extra_headers */
const char * mgos_config_get_http_extra_headers(const struct mgos_config *cfg) { return cfg->http.extra_headers; }
const char * mgos_config_get_default_http_extra_headers(void) { return NULL; }
void mgos_config_set_http_extra_headers(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->http.extra_headers, v); }

/* mjs */
const struct mgos_config_mjs *mgos_config_get_mjs(const struct mgos_config *cfg) { return &cfg->mjs; }

/* mjs.generate_jsc */
int mgos_config_get_mjs_generate_jsc(const struct mgos_config *cfg) { return cfg->mjs.generate_jsc; }
int mgos_config_get_default_mjs_generate_jsc(void) { return true; }
void mgos_config_set_mjs_generate_jsc(struct mgos_config *cfg, int v) { cfg->mjs.generate_jsc = v; }

/* update */
const struct mgos_config_update *mgos_config_get_update(const struct mgos_config *cfg) { return &cfg->update; }

/* update.timeout */
int mgos_config_get_update_timeout(const struct mgos_config *cfg) { return cfg->update.timeout; }
int mgos_config_get_default_update_timeout(void) { return 600; }
void mgos_config_set_update_timeout(struct mgos_config *cfg, int v) { cfg->update.timeout = v; }

/* update.commit_timeout */
int mgos_config_get_update_commit_timeout(const struct mgos_config *cfg) { return cfg->update.commit_timeout; }
int mgos_config_get_default_update_commit_timeout(void) { return 0; }
void mgos_config_set_update_commit_timeout(struct mgos_config *cfg, int v) { cfg->update.commit_timeout = v; }

/* update.key0 */
const char * mgos_config_get_update_key0(const struct mgos_config *cfg) { return cfg->update.key0; }
const char * mgos_config_get_default_update_key0(void) { return NULL; }
void mgos_config_set_update_key0(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key0, v); }

/* update.key1 */
const char * mgos_config_get_update_key1(const struct mgos_config *cfg) { return cfg->update.key1; }
const char * mgos_config_get_default_update_key1(void) { return NULL; }
void mgos_config_set_update_key1(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key1, v); }

/* update.key2 */
const char * mgos_config_get_update_key2(const struct mgos_config *cfg) { return cfg->update.key2; }
const char * mgos_config_get_default_update_key2(void) { return NULL; }
void mgos_config_set_update_key2(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key2, v); }

/* update.key3 */
const char * mgos_config_get_update_key3(const struct mgos_config *cfg) { return cfg->update.key3; }
const char * mgos_config_get_default_update_key3(void) { return NULL; }
void mgos_config_set_update_key3(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key3, v); }

/* update.key4 */
const char * mgos_config_get_update_key4(const struct mgos_config *cfg) { return cfg->update.key4; }
const char * mgos_config_get_default_update_key4(void) { return NULL; }
void mgos_config_set_update_key4(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key4, v); }

/* update.key5 */
const char * mgos_config_get_update_key5(const struct mgos_config *cfg) { return cfg->update.key5; }
const char * mgos_config_get_default_update_key5(void) { return NULL; }
void mgos_config_set_update_key5(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key5, v); }

/* update.key6 */
const char * mgos_config_get_update_key6(const struct mgos_config *cfg) { return cfg->update.key6; }
const char * mgos_config_get_default_update_key6(void) { return NULL; }
void mgos_config_set_update_key6(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key6, v); }

/* update.key7 */
const char * mgos_config_get_update_key7(const struct mgos_config *cfg) { return cfg->update.key7; }
const char * mgos_config_get_default_update_key7(void) { return NULL; }
void mgos_config_set_update_key7(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.key7, v); }

/* update.sig_req_mask */
int mgos_config_get_update_sig_req_mask(const struct mgos_config *cfg) { return cfg->update.sig_req_mask; }
int mgos_config_get_default_update_sig_req_mask(void) { return -1; }
void mgos_config_set_update_sig_req_mask(struct mgos_config *cfg, int v) { cfg->update.sig_req_mask = v; }

/* update.url */
const char * mgos_config_get_update_url(const struct mgos_config *cfg) { return cfg->update.url; }
const char * mgos_config_get_default_update_url(void) { return NULL; }
void mgos_config_set_update_url(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.url, v); }

/* update.interval */
int mgos_config_get_update_interval(const struct mgos_config *cfg) { return cfg->update.interval; }
int mgos_config_get_default_update_interval(void) { return 0; }
void mgos_config_set_update_interval(struct mgos_config *cfg, int v) { cfg->update.interval = v; }

/* update.extra_http_headers */
const char * mgos_config_get_update_extra_http_headers(const struct mgos_config *cfg) { return cfg->update.extra_http_headers; }
const char * mgos_config_get_default_update_extra_http_headers(void) { return NULL; }
void mgos_config_set_update_extra_http_headers(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.extra_http_headers, v); }

/* update.ssl_ca_file */
const char * mgos_config_get_update_ssl_ca_file(const struct mgos_config *cfg) { return cfg->update.ssl_ca_file; }
const char * mgos_config_get_default_update_ssl_ca_file(void) { return "ca.pem"; }
void mgos_config_set_update_ssl_ca_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.ssl_ca_file, v); }

/* update.ssl_client_cert_file */
const char * mgos_config_get_update_ssl_client_cert_file(const struct mgos_config *cfg) { return cfg->update.ssl_client_cert_file; }
const char * mgos_config_get_default_update_ssl_client_cert_file(void) { return NULL; }
void mgos_config_set_update_ssl_client_cert_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.ssl_client_cert_file, v); }

/* update.ssl_server_name */
const char * mgos_config_get_update_ssl_server_name(const struct mgos_config *cfg) { return cfg->update.ssl_server_name; }
const char * mgos_config_get_default_update_ssl_server_name(void) { return NULL; }
void mgos_config_set_update_ssl_server_name(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->update.ssl_server_name, v); }

/* update.enable_post */
int mgos_config_get_update_enable_post(const struct mgos_config *cfg) { return cfg->update.enable_post; }
int mgos_config_get_default_update_enable_post(void) { return true; }
void mgos_config_set_update_enable_post(struct mgos_config *cfg, int v) { cfg->update.enable_post = v; }

/* rpc */
const struct mgos_config_rpc *mgos_config_get_rpc(const struct mgos_config *cfg) { return &cfg->rpc; }

/* rpc.enable */
int mgos_config_get_rpc_enable(const struct mgos_config *cfg) { return cfg->rpc.enable; }
int mgos_config_get_default_rpc_enable(void) { return true; }
void mgos_config_set_rpc_enable(struct mgos_config *cfg, int v) { cfg->rpc.enable = v; }

/* rpc.http_enable */
int mgos_config_get_rpc_http_enable(const struct mgos_config *cfg) { return cfg->rpc.http_enable; }
int mgos_config_get_default_rpc_http_enable(void) { return true; }
void mgos_config_set_rpc_http_enable(struct mgos_config *cfg, int v) { cfg->rpc.http_enable = v; }

/* rpc.service_sys_enable */
int mgos_config_get_rpc_service_sys_enable(const struct mgos_config *cfg) { return cfg->rpc.service_sys_enable; }
int mgos_config_get_default_rpc_service_sys_enable(void) { return true; }
void mgos_config_set_rpc_service_sys_enable(struct mgos_config *cfg, int v) { cfg->rpc.service_sys_enable = v; }

/* rpc.max_frame_size */
int mgos_config_get_rpc_max_frame_size(const struct mgos_config *cfg) { return cfg->rpc.max_frame_size; }
int mgos_config_get_default_rpc_max_frame_size(void) { return 4096; }
void mgos_config_set_rpc_max_frame_size(struct mgos_config *cfg, int v) { cfg->rpc.max_frame_size = v; }

/* rpc.max_queue_length */
int mgos_config_get_rpc_max_queue_length(const struct mgos_config *cfg) { return cfg->rpc.max_queue_length; }
int mgos_config_get_default_rpc_max_queue_length(void) { return 25; }
void mgos_config_set_rpc_max_queue_length(struct mgos_config *cfg, int v) { cfg->rpc.max_queue_length = v; }

/* rpc.max_non_persistent_channels */
int mgos_config_get_rpc_max_non_persistent_channels(const struct mgos_config *cfg) { return cfg->rpc.max_non_persistent_channels; }
int mgos_config_get_default_rpc_max_non_persistent_channels(void) { return 20; }
void mgos_config_set_rpc_max_non_persistent_channels(struct mgos_config *cfg, int v) { cfg->rpc.max_non_persistent_channels = v; }

/* rpc.default_out_channel_idle_close_timeout */
int mgos_config_get_rpc_default_out_channel_idle_close_timeout(const struct mgos_config *cfg) { return cfg->rpc.default_out_channel_idle_close_timeout; }
int mgos_config_get_default_rpc_default_out_channel_idle_close_timeout(void) { return 10; }
void mgos_config_set_rpc_default_out_channel_idle_close_timeout(struct mgos_config *cfg, int v) { cfg->rpc.default_out_channel_idle_close_timeout = v; }

/* rpc.acl */
const char * mgos_config_get_rpc_acl(const struct mgos_config *cfg) { return cfg->rpc.acl; }
const char * mgos_config_get_default_rpc_acl(void) { return NULL; }
void mgos_config_set_rpc_acl(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.acl, v); }

/* rpc.acl_file */
const char * mgos_config_get_rpc_acl_file(const struct mgos_config *cfg) { return cfg->rpc.acl_file; }
const char * mgos_config_get_default_rpc_acl_file(void) { return NULL; }
void mgos_config_set_rpc_acl_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.acl_file, v); }

/* rpc.auth_domain */
const char * mgos_config_get_rpc_auth_domain(const struct mgos_config *cfg) { return cfg->rpc.auth_domain; }
const char * mgos_config_get_default_rpc_auth_domain(void) { return "RPC"; }
void mgos_config_set_rpc_auth_domain(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.auth_domain, v); }

/* rpc.auth_file */
const char * mgos_config_get_rpc_auth_file(const struct mgos_config *cfg) { return cfg->rpc.auth_file; }
const char * mgos_config_get_default_rpc_auth_file(void) { return NULL; }
void mgos_config_set_rpc_auth_file(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.auth_file, v); }

/* rpc.auth_algo */
int mgos_config_get_rpc_auth_algo(const struct mgos_config *cfg) { return cfg->rpc.auth_algo; }
int mgos_config_get_default_rpc_auth_algo(void) { return 0; }
void mgos_config_set_rpc_auth_algo(struct mgos_config *cfg, int v) { cfg->rpc.auth_algo = v; }

/* rpc.uart */
const struct mgos_config_rpc_uart *mgos_config_get_rpc_uart(const struct mgos_config *cfg) { return &cfg->rpc.uart; }

/* rpc.uart.uart_no */
int mgos_config_get_rpc_uart_uart_no(const struct mgos_config *cfg) { return cfg->rpc.uart.uart_no; }
int mgos_config_get_default_rpc_uart_uart_no(void) { return 0; }
void mgos_config_set_rpc_uart_uart_no(struct mgos_config *cfg, int v) { cfg->rpc.uart.uart_no = v; }

/* rpc.uart.baud_rate */
int mgos_config_get_rpc_uart_baud_rate(const struct mgos_config *cfg) { return cfg->rpc.uart.baud_rate; }
int mgos_config_get_default_rpc_uart_baud_rate(void) { return 0; }
void mgos_config_set_rpc_uart_baud_rate(struct mgos_config *cfg, int v) { cfg->rpc.uart.baud_rate = v; }

/* rpc.uart.fc_type */
const char * mgos_config_get_rpc_uart_fc_type(const struct mgos_config *cfg) { return cfg->rpc.uart.fc_type; }
const char * mgos_config_get_default_rpc_uart_fc_type(void) { return NULL; }
void mgos_config_set_rpc_uart_fc_type(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.uart.fc_type, v); }

/* rpc.uart.dst */
const char * mgos_config_get_rpc_uart_dst(const struct mgos_config *cfg) { return cfg->rpc.uart.dst; }
const char * mgos_config_get_default_rpc_uart_dst(void) { return NULL; }
void mgos_config_set_rpc_uart_dst(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->rpc.uart.dst, v); }

/* rpc.uart.enable */
int mgos_config_get_rpc_uart_enable(const struct mgos_config *cfg) { return cfg->rpc.uart.enable; }
int mgos_config_get_default_rpc_uart_enable(void) { return false; }
void mgos_config_set_rpc_uart_enable(struct mgos_config *cfg, int v) { cfg->rpc.uart.enable = v; }

/* rpc.uart.no_delay */
int mgos_config_get_rpc_uart_no_delay(const struct mgos_config *cfg) { return cfg->rpc.uart.no_delay; }
int mgos_config_get_default_rpc_uart_no_delay(void) { return false; }
void mgos_config_set_rpc_uart_no_delay(struct mgos_config *cfg, int v) { cfg->rpc.uart.no_delay = v; }

/* rpc.uart.rx_buf_size */
int mgos_config_get_rpc_uart_rx_buf_size(const struct mgos_config *cfg) { return cfg->rpc.uart.rx_buf_size; }
int mgos_config_get_default_rpc_uart_rx_buf_size(void) { return 0; }
void mgos_config_set_rpc_uart_rx_buf_size(struct mgos_config *cfg, int v) { cfg->rpc.uart.rx_buf_size = v; }

/* rpc.uart.tx_buf_size */
int mgos_config_get_rpc_uart_tx_buf_size(const struct mgos_config *cfg) { return cfg->rpc.uart.tx_buf_size; }
int mgos_config_get_default_rpc_uart_tx_buf_size(void) { return 0; }
void mgos_config_set_rpc_uart_tx_buf_size(struct mgos_config *cfg, int v) { cfg->rpc.uart.tx_buf_size = v; }

/* wifi */
const struct mgos_config_wifi *mgos_config_get_wifi(const struct mgos_config *cfg) { return &cfg->wifi; }

/* wifi.ap */
const struct mgos_config_wifi_ap *mgos_config_get_wifi_ap(const struct mgos_config *cfg) { return &cfg->wifi.ap; }

/* wifi.ap.enable */
int mgos_config_get_wifi_ap_enable(const struct mgos_config *cfg) { return cfg->wifi.ap.enable; }
int mgos_config_get_default_wifi_ap_enable(void) { return false; }
void mgos_config_set_wifi_ap_enable(struct mgos_config *cfg, int v) { cfg->wifi.ap.enable = v; }

/* wifi.ap.ssid */
const char * mgos_config_get_wifi_ap_ssid(const struct mgos_config *cfg) { return cfg->wifi.ap.ssid; }
const char * mgos_config_get_default_wifi_ap_ssid(void) { return NULL; }
void mgos_config_set_wifi_ap_ssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.ssid, v); }

/* wifi.ap.pass */
const char * mgos_config_get_wifi_ap_pass(const struct mgos_config *cfg) { return cfg->wifi.ap.pass; }
const char * mgos_config_get_default_wifi_ap_pass(void) { return NULL; }
void mgos_config_set_wifi_ap_pass(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.pass, v); }

/* wifi.ap.hidden */
int mgos_config_get_wifi_ap_hidden(const struct mgos_config *cfg) { return cfg->wifi.ap.hidden; }
int mgos_config_get_default_wifi_ap_hidden(void) { return false; }
void mgos_config_set_wifi_ap_hidden(struct mgos_config *cfg, int v) { cfg->wifi.ap.hidden = v; }

/* wifi.ap.channel */
int mgos_config_get_wifi_ap_channel(const struct mgos_config *cfg) { return cfg->wifi.ap.channel; }
int mgos_config_get_default_wifi_ap_channel(void) { return 6; }
void mgos_config_set_wifi_ap_channel(struct mgos_config *cfg, int v) { cfg->wifi.ap.channel = v; }

/* wifi.ap.max_connections */
int mgos_config_get_wifi_ap_max_connections(const struct mgos_config *cfg) { return cfg->wifi.ap.max_connections; }
int mgos_config_get_default_wifi_ap_max_connections(void) { return 10; }
void mgos_config_set_wifi_ap_max_connections(struct mgos_config *cfg, int v) { cfg->wifi.ap.max_connections = v; }

/* wifi.ap.ip */
const char * mgos_config_get_wifi_ap_ip(const struct mgos_config *cfg) { return cfg->wifi.ap.ip; }
const char * mgos_config_get_default_wifi_ap_ip(void) { return "192.168.4.1"; }
void mgos_config_set_wifi_ap_ip(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.ip, v); }

/* wifi.ap.netmask */
const char * mgos_config_get_wifi_ap_netmask(const struct mgos_config *cfg) { return cfg->wifi.ap.netmask; }
const char * mgos_config_get_default_wifi_ap_netmask(void) { return "255.255.255.0"; }
void mgos_config_set_wifi_ap_netmask(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.netmask, v); }

/* wifi.ap.gw */
const char * mgos_config_get_wifi_ap_gw(const struct mgos_config *cfg) { return cfg->wifi.ap.gw; }
const char * mgos_config_get_default_wifi_ap_gw(void) { return "192.168.4.1"; }
void mgos_config_set_wifi_ap_gw(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.gw, v); }

/* wifi.ap.dhcp_start */
const char * mgos_config_get_wifi_ap_dhcp_start(const struct mgos_config *cfg) { return cfg->wifi.ap.dhcp_start; }
const char * mgos_config_get_default_wifi_ap_dhcp_start(void) { return "192.168.4.2"; }
void mgos_config_set_wifi_ap_dhcp_start(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.dhcp_start, v); }

/* wifi.ap.dhcp_end */
const char * mgos_config_get_wifi_ap_dhcp_end(const struct mgos_config *cfg) { return cfg->wifi.ap.dhcp_end; }
const char * mgos_config_get_default_wifi_ap_dhcp_end(void) { return "192.168.4.100"; }
void mgos_config_set_wifi_ap_dhcp_end(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.dhcp_end, v); }

/* wifi.ap.trigger_on_gpio */
int mgos_config_get_wifi_ap_trigger_on_gpio(const struct mgos_config *cfg) { return cfg->wifi.ap.trigger_on_gpio; }
int mgos_config_get_default_wifi_ap_trigger_on_gpio(void) { return -1; }
void mgos_config_set_wifi_ap_trigger_on_gpio(struct mgos_config *cfg, int v) { cfg->wifi.ap.trigger_on_gpio = v; }

/* wifi.ap.disable_after */
int mgos_config_get_wifi_ap_disable_after(const struct mgos_config *cfg) { return cfg->wifi.ap.disable_after; }
int mgos_config_get_default_wifi_ap_disable_after(void) { return 0; }
void mgos_config_set_wifi_ap_disable_after(struct mgos_config *cfg, int v) { cfg->wifi.ap.disable_after = v; }

/* wifi.ap.hostname */
const char * mgos_config_get_wifi_ap_hostname(const struct mgos_config *cfg) { return cfg->wifi.ap.hostname; }
const char * mgos_config_get_default_wifi_ap_hostname(void) { return NULL; }
void mgos_config_set_wifi_ap_hostname(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.hostname, v); }

/* wifi.ap.bandwidth_20mhz */
int mgos_config_get_wifi_ap_bandwidth_20mhz(const struct mgos_config *cfg) { return cfg->wifi.ap.bandwidth_20mhz; }
int mgos_config_get_default_wifi_ap_bandwidth_20mhz(void) { return false; }
void mgos_config_set_wifi_ap_bandwidth_20mhz(struct mgos_config *cfg, int v) { cfg->wifi.ap.bandwidth_20mhz = v; }

/* wifi.ap.protocol */
const char * mgos_config_get_wifi_ap_protocol(const struct mgos_config *cfg) { return cfg->wifi.ap.protocol; }
const char * mgos_config_get_default_wifi_ap_protocol(void) { return "BGN"; }
void mgos_config_set_wifi_ap_protocol(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.ap.protocol, v); }

/* wifi.sta */
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta(const struct mgos_config *cfg) { return &cfg->wifi.sta; }

/* wifi.sta.enable */
int mgos_config_get_wifi_sta_enable(const struct mgos_config *cfg) { return cfg->wifi.sta.enable; }
int mgos_config_get_default_wifi_sta_enable(void) { return false; }
void mgos_config_set_wifi_sta_enable(struct mgos_config *cfg, int v) { cfg->wifi.sta.enable = v; }

/* wifi.sta.ssid */
const char * mgos_config_get_wifi_sta_ssid(const struct mgos_config *cfg) { return cfg->wifi.sta.ssid; }
const char * mgos_config_get_default_wifi_sta_ssid(void) { return NULL; }
void mgos_config_set_wifi_sta_ssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.ssid, v); }

/* wifi.sta.pass */
const char * mgos_config_get_wifi_sta_pass(const struct mgos_config *cfg) { return cfg->wifi.sta.pass; }
const char * mgos_config_get_default_wifi_sta_pass(void) { return NULL; }
void mgos_config_set_wifi_sta_pass(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.pass, v); }

/* wifi.sta.bssid */
const char * mgos_config_get_wifi_sta_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta.bssid; }
const char * mgos_config_get_default_wifi_sta_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.bssid, v); }

/* wifi.sta.channel */
int mgos_config_get_wifi_sta_channel(const struct mgos_config *cfg) { return cfg->wifi.sta.channel; }
int mgos_config_get_default_wifi_sta_channel(void) { return 0; }
void mgos_config_set_wifi_sta_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta.channel = v; }

/* wifi.sta.last_bssid */
const char * mgos_config_get_wifi_sta_last_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta.last_bssid; }
const char * mgos_config_get_default_wifi_sta_last_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta_last_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.last_bssid, v); }

/* wifi.sta.last_channel */
int mgos_config_get_wifi_sta_last_channel(const struct mgos_config *cfg) { return cfg->wifi.sta.last_channel; }
int mgos_config_get_default_wifi_sta_last_channel(void) { return 0; }
void mgos_config_set_wifi_sta_last_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta.last_channel = v; }

/* wifi.sta.user */
const char * mgos_config_get_wifi_sta_user(const struct mgos_config *cfg) { return cfg->wifi.sta.user; }
const char * mgos_config_get_default_wifi_sta_user(void) { return NULL; }
void mgos_config_set_wifi_sta_user(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.user, v); }

/* wifi.sta.anon_identity */
const char * mgos_config_get_wifi_sta_anon_identity(const struct mgos_config *cfg) { return cfg->wifi.sta.anon_identity; }
const char * mgos_config_get_default_wifi_sta_anon_identity(void) { return NULL; }
void mgos_config_set_wifi_sta_anon_identity(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.anon_identity, v); }

/* wifi.sta.cert */
const char * mgos_config_get_wifi_sta_cert(const struct mgos_config *cfg) { return cfg->wifi.sta.cert; }
const char * mgos_config_get_default_wifi_sta_cert(void) { return NULL; }
void mgos_config_set_wifi_sta_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.cert, v); }

/* wifi.sta.key */
const char * mgos_config_get_wifi_sta_key(const struct mgos_config *cfg) { return cfg->wifi.sta.key; }
const char * mgos_config_get_default_wifi_sta_key(void) { return NULL; }
void mgos_config_set_wifi_sta_key(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.key, v); }

/* wifi.sta.ca_cert */
const char * mgos_config_get_wifi_sta_ca_cert(const struct mgos_config *cfg) { return cfg->wifi.sta.ca_cert; }
const char * mgos_config_get_default_wifi_sta_ca_cert(void) { return NULL; }
void mgos_config_set_wifi_sta_ca_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.ca_cert, v); }

/* wifi.sta.ip */
const char * mgos_config_get_wifi_sta_ip(const struct mgos_config *cfg) { return cfg->wifi.sta.ip; }
const char * mgos_config_get_default_wifi_sta_ip(void) { return NULL; }
void mgos_config_set_wifi_sta_ip(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.ip, v); }

/* wifi.sta.netmask */
const char * mgos_config_get_wifi_sta_netmask(const struct mgos_config *cfg) { return cfg->wifi.sta.netmask; }
const char * mgos_config_get_default_wifi_sta_netmask(void) { return NULL; }
void mgos_config_set_wifi_sta_netmask(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.netmask, v); }

/* wifi.sta.gw */
const char * mgos_config_get_wifi_sta_gw(const struct mgos_config *cfg) { return cfg->wifi.sta.gw; }
const char * mgos_config_get_default_wifi_sta_gw(void) { return NULL; }
void mgos_config_set_wifi_sta_gw(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.gw, v); }

/* wifi.sta.nameserver */
const char * mgos_config_get_wifi_sta_nameserver(const struct mgos_config *cfg) { return cfg->wifi.sta.nameserver; }
const char * mgos_config_get_default_wifi_sta_nameserver(void) { return NULL; }
void mgos_config_set_wifi_sta_nameserver(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.nameserver, v); }

/* wifi.sta.dhcp_hostname */
const char * mgos_config_get_wifi_sta_dhcp_hostname(const struct mgos_config *cfg) { return cfg->wifi.sta.dhcp_hostname; }
const char * mgos_config_get_default_wifi_sta_dhcp_hostname(void) { return NULL; }
void mgos_config_set_wifi_sta_dhcp_hostname(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.dhcp_hostname, v); }

/* wifi.sta.protocol */
const char * mgos_config_get_wifi_sta_protocol(const struct mgos_config *cfg) { return cfg->wifi.sta.protocol; }
const char * mgos_config_get_default_wifi_sta_protocol(void) { return "BGN"; }
void mgos_config_set_wifi_sta_protocol(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta.protocol, v); }

/* wifi.sta.listen_interval_ms */
int mgos_config_get_wifi_sta_listen_interval_ms(const struct mgos_config *cfg) { return cfg->wifi.sta.listen_interval_ms; }
int mgos_config_get_default_wifi_sta_listen_interval_ms(void) { return 0; }
void mgos_config_set_wifi_sta_listen_interval_ms(struct mgos_config *cfg, int v) { cfg->wifi.sta.listen_interval_ms = v; }

/* wifi.sta1 */
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta1(const struct mgos_config *cfg) { return &cfg->wifi.sta1; }

/* wifi.sta1.enable */
int mgos_config_get_wifi_sta1_enable(const struct mgos_config *cfg) { return cfg->wifi.sta1.enable; }
int mgos_config_get_default_wifi_sta1_enable(void) { return false; }
void mgos_config_set_wifi_sta1_enable(struct mgos_config *cfg, int v) { cfg->wifi.sta1.enable = v; }

/* wifi.sta1.ssid */
const char * mgos_config_get_wifi_sta1_ssid(const struct mgos_config *cfg) { return cfg->wifi.sta1.ssid; }
const char * mgos_config_get_default_wifi_sta1_ssid(void) { return NULL; }
void mgos_config_set_wifi_sta1_ssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.ssid, v); }

/* wifi.sta1.pass */
const char * mgos_config_get_wifi_sta1_pass(const struct mgos_config *cfg) { return cfg->wifi.sta1.pass; }
const char * mgos_config_get_default_wifi_sta1_pass(void) { return NULL; }
void mgos_config_set_wifi_sta1_pass(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.pass, v); }

/* wifi.sta1.bssid */
const char * mgos_config_get_wifi_sta1_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta1.bssid; }
const char * mgos_config_get_default_wifi_sta1_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta1_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.bssid, v); }

/* wifi.sta1.channel */
int mgos_config_get_wifi_sta1_channel(const struct mgos_config *cfg) { return cfg->wifi.sta1.channel; }
int mgos_config_get_default_wifi_sta1_channel(void) { return 0; }
void mgos_config_set_wifi_sta1_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta1.channel = v; }

/* wifi.sta1.last_bssid */
const char * mgos_config_get_wifi_sta1_last_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta1.last_bssid; }
const char * mgos_config_get_default_wifi_sta1_last_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta1_last_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.last_bssid, v); }

/* wifi.sta1.last_channel */
int mgos_config_get_wifi_sta1_last_channel(const struct mgos_config *cfg) { return cfg->wifi.sta1.last_channel; }
int mgos_config_get_default_wifi_sta1_last_channel(void) { return 0; }
void mgos_config_set_wifi_sta1_last_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta1.last_channel = v; }

/* wifi.sta1.user */
const char * mgos_config_get_wifi_sta1_user(const struct mgos_config *cfg) { return cfg->wifi.sta1.user; }
const char * mgos_config_get_default_wifi_sta1_user(void) { return NULL; }
void mgos_config_set_wifi_sta1_user(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.user, v); }

/* wifi.sta1.anon_identity */
const char * mgos_config_get_wifi_sta1_anon_identity(const struct mgos_config *cfg) { return cfg->wifi.sta1.anon_identity; }
const char * mgos_config_get_default_wifi_sta1_anon_identity(void) { return NULL; }
void mgos_config_set_wifi_sta1_anon_identity(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.anon_identity, v); }

/* wifi.sta1.cert */
const char * mgos_config_get_wifi_sta1_cert(const struct mgos_config *cfg) { return cfg->wifi.sta1.cert; }
const char * mgos_config_get_default_wifi_sta1_cert(void) { return NULL; }
void mgos_config_set_wifi_sta1_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.cert, v); }

/* wifi.sta1.key */
const char * mgos_config_get_wifi_sta1_key(const struct mgos_config *cfg) { return cfg->wifi.sta1.key; }
const char * mgos_config_get_default_wifi_sta1_key(void) { return NULL; }
void mgos_config_set_wifi_sta1_key(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.key, v); }

/* wifi.sta1.ca_cert */
const char * mgos_config_get_wifi_sta1_ca_cert(const struct mgos_config *cfg) { return cfg->wifi.sta1.ca_cert; }
const char * mgos_config_get_default_wifi_sta1_ca_cert(void) { return NULL; }
void mgos_config_set_wifi_sta1_ca_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.ca_cert, v); }

/* wifi.sta1.ip */
const char * mgos_config_get_wifi_sta1_ip(const struct mgos_config *cfg) { return cfg->wifi.sta1.ip; }
const char * mgos_config_get_default_wifi_sta1_ip(void) { return NULL; }
void mgos_config_set_wifi_sta1_ip(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.ip, v); }

/* wifi.sta1.netmask */
const char * mgos_config_get_wifi_sta1_netmask(const struct mgos_config *cfg) { return cfg->wifi.sta1.netmask; }
const char * mgos_config_get_default_wifi_sta1_netmask(void) { return NULL; }
void mgos_config_set_wifi_sta1_netmask(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.netmask, v); }

/* wifi.sta1.gw */
const char * mgos_config_get_wifi_sta1_gw(const struct mgos_config *cfg) { return cfg->wifi.sta1.gw; }
const char * mgos_config_get_default_wifi_sta1_gw(void) { return NULL; }
void mgos_config_set_wifi_sta1_gw(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.gw, v); }

/* wifi.sta1.nameserver */
const char * mgos_config_get_wifi_sta1_nameserver(const struct mgos_config *cfg) { return cfg->wifi.sta1.nameserver; }
const char * mgos_config_get_default_wifi_sta1_nameserver(void) { return NULL; }
void mgos_config_set_wifi_sta1_nameserver(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.nameserver, v); }

/* wifi.sta1.dhcp_hostname */
const char * mgos_config_get_wifi_sta1_dhcp_hostname(const struct mgos_config *cfg) { return cfg->wifi.sta1.dhcp_hostname; }
const char * mgos_config_get_default_wifi_sta1_dhcp_hostname(void) { return NULL; }
void mgos_config_set_wifi_sta1_dhcp_hostname(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.dhcp_hostname, v); }

/* wifi.sta1.protocol */
const char * mgos_config_get_wifi_sta1_protocol(const struct mgos_config *cfg) { return cfg->wifi.sta1.protocol; }
const char * mgos_config_get_default_wifi_sta1_protocol(void) { return "BGN"; }
void mgos_config_set_wifi_sta1_protocol(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta1.protocol, v); }

/* wifi.sta1.listen_interval_ms */
int mgos_config_get_wifi_sta1_listen_interval_ms(const struct mgos_config *cfg) { return cfg->wifi.sta1.listen_interval_ms; }
int mgos_config_get_default_wifi_sta1_listen_interval_ms(void) { return 0; }
void mgos_config_set_wifi_sta1_listen_interval_ms(struct mgos_config *cfg, int v) { cfg->wifi.sta1.listen_interval_ms = v; }

/* wifi.sta2 */
const struct mgos_config_wifi_sta *mgos_config_get_wifi_sta2(const struct mgos_config *cfg) { return &cfg->wifi.sta2; }

/* wifi.sta2.enable */
int mgos_config_get_wifi_sta2_enable(const struct mgos_config *cfg) { return cfg->wifi.sta2.enable; }
int mgos_config_get_default_wifi_sta2_enable(void) { return false; }
void mgos_config_set_wifi_sta2_enable(struct mgos_config *cfg, int v) { cfg->wifi.sta2.enable = v; }

/* wifi.sta2.ssid */
const char * mgos_config_get_wifi_sta2_ssid(const struct mgos_config *cfg) { return cfg->wifi.sta2.ssid; }
const char * mgos_config_get_default_wifi_sta2_ssid(void) { return NULL; }
void mgos_config_set_wifi_sta2_ssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.ssid, v); }

/* wifi.sta2.pass */
const char * mgos_config_get_wifi_sta2_pass(const struct mgos_config *cfg) { return cfg->wifi.sta2.pass; }
const char * mgos_config_get_default_wifi_sta2_pass(void) { return NULL; }
void mgos_config_set_wifi_sta2_pass(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.pass, v); }

/* wifi.sta2.bssid */
const char * mgos_config_get_wifi_sta2_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta2.bssid; }
const char * mgos_config_get_default_wifi_sta2_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta2_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.bssid, v); }

/* wifi.sta2.channel */
int mgos_config_get_wifi_sta2_channel(const struct mgos_config *cfg) { return cfg->wifi.sta2.channel; }
int mgos_config_get_default_wifi_sta2_channel(void) { return 0; }
void mgos_config_set_wifi_sta2_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta2.channel = v; }

/* wifi.sta2.last_bssid */
const char * mgos_config_get_wifi_sta2_last_bssid(const struct mgos_config *cfg) { return cfg->wifi.sta2.last_bssid; }
const char * mgos_config_get_default_wifi_sta2_last_bssid(void) { return NULL; }
void mgos_config_set_wifi_sta2_last_bssid(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.last_bssid, v); }

/* wifi.sta2.last_channel */
int mgos_config_get_wifi_sta2_last_channel(const struct mgos_config *cfg) { return cfg->wifi.sta2.last_channel; }
int mgos_config_get_default_wifi_sta2_last_channel(void) { return 0; }
void mgos_config_set_wifi_sta2_last_channel(struct mgos_config *cfg, int v) { cfg->wifi.sta2.last_channel = v; }

/* wifi.sta2.user */
const char * mgos_config_get_wifi_sta2_user(const struct mgos_config *cfg) { return cfg->wifi.sta2.user; }
const char * mgos_config_get_default_wifi_sta2_user(void) { return NULL; }
void mgos_config_set_wifi_sta2_user(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.user, v); }

/* wifi.sta2.anon_identity */
const char * mgos_config_get_wifi_sta2_anon_identity(const struct mgos_config *cfg) { return cfg->wifi.sta2.anon_identity; }
const char * mgos_config_get_default_wifi_sta2_anon_identity(void) { return NULL; }
void mgos_config_set_wifi_sta2_anon_identity(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.anon_identity, v); }

/* wifi.sta2.cert */
const char * mgos_config_get_wifi_sta2_cert(const struct mgos_config *cfg) { return cfg->wifi.sta2.cert; }
const char * mgos_config_get_default_wifi_sta2_cert(void) { return NULL; }
void mgos_config_set_wifi_sta2_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.cert, v); }

/* wifi.sta2.key */
const char * mgos_config_get_wifi_sta2_key(const struct mgos_config *cfg) { return cfg->wifi.sta2.key; }
const char * mgos_config_get_default_wifi_sta2_key(void) { return NULL; }
void mgos_config_set_wifi_sta2_key(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.key, v); }

/* wifi.sta2.ca_cert */
const char * mgos_config_get_wifi_sta2_ca_cert(const struct mgos_config *cfg) { return cfg->wifi.sta2.ca_cert; }
const char * mgos_config_get_default_wifi_sta2_ca_cert(void) { return NULL; }
void mgos_config_set_wifi_sta2_ca_cert(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.ca_cert, v); }

/* wifi.sta2.ip */
const char * mgos_config_get_wifi_sta2_ip(const struct mgos_config *cfg) { return cfg->wifi.sta2.ip; }
const char * mgos_config_get_default_wifi_sta2_ip(void) { return NULL; }
void mgos_config_set_wifi_sta2_ip(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.ip, v); }

/* wifi.sta2.netmask */
const char * mgos_config_get_wifi_sta2_netmask(const struct mgos_config *cfg) { return cfg->wifi.sta2.netmask; }
const char * mgos_config_get_default_wifi_sta2_netmask(void) { return NULL; }
void mgos_config_set_wifi_sta2_netmask(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.netmask, v); }

/* wifi.sta2.gw */
const char * mgos_config_get_wifi_sta2_gw(const struct mgos_config *cfg) { return cfg->wifi.sta2.gw; }
const char * mgos_config_get_default_wifi_sta2_gw(void) { return NULL; }
void mgos_config_set_wifi_sta2_gw(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.gw, v); }

/* wifi.sta2.nameserver */
const char * mgos_config_get_wifi_sta2_nameserver(const struct mgos_config *cfg) { return cfg->wifi.sta2.nameserver; }
const char * mgos_config_get_default_wifi_sta2_nameserver(void) { return NULL; }
void mgos_config_set_wifi_sta2_nameserver(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.nameserver, v); }

/* wifi.sta2.dhcp_hostname */
const char * mgos_config_get_wifi_sta2_dhcp_hostname(const struct mgos_config *cfg) { return cfg->wifi.sta2.dhcp_hostname; }
const char * mgos_config_get_default_wifi_sta2_dhcp_hostname(void) { return NULL; }
void mgos_config_set_wifi_sta2_dhcp_hostname(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.dhcp_hostname, v); }

/* wifi.sta2.protocol */
const char * mgos_config_get_wifi_sta2_protocol(const struct mgos_config *cfg) { return cfg->wifi.sta2.protocol; }
const char * mgos_config_get_default_wifi_sta2_protocol(void) { return "BGN"; }
void mgos_config_set_wifi_sta2_protocol(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->wifi.sta2.protocol, v); }

/* wifi.sta2.listen_interval_ms */
int mgos_config_get_wifi_sta2_listen_interval_ms(const struct mgos_config *cfg) { return cfg->wifi.sta2.listen_interval_ms; }
int mgos_config_get_default_wifi_sta2_listen_interval_ms(void) { return 0; }
void mgos_config_set_wifi_sta2_listen_interval_ms(struct mgos_config *cfg, int v) { cfg->wifi.sta2.listen_interval_ms = v; }

/* wifi.sta_rssi_thr */
int mgos_config_get_wifi_sta_rssi_thr(const struct mgos_config *cfg) { return cfg->wifi.sta_rssi_thr; }
int mgos_config_get_default_wifi_sta_rssi_thr(void) { return -95; }
void mgos_config_set_wifi_sta_rssi_thr(struct mgos_config *cfg, int v) { cfg->wifi.sta_rssi_thr = v; }

/* wifi.sta_connect_timeout */
int mgos_config_get_wifi_sta_connect_timeout(const struct mgos_config *cfg) { return cfg->wifi.sta_connect_timeout; }
int mgos_config_get_default_wifi_sta_connect_timeout(void) { return 15; }
void mgos_config_set_wifi_sta_connect_timeout(struct mgos_config *cfg, int v) { cfg->wifi.sta_connect_timeout = v; }

/* wifi.sta_roam_rssi_thr */
int mgos_config_get_wifi_sta_roam_rssi_thr(const struct mgos_config *cfg) { return cfg->wifi.sta_roam_rssi_thr; }
int mgos_config_get_default_wifi_sta_roam_rssi_thr(void) { return -80; }
void mgos_config_set_wifi_sta_roam_rssi_thr(struct mgos_config *cfg, int v) { cfg->wifi.sta_roam_rssi_thr = v; }

/* wifi.sta_roam_interval */
int mgos_config_get_wifi_sta_roam_interval(const struct mgos_config *cfg) { return cfg->wifi.sta_roam_interval; }
int mgos_config_get_default_wifi_sta_roam_interval(void) { return 0; }
void mgos_config_set_wifi_sta_roam_interval(struct mgos_config *cfg, int v) { cfg->wifi.sta_roam_interval = v; }

/* wifi.sta_ps_mode */
int mgos_config_get_wifi_sta_ps_mode(const struct mgos_config *cfg) { return cfg->wifi.sta_ps_mode; }
int mgos_config_get_default_wifi_sta_ps_mode(void) { return 0; }
void mgos_config_set_wifi_sta_ps_mode(struct mgos_config *cfg, int v) { cfg->wifi.sta_ps_mode = v; }

/* sntp */
const struct mgos_config_sntp *mgos_config_get_sntp(const struct mgos_config *cfg) { return &cfg->sntp; }

/* sntp.enable */
int mgos_config_get_sntp_enable(const struct mgos_config *cfg) { return cfg->sntp.enable; }
int mgos_config_get_default_sntp_enable(void) { return true; }
void mgos_config_set_sntp_enable(struct mgos_config *cfg, int v) { cfg->sntp.enable = v; }

/* sntp.server */
const char * mgos_config_get_sntp_server(const struct mgos_config *cfg) { return cfg->sntp.server; }
const char * mgos_config_get_default_sntp_server(void) { return "time.google.com"; }
void mgos_config_set_sntp_server(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->sntp.server, v); }

/* sntp.use_dhcp_ntp_server */
int mgos_config_get_sntp_use_dhcp_ntp_server(const struct mgos_config *cfg) { return cfg->sntp.use_dhcp_ntp_server; }
int mgos_config_get_default_sntp_use_dhcp_ntp_server(void) { return true; }
void mgos_config_set_sntp_use_dhcp_ntp_server(struct mgos_config *cfg, int v) { cfg->sntp.use_dhcp_ntp_server = v; }

/* sntp.retry_min */
int mgos_config_get_sntp_retry_min(const struct mgos_config *cfg) { return cfg->sntp.retry_min; }
int mgos_config_get_default_sntp_retry_min(void) { return 1; }
void mgos_config_set_sntp_retry_min(struct mgos_config *cfg, int v) { cfg->sntp.retry_min = v; }

/* sntp.retry_max */
int mgos_config_get_sntp_retry_max(const struct mgos_config *cfg) { return cfg->sntp.retry_max; }
int mgos_config_get_default_sntp_retry_max(void) { return 30; }
void mgos_config_set_sntp_retry_max(struct mgos_config *cfg, int v) { cfg->sntp.retry_max = v; }

/* sntp.update_interval */
int mgos_config_get_sntp_update_interval(const struct mgos_config *cfg) { return cfg->sntp.update_interval; }
int mgos_config_get_default_sntp_update_interval(void) { return 7200; }
void mgos_config_set_sntp_update_interval(struct mgos_config *cfg, int v) { cfg->sntp.update_interval = v; }

/* app */
const struct mgos_config_app *mgos_config_get_app(const struct mgos_config *cfg) { return &cfg->app; }

/* app.name */
const char * mgos_config_get_app_name(const struct mgos_config *cfg) { return cfg->app.name; }
const char * mgos_config_get_default_app_name(void) { return NULL; }
void mgos_config_set_app_name(struct mgos_config *cfg, const char * v) { mgos_conf_set_str(&cfg->app.name, v); }
bool mgos_sys_config_get(const struct mg_str key, struct mg_str *value) {
  return mgos_config_get(key, value, &mgos_sys_config, mgos_config_schema());
}
bool mgos_sys_config_set(const struct mg_str key, const struct mg_str value, bool free_strings) {
  return mgos_config_set(key, value, &mgos_sys_config, mgos_config_schema(), free_strings);
}

const struct mgos_conf_entry *mgos_config_schema(void) {
  return mgos_config_get_schema();
}

/* Strings */
static const char *mgos_config_str_table[] = {
  "*",
  "/",
  "192.168.4.1",
  "192.168.4.100",
  "192.168.4.2",
  "255.255.255.0",
  "80",
  "BGN",
  "RPC",
  "bedcontroller",
  "ca.pem",
  "esp32_??????",
  "time.google.com",
};

bool mgos_config_is_default_str(const char *s) {
  int num_str = (sizeof(mgos_config_str_table) / sizeof(mgos_config_str_table[0]));
  for (int i = 0; i < num_str; i++) {
    if (mgos_config_str_table[i] == s) return true;
  }
  return false;
}
