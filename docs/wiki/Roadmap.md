# Roadmap

- **Rev B:** order the board, build it and repeat the bench tests: dry frequency with R1 = 47 kΩ and C3, oscillator during heating, night mode, HTU21D on the tongue.
- **Drop counting:** count single drops in the 2-second readings instead of the 10-second steps. A first look at the logs separates light rain on a wet plate (2.6 events per minute) from a calm wet plate (0.1). Test it offline on all logs first.
- **Power budget:** measure panel, battery and heater current (INA3221) and size panel and cells for winter.
- **Snow:** find out what snow looks like on the heated plate; the frost lock keeps rain off below 1 °C until then.
- **Rain duration:** rain minutes per day from the firmware, so MQTT setups get it too (Home Assistant can count it with a helper).
- **Weather add-ons:** test BME280, LTR390, anemometer, wind vane and tipping bucket (snippets on the Extensions page).
- **Public release:** web installer for the first flash, adoption in ESPHome, updates from GitHub releases.
- **Photos** of the finished sensor once the project leaves prototype status.
