# Flashing and updates

Flash the ESP32 D1 mini over its own USB port before you plug it into the board: on Rev B the I2C terminal sits below the USB port. Later updates go over Wi-Fi.

1. Connect the D1 mini to your computer by USB.
2. In your ESPHome folder, create a device config from [`firmware/examples/regensensor.yaml`](../../firmware/examples/regensensor.yaml) (German entity names) or [`rain-sensor.yaml`](../../firmware/examples/rain-sensor.yaml) (English). It loads the firmware straight from this repository; pick the variant in `files:` and override any substitution there.
3. Install it once over USB. Later updates go over Wi-Fi: *Install* in ESPHome fetches the current firmware from GitHub.

| Variant | File | Secrets |
|---|---|---|
| Home Assistant, German | `regensensor_de.yaml` | `regensensor_api_key` |
| Home Assistant, English | `regensensor_en.yaml` | `rain_sensor_api_key` |
| MQTT + web page, German | `regensensor_mqtt_de.yaml` | `regensensor_ota_password`, `mqtt_*` |
| MQTT + web page, English | `regensensor_mqtt_en.yaml` | `rain_sensor_ota_password`, `mqtt_*` |

`secrets.yaml` also needs `wifi_ssid`, `wifi_password` and `wifi_ap_password`; the MQTT variants additionally `mqtt_broker`, `mqtt_username`, `mqtt_password`. To keep the firmware fixed, set `ref:` to a release tag such as `v0.1.0` instead of `main`. Copying a firmware file into your ESPHome folder and flashing it directly works too.

If the sensor cannot reach your Wi-Fi, it opens the hotspot "Regensensor Fallback" (EN: "Rain Sensor Fallback"). Connect with `wifi_ap_password` (at least 8 characters) and enter new Wi-Fi credentials on the page that opens.

In the Home Assistant variants the API key also encrypts and authenticates OTA updates, so there is no separate OTA password. This needs ESPHome 2026.9 or newer. The key cannot be rotated: keep it, because without it only a USB flash (or the captive-portal upload) gets the device back.

For the standalone variant, see [MQTT and web page](MQTT-and-Web-Page.md).

## Updates

Updates go over Wi-Fi. During the day the sensor is awake and accepts an update at any time. In night mode it wakes every 5 minutes for about 35 s; an update started in that window keeps it awake until it is done. Otherwise wait for the night window to end, or switch *Night Mode* off (takes effect at the next wake).

ESPHome writes the new firmware to a second partition and switches over only once it is complete; an interrupted update leaves the old version running. If a new version crashes repeatedly at boot, ESPHome starts a safe mode with only Wi-Fi and OTA, so a fixed version can still be installed over the air.
