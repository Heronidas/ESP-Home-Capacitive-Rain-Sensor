# How it works

## Measurement

The sensing capacitor sets the frequency of a relaxation oscillator (SN74HC14 with R1 = 220 kΩ). A wetter surface means a larger capacitance and a lower frequency. The ESP32 counts the pulses with its hardware PCNT peripheral, which is far quieter than software counting. You measure your dry sensor once and enter the result as the dry frequency. That value defines 100 pF; everything else scales from it (`C = f_dry × 100 / f`), so cable length and layout drop out of the calibration.

## Rain, drizzle or dew

Capacitance says *how* wet, not *why*. Heavy dew reaches the same values as light rain, and the element already reacts to humid air before any liquid water is present. The firmware therefore adds two criteria:

| Criterion | Rain / drizzle | Dew |
|---|---|---|
| Rate of rise | tens to hundreds of pF/min | a few pF/min |
| Surface vs. dew point | any | at or below the dew point |

A fast rise latches **drizzle** (*Drizzle Detection*, default 60 pF/min) or, from the rain level up, **rain** (*Rain Detection*, default 150 pF/min). Both end after *Rain End After* (default 7 min) without a further rise, or when the surface dries. Dew is reported when the surface is within *Dew Threshold* of the dew point; without outdoor data, slow wetting in the dark counts as dew. Dew reads as morning dew from 04:00 to 11:00 and evening dew from 17:00 to 23:00.

## Heater

The heater dries the film left after rain, and dew or frost once they have ended. It stays off while drizzle or rain is latched, so the sensor can see the precipitation, and while dew or frost is forming, since it would form again at once. After a rain end it dries the surface. If the level is still at rain level after 3 minutes of drying, it is still raining and rain is set again. Rain remains reported until the surface has dried below the rain level, so steady rain never reports a false end.

Morning drying: once a day between 04:00 and 11:00, when it is light (100 lx) and no more dew forms, a surface still at *Morning Drying From* (default 150 pF) or above is dried down to the display threshold. This clears the remaining film below the heating threshold.

Safety: off at 45 °C surface temperature, back on below 40 °C, checked every second (the surface heats at about 0.7 K/s). Heating time is budgeted (default 15 min, then a 2 h pause). Implausible NTC readings switch it off, and it always starts off after a reset.

## Battery

Optional night mode: deep sleep with a 5 min wake interval, about 35 s awake per cycle. Off by default.
