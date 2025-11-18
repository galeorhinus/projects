/* clang-format off */
/*
 * Generated file - do not edit.
 * Command: /mongoose-os/tools/mgos_gen_config.py --c_name=mgos_config --c_global_name=mgos_sys_config --dest_dir=/data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_731529549/build/gen/ /mongoose-os/src/mgos_debug_udp_config.yaml /mongoose-os/platforms/esp32/src/esp32_sys_config.yaml /data/fwbuild-volumes/2.20.0/apps/cg-ap-esp32/esp32/build_contexts/build_ctx_731529549/build/gen/mos_conf_schema.yml
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

/* sys.mount type struct mgos_config_sys_mount */
struct mgos_config_sys_mount {
  const char * path;
  const char * dev_type;
  const char * dev_opts;
  const char * fs_type;
  const char * fs_opts;
};
const struct mgos_conf_entry *mgos_config_sys_mount_get_schema(void);
void mgos_config_sys_mount_set_defaults(struct mgos_config_sys_mount *cfg);
static inline bool mgos_config_sys_mount_parse(struct mg_str json, struct mgos_config_sys_mount *cfg) {
  mgos_config_sys_mount_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_sys_mount_get_schema(), cfg);
}
bool mgos_config_sys_mount_parse_f(const char *fname, struct mgos_config_sys_mount *cfg);
static inline bool mgos_config_sys_mount_emit(const struct mgos_config_sys_mount *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_sys_mount_get_schema(), pretty, out);
}
static inline bool mgos_config_sys_mount_emit_f(const struct mgos_config_sys_mount *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_sys_mount_get_schema(), pretty, fname);
}
static inline bool mgos_config_sys_mount_copy(const struct mgos_config_sys_mount *src, struct mgos_config_sys_mount *dst) {
  return mgos_conf_copy(mgos_config_sys_mount_get_schema(), src, dst);
}
static inline void mgos_config_sys_mount_free(struct mgos_config_sys_mount *cfg) {
  return mgos_conf_free(mgos_config_sys_mount_get_schema(), cfg);
}

/* sys type struct mgos_config_sys */
struct mgos_config_sys {
  const char * tz_spec;
  int wdt_timeout;
  const char * pref_ota_lib;
  struct mgos_config_sys_mount mount;
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

/* devtab.dev0 type struct mgos_config_devtab_dev0 */
struct mgos_config_devtab_dev0 {
  const char * name;
  const char * type;
  const char * opts;
};
const struct mgos_conf_entry *mgos_config_devtab_dev0_get_schema(void);
void mgos_config_devtab_dev0_set_defaults(struct mgos_config_devtab_dev0 *cfg);
static inline bool mgos_config_devtab_dev0_parse(struct mg_str json, struct mgos_config_devtab_dev0 *cfg) {
  mgos_config_devtab_dev0_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_dev0_get_schema(), cfg);
}
bool mgos_config_devtab_dev0_parse_f(const char *fname, struct mgos_config_devtab_dev0 *cfg);
static inline bool mgos_config_devtab_dev0_emit(const struct mgos_config_devtab_dev0 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_dev0_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_dev0_emit_f(const struct mgos_config_devtab_dev0 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_dev0_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_dev0_copy(const struct mgos_config_devtab_dev0 *src, struct mgos_config_devtab_dev0 *dst) {
  return mgos_conf_copy(mgos_config_devtab_dev0_get_schema(), src, dst);
}
static inline void mgos_config_devtab_dev0_free(struct mgos_config_devtab_dev0 *cfg) {
  return mgos_conf_free(mgos_config_devtab_dev0_get_schema(), cfg);
}

/* devtab.dev1 type struct mgos_config_devtab_dev1 */
struct mgos_config_devtab_dev1 {
  const char * name;
  const char * type;
  const char * opts;
};
const struct mgos_conf_entry *mgos_config_devtab_dev1_get_schema(void);
void mgos_config_devtab_dev1_set_defaults(struct mgos_config_devtab_dev1 *cfg);
static inline bool mgos_config_devtab_dev1_parse(struct mg_str json, struct mgos_config_devtab_dev1 *cfg) {
  mgos_config_devtab_dev1_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_dev1_get_schema(), cfg);
}
bool mgos_config_devtab_dev1_parse_f(const char *fname, struct mgos_config_devtab_dev1 *cfg);
static inline bool mgos_config_devtab_dev1_emit(const struct mgos_config_devtab_dev1 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_dev1_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_dev1_emit_f(const struct mgos_config_devtab_dev1 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_dev1_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_dev1_copy(const struct mgos_config_devtab_dev1 *src, struct mgos_config_devtab_dev1 *dst) {
  return mgos_conf_copy(mgos_config_devtab_dev1_get_schema(), src, dst);
}
static inline void mgos_config_devtab_dev1_free(struct mgos_config_devtab_dev1 *cfg) {
  return mgos_conf_free(mgos_config_devtab_dev1_get_schema(), cfg);
}

/* devtab.dev2 type struct mgos_config_devtab_dev2 */
struct mgos_config_devtab_dev2 {
  const char * name;
  const char * type;
  const char * opts;
};
const struct mgos_conf_entry *mgos_config_devtab_dev2_get_schema(void);
void mgos_config_devtab_dev2_set_defaults(struct mgos_config_devtab_dev2 *cfg);
static inline bool mgos_config_devtab_dev2_parse(struct mg_str json, struct mgos_config_devtab_dev2 *cfg) {
  mgos_config_devtab_dev2_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_dev2_get_schema(), cfg);
}
bool mgos_config_devtab_dev2_parse_f(const char *fname, struct mgos_config_devtab_dev2 *cfg);
static inline bool mgos_config_devtab_dev2_emit(const struct mgos_config_devtab_dev2 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_dev2_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_dev2_emit_f(const struct mgos_config_devtab_dev2 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_dev2_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_dev2_copy(const struct mgos_config_devtab_dev2 *src, struct mgos_config_devtab_dev2 *dst) {
  return mgos_conf_copy(mgos_config_devtab_dev2_get_schema(), src, dst);
}
static inline void mgos_config_devtab_dev2_free(struct mgos_config_devtab_dev2 *cfg) {
  return mgos_conf_free(mgos_config_devtab_dev2_get_schema(), cfg);
}

/* devtab.dev3 type struct mgos_config_devtab_dev3 */
struct mgos_config_devtab_dev3 {
  const char * name;
  const char * type;
  const char * opts;
};
const struct mgos_conf_entry *mgos_config_devtab_dev3_get_schema(void);
void mgos_config_devtab_dev3_set_defaults(struct mgos_config_devtab_dev3 *cfg);
static inline bool mgos_config_devtab_dev3_parse(struct mg_str json, struct mgos_config_devtab_dev3 *cfg) {
  mgos_config_devtab_dev3_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_dev3_get_schema(), cfg);
}
bool mgos_config_devtab_dev3_parse_f(const char *fname, struct mgos_config_devtab_dev3 *cfg);
static inline bool mgos_config_devtab_dev3_emit(const struct mgos_config_devtab_dev3 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_dev3_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_dev3_emit_f(const struct mgos_config_devtab_dev3 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_dev3_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_dev3_copy(const struct mgos_config_devtab_dev3 *src, struct mgos_config_devtab_dev3 *dst) {
  return mgos_conf_copy(mgos_config_devtab_dev3_get_schema(), src, dst);
}
static inline void mgos_config_devtab_dev3_free(struct mgos_config_devtab_dev3 *cfg) {
  return mgos_conf_free(mgos_config_devtab_dev3_get_schema(), cfg);
}

/* devtab.dev4 type struct mgos_config_devtab_dev4 */
struct mgos_config_devtab_dev4 {
  const char * name;
  const char * type;
  const char * opts;
};
const struct mgos_conf_entry *mgos_config_devtab_dev4_get_schema(void);
void mgos_config_devtab_dev4_set_defaults(struct mgos_config_devtab_dev4 *cfg);
static inline bool mgos_config_devtab_dev4_parse(struct mg_str json, struct mgos_config_devtab_dev4 *cfg) {
  mgos_config_devtab_dev4_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_dev4_get_schema(), cfg);
}
bool mgos_config_devtab_dev4_parse_f(const char *fname, struct mgos_config_devtab_dev4 *cfg);
static inline bool mgos_config_devtab_dev4_emit(const struct mgos_config_devtab_dev4 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_dev4_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_dev4_emit_f(const struct mgos_config_devtab_dev4 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_dev4_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_dev4_copy(const struct mgos_config_devtab_dev4 *src, struct mgos_config_devtab_dev4 *dst) {
  return mgos_conf_copy(mgos_config_devtab_dev4_get_schema(), src, dst);
}
static inline void mgos_config_devtab_dev4_free(struct mgos_config_devtab_dev4 *cfg) {
  return mgos_conf_free(mgos_config_devtab_dev4_get_schema(), cfg);
}

/* devtab type struct mgos_config_devtab */
struct mgos_config_devtab {
  struct mgos_config_devtab_dev0 dev0;
  struct mgos_config_devtab_dev1 dev1;
  struct mgos_config_devtab_dev2 dev2;
  struct mgos_config_devtab_dev3 dev3;
  struct mgos_config_devtab_dev4 dev4;
};
const struct mgos_conf_entry *mgos_config_devtab_get_schema(void);
void mgos_config_devtab_set_defaults(struct mgos_config_devtab *cfg);
static inline bool mgos_config_devtab_parse(struct mg_str json, struct mgos_config_devtab *cfg) {
  mgos_config_devtab_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_devtab_get_schema(), cfg);
}
bool mgos_config_devtab_parse_f(const char *fname, struct mgos_config_devtab *cfg);
static inline bool mgos_config_devtab_emit(const struct mgos_config_devtab *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_devtab_get_schema(), pretty, out);
}
static inline bool mgos_config_devtab_emit_f(const struct mgos_config_devtab *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_devtab_get_schema(), pretty, fname);
}
static inline bool mgos_config_devtab_copy(const struct mgos_config_devtab *src, struct mgos_config_devtab *dst) {
  return mgos_conf_copy(mgos_config_devtab_get_schema(), src, dst);
}
static inline void mgos_config_devtab_free(struct mgos_config_devtab *cfg) {
  return mgos_conf_free(mgos_config_devtab_get_schema(), cfg);
}

/* fstab.fs0 type struct mgos_config_fstab_fs0 */
struct mgos_config_fstab_fs0 {
  const char * dev;
  const char * type;
  const char * opts;
  const char * path;
  int create;
  int optional;
  int created;
};
const struct mgos_conf_entry *mgos_config_fstab_fs0_get_schema(void);
void mgos_config_fstab_fs0_set_defaults(struct mgos_config_fstab_fs0 *cfg);
static inline bool mgos_config_fstab_fs0_parse(struct mg_str json, struct mgos_config_fstab_fs0 *cfg) {
  mgos_config_fstab_fs0_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_fstab_fs0_get_schema(), cfg);
}
bool mgos_config_fstab_fs0_parse_f(const char *fname, struct mgos_config_fstab_fs0 *cfg);
static inline bool mgos_config_fstab_fs0_emit(const struct mgos_config_fstab_fs0 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_fstab_fs0_get_schema(), pretty, out);
}
static inline bool mgos_config_fstab_fs0_emit_f(const struct mgos_config_fstab_fs0 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_fstab_fs0_get_schema(), pretty, fname);
}
static inline bool mgos_config_fstab_fs0_copy(const struct mgos_config_fstab_fs0 *src, struct mgos_config_fstab_fs0 *dst) {
  return mgos_conf_copy(mgos_config_fstab_fs0_get_schema(), src, dst);
}
static inline void mgos_config_fstab_fs0_free(struct mgos_config_fstab_fs0 *cfg) {
  return mgos_conf_free(mgos_config_fstab_fs0_get_schema(), cfg);
}

/* fstab.fs1 type struct mgos_config_fstab_fs1 */
struct mgos_config_fstab_fs1 {
  const char * dev;
  const char * type;
  const char * opts;
  const char * path;
  int create;
  int optional;
  int created;
};
const struct mgos_conf_entry *mgos_config_fstab_fs1_get_schema(void);
void mgos_config_fstab_fs1_set_defaults(struct mgos_config_fstab_fs1 *cfg);
static inline bool mgos_config_fstab_fs1_parse(struct mg_str json, struct mgos_config_fstab_fs1 *cfg) {
  mgos_config_fstab_fs1_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_fstab_fs1_get_schema(), cfg);
}
bool mgos_config_fstab_fs1_parse_f(const char *fname, struct mgos_config_fstab_fs1 *cfg);
static inline bool mgos_config_fstab_fs1_emit(const struct mgos_config_fstab_fs1 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_fstab_fs1_get_schema(), pretty, out);
}
static inline bool mgos_config_fstab_fs1_emit_f(const struct mgos_config_fstab_fs1 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_fstab_fs1_get_schema(), pretty, fname);
}
static inline bool mgos_config_fstab_fs1_copy(const struct mgos_config_fstab_fs1 *src, struct mgos_config_fstab_fs1 *dst) {
  return mgos_conf_copy(mgos_config_fstab_fs1_get_schema(), src, dst);
}
static inline void mgos_config_fstab_fs1_free(struct mgos_config_fstab_fs1 *cfg) {
  return mgos_conf_free(mgos_config_fstab_fs1_get_schema(), cfg);
}

/* fstab.fs2 type struct mgos_config_fstab_fs2 */
struct mgos_config_fstab_fs2 {
  const char * dev;
  const char * type;
  const char * opts;
  const char * path;
  int create;
  int optional;
  int created;
};
const struct mgos_conf_entry *mgos_config_fstab_fs2_get_schema(void);
void mgos_config_fstab_fs2_set_defaults(struct mgos_config_fstab_fs2 *cfg);
static inline bool mgos_config_fstab_fs2_parse(struct mg_str json, struct mgos_config_fstab_fs2 *cfg) {
  mgos_config_fstab_fs2_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_fstab_fs2_get_schema(), cfg);
}
bool mgos_config_fstab_fs2_parse_f(const char *fname, struct mgos_config_fstab_fs2 *cfg);
static inline bool mgos_config_fstab_fs2_emit(const struct mgos_config_fstab_fs2 *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_fstab_fs2_get_schema(), pretty, out);
}
static inline bool mgos_config_fstab_fs2_emit_f(const struct mgos_config_fstab_fs2 *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_fstab_fs2_get_schema(), pretty, fname);
}
static inline bool mgos_config_fstab_fs2_copy(const struct mgos_config_fstab_fs2 *src, struct mgos_config_fstab_fs2 *dst) {
  return mgos_conf_copy(mgos_config_fstab_fs2_get_schema(), src, dst);
}
static inline void mgos_config_fstab_fs2_free(struct mgos_config_fstab_fs2 *cfg) {
  return mgos_conf_free(mgos_config_fstab_fs2_get_schema(), cfg);
}

/* fstab type struct mgos_config_fstab */
struct mgos_config_fstab {
  struct mgos_config_fstab_fs0 fs0;
  struct mgos_config_fstab_fs1 fs1;
  struct mgos_config_fstab_fs2 fs2;
};
const struct mgos_conf_entry *mgos_config_fstab_get_schema(void);
void mgos_config_fstab_set_defaults(struct mgos_config_fstab *cfg);
static inline bool mgos_config_fstab_parse(struct mg_str json, struct mgos_config_fstab *cfg) {
  mgos_config_fstab_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_fstab_get_schema(), cfg);
}
bool mgos_config_fstab_parse_f(const char *fname, struct mgos_config_fstab *cfg);
static inline bool mgos_config_fstab_emit(const struct mgos_config_fstab *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_fstab_get_schema(), pretty, out);
}
static inline bool mgos_config_fstab_emit_f(const struct mgos_config_fstab *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_fstab_get_schema(), pretty, fname);
}
static inline bool mgos_config_fstab_copy(const struct mgos_config_fstab *src, struct mgos_config_fstab *dst) {
  return mgos_conf_copy(mgos_config_fstab_get_schema(), src, dst);
}
static inline void mgos_config_fstab_free(struct mgos_config_fstab *cfg) {
  return mgos_conf_free(mgos_config_fstab_get_schema(), cfg);
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
  const char * default_file;
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
  const char * main;
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

/* rpc.uart type struct mgos_config_rpc_uart */
struct mgos_config_rpc_uart {
  int uart_no;
  int baud_rate;
  int fc_type;
  const char * dst;
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

/* rpc.ws type struct mgos_config_rpc_ws */
struct mgos_config_rpc_ws {
  int enable;
  const char * server_address;
  int reconnect_interval_min;
  int reconnect_interval_max;
  const char * ssl_server_name;
  const char * ssl_cert;
  const char * ssl_key;
  const char * ssl_ca_cert;
};
const struct mgos_conf_entry *mgos_config_rpc_ws_get_schema(void);
void mgos_config_rpc_ws_set_defaults(struct mgos_config_rpc_ws *cfg);
static inline bool mgos_config_rpc_ws_parse(struct mg_str json, struct mgos_config_rpc_ws *cfg) {
  mgos_config_rpc_ws_set_defaults(cfg);
  return mgos_conf_parse_sub(json, mgos_config_rpc_ws_get_schema(), cfg);
}
bool mgos_config_rpc_ws_parse_f(const char *fname, struct mgos_config_rpc_ws *cfg);
static inline bool mgos_config_rpc_ws_emit(const struct mgos_config_rpc_ws *cfg, bool pretty, struct json_out *out) {
  return mgos_conf_emit_json_out(cfg, NULL, mgos_config_rpc_ws_get_schema(), pretty, out);
}
static inline bool mgos_config_rpc_ws_emit_f(const struct mgos_config_rpc_ws *cfg, bool pretty, const char *fname) {
  return mgos_conf_emit_f(cfg, NULL, mgos_config_rpc_ws_get_schema(), pretty, fname);
}
static inline bool mgos_config_rpc_ws_copy(const struct mgos_config_rpc_ws *src, struct mgos_config_rpc_ws *dst) {
  return mgos_conf_copy(mgos_config_rpc_ws_get_schema(), src, dst);
}
static inline void mgos_config_rpc_ws_free(struct mgos_config_rpc_ws *cfg) {
  return mgos_conf_free(mgos_config_rpc_ws_get_schema(), cfg);
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
  struct mgos_config_rpc_ws ws;
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

/* <root> type struct mgos_config */
struct mgos_config {
  struct mgos_config_debug debug;
  struct mgos_config_device device;
  struct mgos_config_sys sys;
  const char * conf_acl;
  struct mgos_config_dns_sd dns_sd;
  struct mgos_config_devtab devtab;
  struct mgos_config_fstab fstab;
  struct mgos_config_http http;
  struct mgos_config_mjs mjs;
  struct mgos_config_rpc rpc;
  struct mgos_config_wifi wifi;
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

/* sys.mount */
#define MGOS_CONFIG_HAVE_SYS_MOUNT
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT
const struct mgos_config_sys_mount *mgos_config_get_sys_mount(const struct mgos_config *cfg);
static inline const struct mgos_config_sys_mount *mgos_sys_config_get_sys_mount(void) { return mgos_config_get_sys_mount(&mgos_sys_config); }

/* sys.mount.path */
#define MGOS_CONFIG_HAVE_SYS_MOUNT_PATH
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT_PATH
const char * mgos_config_get_sys_mount_path(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_mount_path(void);
static inline const char * mgos_sys_config_get_sys_mount_path(void) { return mgos_config_get_sys_mount_path(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_mount_path(void) { return mgos_config_get_default_sys_mount_path(); }
void mgos_config_set_sys_mount_path(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_mount_path(const char * v) { mgos_config_set_sys_mount_path(&mgos_sys_config, v); }

/* sys.mount.dev_type */
#define MGOS_CONFIG_HAVE_SYS_MOUNT_DEV_TYPE
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT_DEV_TYPE
const char * mgos_config_get_sys_mount_dev_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_mount_dev_type(void);
static inline const char * mgos_sys_config_get_sys_mount_dev_type(void) { return mgos_config_get_sys_mount_dev_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_mount_dev_type(void) { return mgos_config_get_default_sys_mount_dev_type(); }
void mgos_config_set_sys_mount_dev_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_mount_dev_type(const char * v) { mgos_config_set_sys_mount_dev_type(&mgos_sys_config, v); }

/* sys.mount.dev_opts */
#define MGOS_CONFIG_HAVE_SYS_MOUNT_DEV_OPTS
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT_DEV_OPTS
const char * mgos_config_get_sys_mount_dev_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_mount_dev_opts(void);
static inline const char * mgos_sys_config_get_sys_mount_dev_opts(void) { return mgos_config_get_sys_mount_dev_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_mount_dev_opts(void) { return mgos_config_get_default_sys_mount_dev_opts(); }
void mgos_config_set_sys_mount_dev_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_mount_dev_opts(const char * v) { mgos_config_set_sys_mount_dev_opts(&mgos_sys_config, v); }

/* sys.mount.fs_type */
#define MGOS_CONFIG_HAVE_SYS_MOUNT_FS_TYPE
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT_FS_TYPE
const char * mgos_config_get_sys_mount_fs_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_mount_fs_type(void);
static inline const char * mgos_sys_config_get_sys_mount_fs_type(void) { return mgos_config_get_sys_mount_fs_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_mount_fs_type(void) { return mgos_config_get_default_sys_mount_fs_type(); }
void mgos_config_set_sys_mount_fs_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_mount_fs_type(const char * v) { mgos_config_set_sys_mount_fs_type(&mgos_sys_config, v); }

/* sys.mount.fs_opts */
#define MGOS_CONFIG_HAVE_SYS_MOUNT_FS_OPTS
#define MGOS_SYS_CONFIG_HAVE_SYS_MOUNT_FS_OPTS
const char * mgos_config_get_sys_mount_fs_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_sys_mount_fs_opts(void);
static inline const char * mgos_sys_config_get_sys_mount_fs_opts(void) { return mgos_config_get_sys_mount_fs_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_sys_mount_fs_opts(void) { return mgos_config_get_default_sys_mount_fs_opts(); }
void mgos_config_set_sys_mount_fs_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_sys_mount_fs_opts(const char * v) { mgos_config_set_sys_mount_fs_opts(&mgos_sys_config, v); }

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

/* devtab */
#define MGOS_CONFIG_HAVE_DEVTAB
#define MGOS_SYS_CONFIG_HAVE_DEVTAB
const struct mgos_config_devtab *mgos_config_get_devtab(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab *mgos_sys_config_get_devtab(void) { return mgos_config_get_devtab(&mgos_sys_config); }

/* devtab.dev0 */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV0
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV0
const struct mgos_config_devtab_dev0 *mgos_config_get_devtab_dev0(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab_dev0 *mgos_sys_config_get_devtab_dev0(void) { return mgos_config_get_devtab_dev0(&mgos_sys_config); }

/* devtab.dev0.name */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV0_NAME
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV0_NAME
const char * mgos_config_get_devtab_dev0_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev0_name(void);
static inline const char * mgos_sys_config_get_devtab_dev0_name(void) { return mgos_config_get_devtab_dev0_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev0_name(void) { return mgos_config_get_default_devtab_dev0_name(); }
void mgos_config_set_devtab_dev0_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev0_name(const char * v) { mgos_config_set_devtab_dev0_name(&mgos_sys_config, v); }

/* devtab.dev0.type */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV0_TYPE
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV0_TYPE
const char * mgos_config_get_devtab_dev0_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev0_type(void);
static inline const char * mgos_sys_config_get_devtab_dev0_type(void) { return mgos_config_get_devtab_dev0_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev0_type(void) { return mgos_config_get_default_devtab_dev0_type(); }
void mgos_config_set_devtab_dev0_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev0_type(const char * v) { mgos_config_set_devtab_dev0_type(&mgos_sys_config, v); }

/* devtab.dev0.opts */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV0_OPTS
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV0_OPTS
const char * mgos_config_get_devtab_dev0_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev0_opts(void);
static inline const char * mgos_sys_config_get_devtab_dev0_opts(void) { return mgos_config_get_devtab_dev0_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev0_opts(void) { return mgos_config_get_default_devtab_dev0_opts(); }
void mgos_config_set_devtab_dev0_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev0_opts(const char * v) { mgos_config_set_devtab_dev0_opts(&mgos_sys_config, v); }

/* devtab.dev1 */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV1
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV1
const struct mgos_config_devtab_dev1 *mgos_config_get_devtab_dev1(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab_dev1 *mgos_sys_config_get_devtab_dev1(void) { return mgos_config_get_devtab_dev1(&mgos_sys_config); }

/* devtab.dev1.name */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV1_NAME
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV1_NAME
const char * mgos_config_get_devtab_dev1_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev1_name(void);
static inline const char * mgos_sys_config_get_devtab_dev1_name(void) { return mgos_config_get_devtab_dev1_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev1_name(void) { return mgos_config_get_default_devtab_dev1_name(); }
void mgos_config_set_devtab_dev1_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev1_name(const char * v) { mgos_config_set_devtab_dev1_name(&mgos_sys_config, v); }

/* devtab.dev1.type */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV1_TYPE
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV1_TYPE
const char * mgos_config_get_devtab_dev1_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev1_type(void);
static inline const char * mgos_sys_config_get_devtab_dev1_type(void) { return mgos_config_get_devtab_dev1_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev1_type(void) { return mgos_config_get_default_devtab_dev1_type(); }
void mgos_config_set_devtab_dev1_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev1_type(const char * v) { mgos_config_set_devtab_dev1_type(&mgos_sys_config, v); }

/* devtab.dev1.opts */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV1_OPTS
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV1_OPTS
const char * mgos_config_get_devtab_dev1_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev1_opts(void);
static inline const char * mgos_sys_config_get_devtab_dev1_opts(void) { return mgos_config_get_devtab_dev1_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev1_opts(void) { return mgos_config_get_default_devtab_dev1_opts(); }
void mgos_config_set_devtab_dev1_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev1_opts(const char * v) { mgos_config_set_devtab_dev1_opts(&mgos_sys_config, v); }

/* devtab.dev2 */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV2
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV2
const struct mgos_config_devtab_dev2 *mgos_config_get_devtab_dev2(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab_dev2 *mgos_sys_config_get_devtab_dev2(void) { return mgos_config_get_devtab_dev2(&mgos_sys_config); }

/* devtab.dev2.name */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV2_NAME
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV2_NAME
const char * mgos_config_get_devtab_dev2_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev2_name(void);
static inline const char * mgos_sys_config_get_devtab_dev2_name(void) { return mgos_config_get_devtab_dev2_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev2_name(void) { return mgos_config_get_default_devtab_dev2_name(); }
void mgos_config_set_devtab_dev2_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev2_name(const char * v) { mgos_config_set_devtab_dev2_name(&mgos_sys_config, v); }

/* devtab.dev2.type */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV2_TYPE
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV2_TYPE
const char * mgos_config_get_devtab_dev2_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev2_type(void);
static inline const char * mgos_sys_config_get_devtab_dev2_type(void) { return mgos_config_get_devtab_dev2_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev2_type(void) { return mgos_config_get_default_devtab_dev2_type(); }
void mgos_config_set_devtab_dev2_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev2_type(const char * v) { mgos_config_set_devtab_dev2_type(&mgos_sys_config, v); }

/* devtab.dev2.opts */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV2_OPTS
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV2_OPTS
const char * mgos_config_get_devtab_dev2_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev2_opts(void);
static inline const char * mgos_sys_config_get_devtab_dev2_opts(void) { return mgos_config_get_devtab_dev2_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev2_opts(void) { return mgos_config_get_default_devtab_dev2_opts(); }
void mgos_config_set_devtab_dev2_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev2_opts(const char * v) { mgos_config_set_devtab_dev2_opts(&mgos_sys_config, v); }

/* devtab.dev3 */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV3
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV3
const struct mgos_config_devtab_dev3 *mgos_config_get_devtab_dev3(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab_dev3 *mgos_sys_config_get_devtab_dev3(void) { return mgos_config_get_devtab_dev3(&mgos_sys_config); }

/* devtab.dev3.name */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV3_NAME
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV3_NAME
const char * mgos_config_get_devtab_dev3_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev3_name(void);
static inline const char * mgos_sys_config_get_devtab_dev3_name(void) { return mgos_config_get_devtab_dev3_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev3_name(void) { return mgos_config_get_default_devtab_dev3_name(); }
void mgos_config_set_devtab_dev3_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev3_name(const char * v) { mgos_config_set_devtab_dev3_name(&mgos_sys_config, v); }

/* devtab.dev3.type */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV3_TYPE
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV3_TYPE
const char * mgos_config_get_devtab_dev3_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev3_type(void);
static inline const char * mgos_sys_config_get_devtab_dev3_type(void) { return mgos_config_get_devtab_dev3_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev3_type(void) { return mgos_config_get_default_devtab_dev3_type(); }
void mgos_config_set_devtab_dev3_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev3_type(const char * v) { mgos_config_set_devtab_dev3_type(&mgos_sys_config, v); }

/* devtab.dev3.opts */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV3_OPTS
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV3_OPTS
const char * mgos_config_get_devtab_dev3_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev3_opts(void);
static inline const char * mgos_sys_config_get_devtab_dev3_opts(void) { return mgos_config_get_devtab_dev3_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev3_opts(void) { return mgos_config_get_default_devtab_dev3_opts(); }
void mgos_config_set_devtab_dev3_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev3_opts(const char * v) { mgos_config_set_devtab_dev3_opts(&mgos_sys_config, v); }

/* devtab.dev4 */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV4
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV4
const struct mgos_config_devtab_dev4 *mgos_config_get_devtab_dev4(const struct mgos_config *cfg);
static inline const struct mgos_config_devtab_dev4 *mgos_sys_config_get_devtab_dev4(void) { return mgos_config_get_devtab_dev4(&mgos_sys_config); }

/* devtab.dev4.name */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV4_NAME
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV4_NAME
const char * mgos_config_get_devtab_dev4_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev4_name(void);
static inline const char * mgos_sys_config_get_devtab_dev4_name(void) { return mgos_config_get_devtab_dev4_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev4_name(void) { return mgos_config_get_default_devtab_dev4_name(); }
void mgos_config_set_devtab_dev4_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev4_name(const char * v) { mgos_config_set_devtab_dev4_name(&mgos_sys_config, v); }

/* devtab.dev4.type */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV4_TYPE
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV4_TYPE
const char * mgos_config_get_devtab_dev4_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev4_type(void);
static inline const char * mgos_sys_config_get_devtab_dev4_type(void) { return mgos_config_get_devtab_dev4_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev4_type(void) { return mgos_config_get_default_devtab_dev4_type(); }
void mgos_config_set_devtab_dev4_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev4_type(const char * v) { mgos_config_set_devtab_dev4_type(&mgos_sys_config, v); }

/* devtab.dev4.opts */
#define MGOS_CONFIG_HAVE_DEVTAB_DEV4_OPTS
#define MGOS_SYS_CONFIG_HAVE_DEVTAB_DEV4_OPTS
const char * mgos_config_get_devtab_dev4_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_devtab_dev4_opts(void);
static inline const char * mgos_sys_config_get_devtab_dev4_opts(void) { return mgos_config_get_devtab_dev4_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_devtab_dev4_opts(void) { return mgos_config_get_default_devtab_dev4_opts(); }
void mgos_config_set_devtab_dev4_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_devtab_dev4_opts(const char * v) { mgos_config_set_devtab_dev4_opts(&mgos_sys_config, v); }

/* fstab */
#define MGOS_CONFIG_HAVE_FSTAB
#define MGOS_SYS_CONFIG_HAVE_FSTAB
const struct mgos_config_fstab *mgos_config_get_fstab(const struct mgos_config *cfg);
static inline const struct mgos_config_fstab *mgos_sys_config_get_fstab(void) { return mgos_config_get_fstab(&mgos_sys_config); }

/* fstab.fs0 */
#define MGOS_CONFIG_HAVE_FSTAB_FS0
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0
const struct mgos_config_fstab_fs0 *mgos_config_get_fstab_fs0(const struct mgos_config *cfg);
static inline const struct mgos_config_fstab_fs0 *mgos_sys_config_get_fstab_fs0(void) { return mgos_config_get_fstab_fs0(&mgos_sys_config); }

/* fstab.fs0.dev */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_DEV
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_DEV
const char * mgos_config_get_fstab_fs0_dev(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs0_dev(void);
static inline const char * mgos_sys_config_get_fstab_fs0_dev(void) { return mgos_config_get_fstab_fs0_dev(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs0_dev(void) { return mgos_config_get_default_fstab_fs0_dev(); }
void mgos_config_set_fstab_fs0_dev(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs0_dev(const char * v) { mgos_config_set_fstab_fs0_dev(&mgos_sys_config, v); }

/* fstab.fs0.type */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_TYPE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_TYPE
const char * mgos_config_get_fstab_fs0_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs0_type(void);
static inline const char * mgos_sys_config_get_fstab_fs0_type(void) { return mgos_config_get_fstab_fs0_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs0_type(void) { return mgos_config_get_default_fstab_fs0_type(); }
void mgos_config_set_fstab_fs0_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs0_type(const char * v) { mgos_config_set_fstab_fs0_type(&mgos_sys_config, v); }

/* fstab.fs0.opts */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_OPTS
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_OPTS
const char * mgos_config_get_fstab_fs0_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs0_opts(void);
static inline const char * mgos_sys_config_get_fstab_fs0_opts(void) { return mgos_config_get_fstab_fs0_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs0_opts(void) { return mgos_config_get_default_fstab_fs0_opts(); }
void mgos_config_set_fstab_fs0_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs0_opts(const char * v) { mgos_config_set_fstab_fs0_opts(&mgos_sys_config, v); }

/* fstab.fs0.path */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_PATH
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_PATH
const char * mgos_config_get_fstab_fs0_path(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs0_path(void);
static inline const char * mgos_sys_config_get_fstab_fs0_path(void) { return mgos_config_get_fstab_fs0_path(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs0_path(void) { return mgos_config_get_default_fstab_fs0_path(); }
void mgos_config_set_fstab_fs0_path(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs0_path(const char * v) { mgos_config_set_fstab_fs0_path(&mgos_sys_config, v); }

/* fstab.fs0.create */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_CREATE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_CREATE
int mgos_config_get_fstab_fs0_create(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs0_create(void);
static inline int mgos_sys_config_get_fstab_fs0_create(void) { return mgos_config_get_fstab_fs0_create(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs0_create(void) { return mgos_config_get_default_fstab_fs0_create(); }
void mgos_config_set_fstab_fs0_create(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs0_create(int v) { mgos_config_set_fstab_fs0_create(&mgos_sys_config, v); }

/* fstab.fs0.optional */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_OPTIONAL
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_OPTIONAL
int mgos_config_get_fstab_fs0_optional(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs0_optional(void);
static inline int mgos_sys_config_get_fstab_fs0_optional(void) { return mgos_config_get_fstab_fs0_optional(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs0_optional(void) { return mgos_config_get_default_fstab_fs0_optional(); }
void mgos_config_set_fstab_fs0_optional(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs0_optional(int v) { mgos_config_set_fstab_fs0_optional(&mgos_sys_config, v); }

/* fstab.fs0.created */
#define MGOS_CONFIG_HAVE_FSTAB_FS0_CREATED
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS0_CREATED
int mgos_config_get_fstab_fs0_created(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs0_created(void);
static inline int mgos_sys_config_get_fstab_fs0_created(void) { return mgos_config_get_fstab_fs0_created(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs0_created(void) { return mgos_config_get_default_fstab_fs0_created(); }
void mgos_config_set_fstab_fs0_created(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs0_created(int v) { mgos_config_set_fstab_fs0_created(&mgos_sys_config, v); }

/* fstab.fs1 */
#define MGOS_CONFIG_HAVE_FSTAB_FS1
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1
const struct mgos_config_fstab_fs1 *mgos_config_get_fstab_fs1(const struct mgos_config *cfg);
static inline const struct mgos_config_fstab_fs1 *mgos_sys_config_get_fstab_fs1(void) { return mgos_config_get_fstab_fs1(&mgos_sys_config); }

/* fstab.fs1.dev */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_DEV
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_DEV
const char * mgos_config_get_fstab_fs1_dev(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs1_dev(void);
static inline const char * mgos_sys_config_get_fstab_fs1_dev(void) { return mgos_config_get_fstab_fs1_dev(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs1_dev(void) { return mgos_config_get_default_fstab_fs1_dev(); }
void mgos_config_set_fstab_fs1_dev(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs1_dev(const char * v) { mgos_config_set_fstab_fs1_dev(&mgos_sys_config, v); }

/* fstab.fs1.type */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_TYPE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_TYPE
const char * mgos_config_get_fstab_fs1_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs1_type(void);
static inline const char * mgos_sys_config_get_fstab_fs1_type(void) { return mgos_config_get_fstab_fs1_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs1_type(void) { return mgos_config_get_default_fstab_fs1_type(); }
void mgos_config_set_fstab_fs1_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs1_type(const char * v) { mgos_config_set_fstab_fs1_type(&mgos_sys_config, v); }

/* fstab.fs1.opts */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_OPTS
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_OPTS
const char * mgos_config_get_fstab_fs1_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs1_opts(void);
static inline const char * mgos_sys_config_get_fstab_fs1_opts(void) { return mgos_config_get_fstab_fs1_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs1_opts(void) { return mgos_config_get_default_fstab_fs1_opts(); }
void mgos_config_set_fstab_fs1_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs1_opts(const char * v) { mgos_config_set_fstab_fs1_opts(&mgos_sys_config, v); }

/* fstab.fs1.path */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_PATH
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_PATH
const char * mgos_config_get_fstab_fs1_path(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs1_path(void);
static inline const char * mgos_sys_config_get_fstab_fs1_path(void) { return mgos_config_get_fstab_fs1_path(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs1_path(void) { return mgos_config_get_default_fstab_fs1_path(); }
void mgos_config_set_fstab_fs1_path(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs1_path(const char * v) { mgos_config_set_fstab_fs1_path(&mgos_sys_config, v); }

/* fstab.fs1.create */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_CREATE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_CREATE
int mgos_config_get_fstab_fs1_create(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs1_create(void);
static inline int mgos_sys_config_get_fstab_fs1_create(void) { return mgos_config_get_fstab_fs1_create(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs1_create(void) { return mgos_config_get_default_fstab_fs1_create(); }
void mgos_config_set_fstab_fs1_create(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs1_create(int v) { mgos_config_set_fstab_fs1_create(&mgos_sys_config, v); }

/* fstab.fs1.optional */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_OPTIONAL
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_OPTIONAL
int mgos_config_get_fstab_fs1_optional(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs1_optional(void);
static inline int mgos_sys_config_get_fstab_fs1_optional(void) { return mgos_config_get_fstab_fs1_optional(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs1_optional(void) { return mgos_config_get_default_fstab_fs1_optional(); }
void mgos_config_set_fstab_fs1_optional(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs1_optional(int v) { mgos_config_set_fstab_fs1_optional(&mgos_sys_config, v); }

/* fstab.fs1.created */
#define MGOS_CONFIG_HAVE_FSTAB_FS1_CREATED
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS1_CREATED
int mgos_config_get_fstab_fs1_created(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs1_created(void);
static inline int mgos_sys_config_get_fstab_fs1_created(void) { return mgos_config_get_fstab_fs1_created(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs1_created(void) { return mgos_config_get_default_fstab_fs1_created(); }
void mgos_config_set_fstab_fs1_created(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs1_created(int v) { mgos_config_set_fstab_fs1_created(&mgos_sys_config, v); }

/* fstab.fs2 */
#define MGOS_CONFIG_HAVE_FSTAB_FS2
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2
const struct mgos_config_fstab_fs2 *mgos_config_get_fstab_fs2(const struct mgos_config *cfg);
static inline const struct mgos_config_fstab_fs2 *mgos_sys_config_get_fstab_fs2(void) { return mgos_config_get_fstab_fs2(&mgos_sys_config); }

/* fstab.fs2.dev */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_DEV
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_DEV
const char * mgos_config_get_fstab_fs2_dev(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs2_dev(void);
static inline const char * mgos_sys_config_get_fstab_fs2_dev(void) { return mgos_config_get_fstab_fs2_dev(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs2_dev(void) { return mgos_config_get_default_fstab_fs2_dev(); }
void mgos_config_set_fstab_fs2_dev(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs2_dev(const char * v) { mgos_config_set_fstab_fs2_dev(&mgos_sys_config, v); }

/* fstab.fs2.type */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_TYPE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_TYPE
const char * mgos_config_get_fstab_fs2_type(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs2_type(void);
static inline const char * mgos_sys_config_get_fstab_fs2_type(void) { return mgos_config_get_fstab_fs2_type(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs2_type(void) { return mgos_config_get_default_fstab_fs2_type(); }
void mgos_config_set_fstab_fs2_type(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs2_type(const char * v) { mgos_config_set_fstab_fs2_type(&mgos_sys_config, v); }

/* fstab.fs2.opts */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_OPTS
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_OPTS
const char * mgos_config_get_fstab_fs2_opts(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs2_opts(void);
static inline const char * mgos_sys_config_get_fstab_fs2_opts(void) { return mgos_config_get_fstab_fs2_opts(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs2_opts(void) { return mgos_config_get_default_fstab_fs2_opts(); }
void mgos_config_set_fstab_fs2_opts(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs2_opts(const char * v) { mgos_config_set_fstab_fs2_opts(&mgos_sys_config, v); }

/* fstab.fs2.path */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_PATH
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_PATH
const char * mgos_config_get_fstab_fs2_path(const struct mgos_config *cfg);
const char * mgos_config_get_default_fstab_fs2_path(void);
static inline const char * mgos_sys_config_get_fstab_fs2_path(void) { return mgos_config_get_fstab_fs2_path(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_fstab_fs2_path(void) { return mgos_config_get_default_fstab_fs2_path(); }
void mgos_config_set_fstab_fs2_path(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_fstab_fs2_path(const char * v) { mgos_config_set_fstab_fs2_path(&mgos_sys_config, v); }

/* fstab.fs2.create */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_CREATE
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_CREATE
int mgos_config_get_fstab_fs2_create(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs2_create(void);
static inline int mgos_sys_config_get_fstab_fs2_create(void) { return mgos_config_get_fstab_fs2_create(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs2_create(void) { return mgos_config_get_default_fstab_fs2_create(); }
void mgos_config_set_fstab_fs2_create(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs2_create(int v) { mgos_config_set_fstab_fs2_create(&mgos_sys_config, v); }

/* fstab.fs2.optional */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_OPTIONAL
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_OPTIONAL
int mgos_config_get_fstab_fs2_optional(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs2_optional(void);
static inline int mgos_sys_config_get_fstab_fs2_optional(void) { return mgos_config_get_fstab_fs2_optional(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs2_optional(void) { return mgos_config_get_default_fstab_fs2_optional(); }
void mgos_config_set_fstab_fs2_optional(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs2_optional(int v) { mgos_config_set_fstab_fs2_optional(&mgos_sys_config, v); }

/* fstab.fs2.created */
#define MGOS_CONFIG_HAVE_FSTAB_FS2_CREATED
#define MGOS_SYS_CONFIG_HAVE_FSTAB_FS2_CREATED
int mgos_config_get_fstab_fs2_created(const struct mgos_config *cfg);
int mgos_config_get_default_fstab_fs2_created(void);
static inline int mgos_sys_config_get_fstab_fs2_created(void) { return mgos_config_get_fstab_fs2_created(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_fstab_fs2_created(void) { return mgos_config_get_default_fstab_fs2_created(); }
void mgos_config_set_fstab_fs2_created(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_fstab_fs2_created(int v) { mgos_config_set_fstab_fs2_created(&mgos_sys_config, v); }

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

/* http.default_file */
#define MGOS_CONFIG_HAVE_HTTP_DEFAULT_FILE
#define MGOS_SYS_CONFIG_HAVE_HTTP_DEFAULT_FILE
const char * mgos_config_get_http_default_file(const struct mgos_config *cfg);
const char * mgos_config_get_default_http_default_file(void);
static inline const char * mgos_sys_config_get_http_default_file(void) { return mgos_config_get_http_default_file(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_http_default_file(void) { return mgos_config_get_default_http_default_file(); }
void mgos_config_set_http_default_file(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_http_default_file(const char * v) { mgos_config_set_http_default_file(&mgos_sys_config, v); }

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

/* mjs.main */
#define MGOS_CONFIG_HAVE_MJS_MAIN
#define MGOS_SYS_CONFIG_HAVE_MJS_MAIN
const char * mgos_config_get_mjs_main(const struct mgos_config *cfg);
const char * mgos_config_get_default_mjs_main(void);
static inline const char * mgos_sys_config_get_mjs_main(void) { return mgos_config_get_mjs_main(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_mjs_main(void) { return mgos_config_get_default_mjs_main(); }
void mgos_config_set_mjs_main(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_mjs_main(const char * v) { mgos_config_set_mjs_main(&mgos_sys_config, v); }

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
int mgos_config_get_rpc_uart_fc_type(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_uart_fc_type(void);
static inline int mgos_sys_config_get_rpc_uart_fc_type(void) { return mgos_config_get_rpc_uart_fc_type(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_uart_fc_type(void) { return mgos_config_get_default_rpc_uart_fc_type(); }
void mgos_config_set_rpc_uart_fc_type(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_uart_fc_type(int v) { mgos_config_set_rpc_uart_fc_type(&mgos_sys_config, v); }

/* rpc.uart.dst */
#define MGOS_CONFIG_HAVE_RPC_UART_DST
#define MGOS_SYS_CONFIG_HAVE_RPC_UART_DST
const char * mgos_config_get_rpc_uart_dst(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_uart_dst(void);
static inline const char * mgos_sys_config_get_rpc_uart_dst(void) { return mgos_config_get_rpc_uart_dst(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_uart_dst(void) { return mgos_config_get_default_rpc_uart_dst(); }
void mgos_config_set_rpc_uart_dst(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_uart_dst(const char * v) { mgos_config_set_rpc_uart_dst(&mgos_sys_config, v); }

/* rpc.ws */
#define MGOS_CONFIG_HAVE_RPC_WS
#define MGOS_SYS_CONFIG_HAVE_RPC_WS
const struct mgos_config_rpc_ws *mgos_config_get_rpc_ws(const struct mgos_config *cfg);
static inline const struct mgos_config_rpc_ws *mgos_sys_config_get_rpc_ws(void) { return mgos_config_get_rpc_ws(&mgos_sys_config); }

/* rpc.ws.enable */
#define MGOS_CONFIG_HAVE_RPC_WS_ENABLE
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_ENABLE
int mgos_config_get_rpc_ws_enable(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_ws_enable(void);
static inline int mgos_sys_config_get_rpc_ws_enable(void) { return mgos_config_get_rpc_ws_enable(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_ws_enable(void) { return mgos_config_get_default_rpc_ws_enable(); }
void mgos_config_set_rpc_ws_enable(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_ws_enable(int v) { mgos_config_set_rpc_ws_enable(&mgos_sys_config, v); }

/* rpc.ws.server_address */
#define MGOS_CONFIG_HAVE_RPC_WS_SERVER_ADDRESS
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_SERVER_ADDRESS
const char * mgos_config_get_rpc_ws_server_address(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_ws_server_address(void);
static inline const char * mgos_sys_config_get_rpc_ws_server_address(void) { return mgos_config_get_rpc_ws_server_address(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_ws_server_address(void) { return mgos_config_get_default_rpc_ws_server_address(); }
void mgos_config_set_rpc_ws_server_address(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_ws_server_address(const char * v) { mgos_config_set_rpc_ws_server_address(&mgos_sys_config, v); }

/* rpc.ws.reconnect_interval_min */
#define MGOS_CONFIG_HAVE_RPC_WS_RECONNECT_INTERVAL_MIN
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_RECONNECT_INTERVAL_MIN
int mgos_config_get_rpc_ws_reconnect_interval_min(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_ws_reconnect_interval_min(void);
static inline int mgos_sys_config_get_rpc_ws_reconnect_interval_min(void) { return mgos_config_get_rpc_ws_reconnect_interval_min(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_ws_reconnect_interval_min(void) { return mgos_config_get_default_rpc_ws_reconnect_interval_min(); }
void mgos_config_set_rpc_ws_reconnect_interval_min(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_ws_reconnect_interval_min(int v) { mgos_config_set_rpc_ws_reconnect_interval_min(&mgos_sys_config, v); }

/* rpc.ws.reconnect_interval_max */
#define MGOS_CONFIG_HAVE_RPC_WS_RECONNECT_INTERVAL_MAX
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_RECONNECT_INTERVAL_MAX
int mgos_config_get_rpc_ws_reconnect_interval_max(const struct mgos_config *cfg);
int mgos_config_get_default_rpc_ws_reconnect_interval_max(void);
static inline int mgos_sys_config_get_rpc_ws_reconnect_interval_max(void) { return mgos_config_get_rpc_ws_reconnect_interval_max(&mgos_sys_config); }
static inline int mgos_sys_config_get_default_rpc_ws_reconnect_interval_max(void) { return mgos_config_get_default_rpc_ws_reconnect_interval_max(); }
void mgos_config_set_rpc_ws_reconnect_interval_max(struct mgos_config *cfg, int v);
static inline void mgos_sys_config_set_rpc_ws_reconnect_interval_max(int v) { mgos_config_set_rpc_ws_reconnect_interval_max(&mgos_sys_config, v); }

/* rpc.ws.ssl_server_name */
#define MGOS_CONFIG_HAVE_RPC_WS_SSL_SERVER_NAME
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_SSL_SERVER_NAME
const char * mgos_config_get_rpc_ws_ssl_server_name(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_ws_ssl_server_name(void);
static inline const char * mgos_sys_config_get_rpc_ws_ssl_server_name(void) { return mgos_config_get_rpc_ws_ssl_server_name(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_ws_ssl_server_name(void) { return mgos_config_get_default_rpc_ws_ssl_server_name(); }
void mgos_config_set_rpc_ws_ssl_server_name(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_ws_ssl_server_name(const char * v) { mgos_config_set_rpc_ws_ssl_server_name(&mgos_sys_config, v); }

/* rpc.ws.ssl_cert */
#define MGOS_CONFIG_HAVE_RPC_WS_SSL_CERT
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_SSL_CERT
const char * mgos_config_get_rpc_ws_ssl_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_ws_ssl_cert(void);
static inline const char * mgos_sys_config_get_rpc_ws_ssl_cert(void) { return mgos_config_get_rpc_ws_ssl_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_ws_ssl_cert(void) { return mgos_config_get_default_rpc_ws_ssl_cert(); }
void mgos_config_set_rpc_ws_ssl_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_ws_ssl_cert(const char * v) { mgos_config_set_rpc_ws_ssl_cert(&mgos_sys_config, v); }

/* rpc.ws.ssl_key */
#define MGOS_CONFIG_HAVE_RPC_WS_SSL_KEY
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_SSL_KEY
const char * mgos_config_get_rpc_ws_ssl_key(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_ws_ssl_key(void);
static inline const char * mgos_sys_config_get_rpc_ws_ssl_key(void) { return mgos_config_get_rpc_ws_ssl_key(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_ws_ssl_key(void) { return mgos_config_get_default_rpc_ws_ssl_key(); }
void mgos_config_set_rpc_ws_ssl_key(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_ws_ssl_key(const char * v) { mgos_config_set_rpc_ws_ssl_key(&mgos_sys_config, v); }

/* rpc.ws.ssl_ca_cert */
#define MGOS_CONFIG_HAVE_RPC_WS_SSL_CA_CERT
#define MGOS_SYS_CONFIG_HAVE_RPC_WS_SSL_CA_CERT
const char * mgos_config_get_rpc_ws_ssl_ca_cert(const struct mgos_config *cfg);
const char * mgos_config_get_default_rpc_ws_ssl_ca_cert(void);
static inline const char * mgos_sys_config_get_rpc_ws_ssl_ca_cert(void) { return mgos_config_get_rpc_ws_ssl_ca_cert(&mgos_sys_config); }
static inline const char * mgos_sys_config_get_default_rpc_ws_ssl_ca_cert(void) { return mgos_config_get_default_rpc_ws_ssl_ca_cert(); }
void mgos_config_set_rpc_ws_ssl_ca_cert(struct mgos_config *cfg, const char * v);
static inline void mgos_sys_config_set_rpc_ws_ssl_ca_cert(const char * v) { mgos_config_set_rpc_ws_ssl_ca_cert(&mgos_sys_config, v); }

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

bool mgos_sys_config_get(const struct mg_str key, struct mg_str *value);
bool mgos_sys_config_set(const struct mg_str key, const struct mg_str value, bool free_strings);

bool mgos_config_is_default_str(const char *s);

/* Backward compatibility. */
const struct mgos_conf_entry *mgos_config_schema(void);

#ifdef __cplusplus
}
#endif
