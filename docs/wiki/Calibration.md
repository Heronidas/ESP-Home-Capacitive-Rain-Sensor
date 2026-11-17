# Calibration

1. **Dry frequency.** Mount the sensor where it will stay, surface dry, heater off, sealant cured. Let it settle outdoors for 1–2 hours, average *Frequency* over the last half hour and enter it as *Dry Frequency*. The YAML start value (125,000 Hz) fits Rev B with R1 = 47 kΩ; cable, holder and sealant shift it. The Rev A board with R1 = 38.7 kΩ, the 45° holder and its cable reads about 151,500 Hz.

   The dry frequency also follows the air humidity. Indoors it moved by about 0.2 % per percentage point of relative humidity, and the sealant shifted it for about a day after bonding. Calibrate outdoors with a cured holder.
2. **NTC.** Reference thermometer next to the head, same air, no sun, heater off for 30 min. Trim with `adc_faktor` / `adc_factor` (coarse) or *Temperature Offset (NTC)* (fine, ±5 K). Do not calibrate against the air under a clear night sky: the plate runs 1.5–3 K colder there.
3. **Thresholds.** The defaults come from the Rev A board on the 45° holder, two months outdoors:

   | Condition | Capacitance |
   |---|---|
   | dry | 100–108 pF (rises about 0.2 pF per kelvin) |
   | evening film, dew | 103–115 pF |
   | rain, wet plate | 130–300 pF; heavy rain reads lower, the water runs off |
   | thawing frost film | up to 460 pF |

   The thresholds work in pF and pF/min relative to the dry frequency, so they carry over to other boards. Check them against your first rain: watch *Capacitance Rate of Change* and *Capacitance Steps* at the start and *Capacitance Unrest* at the end. Adjust the number entities; no reflash.
4. **Dry Below.** Note the level your plate settles at on a dry evening and keep *Dry Below* a few pF above it.
5. **First night.** Leave *Auto Mode* off to see the raw values without heater influence.

`tools/regen_replay.py` replays a log of the German firmware through the day detection. Set the thresholds at the top of the script and test them on a past rain before you change them on the device.
