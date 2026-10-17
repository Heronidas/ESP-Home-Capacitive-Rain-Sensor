# Calibration

1. **Dry frequency.** Surface dry, heater off. Average *Frequency* over a few minutes and enter it as *Dry Frequency*. The YAML default (35000 Hz) is typical for the carrier board; measure your own.
2. **NTC.** Reference thermometer next to the head, same air, no sun, heater off for 30 min. Trim with `adc_faktor` (coarse) or *NTC Offset* (fine, ±5 K). Do not calibrate against air temperature under a clear night sky: the plate is legitimately colder.
3. **Thresholds.** Defaults: heating 300 pF, rain 500 pF. Values on the carrier board with the 45° holder (dry frequency 35,170 Hz):

   | Condition | Frequency | Capacitance |
   |---|---|---|
   | dry | 35,100 Hz | 100 pF |
   | one drop | 16,200 Hz | ~215 pF |
   | four drops | 6,050 Hz | ~580 pF |
   | surface fully wet | 1,140 Hz | ~3,100 pF |

   Check the thresholds against your first real drizzle and rain and adjust them via the number entities; no reflash.
4. **Dew nights.** Note the level dew settles at in a clear night and keep the heating threshold above it, otherwise the heater pulses all night for nothing.
5. **First night.** Leave *Auto Mode* off to see the raw values without heater influence.
