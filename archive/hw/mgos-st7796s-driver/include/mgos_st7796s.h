#pragma once

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

/**
 * @brief Initialize the ST7796S driver.
 * This function will be called by Mongoose OS on boot.
 *
 * @return true on success, false on failure.
 */
bool mgos_st7796s_init(void);

#ifdef __cplusplus
}
#endif // __cplusplus
