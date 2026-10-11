# Roadmap

- **Rev A board:** build and test the carrier board; results go into [Known limitations](Known-Limitations.md).
- **Real rain:** confirm the drizzle and rain detection (15–18 / 150 pF/min), the rain-end timer and the heater test in real rain.
- **Fog:** report fog as its own state; in fog the plate wets again within minutes after a heat pulse while the surface temperature stays steady.
- **Rain duration:** rain minutes per day from the firmware, so MQTT setups get it too (Home Assistant can already count it with a helper).
- **Frost and snow:** detect frost (surface below 0 °C and rising capacitance) and thaw on purpose; snow needs a winter of testing.
- **Weather add-ons:** test BME280, LTR390, anemometer, wind vane and tipping bucket (snippets on the Extensions page).
- **Public release:** web installer for the first flash, adoption in ESPHome, updates from GitHub releases.
- **Photos** of the finished sensor once the project leaves prototype status.
