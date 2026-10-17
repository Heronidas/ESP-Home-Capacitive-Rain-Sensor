# Roadmap

- **Rev A board:** run it outdoors in the new holder. Find out whether the heater disturbs the oscillator through the board, the cable or the sensor itself.
- **Real rain:** set the drizzle and rain thresholds from real drizzle and rain, and confirm the rain-end timer and the heater test.
- **Fog:** report fog as its own state; in fog the plate wets again within minutes after a heat pulse while the surface temperature stays steady.
- **Rain duration:** rain minutes per day from the firmware, so MQTT setups get it too (Home Assistant can already count it with a helper).
- **Frost and snow:** detect frost (surface below 0 °C and rising capacitance) and thaw on purpose; snow needs a winter of testing.
- **Weather add-ons:** test BME280, LTR390, anemometer, wind vane and tipping bucket (snippets on the Extensions page).
- **Public release:** web installer for the first flash, adoption in ESPHome, updates from GitHub releases.
- **Photos** of the finished sensor once the project leaves prototype status.
