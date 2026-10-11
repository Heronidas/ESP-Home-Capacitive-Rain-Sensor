# Calibration

1. **Dry frequency.** Surface dry, heater off. Average *Frequency* over a few minutes and enter it as *Dry Frequency*. The YAML default (13549 Hz) is only a placeholder from the vendor example.
2. **NTC.** Reference thermometer next to the head, same air, no sun, heater off for 30 min. Trim with `adc_faktor` (coarse) or *NTC Offset* (fine, ±5 K). Do not calibrate against air temperature under a clear night sky: the plate is legitimately colder.
3. **Thresholds.** Defaults: heating 300 pF, rain 500 pF. Measured values:

   | Condition | Capacitance |
   |---|---|
   | dry | ~100 pF |
   | dew, cloudy night | ~105–120 pF |
   | dew, clear night | ~170–250 pF |
   | spray mist (bottle) | ~270 pF |
   | three drops | ~290 pF |
   | heavy spray | ~600 pF |
   | soaked cloth | 870–1240 pF |

   Adjust them via the number entities; no reflash.
4. **Dew nights.** Note the level dew settles at in a clear night and keep the heating threshold above it, otherwise the heater pulses all night for nothing.
5. **First night.** Leave *Auto Mode* off to see the raw values without heater influence.
