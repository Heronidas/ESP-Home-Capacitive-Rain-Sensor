# MQTT and web page

`firmware/regensensor_mqtt_de.yaml` / `regensensor_mqtt_en.yaml`: same logic and entities, without the Home Assistant API. For FHEM, ioBroker, Node-RED or any MQTT broker; Home Assistant still finds the device through MQTT discovery.

- **Web page.** `http://<device-ip>/` shows all states and settings and accepts OTA uploads. Served by the device itself, no internet or login required; keep it in a trusted network.
- **MQTT.** `secrets.yaml` additionally needs `mqtt_broker`, `mqtt_username` and `mqtt_password`. States go to `regensensor/<component>/<name>/state` (EN: `rain-sensor/…`), retained. Birth, will and shutdown messages are off, so the last states stay visible while the device sleeps.
- **Time.** From SNTP (`zeitzone` / `timezone` substitution, default Europe/Berlin).
- **Night mode.** Commands sent while the device sleeps are lost, as with the API. Switch night mode off while it is awake.
