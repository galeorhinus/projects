# Clock75 UI Requirements

## Screen
- Size: 7.5" e-paper
- Resolution: 800x480
- Orientation: landscape

## Data & Units
- Outdoor + indoor temperature (and related stats)
- Units: configurable, default to °F
- Time format: configurable (12/24-hour)

## Layout Direction
- Base style: follow **Status Panel** sizing/typography
- Remove the large weather icon from Status Panel
- Replace the large icon area with a **Moon/Tithi block**
- Add **Forecast Columns** on the far right, without icons

## Required Blocks
### Status Panel (kept)
- Big outdoor temperature (primary value)
- Indoor temperature block (secondary value)
- Date line (day + date)
- Time (large)
- High/Low for outdoor and indoor
- "Next 12 to 24 hours" label (if space allows)
- Signal/battery indicators (small)

### Moon/Tithi (replaces big weather icon)
- Moon phase icon
- Tithi text (Shukla/Krishna + tithi name)
- Moonrise and moonset times
- Sunrise and sunset times

### Forecast Columns (right side)
- Two columns, **text-only**, no icons
- Column 1: "Later Today" (7 rows)
- Column 2: "7-Day Forecast" (7 rows)

## Update Cadence
- Clock: every minute
- Other items: slower cadence (TBD)

## Constraints / Notes
- Keep the overall visual hierarchy and sizing similar to Status Panel.
- If space is tight, prioritize: time, outdoor temp, indoor temp, moon/tithi, then forecasts.
