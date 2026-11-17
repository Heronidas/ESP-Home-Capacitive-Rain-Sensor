# Extensions

| Sensor | Connection | Status |
|---|---|---|
| RC-SPC1KA (capacitance, NTC, heater) | screw terminals SENSOR / HEATER | ✅ supported |
| VEML7700 light sensor | I2C (socket, header or terminal), 0x10 | ✅ supported |
| HTU21D temperature / humidity, inside the enclosure | on board (Rev B); Rev A: I2C socket | ✅ supported |
| Battery voltage | J1 pin BAT | ✅ supported |
| BME280 / BMP280 pressure, LTR390 UV | I2C, 3.3 V modules (0x76, 0x53) | ⚪ snippet below, untested |
| Cup anemometer, wind vane, tipping bucket | J8: IO27, IO33, IO26 | ⚪ snippet below, untested; tips during night-mode sleep are lost |
| DS18B20, CO₂ and others | J8 / I2C | ⚪ hardware ready, no firmware |

IO32 doubles as the alternative NTC pull-up drive (see [solder jumpers](Board-Reference.md#solder-jumpers)). The expansion header has no 5 V pin. The HTU21D on the board uses I2C address 0x40; modules on the same bus need another address.

## Untested snippets

Add under `sensor:` and check address and pins.

```yaml
  # Pressure, temperature, humidity (I2C 0x76; BMP280: bmp280_i2c).
  - platform: bme280_i2c
    address: 0x76
    update_interval: 8s
    temperature:
      name: "Outdoor Temperature"
    pressure:
      name: "Pressure"
    humidity:
      name: "Outdoor Humidity"

  # UV (I2C 0x53).
  - platform: ltr390
    address: 0x53
    update_interval: 8s
    uv_index:
      name: "UV Index"

  # Cup anemometer, reed contact to GND (2.4 km/h per pulse/s is common).
  - platform: pulse_counter
    pin:
      number: GPIO27
      mode: INPUT_PULLUP
    name: "Wind"
    unit_of_measurement: "km/h"
    update_interval: 10s
    filters:
      - multiply: 0.04   # pulses/min -> km/h

  # Wind vane (resistor network to GND, pull-up to 3V3): raw voltage, map it
  # to directions for your vane. ADC1 pin, so it works with WiFi.
  - platform: adc
    pin: GPIO33
    name: "Wind Vane Voltage"
    attenuation: 12db
    update_interval: 10s

  # Tipping bucket, reed contact to GND (0.2794 mm per tip is common).
  - platform: pulse_counter
    pin:
      number: GPIO26
      mode: INPUT_PULLUP
    name: "Rain Rate"
    unit_of_measurement: "mm/h"
    update_interval: 60s
    filters:
      - multiply: 16.764  # tips/min -> mm/h
    total:
      name: "Rain Amount"
      unit_of_measurement: "mm"
      filters:
        - multiply: 0.2794
```
