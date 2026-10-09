# Calibration

1. **Dry frequency.** Surface dry, heater off. Average *Frequency* over a few minutes and enter it as *Dry Frequency*. The YAML default (13549 Hz) is only a placeholder from the vendor example.
2. **NTC.** Reference thermometer next to the head, same air, no sun, heater off for 30 min. Trim with `adc_faktor` (coarse) or *NTC Offset* (fine, ±5 K). Do not calibrate against air temperature under a clear night sky: the plate is legitimately colder.
3. **Thresholds.** Defaults: display 110 pF, heating 200 pF, rain 500 pF. Measured values:

   | Condition | Capacitance |
   |---|---|
   | dry | ~100 pF |
   | dew, cloudy night | ~105–120 pF |
   | dew, clear night | ~170–200 pF |
   | spray mist (bottle) | ~270 pF |
   | three drops | ~290 pF |
   | heavy spray | ~600 pF |
   | soaked cloth | 870–1240 pF |

   Adjust them via the number entities; no reflash.
4. **Humid nights.** Note the maximum capacitance in a humid night without dew and keep the display threshold above it, otherwise humid air alone reads as wet.
5. **First night.** Leave *Auto Mode* off to see the raw values without heater influence.
