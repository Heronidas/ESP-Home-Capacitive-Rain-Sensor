# Known limitations

- Footprint stand-ins must be checked against the parts you actually use: screw terminals (Phoenix MKDS 1,5 5.08 mm for KF128/DG128-type 5.08 mm terminals) and inductor (Bourns SRN6045TA for CKCS6028).
- C1, C10, C11 (22 µF, 25 V, 0805) lose most of their capacitance at 12 V DC bias; the boost is stable with it, but check part availability.
- The feedback divider draws ~24 µA and the NTC pull-up ~0.9 mA permanently, unless the GPIO32 option is used (relevant for deep-sleep battery operation).
- DRC: the bridged solder jumper SJ2 is reported as intended, plus cosmetic silkscreen warnings (small text, overlaps). Library-not-found warnings only appear if the KiCad libraries are not configured.
- The files use KiCad 7 formats; KiCad 8–10 upgrade them on opening. Save once and re-run DRC.
- Rev A boots and runs Wi-Fi, encrypted OTA, I2C and the battery voltage divider as designed. The test with sensor and heater is still open; results will be added here.
