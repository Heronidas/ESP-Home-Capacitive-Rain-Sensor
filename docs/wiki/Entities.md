# Entities

The DE firmware uses German entity names, the EN firmware English ones. Logic and defaults are identical.

| DE | EN | Meaning |
|---|---|---|
| Wetterlage | Weather State | trocken / dry, feucht / humid, nass / wet, Tau / Dew (Morgentau / Morning Dew, Abendtau / Evening Dew), Reif / Frost, Niesel / Drizzle, Regen / Rain |
| Regen, Feucht | Rain, Humid | binary sensors |
| Kapazität | Capacitance | capacitance in pF |
| Kapazität Änderungsrate | Capacitance Rate of Change | pF/min, 1 min mean |
| Benetzung | Wetness | wetting in % (RC-SPC1K datasheet curve, 100 % from 550 pF) |
| Oberflächentemperatur | Surface Temperature | sensor surface temperature |
| Taupunkt, Abstand zum Taupunkt | Dew Point, Distance to Dew Point | outdoor dew point, surface minus dew point |
| Trockenfrequenz | Dry Frequency | calibration value, defines 100 pF |
| Anzeigeschwelle, Feuchtigkeitsschwelle, Regenschwelle | Display / Humidity / Rain Threshold | capacitance thresholds (default 110 / 200 / 500 pF) |
| Tauschwelle | Dew Threshold | distance to the dew point from which the state shows dew (default 2 °C) |
| Niesel Erkennung, Regen Erkennung | Drizzle Detection, Rain Detection | rise that counts as drizzle / rain (default 60 / 150 pF/min) |
| Regenende nach | Rain End After | drizzle and rain end after this long without a rise (default 7 min) |
| Morgentrocknung ab | Morning Drying From | level from which the surface gets one heat pulse each morning (default 150 pF; at or above the heating threshold: off) |
| Morgentrocknung Temperatur | Morning Drying Temperature | target of the morning heat pulse (default 55 °C, 45–60 °C) |
| Heizung, Automatikbetrieb | Heater, Auto Mode | heater switch; master switch for automatic heating and night mode |
| Max. Heizdauer, Pause je Heizminute, Heizpause | Max. Heating Time, Pause per Heating Minute, Heating Pause | heating-time budget |
| Heizsperre aktiv, Heizkonto, Sperre verbleibend | Heating Lockout Active, Heating Account, Lockout Remaining | heating-time budget state |
| Nachtmodus, Nachtmodus von / bis | Night Mode, Night Mode From / Until | allows deep sleep in the night window (off by default); half hours, e.g. 22.5 = 22:30 |
| Glasfaktor | Glass Factor | compensates the VEML7700 cover attenuation (default 1.6, estimate) |
| Helligkeit, Sonneneinstrahlung, Box Temperatur / Luftfeuchte, Batteriespannung | Brightness, Solar Irradiance, Box Temperature / Humidity, Battery Voltage | optional sensors |
