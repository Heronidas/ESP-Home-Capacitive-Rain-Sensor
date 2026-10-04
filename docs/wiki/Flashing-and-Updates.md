# Flashing and updates

The board has no USB port. Use the UART header J7 (adapter RX to TX, TX to RX, GND to GND) and power the board through POWER IN; J7 has no power pin.

1. Hold BOOT, tap RESET, release BOOT.
2. In your ESPHome folder, create a device config from [`firmware/examples/regensensor.yaml`](../../firmware/examples/regensensor.yaml) (German entity names) or [`rain-sensor.yaml`](../../firmware/examples/rain-sensor.yaml) (English). It loads the firmware straight from this repository; pick the variant in `files:` and override any substitution there.
3. Install it once over USB/UART. Later updates go over Wi-Fi: *Install* in ESPHome fetches the current firmware from GitHub.

| Variant | File | API key | OTA password |
|---|---|---|---|
| Home Assistant, German | `regensensor_de.yaml` | `regensensor_api_key` | `regensensor_ota_password` |
| Home Assistant, English | `regensensor_en.yaml` | `rain_sensor_api_key` | `rain_sensor_ota_password` |
| MQTT + web page, German | `regensensor_mqtt_de.yaml` | – | `regensensor_ota_password` |
| MQTT + web page, English | `regensensor_mqtt_en.yaml` | – | `rain_sensor_ota_password` |

`secrets.yaml` needs `wifi_ssid`, `wifi_password` and the keys above (MQTT variants also `mqtt_broker`, `mqtt_username`, `mqtt_password`). To keep the firmware fixed, set `ref:` to a release tag instead of `main`. Copying a firmware file into your ESPHome folder and flashing it directly works too.

For the dew point, set your outdoor sensors in the substitutions (`aussen_temp_entity` / `aussen_feuchte_entity` in DE, `outdoor_temp_entity` / `outdoor_humidity_entity` in EN), or use the [blueprint](Outdoor-Air.md). Missing entities are fine; the fallback applies. For the standalone variant, see [MQTT and web page](MQTT-and-Web-Page.md).

## Updates

Updates go over Wi-Fi. During the day the sensor is awake and accepts an update at any time. In night mode it wakes every 5 minutes for about 35 s; an update started in that window keeps it awake until it is done. Otherwise wait for the night window to end, or switch *Night Mode* off (takes effect at the next wake).

ESPHome writes the new firmware to a second partition and switches over only once it is complete; an interrupted update leaves the old version running. If a new version crashes repeatedly at boot, ESPHome starts a safe mode with only Wi-Fi and OTA, so a fixed version can still be installed over the air.
