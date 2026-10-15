<div align="center">

# 🌧️ ESPHome Capacitive Rain Sensor

**A heated, sealed rain sensor for Home Assistant that tells rain from dew and fog.**<br>
RC-SPC1KA sensor element · ESP32 carrier board · ESPHome firmware

[![ESPHome](https://img.shields.io/badge/ESPHome-2026.x-000000?logo=esphome&logoColor=white)](https://esphome.io)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-native%20API-18BCF2?logo=homeassistant&logoColor=white)](https://www.home-assistant.io)
[![MQTT](https://img.shields.io/badge/MQTT-standalone%20variant-660066?logo=mqtt&logoColor=white)](docs/wiki/MQTT-and-Web-Page.md)
[![ESP32](https://img.shields.io/badge/ESP32-WROOM--32E-E7352C?logo=espressif&logoColor=white)](docs/wiki/Board-Reference.md)
[![KiCad](https://img.shields.io/badge/KiCad-7%2B-314CB0?logo=kicad&logoColor=white)](hardware/)
[![Status](https://img.shields.io/badge/status-prototype-orange)](#-project-status)
[![Firmware: GPL-3.0](https://img.shields.io/badge/firmware-GPL--3.0-blue)](LICENSES/GPL-3.0.txt)
[![Hardware: CC BY-NC-SA 4.0](https://img.shields.io/badge/hardware-CC%20BY--NC--SA%204.0-lightgrey)](LICENSES/CC-BY-NC-SA-4.0.txt)

<img src="docs/board-3d.png" alt="Rev A carrier board, KiCad 3D view" width="560">

<sub>Rev A carrier board, 72 × 56 mm (KiCad 3D view; magenta dots mark pin 1 as in the JLCPCB preview)</sub>

[Features](#-features) · [Status](#-project-status) · [Get started](#-get-started) · [Documentation](#-documentation) · [License](#-license)

</div>

---

## 💡 Why this sensor

Most affordable rain sensors are contact grids that corrode within a season, or tipping buckets that only report once a measurable amount of water has fallen. Off-the-shelf Zigbee and Wi-Fi rain sensors are a black box: you get *rain: yes/no*, and no way to fix it when it reports dew as rain every morning.

This project takes a different approach:

- **Sealed capacitive element.** No exposed metal, nothing to corrode. It reacts to a few drops, not to a bucketful.
- **Heated.** Once the rain stops, the heater dries the surface, so the sensor reports dry within minutes instead of hours. It also clears frost.
- **Knows what it measures.** Precipitation wets the surface many times faster than dew, fog or humid air; the rate of rise tells them apart.
- **Fully adjustable.** Hardware and firmware are published in full. Thresholds, heater limits and night mode are runtime settings in Home Assistant or on the device's own web page; no reflash needed.

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

- [x] Weather state: dry, drizzle, rain
- [x] Drizzle and rain detected by rate of rise
- [x] Wetting in % (RC-SPC1K datasheet curve)

</details>

<details>
<summary><b>Heater control</b></summary>

- [x] Dries the film after rain, heavy fog and frost
- [x] Stalled oscillator (water at the pads): one 10-minute drying attempt, then waits
- [x] Stays off during drizzle and rain, so the sensor can see the precipitation
- [x] Rain end detection: no rise for a set time, then a short heater test confirms
- [x] Over-temperature cut-off at 45 °C, checked every second
- [x] Heating-time budget with enforced pause
- [x] Safe defaults: off after reset, off on an implausible NTC reading (open or shorted wire)

</details>

<details>
<summary><b>Connectivity and power</b></summary>

- [x] Home Assistant via the native ESPHome API
- [x] Standalone variant: local web page and MQTT (FHEM, ioBroker, Node-RED, Home Assistant MQTT discovery)
- [x] Encrypted OTA updates over Wi-Fi (Home Assistant variant)
- [x] Optional night mode: deep sleep with 5 min wake interval
- [x] Battery voltage monitoring
- [x] All settings adjustable at runtime, stored across reboots and sleep
- [x] German and English entity names

</details>

<details>
<summary><b>Hardware</b></summary>

- [x] ESP32 carrier board, 72 × 56 mm, 2 layers, orderable fully assembled from JLCPCB
- [x] Runs from a single 5 V supply; generates the 12 V for the heater on board
- [x] Reverse-polarity protection
- [x] I2C on Qwiic, pin socket and screw terminal; 8-pin expansion header
- [x] Supported add-ons: VEML7700 light sensor, HTU21D enclosure climate
- [ ] BME280, LTR390, anemometer, wind vane, tipping bucket (snippets in the wiki, untested)
- [x] 3D-printable sensor holder

</details>

---

## 🚦 Project status

| Part | Status |
|---|---|
| Firmware | ✅ Running on the Rev A board; detection logic tested on a perfboard prototype in spray, drop and soak tests |
| Rain detection in real rain | 🟡 Thresholds set from tests, confirmation in real rain pending |
| Rev A carrier board | 🟡 Built and flashed: boots, Wi-Fi, encrypted OTA, I2C and battery voltage work; test with sensor and heater pending |
| Sensor holder | 🟡 New 45° holder, STLs available; field test pending |
| Weather add-ons | ⚪ Prepared in the YAML, untested |

How it got here: [Milestones](docs/wiki/Milestones.md) · What comes next: [Roadmap](docs/wiki/Roadmap.md)

---

## 🚀 Get started

1. **Parts.** The assembled board from JLCPCB ([ordering](docs/wiki/Ordering-the-Board.md)) or a build from modules on perfboard ([Module Build Guide, PDF](docs/module-build-guide.pdf)), plus an RC-SPC1KA ([parts](docs/wiki/Parts.md)).
2. **Wiring.** Sensor to the SENSOR and HEATER terminals, 5 V to POWER IN ([wiring](docs/wiki/Wiring.md)).
3. **Flashing.** Once over the UART header with a device config that loads the firmware from this repository; all later updates go over Wi-Fi ([flashing and updates](docs/wiki/Flashing-and-Updates.md)).
4. **Calibration.** Enter the dry frequency, check the thresholds ([calibration](docs/wiki/Calibration.md)).
5. **Home Assistant.** The device is discovered automatically. Without Home Assistant, use the [MQTT and web page](docs/wiki/MQTT-and-Web-Page.md) variant.

---

## 📚 Documentation

The **[wiki](docs/wiki/Home.md)** covers everything in detail:

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
| `hardware/` | KiCad project (schematic, PCB) |
| `fabrication/` | Gerbers, drill files, JLCPCB BOM and CPL |
| `mechanical/` | Sensor holder STLs, board outline DXF |
| `docs/` | Wiki pages (`docs/wiki/`), images, Module Build Guide (PDF) and its source (`docs/build-guide/`) |
| `tools/` | Python scripts (KiCad 7 `pcbnew`) generating schematic, PCB and fabrication files from `design.py` |
| `.github/workflows/fab.yml` | CI: DRC and Gerber export |

---

## ☕ Support

If this project saved you time, you can support it on Ko-fi. Not required, always appreciated.

<a href="https://ko-fi.com/heronidas"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support on Ko-fi"></a>

---

## 📄 License

The firmware is open source under the GPL. The hardware is free for private and non-commercial use; commercial use of the hardware requires written permission, and commercial licenses are available on request.

| Part | License |
|---|---|
| Hardware, fabrication files, sensor holder, documentation | [CC BY-NC-SA 4.0](LICENSES/CC-BY-NC-SA-4.0.txt) |
| Firmware and tools | [GPL-3.0-or-later](LICENSES/GPL-3.0.txt) |

If you build on this project, a mention with a link back to this repository is appreciated. This is a friendly request, not an extra license condition.

Details, including passing on spare boards at cost, in [`LICENSE.md`](LICENSE.md).

<sub>RC-SPC1KA is a product of Radiocontrolli S.r.l. This project is independent and not affiliated with or endorsed by Radiocontrolli.</sub>
