# Calibration

1. **Dry frequency.** Surface dry, heater off. Average *Frequency* over a few minutes and enter it as *Dry Frequency*. The YAML default (13549 Hz) is only a placeholder from the vendor example.
2. **NTC.** Reference thermometer next to the head, same air, no sun, heater off for 30 min. Trim with `adc_faktor` (coarse) or *NTC Offset* (fine, ±5 K). Do not calibrate against air temperature under a clear night sky: the plate is legitimately colder, which is the dew signal.
3. **Thresholds.** Defaults: display 110 pF, heating 200 pF, rain 500 pF. Measured values:

   | Condition | Capacitance |
   |---|---|
   | dry | ~100 pF |
   | dew, cloudy night | ~105–120 pF |
   | dew, clear night | ~170–200 pF |
   | fine mist | ~270 pF |
   | three drops | ~290 pF |
   | heavy spray | ~600 pF |
   | soaked cloth | 870–1240 pF |

   Adjust them via the number entities; no reflash.
4. **Dew threshold.** *Dew Threshold* (default 2 °C) is the surface-minus-dew-point distance from which the state reads dew. The outdoor sensor and the plate sit in different places, so tune it on real dew mornings.
5. **Humid nights.** Note the maximum capacitance in a dry but humid night and keep the display threshold above it, otherwise every foggy night reads as wet. *Distance to Dew Point* helps here.
6. **First night.** Leave *Auto Mode* off to see the raw values without heater influence.
