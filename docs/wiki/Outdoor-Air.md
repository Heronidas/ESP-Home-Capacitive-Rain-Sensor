# Outdoor air and blueprint

Both ways are optional. Without outdoor data the firmware uses the fallback (slow wetting in the dark reads as dew).

- **Substitutions.** Set the outdoor temperature and humidity entities in the YAML. Simple, but Home Assistant can take up to a minute to deliver the values after boot, so it does not help in night mode (the device is awake for about 35 s).
- **Blueprint (recommended).** `blueprints/regensensor_aussenluft.yaml`: pick your outdoor sensors in the UI (trigger sensor: *NTC Widerstand* / *NTC Resistance* of the rain sensor). It pushes them through the `set_aussenluft` action on the first reading after each wake-up; the dew point is available about 12 s after waking. While the device is awake all day, it pushes about every 40 s. Copy the file to `config/blueprints/automation/` (or import it from the GitHub URL) and create an automation from it.
