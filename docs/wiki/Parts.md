# Parts

- The carrier board, assembled by JLCPCB ([Ordering](Ordering-the-Board.md)); screw terminals and pin headers are hand-soldered (see below)
- RC-SPC1KA
- 5 V supply, 1.5 A or more. The heater draws about 0.8 A at 5 V (estimated from 3.4 W plus boost losses, not measured). Tested with the Waveshare Solar Power Manager (D).
- USB-UART adapter with 3.3 V logic for the first flash; updates then go over Wi-Fi
- Optional: VEML7700 light sensor (I2C 0x10), HTU21D (GY-21) inside the enclosure
- Cable to the sensor head (the prototype uses 8-core), IP67 enclosure with desiccant. Keep metal and enclosure walls away from the antenna at the board's top edge; an optional reflector is described in [Board reference](Board-Reference.md#dimensions).

## Parts to solder yourself

JLCPCB does not place the through-hole connectors. You need:

| Ref | Function | Part | Pitch | Hole |
|---|---|---|---|---|
| J1 | Power in (5V, GND, BAT) | screw terminal, 3 pins, wire entry from the board edge | 5.08 mm | 1.3 mm |
| J2 | Sensor (OSC, GND, NTC) | screw terminal, 3 pins, same type | 5.08 mm | 1.3 mm |
| J3 | Heater (GND, HEAT-, 12V) | screw terminal, 3 pins, same type | 5.08 mm | 1.3 mm |
| J6 | I2C (3V3, GND, SDA, SCL) | screw terminal, 4 pins, same type | 5.08 mm | 1.3 mm |
| J4 | Socket for the HTU21D module | female header, 1×4 | 2.54 mm | 1.0 mm |
| J5 | I2C header (3V3, GND, SCL, SDA) | male header, 1×4 (optional) | 2.54 mm | 1.0 mm |
| J7 | UART for the first flash | male header, 1×5 | 2.54 mm | 1.0 mm |
| J8 | Expansion | male header, 1×8 (optional) | 2.54 mm | 1.0 mm |

The terminal footprint follows the Phoenix MKDS 1,5/…-5,08 (horizontal, wire from the side, max. 15.2 mm long for 3 pins and 20.3 mm for 4). Common 5.08 mm terminals such as the KF128 or DG128 fit as well; the blocks sit 1.2 mm apart.

The test points (5V, 3V3, 12V, GND, OSC) need no parts.

## The sensor

The **RC-SPC1KA** from Radiocontrolli is a sealed capacitive rain sensor on an alumina substrate. Besides the sensing capacitor it carries a heater (about 42 Ω, roughly 3.4 W at 12 V) and an NTC (1 kΩ at 25 °C) for the surface temperature.

Dry, it measures about 100 pF. On the carrier board a fully wet surface reads about 3,100 pF (RC-SPC1K datasheet: more than 550 pF at full water cover).

It is sold by electronics distributors, for example [Novaut](https://www.novaut.com/en/620521-rc-spc1ka-radiocontrolli.html) (about 13 EUR incl. VAT, EU shipping), [TME](https://www.tme.com/us/en-us/details/rc-spc1ka/humidity-sensors/radiocontrolli/) and [DigiKey](https://www.digikey.com/en/products/detail/radiocontrolli/RC-SPC1KA/13688193). Prices and stock as of 2026-09; this project is not affiliated with any of them, nor with Radiocontrolli.

The element alone does nothing. This project adds the rest: a board that reads it and powers the heater from 5 V, and firmware that turns raw readings into a weather state and runs the heater safely.
