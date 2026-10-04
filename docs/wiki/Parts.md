# Parts

- The carrier board, assembled by JLCPCB ([Ordering](Ordering-the-Board.md)); screw terminals and pin headers are hand-soldered
- RC-SPC1KA
- 5 V supply, 1.5 A or more. The heater draws about 0.8 A at 5 V (estimated from 3.4 W plus boost losses, not measured). Tested with the Waveshare Solar Power Manager (D).
- USB-UART adapter with 3.3 V logic for the first flash; updates then go over Wi-Fi
- Optional: VEML7700 light sensor (I2C 0x10), HTU21D (GY-21) inside the enclosure
- Cable to the sensor head (the prototype uses 8-core), IP67 enclosure with desiccant. Keep metal and enclosure walls away from the antenna at the board's top edge.

## The sensor

The **RC-SPC1KA** from Radiocontrolli is a sealed capacitive rain sensor on an alumina substrate. Besides the sensing capacitor it carries a heater (about 42 Ω, roughly 3.4 W at 12 V) and an NTC (1 kΩ at 25 °C) for the surface temperature.

Dry, it measures about 100 pF. On the prototype a soaked surface reads about 900–1250 pF (RC-SPC1K datasheet: more than 550 pF at full water cover).

It is sold by electronics distributors, for example [Novaut](https://www.novaut.com/en/620521-rc-spc1ka-radiocontrolli.html) (about 13 EUR incl. VAT, EU shipping), [TME](https://www.tme.com/us/en-us/details/rc-spc1ka/humidity-sensors/radiocontrolli/) and [DigiKey](https://www.digikey.com/en/products/detail/radiocontrolli/RC-SPC1KA/13688193). Prices and stock as of 2026-09; this project is not affiliated with any of them, nor with Radiocontrolli.

The element alone does nothing. This project adds the rest: a board that reads it and powers the heater from 5 V, and firmware that turns raw readings into a weather state and runs the heater safely.
