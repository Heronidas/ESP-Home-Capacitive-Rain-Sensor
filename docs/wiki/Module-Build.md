# Module build (perfboard)

The step-by-step **[Module Build Guide (PDF)](../module-build-guide.pdf)** covers this build in full: parts list, circuit, wiring, checks and function test.

## Short version

The SMD parts on the board are too small for most people to solder by hand, so the options are the assembled board from JLCPCB or a perfboard build. The circuit is small; pins match the GPIO map in the [hardware reference](Board-Reference.md), so the firmware runs unchanged.

### Parts

- ESP32 dev board (30 or 38 pin, with GPIO13, 21, 22, 25, 34, 35 broken out)
- SN74HC14 (DIP-14 works), 100 nF, 220 kΩ
- NTC pull-up: 2.8 kΩ (two 5.6 kΩ in parallel, or 2.7 kΩ), 100 nF
- MT3608 boost module, set to 12 V
- Logic-level N-MOSFET (e.g. IRLZ44N, or AO3400A on a breakout), 100 Ω gate resistor, 100 kΩ gate pull-down
- Optional battery monitor: 2 × 100 kΩ

### Wiring

| From | To |
|---|---|
| 74HC14 pin 14 | 3.3 V, with 100 nF to GND next to it |
| 74HC14 pin 7 | GND |
| 74HC14 pins 3, 5, 9, 11, 13 | GND (unused inputs) |
| 74HC14 pin 2 (output) | GPIO25 |
| 220 kΩ | between 74HC14 pins 1 and 2 |
| Sensor pin 6 (OSC) | 74HC14 pin 1 |
| Sensor pins 1 and 4 | GND |
| Sensor pin 3 (NTC) | GPIO34, 2.8 kΩ to 3.3 V, 100 nF to GND |
| Sensor pin 5 (+12 V) | boost module OUT+ |
| Sensor pin 2 (HEAT-) | MOSFET drain |
| MOSFET source | GND |
| MOSFET gate | GPIO13 via 100 Ω, 100 kΩ from gate to GND |
| Boost module IN+ / GND | 5 V supply / GND |
| Boost module GND, ESP32 GND | common ground |
| I2C SDA / SCL | GPIO21 / GPIO22, 4.7 kΩ pull-ups to 3.3 V |
| Battery (optional) | 100 kΩ to GPIO35, 100 kΩ from GPIO35 to GND, `batt_teiler_faktor` 2.0 |

### Notes

- Keep the wire from sensor pin 6 to the 74HC14 short; the oscillator input is high impedance. Long leads add capacitance and shift the readings; re-run the [calibration](Calibration.md) afterwards.
- Set the boost module to 12 V before connecting the sensor and check with a multimeter.
- Modules without an enable pin keep the boost converter running all the time. Fine on mains power, a poor choice for battery operation. The board switches the converter off through the MT3608 EN pin.
- Power the 74HC14 from the ESP32's 3.3 V, not 5 V, so the oscillator output stays within GPIO limits.

