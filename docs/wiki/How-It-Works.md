# How it works

## Measurement

The sensing capacitor sets the frequency of a relaxation oscillator (SN74HC14 with R1 = 220 kΩ). A wetter surface means a larger capacitance and a lower frequency. The ESP32 counts the pulses with its hardware PCNT peripheral, which is far quieter than software counting. You measure your dry sensor once and enter the result as the dry frequency. That value defines 100 pF; everything else scales from it (`C = f_dry × 100 / f`), so cable length and layout drop out of the calibration.

If water reaches bare metal (an unsealed solder joint or the cable entry), the oscillator stops or sputters. Below 1/50 of the dry frequency the firmware reports "Oszillator steht", sets the capacitance to 5000 pF, holds the weather state and the rain latches, and heats the plate to dry the leak.

## Rain or not

Capacitance says *how* wet, not *why*. Heavy dew reaches the same values as light rain, and the element already reacts to humid air before any liquid water is present. What separates them is the rate of rise:

| Source | Rate of rise |
|---|---|
| dew, fog, humid air | up to ~8 pF/min |
| warm plate taking up humidity right after heating | up to ~30 pF/min |
| drizzle | ~15–50 pF/min |
| rain | hundreds of pF/min |

A rise of *Drizzle Detection* (default 18 pF/min) or more latches **drizzle**, except within 7 minutes after heating. From the rain level up, *Rain Detection* (default 150 pF/min) latches **rain**, and so does drizzle that grows to the rain level. Both end after *Rain End After* (default 7 min) without a further rise, or when the surface dries. Everything else wet reads **wet**: dew, fog, or a surface drying after rain.

## Heater

The heater keeps the surface dry: from the heating threshold it dries dew, fog, frost and the film left after rain. Dew wets the plate slowly, so a dew night needs only a few short pulses (replayed from logged dew nights: about 2 minutes of heating per night), and the dry plate stays sensitive for the next rain. Once on, it heats until the level falls to 85 % of the heating threshold. It stays off while drizzle or rain is latched, so the sensor can see the precipitation. After a rain end it dries the surface. If the level is still at rain level after 3 minutes of drying, it is still raining and rain is set again. Rain remains reported until the surface has dried below the rain level, so steady rain never reports a false end.

Safety: off at 45 °C surface temperature, back on below 40 °C, checked every second (the surface heats at about 0.7 K/s). Heating time is budgeted (default 15 min, then a 2 h pause). Implausible NTC readings switch it off, and it always starts off after a reset.

## Battery

Optional night mode: deep sleep with a 5 min wake interval, about 35 s awake per cycle. Off by default.
