#pragma once

#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    time_t t;
    float elev_deg;
} mooncalc_point_t;

// Elevation of the moon in degrees for the given UTC timestamp.
float mooncalc_elevation_deg(time_t utc_time, double lat_deg, double lon_deg);

// Build an elevation curve between start and end (inclusive) at step_minutes.
// Returns number of points written to out (up to max_points).
int mooncalc_build_curve(time_t start_utc,
                         time_t end_utc,
                         int step_minutes,
                         double lat_deg,
                         double lon_deg,
                         mooncalc_point_t *out,
                         int max_points);

// Find approximate moonrise and moonset within [start_utc, end_utc].
// Returns 0 on success, -1 if no crossings found.
int mooncalc_find_rise_set(time_t start_utc,
                           time_t end_utc,
                           int step_minutes,
                           double lat_deg,
                           double lon_deg,
                           time_t *rise_utc,
                           time_t *set_utc);

#ifdef __cplusplus
}
#endif
