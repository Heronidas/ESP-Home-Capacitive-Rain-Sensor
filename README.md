# ESPHome Capacitive Rain Sensor (RC-SPC1KA + ESP32)

Complete build of a heated capacitive rain sensor that can grow into a small weather station. The carrier board takes 5 V (for example from a solar power manager), generates the 12 V for the sensor heater, and carries an ESP32 that measures the sensor's oscillator frequency. I2C sensors (light, temperature, humidity, pressure) plug into Qwiic, a socket or a screw terminal; an expansion header brings out six GPIOs for wind or other sensors. The ESPHome firmware tells rain from dew and drizzle, controls the heater with safety limits, and supports a deep-sleep night mode for battery use.

Made to be ordered fully assembled from JLCPCB (or bare from any other fab). Status: rev A, not yet built or tested.

* 72 x 56 mm, 2 layers, 4x M3 holes, ESP32 antenna overhangs the top edge (keep metal and enclosure walls away from it)
* Input: **5 V** (e.g. Waveshare Solar Power Manager (D), USB, any 5 V supply, <= 3 A). No solar/battery charging on this board.
* On board: AP2112K 3.3 V LDO, MT3608 boost to a fixed **12 V** for the sensor heater (switched by GPIO13 through a low-side MOSFET), reverse-polarity PMOS, SN74HC14 relaxation oscillator, NTC divider, optional battery-voltage divider, I2C pull-ups, BOOT/RESET buttons, UART header
* I2C: Qwiic/STEMMA-QT (JST-SH), 1x4 2.54 mm socket and a 4-pin screw terminal, all in parallel
* Firmware: `firmware/regensensor.yaml`

## Sensors and extensions

| Sensor | Connection | Status |
|---|---|---|
| RC-SPC1KA (capacitance, NTC, heater) | screw terminals SENSOR / HEATER | in firmware |
| VEML7700 light sensor | I2C (Qwiic, socket or terminal), address 0x10 | in firmware |
| HTU21D temperature/humidity (inside the enclosure) | I2C, socket labelled HTU21D | in firmware |
| Battery voltage | J1 pin BAT | in firmware |
| Pressure (BME280/BMP280), UV (LTR390), CO2 etc. | I2C, 3.3 V modules | hardware supports it, no ESPHome config yet, untested |
| Wind (pulse anemometer), tipping bucket, DS18B20 | expansion header J8: 3V3, GND, IO32, IO33, IO26, IO27, IO14, IO4 | hardware supports it, no ESPHome config yet, untested |

IO32 is also the alternative NTC pull-up drive (see solder jumpers). The expansion header has no 5 V pin.

## Connectors

| Ref | Function | Pins (1 -> n) |
|---|---|---|
| J1 | Power in | 5V, GND, BAT (battery voltage sense input, optional) |
| J6 | I2C screw terminal | 3V3, GND, SDA, SCL |
| J3 | Sensor heater | GND, HEAT- (switched return), +12V |
| J2 | Sensor capacitor/NTC | OSC (cap. node), GND, NTC |
| J4 | I2C socket, silkscreen "HTU21D" (any 3V3/GND/SCL/SDA module) | 3V3, GND, SCL, SDA |
| J5 | Qwiic (legend on silkscreen, top to bottom: 4 SCL, 3 SDA, 2 3V3, 1 GND) | GND, 3V3, SDA, SCL |
| J7 | UART programming | GND, TXD, RXD, IO0, EN (no power pin - power the board via J1) |
| J8 | Expansion | 3V3, GND, IO32, IO33, IO26, IO27, IO14, IO4 |

Silkscreen: each screw terminal is labelled below the block with pin function and pin number. On the HEATER and SENSOR terminals `#n` is the wire/pin number of the RC-SPC1KA (`#-` = unused). J1 pin 3 (BAT) is only needed for battery-voltage monitoring; leave it open otherwise.

RC-SPC1KA wiring (datasheet rev 1.2): pin 1 (white) -> J2-GND *and* the outer electrode ground; pin 6 (green) -> J2-OSC; pin 3 (red, NTC) -> J2-NTC; pin 4 (pink, NTC) -> J2-GND; pin 5 (red, 12 V) -> J3-+12V; pin 2 (black) -> J3-HEAT-. The J2/J3 order keeps the sensitive oscillator node away from 12 V. Never bridge OSC to +12V.

## GPIO map

| GPIO | Use |
|---|---|
| 21 / 22 | I2C SDA / SCL (4.7 k pull-ups) |
| 13 | Heater enable: boost EN + MOSFET gate (100 k pulldown, default off) |
| 25 | Oscillator input (PCNT) |
| 34 | NTC (2.8 k pull-up to 3V3 via SJ1) |
| 32 | Alternative NTC pull-up drive: move SJ1 to pad 3 to power the divider only when needed |
| 35 | Battery voltage through 100k/100k (SJ2 bridged by default; cut it to remove the divider load) |
| 0 / EN | BOOT / RESET buttons and J7 |

## Solder jumpers
* **SJ1** (default 3V3 -> NTC pull-up): cut and bridge the other side to drive the pull-up from GPIO32.
* **SJ2** (default bridged): closes the battery divider to GND. Leave bridged; if left open GPIO35 sees the unattenuated battery voltage.

## Ordering (JLCPCB)
1. PCB: upload `fabrication/regensensor_gerbers.zip`, 2 layers, 1.6 mm, HASL lead-free is fine.
2. Assembly: enable SMT assembly, top side. The ESP32 module (C701341) is only offered in **Standard PCBA** (one-time 25 USD setup fee per side; JLCPCB adds edge rails, board becomes 72 x 70 mm in the panel and the rails break off).
3. Upload `fabrication/bom_jlcpcb.csv` and `fabrication/cpl_jlcpcb.csv`, then check that every line has stock (swap a part with the magnifier if not; the 100k resistor and SS34 diode numbers in the BOM were chosen for stock).
4. **Check the placement preview.** The magenta dot marks pin 1. In the CPL, U2 and U3 (SOT-23-5/-6) are rotated 270 degrees because JLCPCB's models are turned 90 degrees against KiCad's footprints. Q1/Q2 (SOT-23) use 180. Verify U1-U4, Q1, Q2, D1 and J5 anyway.
5. Product info: e.g. Sensor / Rain gauge (HS 901590). Shipping to Germany: EuroPacket is a good compromise, check that import VAT is included at checkout.
6. Through-hole parts (J1, J2, J3, J6 screw terminals; J4, J7, J8 headers) are not in the BOM: solder them yourself. J5 (Qwiic) and L1 are assembled.

## Known limitations / to verify before ordering
* Footprints for the screw terminals (Phoenix PT 1,5 3.5 mm screw terminal as stand-in for KF350-3.5), the inductor (Bourns SRN6045TA stand-in for CKCS6028) must be compared against the datasheets of the parts you actually use.
* CPL rotations were corrected against the JLCPCB placement preview (U2/U3); other parts should be re-checked by anyone ordering.
* C1/C10/C11 (22 uF, 25 V, 0805) lose most capacity at 12 V DC bias; the boost is stable with it but check part availability.
* Feedback divider draws ~24 uA and the NTC pull-up ~0.9 mA permanently unless the GPIO32 option is used (matters for deep-sleep battery use).
* DRC: one intended report remains, the bridged solder jumper SJ2 (deliberate short to GND). Library-not-found warnings appear only if the KiCad footprint libraries are not configured.
* The files were generated with KiCad 7 file formats; KiCad 8-10 upgrade them on opening. Save once and re-run DRC.
* Not yet built or tested. Treat rev A as a prototype.

## Repository
* `hardware/` KiCad project (schematic, PCB)
* `fabrication/` Gerbers, drill, JLCPCB BOM/CPL
* `firmware/` ESPHome config
* `tools/` scripts that generated the schematic/PCB/fab files from `design.py`
* `.github/workflows/fab.yml` CI: DRC + Gerber export

## Calibration
Flash, read the dry oscillator frequency (entity "Frequenz"), write it into "Trockenfrequenz", then run a wet test and adjust the thresholds. Calibrate the NTC against a reference thermometer via `adc_faktor`.

## License
Hardware CERN-OHL-P-2.0, firmware/docs MIT, see `LICENSE.md`.
