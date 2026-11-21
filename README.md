<div align="center">

# 🌧️ ESPHome Capacitive Rain Sensor

**A heated, sealed rain sensor for Home Assistant that tells rain from dew and fog.**<br>
RC-SPC1KA sensor element · ESP32 carrier board · ESPHome firmware

**English** · [Deutsch](README.de.md)

[![ESPHome](https://img.shields.io/badge/ESPHome-2026.x-000000?logo=esphome&logoColor=white)](https://esphome.io)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-native%20API-18BCF2?logo=homeassistant&logoColor=white)](https://www.home-assistant.io)
[![MQTT](https://img.shields.io/badge/MQTT-standalone%20variant-660066?logo=mqtt&logoColor=white)](docs/wiki/MQTT-and-Web-Page.md)
[![ESP32](https://img.shields.io/badge/ESP32-D1%20mini-E7352C?logo=espressif&logoColor=white)](docs/wiki/Board-Reference.md)
[![KiCad](https://img.shields.io/badge/KiCad-8%2B-314CB0?logo=kicad&logoColor=white)](hardware/)
[![Status](https://img.shields.io/badge/status-prototype-orange)](#-project-status)
[![Firmware: GPL-3.0](https://img.shields.io/badge/firmware-GPL--3.0-blue)](LICENSES/GPL-3.0.txt)
[![Hardware: CC BY-NC-SA 4.0](https://img.shields.io/badge/hardware-CC%20BY--NC--SA%204.0-lightgrey)](LICENSES/CC-BY-NC-SA-4.0.txt)

<img src="docs/board-rev-b.png" alt="Rev B carrier board, KiCad 3D view" width="620">

<sub>Rev B carrier board, 100 × 70 mm (KiCad 3D view). The ESP32 D1 mini and the XL6009 module plug in where the outlines are.</sub>

[Features](#-features) · [Status](#-project-status) · [Get started](#-get-started) · [Documentation](#-documentation) · [License](#-license)

</div>

---

## 💡 Why this sensor

<img src="docs/images/sensor-outdoor.jpg" alt="The sensor in its painted holder on the balcony, wet after rain" width="300" align="right">

Affordable rain sensors use contact grids that corrode within a season, or tipping buckets that report once a measurable amount of water has fallen. Off-the-shelf Zigbee and Wi-Fi rain sensors give you *rain: yes/no* and no way to fix it when they report morning dew as rain.

This sensor works differently:

- **Sealed capacitive element.** The electrodes sit under a sealed surface, so no metal is exposed to corrode. A few drops register.
- **Reads how the level moves.** Rain makes the reading jump; dew and a resting film keep it calm. The firmware starts rain on a fast rise or on jumps; the level alone never starts it.
- **Heated.** After the rain the heater dries the surface in one short run, and it clears frost.
- **Adjustable.** You get the full hardware and firmware. You change thresholds, heater limits and night mode in Home Assistant or on the device's web page, without reflashing.

### Typical uses

- Get notified when it starts to rain, before the laundry on the balcony is wet.
- Close roof windows, skylights, awnings or a pergola roof automatically, and open them again once it is dry.
- Turn on a light when heavy rain darkens the room.
- Pause irrigation during and right after rain.
- Log how long and how often it rained.
- Extend the board with light, pressure, UV or wind sensors and turn it into a small weather station.

---

## ✨ Features

<details open>
<summary><b>Detection</b></summary>

- [x] Weather state: dry or rain, plus a stalled-oscillator state
- [x] Start from the rate of rise on a dry plate and from the jumps on a wet one
- [x] End after a few calm minutes; at night from two calm 5-minute wakes
- [x] Frost lock: no false rain from thawing frost or snow
- [x] Tested in two months outdoors next to a tipping-bucket gauge: rain reported 2–5 minutes before the first tip
- [x] Wetting in % (RC-SPC1KA datasheet curve)

</details>

<details>
<summary><b>Heater control</b></summary>

- [x] One drying run 15 minutes after the rain ends
- [x] Frost heating below 1 °C plate temperature
- [x] Stays off during rain, so the sensor can see it
- [x] Stalled oscillator: one 10-minute drying attempt, then waits
- [x] Adjustable cut-off temperature (default 45 °C, at most 60 °C), checked every second
- [x] Heating-time budget with enforced pause; no new pulse on a low battery
- [x] Safe defaults: off after reset, off on an implausible NTC reading (open or shorted wire)

</details>

<details>
<summary><b>Connectivity and power</b></summary>

<img src="docs/images/ha-dashboard.jpg" alt="Home Assistant dashboard on a phone" width="220" align="right">

- [x] Home Assistant via the native ESPHome API
- [x] Standalone variant: local web page and MQTT (FHEM, ioBroker, Node-RED, Home Assistant MQTT discovery)
- [x] Encrypted OTA updates over Wi-Fi (Home Assistant variant)
- [x] Optional night mode: deep sleep with 5 min wake interval (needs a supply that stays on at low load)
- [x] Battery voltage monitoring
- [x] All settings adjustable at runtime, stored across reboots and sleep
- [x] German and English entity names

</details>

<details>
<summary><b>Hardware</b></summary>

- [x] Carrier board Rev B, 100 × 70 mm, 2 layers; JLCPCB places the SMD parts
- [x] ESP32 D1 mini and XL6009 heater module plug in; flash over the D1 mini's USB port
- [x] Runs from a single 5 V supply; the XL6009 makes the 12 V for the heater
- [x] Heater current on its own return path, away from the oscillator ground
- [x] HTU21D on board for the enclosure climate
- [x] I2C on socket, pin header and screw terminal; 8-pin expansion header
- [x] Supported add-ons: VEML7700 light sensor
- [ ] BME280, LTR390, anemometer, wind vane, tipping bucket (snippets in the wiki, untested)
- [x] 3D-printable sensor holder, also on [MakerWorld](https://makerworld.com/en/models/3655333-heated-rain-sensor-for-home-assistant) with a print profile
- [x] Perfboard build from modules as an alternative

</details>

---

## 🚦 Project status

| Part | Status |
|---|---|
| Firmware, German, Home Assistant API | ✅ Running outdoors on the Rev A board since 24 October |
| Firmware, English and MQTT variants | 🟡 Same logic, generated from the German file; compile in CI, not yet run on a device |
| Rain detection in real rain | ✅ Tested on more than ten rain days next to a tipping-bucket gauge, including two days of steady rain |
| Rev A carrier board | ✅ Runs outdoors with an external XL6009 heater module, R1 = 38.7 kΩ and the series capacitor; no oscillator stall since 7 November |
| Rev B carrier board | ⚪ Layout done with the Rev A fixes (R1 47 kΩ, series capacitor C3), DRC clean, fabrication files in the repo; not yet ordered |
| Sensor holder | ✅ 45° holder outdoors since 24 October |
| Weather add-ons | ⚪ Prepared in the YAML, untested |

How it got here: [Milestones](docs/wiki/Milestones.md) · What comes next: [Roadmap](docs/wiki/Roadmap.md)

---

## 🚀 Get started

1. **Parts.** The board from JLCPCB with an ESP32 D1 mini and an XL6009 module ([ordering](docs/wiki/Ordering-the-Board.md)), or a build from modules on perfboard ([Module Build Guide, PDF](docs/module-build-guide.pdf)), plus an RC-SPC1KA ([parts](docs/wiki/Parts.md)).
2. **Wiring.** Sensor to the SENSOR and HEATER terminals, 5 V to POWER IN ([wiring](docs/wiki/Wiring.md)).
3. **Flashing.** Flash the D1 mini once over USB with a device config that loads the firmware from this repository; later updates go over Wi-Fi ([flashing and updates](docs/wiki/Flashing-and-Updates.md)).
4. **Calibration.** Measure the dry frequency outdoors, check the thresholds ([calibration](docs/wiki/Calibration.md)).
5. **Home Assistant.** Home Assistant discovers the device. Without Home Assistant, use the [MQTT and web page](docs/wiki/MQTT-and-Web-Page.md) variant.

---

## 📚 Documentation

The **[wiki](docs/wiki/Home.md)** has the details:

| | |
|---|---|
| Getting started | [Parts](docs/wiki/Parts.md) · [Wiring](docs/wiki/Wiring.md) · [Flashing and updates](docs/wiki/Flashing-and-Updates.md) · [Calibration](docs/wiki/Calibration.md) |
| Build | [Ordering the board](docs/wiki/Ordering-the-Board.md) · [Module build](docs/wiki/Module-Build.md) · [Sensor holder](docs/wiki/Sensor-Holder.md) · [Board dimensions](docs/wiki/Board-Reference.md#dimensions) |
| Home Assistant | [Entities](docs/wiki/Entities.md) · [MQTT and web page](docs/wiki/MQTT-and-Web-Page.md) |
| How it works | [Measurement, rain or not, heater](docs/wiki/How-It-Works.md) |
| Reference | [Board reference](docs/wiki/Board-Reference.md) · [Extensions](docs/wiki/Extensions.md) · [Troubleshooting](docs/wiki/Troubleshooting.md) · [Known limitations](docs/wiki/Known-Limitations.md) |
| Project | [Milestones](docs/wiki/Milestones.md) · [Roadmap](docs/wiki/Roadmap.md) |

---

## 📁 Repository layout

| Path | Content |
|---|---|
| `firmware/` | ESPHome firmware: `regensensor_de/_en.yaml` (Home Assistant API), `regensensor_mqtt_de/_en.yaml` (web page and MQTT); `examples/` device configs that load it from GitHub |
| `hardware/` | KiCad project of the Rev B board (schematic, PCB, own symbols and footprints for D1 mini and XL6009) |
| `fabrication/` | Gerbers, drill files, JLCPCB BOM and CPL |
| `3d-files/` | Sensor holder STLs for 3D printing, board outline DXF for CAD |
| `docs/` | Wiki pages (`docs/wiki/`), images, Module Build Guide (PDF) and its source (`docs/build-guide/`) |
| `tools/` | Python scripts (KiCad 8 `pcbnew`, Freerouting) generating schematic, PCB, fabrication files and the dimension drawing from `design.py`; `regen_replay.py` replays a device log through the rain detection; `wiki_sync.py` mirrors `docs/wiki/` into the GitHub wiki |
| `.github/workflows/` | CI: firmware check of all four variants (`firmware.yml`), wiki mirror (`wiki.yml`), DRC and Gerber export (`fab.yml`) |

---

## ☕ Support

If this project saved you time, you can support it on Ko-fi.

<a href="https://ko-fi.com/heronidas"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support on Ko-fi"></a>

---

## 📄 License

The firmware is open source under the GPL. You may use the hardware for private and non-commercial purposes; commercial use needs my written permission, and I offer commercial licenses on request.

| Part | License |
|---|---|
| Hardware, fabrication files, sensor holder, documentation | [CC BY-NC-SA 4.0](LICENSES/CC-BY-NC-SA-4.0.txt) |
| Firmware and tools | [GPL-3.0-or-later](LICENSES/GPL-3.0.txt) |

If you build on this project, I'd appreciate a mention with a link back to this repository. The license does not require it.

[`LICENSE.md`](LICENSE.md) has the details, including passing on spare boards at cost.

<sub>RC-SPC1KA is a product of Radiocontrolli S.r.l. This project is independent and not affiliated with or endorsed by Radiocontrolli.</sub>
