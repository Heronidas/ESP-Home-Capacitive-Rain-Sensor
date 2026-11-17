# Board reference

This page describes the carrier board **Rev B**, the version in `hardware/` and `fabrication/`. Rev A (ESP32-WROOM-32E soldered on the board, MT3608 boost on board) runs the same firmware; it is not developed further.

## Dimensions

<p align="center"><img src="../board-dimensions.svg" alt="Board dimensions" width="720"></p>

| | |
|---|---|
| Board | 100 × 70 mm, 1.6 mm thick, 2 layers |
| Mounting holes | 4 × Ø3.2 mm (M3), centres 3.5 mm from each edge |
| Hole spacing | 93 mm × 63 mm (centre to centre) |
| Keep-out around each hole | Ø6.8 mm, for screw heads, nuts or standoffs |
| ESP32 D1 mini | plugs into four 1×10 sockets at the top right; the antenna stays inside the board outline over a copper-free area, the USB port points down |
| XL6009 module | sits on four pin-header pins at the left |

The D1 mini and the XL6009 module are the tallest parts. Measure your stack of socket, module and plugged cables before you size an enclosure, and leave about 3 mm below the board for the through-hole solder joints (e.g. 3–5 mm standoffs). The screw terminals sit along the bottom edge, so plan room for the cables there. Keep metal and enclosure walls away from the antenna, except an optional reflector: a metal plate at least 2 cm (ideally 3 cm) behind the antenna, on the side facing away from the access point, strengthens the signal towards it. JLCPCB adds edge rails for assembly and breaks them off afterwards; small residues can remain at the edges, so allow about 0.5 mm clearance around the board.

[`mechanical/board-outline.dxf`](../../mechanical/board-outline.dxf) holds the outline, the holes, the antenna area and the connector and module positions for import into CAD (mm, origin at the bottom-left corner, top view; one layer each: OUTLINE, HOLES, ANTENNA, CONNECTORS).

## Overview

- Input: **5 V** (e.g. Waveshare Solar Power Manager (D), USB, any 5 V supply of 1.5 A or more). No solar or battery charging on this board, no reverse-polarity protection.
- ESP32 D1 mini (MH-ET LIVE MiniKit layout) on sockets. Its own regulator supplies the 3.3 V; flash it over its USB port.
- Heater: XL6009 boost module set to **12 V**. An AOD4184A N-MOSFET switches the module's input return, driven by GPIO13 (100 Ω gate resistor, 100 k pull-down, off by default). The module draws no current while the heater is off.
- Ground: the heater current returns on its own copper to the GND pin of POWER IN and meets the logic ground only there (net tie NT1). The 5 V for the heater and for the D1 mini also split at the terminal (NT2). This keeps the heater current out of the oscillator ground.
- Measurement: SN74HC14 relaxation oscillator (R1 = 47 kΩ, dry about 125 kHz), 100 nF in series to the sensor (C3) against water films on the face, NTC divider (2 × 5.6 kΩ pull-up), optional battery voltage divider (100k/100k).
- HTU21D on board, on a tongue with slots around it that keep the board's heat away. It measures the air in the enclosure.
- I2C on a 1×4 socket (J4), a 1×4 pin header beside it (J5) and a 4-pin screw terminal (J6), all in parallel, with 4.7 k pull-ups.
- Optional 1000 µF electrolytic (C1) at the XL6009 input, through-hole, not needed in tests.
- Test points: 5V, 3V3, 12V, GND and OSC.

## Connectors

| Ref | Function | Pins (1 → n) |
|---|---|---|
| J1 | Power in | 5V, GND, BAT (battery voltage sense, optional) |
| J3 | Sensor heater | HEAT+ (12 V), HEAT− |
| J2 | Sensor capacitor / NTC | OSC (to the oscillator through C3), GND, NTC |
| J6 | I2C screw terminal | 3V3, GND, SDA, SCL |
| J4 | I2C socket (any 3V3/GND/SCL/SDA module) | 3V3, GND, SCL, SDA |
| J5 | I2C pin header, beside J4 | 3V3, GND, SCL, SDA |
| J8 | Expansion | 3V3, GND, IO32, IO33, IO26, IO27, IO14, IO4 |

Each screw terminal is labelled below the block with pin function and number. On HEATER and SENSOR, `#n` is the RC-SPC1KA pin number. J6 sits below the D1 mini's USB port: flash the D1 mini before you plug it in, later updates go over Wi-Fi.

## GPIO map

The silkscreen repeats this table next to the D1 mini.

| GPIO | Use |
|---|---|
| 25 | Oscillator input (PCNT) |
| 34 | NTC (2.8 k pull-up to 3V3 via SJ1) |
| 35 | Battery voltage through 100k/100k (SJ2 bridged by default) |
| 13 | Heater MOSFET gate (100 k pull-down, default off) |
| 21 / 22 | I2C SDA / SCL (4.7 k pull-ups) |
| 32 | Alternative NTC pull-up drive: move SJ1 to pad 3 to power the divider only when needed |

## Solder jumpers

- **SJ1** (default: 3V3 → NTC pull-up). Cut and bridge the other side to drive the pull-up from GPIO32.
- **SJ2** (default: bridged). Closes the battery divider to GND. Leave it bridged; if open, GPIO35 sees the unattenuated battery voltage.
