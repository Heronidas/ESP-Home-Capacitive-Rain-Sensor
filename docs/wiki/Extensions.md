# Extensions

| Sensor | Connection | Status |
|---|---|---|
| RC-SPC1KA (capacitance, NTC, heater) | screw terminals SENSOR / HEATER | ✅ supported |
| VEML7700 light sensor | I2C (Qwiic, socket or terminal), 0x10 | ✅ supported |
| HTU21D temperature / humidity, inside the enclosure | I2C socket labelled HTU21D | ✅ supported |
| Battery voltage | J1 pin BAT | ✅ supported |
| BME280 / BMP280 pressure, LTR390 UV | I2C, 3.3 V modules (0x76, 0x53) | ⚪ commented out in the YAML, untested |
| Cup anemometer, wind vane, tipping bucket | J8: IO27, IO33, IO26 | ⚪ commented out in the YAML, untested; tips during night-mode sleep are lost |
| DS18B20, CO₂ and others | J8 / I2C | ⚪ hardware ready, no firmware |

IO32 doubles as the alternative NTC pull-up drive (see solder jumpers). The expansion header has no 5 V pin.
