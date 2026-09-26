# ESPHome Capacitive Rain Sensor (RC-SPC1KA + ESP32)

A complete build of a heated capacitive rain sensor for Home Assistant that can grow into a small weather station: carrier board (KiCad, ready to order assembled from JLCPCB), ESPHome firmware and a build guide.

**Status: rev A, ordered but not yet built or tested.** Read [Known limitations](#known-limitations--to-verify-before-ordering) before ordering.

* [What is this?](#what-is-this)
* [How it works](#how-it-works)
* [What you need](#what-you-need)
* [Build guide](#build-guide)
* [Calibration](#calibration)
* [Entities in Home Assistant](#entities-in-home-assistant)
* [Troubleshooting](#troubleshooting)
* [Board reference](#board-reference) (connectors, GPIO map, jumpers, ordering)
* [Sensors and extensions](#sensors-and-extensions)

## What is this?

Cheap rain sensors are a plate of exposed copper traces that detect water by conductivity. They corrode within a season and stay "wet" long after the rain has stopped.

The **RC-SPC1KA** (by Radiocontrolli, roughly 13 EUR from distributors such as Novaut or TME) is different. It is a sealed **capacitive** sensor: no exposed metal, so nothing to corrode. Water on its surface changes its capacitance. It also has a **built-in heater** (about 42 ohm, so roughly 3.4 W at 12 V) that dries the surface after rain, and an **NTC thermistor** (1 kOhm at 25 C) that measures the surface temperature.

The sensor is only the element. It needs electronics to read the capacitance, a 12 V supply for the heater, and software that decides what the readings mean. This project provides all three:

* **Board:** 5 V in, generates the 12 V for the heater, ESP32 on board, reads the sensor.
* **Firmware:** ESPHome configuration that reports rain, dew, drizzle and dry, and runs the heater safely.
* **Guide:** this document, written for people who have never used the sensor.

You do not need to know the sensor beforehand. You do need to be able to solder screw terminals and pin headers and to flash an ESP32 over a USB-UART adapter.

## How it works

**Measuring wetness.** The sensor's capacitance (about 100 pF dry, well over 1000 pF when soaked) is part of a relaxation oscillator built from an SN74HC14 Schmitt-trigger inverter and a 1 MOhm resistor. The wetter the surface, the larger the capacitance and the **lower the oscillator frequency**. The ESP32 counts the pulses with its hardware pulse counter (PCNT), which is far less noisy than counting in software.

The firmware does not need any capacitance formula from the datasheet. You measure the frequency of your own dry sensor once and enter it as *Trockenfrequenz* ("dry frequency"); that value is defined as 100 pF, and every other reading is scaled from it: `C = dry_frequency * 100 / f`. Cable length and the layout are calibrated out this way, so keep the cable length the same after calibrating.

**Telling rain from dew.** Capacitance alone says *how wet*, not *why*. Heavy dew can reach the same capacitance as light rain, and the sensor even reacts to very humid air before any liquid water is present (a thin adsorbed film raises the reading, and it is fully reversible). The firmware therefore also looks at:

* **How fast the reading rises** (rain: hundreds of pF per minute; condensation: a few pF per minute).
* **The dew point:** if you provide outdoor temperature and humidity from Home Assistant, it computes the dew point and checks whether the sensor surface is at or below it (water condenses). Without outdoor data it falls back to "surface much colder than the enclosure air and dark", which is what a clear night looks like.

The result is the *Wetterlage* ("weather state") text: `trocken` (dry), `Tau` (dew), `Niesel` (drizzle), `trocknet ab` (drying) or `Regen` (rain).

**Heating.** When the surface is wet but it is not raining hard, the heater dries it so the sensor reports "dry" soon after the rain ends, and melts snow and frost. The controller:

* switches the heater off at 45 C surface temperature and back on below 40 C (checked every second, the heater warms the surface by about 0.7 K/s),
* never heats during real rain (it cannot keep up),
* limits the heating time per period (default: at most 15 minutes, then a 2 hour pause) so fog or drizzle cannot make it run for hours,
* switches the heater off whenever the temperature reading is implausible (open or shorted NTC wire),
* always starts with the heater off after a reset.

**Battery operation.** An optional night mode puts the ESP32 into deep sleep and wakes it every 5 minutes to measure. It is off by default and meant for battery or solar setups.

## What you need

| Item | Notes |
|---|---|
| Carrier board (this repo) | Order it assembled, see [Ordering](#ordering-jlcpcb). |
| RC-SPC1KA | Six pins or wires, see the wiring table. |
| 5 V supply, at least 1.5 A | USB charger, or a solar power manager with a 5 V output (developed with the Waveshare Solar Power Manager (D)). The 12 V boost for the heater draws about 0.8 A at 5 V while heating. |
| Screw terminals, pin headers | Not assembled by JLCPCB: 3x 3-pole and 1x 4-pole screw terminal (Phoenix PT 1,5 style, 3.5 mm pitch), a 1x5 and a 1x8 pin header, a 1x4 socket. See [Ordering](#ordering-jlcpcb). |
| USB-UART adapter (3.3 V logic) | For the first flash. Later updates go over WiFi (OTA). |
| Optional: VEML7700 light sensor | I2C, address 0x10. |
| Optional: HTU21D (GY-21) | I2C, sits inside the enclosure. Measures enclosure temperature and humidity (a desiccant bag check). |
| Cable to the sensor head | Multi-core, at least 6 wires plus 4 more for the I2C sensor (the prototype uses an 8-core cable). |
| Enclosure | IP67 for outdoor use, with a desiccant bag. Keep metal and enclosure walls away from the ESP32 antenna at the board's top edge. |

## Build guide

### 1. Order and solder the board

Follow [Ordering](#ordering-jlcpcb). When the assembled boards arrive, solder the through-hole parts by hand: the four screw terminals, the pin headers and the HTU21D socket. Then check visually for solder bridges.

### 2. Mount the sensor head

The RC-SPC1KA and the VEML7700 typically sit together in a small holder (a 3D-printed ASA holder on a bracket, sensor glued in with a transparent MS-polymer adhesive, the back with the heater and NTC contacts covered with Kapton tape). Mount it where rain reaches it and water can run off. The prototype sits in a shaded spot on a balcony.

### 3. Wire the sensor

The RC-SPC1KA has six pins. The wire colors below are from the sensor I used; check yours with a multimeter against the function column (heater about 42 ohm between pins 2 and 5, NTC about 1 kOhm at room temperature between pins 3 and 4, capacitor pins 1 and 6 are isolated from the others).

| Sensor pin | Wire | Function | Board terminal |
|---|---|---|---|
| 6 | green | capacitor, oscillator node | SENSOR **OSC** |
| 1 | white | capacitor, ground side | SENSOR **GND** |
| 4 | pink | NTC | SENSOR **GND** |
| 3 | red | NTC | SENSOR **NTC** |
| 2 | black | heater, switched ground | HEATER **HEAT-** |
| 5 | red | heater, +12 V | HEATER **12V** |

The board silkscreen prints the sensor's pin numbers (`#6`, `#1+4`, `#3`, `#2`, `#5`) next to each terminal, so you can wire it without this table.

Two rules that matter:

* **Never connect OSC to 12 V** and never bridge the heater wires to the capacitor wires. The heater and the capacitor are electrically isolated inside the sensor, keep it that way.
* Pin 1 and pin 4 both go to GND. Pin 1 is also the outer electrode, so a solid ground connection there reduces noise.

The optional VEML7700 goes to the I2C terminal (3V3, GND, SDA, SCL), or plug it in through Qwiic. The HTU21D goes into the 1x4 socket labelled HTU21D.

### 4. Power

Connect 5 V and GND to the POWER IN terminal (pins 5V and GND). The board has reverse-polarity protection. The third pin, BAT, is only for battery-voltage monitoring: connect it to the battery plus of a supply that has a 1S Li-ion battery (up to 4.2 V) and leave it open otherwise.

### 5. Flash the firmware

The board has no USB port. Use a USB-UART adapter with **3.3 V** logic:

| Adapter | UART header J7 |
|---|---|
| GND | GND |
| RX | TX |
| TX | RX |

The header has no power pin: power the board through POWER IN while flashing (share GND with the adapter).

1. Install ESPHome (a current release; the configuration validates with ESPHome 2026.6.5).
2. Copy `firmware/regensensor.yaml` next to a `secrets.yaml` containing `wifi_ssid`, `wifi_password`, `regensensor_api_key` (generate one in the ESPHome dashboard) and `regensensor_ota_password`.
3. In the `substitutions` at the top, set `aussen_temp_entity` and `aussen_feuchte_entity` to your outdoor temperature and humidity entities in Home Assistant. If they do not exist, the sensors stay empty and the firmware falls back to the undercooling method.
4. Hold the **BOOT** button, tap **RESET**, release BOOT. The ESP32 is now in flash mode. Run `esphome run regensensor.yaml` and pick the serial port.
5. Home Assistant discovers the device. Later updates work over WiFi.

## Calibration

Do these once, in this order.

1. **Dry frequency.** Make sure the sensor surface is completely dry and the heater is off. Watch the *Frequenz* entity for a few minutes, take the mean, and enter it in *Trockenfrequenz*. Now *Kapazität* reads about 100 pF when dry. The default in the YAML (13549 Hz) is only a placeholder from the vendor's example, not from your build.
2. **Temperature (NTC).** Put a reference thermometer next to the sensor head, in the same air, no direct sun and no clear night sky, heater off for at least 30 minutes. Compare, then adjust `adc_faktor` (coarse) or the *NTC Offset* entity (fine, +-5 K) until the readings agree. Do not calibrate to air temperature under a clear night sky: the plate is correctly colder than the air then, and that is the dew signal.
3. **Thresholds.** Start with the defaults (display 300 pF, heat 380 pF, rain 650 pF; the datasheet table suggests 320 / 450 / 2000 pF). Then do a wet test: wet the surface completely, let it dry, and note the capacitances. A soaked sensor reads several thousand pF. Set the thresholds from your own values with the number entities, no reflash needed.
4. **Watch a humid night before trusting it.** Note the highest capacitance in a dry but humid night (entity *Abstand zum Taupunkt* helps) and keep the thresholds above it. Otherwise every foggy night is reported as wet.
5. **Automatic mode.** Consider leaving *Automatikbetrieb* off for the first night so that you can see the raw values undisturbed by the heater.

## Entities in Home Assistant

The entity names are German (the firmware started as a private project); they are kept so existing dashboards keep working.

| Entity | Meaning |
|---|---|
| Wetterlage | Weather state: trocken, Tau, Niesel, trocknet ab, Regen |
| Regen, Feucht | Binary sensors (rain, wet) |
| Kapazität, Benetzung | Capacitance in pF, and wetting in percent |
| Oberflächentemperatur | Sensor surface temperature |
| Taupunkt, Abstand zum Taupunkt | Outdoor dew point and how far the surface is above it |
| Heizung | Heater switch (also usable by hand) |
| Automatikbetrieb | Master switch for automatic heating and night mode |
| Nachtmodus | Allows deep sleep in the night window (off by default) |
| Heizsperre aktiv, Heizkonto, Sperre verbleibend | State of the heating-time limit |
| Trockenfrequenz, Anzeige-/Feuchtigkeits-/Regenschwelle, ... | Calibration and settings, changeable at runtime |
| Helligkeit, Sonneneinstrahlung, Box Temperatur/Luftfeuchte, Batteriespannung | Optional sensors |

An API action `set_aussenluft(temperatur, feuchte)` lets an automation push outdoor values instead of subscribing to entities.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| *Kapazität* unknown / NaN | *Trockenfrequenz* not set, or no oscillator signal (see next line). |
| *Frequenz* is 0 | The oscillator does not run: check the OSC wire, GND, and that the sensor face is not soaked. A stopped oscillator is reported as "wet". |
| *Frequenz* jumps around | I2C traffic crosstalk (already median-filtered), poor GND connection of sensor pin 1, or a very long cable. |
| Oberflächentemperatur is NaN and the heater never runs | NTC wire open or shorted (implausible resistance): check the SENSOR terminal. This is deliberate, the heater stays off. |
| Every humid night reads "wet" or "Tau" | Thresholds too low, see calibration step 4. |
| Heater switches off after 15 minutes | The heating limit (*Max. Heizdauer*) for fog and drizzle. It resumes after *Heizpause*. |
| Cannot flash | Use 3.3 V UART, cross RX and TX, hold BOOT while tapping RESET, power the board through POWER IN. |
| Device never comes back after night mode | Night mode needs a valid clock and a supply that does not switch off at low load. Turn *Nachtmodus* off to keep it awake. |

## Board reference

* 72 x 56 mm, 2 layers, 4x M3 holes, ESP32 antenna overhangs the top edge (keep metal and enclosure walls away from it)
* Input: **5 V** (e.g. Waveshare Solar Power Manager (D), USB, any 5 V supply, <= 3 A). No solar/battery charging on this board.
* On board: AP2112K 3.3 V LDO, MT3608 boost to a fixed **12 V** for the sensor heater (switched by GPIO13 through a low-side MOSFET), reverse-polarity PMOS, SN74HC14 relaxation oscillator, NTC divider, optional battery-voltage divider, I2C pull-ups, BOOT/RESET buttons, UART header
* I2C: Qwiic/STEMMA-QT (JST-SH), 1x4 2.54 mm socket and a 4-pin screw terminal, all in parallel

### Connectors

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

Silkscreen: each screw terminal is labelled below the block with pin function and pin number. On the HEATER and SENSOR terminals `#n` is the wire/pin number of the RC-SPC1KA (`#-` = unused). The J2/J3 order keeps the sensitive oscillator node away from 12 V.

### GPIO map

| GPIO | Use |
|---|---|
| 21 / 22 | I2C SDA / SCL (4.7 k pull-ups) |
| 13 | Heater enable: boost EN + MOSFET gate (100 k pulldown, default off) |
| 25 | Oscillator input (PCNT) |
| 34 | NTC (2.8 k pull-up to 3V3 via SJ1) |
| 32 | Alternative NTC pull-up drive: move SJ1 to pad 3 to power the divider only when needed |
| 35 | Battery voltage through 100k/100k (SJ2 bridged by default; cut it to remove the divider load) |
| 0 / EN | BOOT / RESET buttons and J7 |

### Solder jumpers
* **SJ1** (default 3V3 -> NTC pull-up): cut and bridge the other side to drive the pull-up from GPIO32.
* **SJ2** (default bridged): closes the battery divider to GND. Leave bridged; if left open GPIO35 sees the unattenuated battery voltage.

### Ordering (JLCPCB)
1. PCB: upload `fabrication/regensensor_gerbers.zip`, 2 layers, 1.6 mm, HASL lead-free is fine.
2. Assembly: enable SMT assembly, top side. The ESP32 module (C701341) is only offered in **Standard PCBA** (one-time 25 USD setup fee per side; JLCPCB adds edge rails, board becomes 72 x 70 mm in the panel and the rails break off).
3. Upload `fabrication/bom_jlcpcb.csv` and `fabrication/cpl_jlcpcb.csv`, then check that every line has stock (swap a part with the magnifier if not; the 100k resistor and SS34 diode numbers in the BOM were chosen for stock).
4. **Check the placement preview.** The magenta dot marks pin 1. In the CPL, U2 and U3 (SOT-23-5/-6) are rotated 270 degrees because JLCPCB's models are turned 90 degrees against KiCad's footprints. Q1/Q2 (SOT-23) use 180. Verify U1-U4, Q1, Q2, D1 and J5 anyway.
5. Product info: e.g. Sensor / Rain gauge (HS 901590). Shipping to Germany: EuroPacket is a good compromise, check that import VAT is included at checkout.
6. Through-hole parts (J1, J2, J3, J6 screw terminals; J4, J7, J8 headers) are not in the BOM: solder them yourself. J5 (Qwiic) and L1 are assembled.

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

## Known limitations / to verify before ordering
* Footprints for the screw terminals (Phoenix PT 1,5 3.5 mm screw terminal as stand-in for KF350-3.5), the inductor (Bourns SRN6045TA stand-in for CKCS6028) must be compared against the datasheets of the parts you actually use.
* CPL rotations were corrected against the JLCPCB placement preview (U2/U3); other parts should be re-checked by anyone ordering.
* C1/C10/C11 (22 uF, 25 V, 0805) lose most capacity at 12 V DC bias; the boost is stable with it but check part availability.
* Feedback divider draws ~24 uA and the NTC pull-up ~0.9 mA permanently unless the GPIO32 option is used (matters for deep-sleep battery use).
* DRC: one intended report remains, the bridged solder jumper SJ2 (deliberate short to GND). Library-not-found warnings appear only if the KiCad footprint libraries are not configured.
* The files were generated with KiCad 7 file formats; KiCad 8-10 upgrade them on opening. Save once and re-run DRC.
* The threshold defaults and the wetting-percent curve are starting values, not from a finished wet test.
* Not yet built or tested. Treat rev A as a prototype.

## Repository
* `hardware/` KiCad project (schematic, PCB)
* `fabrication/` Gerbers, drill, JLCPCB BOM/CPL
* `firmware/` ESPHome config
* `tools/` scripts that generated the schematic/PCB/fab files from `design.py`
* `.github/workflows/fab.yml` CI: DRC + Gerber export

## License
Hardware CERN-OHL-P-2.0, firmware/docs MIT, see `LICENSE.md`.
