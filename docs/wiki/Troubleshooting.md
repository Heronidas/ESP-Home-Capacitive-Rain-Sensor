# Troubleshooting

| Symptom | Cause |
|---|---|
| Capacitance unknown | *Dry Frequency* not set, or no oscillator signal |
| Frequency 0 | Oscillator stopped: OSC wire, GND, R1 or C3, or water at bare metal of the sensor (leaky holder). *Oscillator Stalled* turns on and the weather state holds. Without the series capacitor C3 a water film on the face stops it as well. |
| Frequency stops or jumps while the heater runs | Boost converter or heater current on the logic ground (Rev A, or a shared ground wire). The firmware skips these readings. On Rev B, check that the heater wires go only to HEATER. |
| Frequency drifts slowly over the day | Air humidity (about 0.2 % per percentage point) and plate temperature; the first day after bonding also the curing sealant. Calibrate outdoors. |
| Frequency jumps | I2C crosstalk (median-filtered), weak GND at sensor pin 1, very long cable |
| Rain reported on a dry, sunny morning after frost | Firmware older than the frost lock. Update; the frost lock holds rain off until the thawed plate is dry. |
| No rain reported in light rain on a wet plate | *Capacitance Steps* stayed below *Rain Start Steps*. Compare both in the history and lower the threshold by 0.1–0.2 pF. |
| Rain ends during a long shower | *Capacitance Unrest* dropped below 1.5 pF for *Rain End Threshold*. Raise the threshold to 5–10 min. |
| Surface temperature NaN, heater never runs | Implausible NTC resistance (open or shorted): check the SENSOR terminal. The heater stays off on purpose. |
| Heater stops after 15 min | Heating-time budget (*Max. Heating Time*); resumes after *Heating Lockout* |
| No drying run after rain | *Drying Run* off, battery below 3.5 V, or new rain within the 15-minute wait |
| All entities unavailable after swapping the board | Home Assistant still connects to the old board. Add the newly discovered device and choose *Migrate* in the name-conflict dialog; entity IDs and history stay. |
| No values all night, back at dawn | The supply switched off at low load while the ESP32 slept. On the Waveshare Solar Power Manager (D), double-click the function button for low-current mode; repeat after a deep discharge. Switch *Night Mode* off to keep the device awake. |
