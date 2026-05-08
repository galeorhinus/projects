#include "mooncalc.h"

#include <math.h>
#include <stddef.h>

// Simple lunar position approximation (Schlyter-style, low precision).
// Good enough for a UI curve; not for navigation.

static double deg_to_rad(double deg) { return deg * M_PI / 180.0; }
static double rad_to_deg(double rad) { return rad * 180.0 / M_PI; }

static double normalize_deg(double d)
{
    double r = fmod(d, 360.0);
    if (r < 0) r += 360.0;
    return r;
}

float mooncalc_elevation_deg(time_t utc_time, double lat_deg, double lon_deg)
{
    // Days since J2000.0 (2000-01-01 12:00 UTC)
    const time_t J2000 = 946728000;
    double d = (double)(utc_time - J2000) / 86400.0;

    // Orbital elements
    double N = normalize_deg(125.1228 - 0.0529538083 * d);
    double i = 5.1454;
    double w = normalize_deg(318.0634 + 0.1643573223 * d);
    double a = 60.2666;
    double e = 0.054900;
    double M = normalize_deg(115.3654 + 13.0649929509 * d);

    // Eccentric anomaly
    double Mrad = deg_to_rad(M);
    double E = M + rad_to_deg(e * sin(Mrad) * (1.0 + e * cos(Mrad)));
    double Erad = deg_to_rad(E);

    // Moon position in its orbital plane
    double x = a * (cos(Erad) - e);
    double y = a * (sqrt(1.0 - e * e) * sin(Erad));
    double r = sqrt(x * x + y * y);
    double v = rad_to_deg(atan2(y, x));

    // Ecliptic coordinates
    double Nr = deg_to_rad(N);
    double ir = deg_to_rad(i);
    double wr = deg_to_rad(w);
    double vr = deg_to_rad(v);

    double xeclip = r * (cos(Nr) * cos(vr + wr) - sin(Nr) * sin(vr + wr) * cos(ir));
    double yeclip = r * (sin(Nr) * cos(vr + wr) + cos(Nr) * sin(vr + wr) * cos(ir));
    double zeclip = r * (sin(vr + wr) * sin(ir));

    // Obliquity of the ecliptic
    double ecl = deg_to_rad(23.4393 - 3.563e-7 * d);

    // Equatorial coordinates
    double xeq = xeclip;
    double yeq = yeclip * cos(ecl) - zeclip * sin(ecl);
    double zeq = yeclip * sin(ecl) + zeclip * cos(ecl);

    double ra = atan2(yeq, xeq);
    double dec = atan2(zeq, sqrt(xeq * xeq + yeq * yeq));

    // Sidereal time
    double GMST = 18.697374558 + 24.06570982441908 * d; // hours
    double LST = GMST + lon_deg / 15.0;
    double LSTrad = deg_to_rad(normalize_deg(LST * 15.0));

    double HA = LSTrad - ra;
    double lat = deg_to_rad(lat_deg);

    double elev = asin(sin(lat) * sin(dec) + cos(lat) * cos(dec) * cos(HA));
    return (float)rad_to_deg(elev);
}

int mooncalc_build_curve(time_t start_utc,
                         time_t end_utc,
                         int step_minutes,
                         double lat_deg,
                         double lon_deg,
                         mooncalc_point_t *out,
                         int max_points)
{
    if (!out || max_points <= 0 || step_minutes <= 0) {
        return 0;
    }

    int count = 0;
    time_t t = start_utc;
    while (t <= end_utc && count < max_points) {
        out[count].t = t;
        out[count].elev_deg = mooncalc_elevation_deg(t, lat_deg, lon_deg);
        count++;
        t += (time_t)step_minutes * 60;
    }
    if (t < end_utc && count < max_points) {
        out[count].t = end_utc;
        out[count].elev_deg = mooncalc_elevation_deg(end_utc, lat_deg, lon_deg);
        count++;
    }
    return count;
}

int mooncalc_find_rise_set(time_t start_utc,
                           time_t end_utc,
                           int step_minutes,
                           double lat_deg,
                           double lon_deg,
                           time_t *rise_utc,
                           time_t *set_utc)
{
    if (step_minutes <= 0) {
        return -1;
    }
    float prev = mooncalc_elevation_deg(start_utc, lat_deg, lon_deg);
    time_t prev_t = start_utc;
    int found = 0;
    time_t rise = 0;
    time_t set = 0;

    for (time_t t = start_utc + (time_t)step_minutes * 60; t <= end_utc; t += (time_t)step_minutes * 60) {
        float cur = mooncalc_elevation_deg(t, lat_deg, lon_deg);
        if (prev <= 0 && cur > 0) {
            // rising crossing
            double frac = (0 - prev) / (cur - prev);
            rise = prev_t + (time_t)(frac * (t - prev_t));
            found |= 1;
        } else if (prev >= 0 && cur < 0) {
            // setting crossing
            double frac = (0 - prev) / (cur - prev);
            set = prev_t + (time_t)(frac * (t - prev_t));
            found |= 2;
        }
        prev = cur;
        prev_t = t;
    }

    if ((found & 1) && rise_utc) *rise_utc = rise;
    if ((found & 2) && set_utc) *set_utc = set;
    return (found == 0) ? -1 : 0;
}
