# Module build (perfboard)

The step-by-step **[Module Build Guide (PDF)](../module-build-guide.pdf)** covers this build in full: parts list, circuit, wiring, checks and function test.

## Short version

The SMD parts on the board are too small for most people to solder by hand, so the options are the assembled board from JLCPCB or a perfboard build. The circuit is small; pins match the GPIO map in the [hardware reference](Board-Reference.md), so the firmware runs unchanged.

### Parts

- ESP32 dev board (30 or 38 pin, with GPIO13, 21, 22, 25, 34, 35 broken out)
- SN74HC14 (DIP-14 works), 2 × 100 nF, 47 kΩ
- NTC pull-up: 2.8 kΩ (two 5.6 kΩ in parallel, or 2.7 kΩ), 100 nF
- XL6009 boost module, set to 12 V
- Logic-level N-MOSFET (e.g. IRLZ44N, or an AOD4184 module), 100 Ω gate resistor, 100 kΩ gate pull-down
- Optional battery monitor: 2 × 100 kΩ

### Wiring

| From | To |
|---|---|
| 74HC14 pin 14 | 3.3 V, with 100 nF to GND next to it |
| 74HC14 pin 7 | GND |
| 74HC14 pins 3, 5, 9, 11, 13 | GND (unused inputs) |
| 74HC14 pin 2 (output) | GPIO25 |
| 47 kΩ | between 74HC14 pins 1 and 2 |
| 100 nF | between 74HC14 pin 1 and sensor pin 6 (OSC), in series |
| Sensor pins 1 and 4 | GND |
| Sensor pin 3 (NTC) | GPIO34, 2.8 kΩ to 3.3 V, 100 nF to GND |
| Sensor pin 5 / pin 2 | boost module OUT+ / OUT− |
| Boost module IN− | MOSFET drain |
| MOSFET source | own wire to the GND terminal of the 5 V supply |
| MOSFET gate | GPIO13 via 100 Ω, 100 kΩ from gate to logic GND |
| Boost module IN+ | 5 V supply |
| ESP32 GND, 74HC14, NTC, I2C | logic ground, one wire to the GND terminal of the supply |
| I2C SDA / SCL | GPIO21 / GPIO22, 4.7 kΩ pull-ups to 3.3 V |
| Battery (optional) | 100 kΩ to GPIO35, 100 kΩ from GPIO35 to GND, `batt_teiler_faktor` / `batt_divider_factor` 2.0 |

### Notes

- Keep the wire from sensor pin 6 to the 74HC14 short; the oscillator input is high impedance. Long leads add capacitance and shift the readings; re-run the [calibration](Calibration.md) afterwards.
- Set the boost module to 12 V before connecting the sensor and check with a multimeter.
- The MOSFET switches the input return of the boost module, so the module draws nothing while the heater is off. Keep the heater return and the logic ground apart up to the supply terminal; with a shared wire the frequency jumps while the heater runs.
- Power the 74HC14 from the ESP32's 3.3 V, not 5 V, so the oscillator output stays within GPIO limits.
- The 100 nF in series to the sensor blocks the DC path through a water film on the sensor face. Without it, light rain or thawing frost can stop the oscillator.

