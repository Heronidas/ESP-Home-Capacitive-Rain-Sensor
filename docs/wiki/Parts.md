# Parts

- The carrier board Rev B, SMD parts assembled by JLCPCB ([Ordering](Ordering-the-Board.md))
- ESP32 D1 mini (MH-ET LIVE MiniKit layout, 4 × 10 pins)
- XL6009 boost module, 41 × 18 mm, the common blue module with IN+/IN−/OUT+/OUT− holes at the corners
- RC-SPC1KA
- 5 V supply, 1.5 A or more. The heater draws about 0.8 A at 5 V (estimated from 3.4 W plus boost losses, not measured). Tested with the Waveshare Solar Power Manager (D).
- Optional: VEML7700 light sensor (I2C 0x10) in the sensor head
- Cable to the sensor head (the prototype uses 8-core), IP67 enclosure with desiccant. Keep metal and enclosure walls away from the antenna of the D1 mini; an optional reflector is described in [Board reference](Board-Reference.md#dimensions).

## Parts to solder yourself

JLCPCB places the SMD parts, including the HTU21D. You solder:

| Ref | Function | Part | Pitch | Hole |
|---|---|---|---|---|
| U1 | ESP32 D1 mini | 4 × female header 1×10, plus the matching male headers on the D1 mini | 2.54 mm | 1.0 mm |
| U2 | XL6009 module | 4 pins cut from a male header, through the module's IN/OUT holes | 2.54 mm | 1.0 mm |
| J1 | Power in (5V, GND, BAT) | screw terminal, 3 pins, wire entry from the board edge | 5.08 mm | 1.3 mm |
| J3 | Heater (HEAT+, HEAT−) | screw terminal, 2 pins, same type | 5.08 mm | 1.3 mm |
| J2 | Sensor (OSC, GND, NTC) | screw terminal, 3 pins, same type | 5.08 mm | 1.3 mm |
| J6 | I2C (3V3, GND, SDA, SCL) | screw terminal, 4 pins, same type | 5.08 mm | 1.3 mm |
| J4 | I2C socket | female header, 1×4 (optional) | 2.54 mm | 1.0 mm |
| J5 | I2C header | male header, 1×4 (optional) | 2.54 mm | 1.0 mm |
| J8 | Expansion | male header, 1×8 (optional) | 2.54 mm | 1.0 mm |
| C1 | Heater input buffer | 1000 µF / 16 V electrolytic, Ø10 mm, 5 mm pitch (optional) | 5.0 mm | – |

The terminal footprint follows the Phoenix MKDS 1,5/…-5,08 (horizontal, wire from the side). Common 5.08 mm terminals such as the KF128 or DG128 fit as well.

Set the XL6009 to 12 V before you solder it in: 5 V on IN, turn the trimmer until a multimeter reads 12 V at OUT.

## The sensor

The **RC-SPC1KA** from Radiocontrolli is a sealed capacitive rain sensor on an alumina substrate. Besides the sensing capacitor it carries a heater (about 42 Ω, roughly 3.4 W at 12 V) and an NTC (1 kΩ at 25 °C) for the surface temperature.

Dry, it measures about 100 pF. On the carrier board a fully wet surface reads about 3,100 pF (datasheet: more than 3,000 pF at full water cover). Rain on the 45° holder reads about 130–300 pF, because most of the water runs off; heavy rain reads lower than light rain.

It is sold by electronics distributors, for example [Novaut](https://www.novaut.com/en/620521-rc-spc1ka-radiocontrolli.html) (about 13 EUR incl. VAT, EU shipping), [TME](https://www.tme.com/us/en-us/details/rc-spc1ka/humidity-sensors/radiocontrolli/) and [DigiKey](https://www.digikey.com/en/products/detail/radiocontrolli/RC-SPC1KA/13688193). Prices and stock as of 2026-09; this project is not affiliated with any of them, nor with Radiocontrolli.

The element alone does nothing. This project adds the rest: a board that reads it and powers the heater from 5 V, and firmware that turns raw readings into a weather state and runs the heater safely.
