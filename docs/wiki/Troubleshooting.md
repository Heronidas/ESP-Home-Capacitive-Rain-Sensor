# Troubleshooting

| Symptom | Cause |
|---|---|
| Capacitance unknown | *Dry Frequency* not set, or no oscillator signal |
| Frequency 0 | Oscillator stopped: OSC wire, GND or R1. Reported as wet. |
| Frequency jumps | I2C crosstalk (already median-filtered), weak GND at sensor pin 1, very long cable |
| Surface temperature NaN, heater never runs | Implausible NTC resistance (open or shorted): check the SENSOR terminal. Deliberate: the heater stays off. |
| Humid nights read wet | Display threshold too low (calibration step 4) |
| Heater stops after 15 min | Heating-time budget (*Max. Heating Time*); resumes after *Heating Pause* |
| Device does not wake from night mode | Needs a valid clock and a supply that stays on at low load; switch *Night Mode* off to keep it awake |
