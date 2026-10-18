# Entities

The DE firmware uses German entity names, the EN firmware English ones. Logic and defaults are identical.

| DE | EN | Meaning |
|---|---|---|
| Wetterlage | Weather State | trocken / dry, Niesel / Drizzle, Regen / Rain |
| Regen, Feucht | Rain, Humid | binary sensors |
| Kapazität | Capacitance | capacitance in pF |
| Kapazität Änderungsrate | Capacitance Rate of Change | pF/min, 1 min mean |
| Benetzung | Wetness | wetting in % (RC-SPC1K datasheet curve, 100 % from 550 pF) |
| Oberflächentemperatur | Surface Temperature | sensor surface temperature |
| Trockenfrequenz | Dry Frequency | calibration value, defines 100 pF |
| Feuchtigkeitsschwelle, Regenschwelle | Humidity / Rain Threshold | heating and rain level (default 300 / 500 pF) |
| Niesel Erkennung, Regen Erkennung | Drizzle Detection, Rain Detection | rise that counts as drizzle / rain (default 18 / 150 pF/min) |
| Regenende nach | Rain End After | drizzle and rain end after this long without a rise (default 7 min) |
| Heizung, Automatikbetrieb | Heater, Auto Mode | heater switch; master switch for automatic heating and night mode |
| Max. Heizdauer, Pause je Heizminute, Heizpause | Max. Heating Time, Pause per Heating Minute, Heating Pause | heating-time budget |
| Heizsperre aktiv, Heizkonto, Sperre verbleibend | Heating Lockout Active, Heating Account, Lockout Remaining | heating-time budget state |
| Oszillator steht | Oscillator Stalled | oscillator stopped (water reached bare metal); weather state and rain latches are held; the heater tries to dry the plate for up to 10 min, then waits until the cooled plate reads below the heating threshold |
| Nachtmodus, Nachtmodus von / bis | Night Mode, Night Mode From / Until | allows deep sleep in the night window (off by default); half hours, e.g. 22.5 = 22:30 |
| Glasfaktor | Glass Factor | compensates the VEML7700 cover attenuation (default 1.0) |
| Helligkeit, Sonneneinstrahlung, Box Temperatur / Luftfeuchte, Batteriespannung | Brightness, Solar Irradiance, Box Temperature / Humidity, Battery Voltage | optional sensors |
