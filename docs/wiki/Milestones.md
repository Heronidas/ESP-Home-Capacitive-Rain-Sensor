# Milestones

How I got the sensor to where it is, dead ends included. Each setback carries a short note on what I learned, so you can skip the same mistakes.

### Early September 2026: a rain sensor that does not corrode
Affordable rain sensors use copper comb boards that corrode within a season. I considered coating one with gold leaf and dropped the idea: the leaf does not bond and the copper corrodes at each pore. A Zigbee comb sensor served as a stopgap. For the real solution I followed Magnus Thomé's capacitive rainmeter with the sealed, heated RC-SPC1KA element.

### Early September: a heater does not run on batteries *(setback)*
My first plan assumed battery power alone, which rules out a heater. I answered that with a small solar system: an 18 V / 10 W panel, a Waveshare Solar Power Manager, three 18650 cells and a 5 V to 12 V boost converter that switches off together with the heater.

**Learned:** the heater sets the power budget; the rest draws little.

### Mid September: dew point dropped, then back for free
I planned an SHT31 for the dew point, then dropped it to save a sensor and let the heater work on capacitance bands alone. Later the outdoor sensor already in Home Assistant supplied temperature and humidity, and the dew point came back without extra hardware.

**Learned:** use the data the smart home already has.

### Mid September: first build
I built a Wemos D1 mini (ESP8266) on perfboard and measured capacitance as charge time through 1 MΩ, as in the reference project. I glued the sensor into a printed ASA holder and covered the contacts on the back with Kapton tape.

### ~20 September: capacitance always "NaN" *(setback)*
The measurement never returned a value. I checked the sensor, the cable, the GPIOs and the solder joints, and they were fine. The 1 MΩ charge resistor was too large for this measuring method.

### 24 September: charge-time measurement hits its limit *(setback)*
With 500 kΩ the samples jumped around; 100 kΩ worked but read about 166 pF dry, and drizzle stayed below the threshold. A small leakage at the measuring node keeps the voltage from reaching the ESP8266 switching point at 75 % of the supply, and a larger resistor makes it worse. The datasheet's reference circuit uses a Schmitt-trigger oscillator, which switches at about half the supply.

**Learned:** follow the measuring principle the manufacturer designed the element for.

### 25 September: frequency measurement on an ESP32
I switched to an SN74HC14 Schmitt-trigger relaxation oscillator. On the ESP8266 the I2C reads disturbed the software counting, so I moved to an ESP32 and its hardware pulse counter (PCNT). The firmware now calculates capacitance relative to the measured dry frequency, which needs no offset calibration.

**Learned:** hardware counting gives far less noise than software interrupts.

### 26 September: night mode needed a different charge controller *(setback)*
The Waveshare Solar Power Manager (C) switched its output off at low load, so the ESP32 never woke from deep sleep. The (D) version keeps the output on in low-current mode. I also replaced the DHT11 with an HTU21D.

**Learned:** check that the supply stays on at a few mA before you rely on deep sleep.

### 26 September: Rev A carrier board
I designed the board in KiCad, ordered it fully assembled from JLCPCB and created the repository.

### 27 September: weather state logic
I added dew detection via the distance to the dew point, a frost point below 0 °C, morning and evening dew, and hysteresis against flickering states.

### 28 September: placement error caught before production *(setback)*
The JLCPCB preview showed U2 and U3 (SOT-23-5/6) rotated by 90°. I fixed the rotation in the CPL file.

**Learned:** check pin 1 of each IC in the assembly preview.

### 1 October: standalone variant
I added a local web page and MQTT for FHEM, ioBroker and others, plus English firmware alongside German.

### 2 October: first real rain, oscillator stalled *(setback)*
The frequency dropped to 0 Hz. Water on the plate added a leakage path that the oscillator could not drive with a 1 MΩ feedback resistor. Before that, dew had read almost like rain, and the sensor missed rain. I changed R1 to 220 kΩ.

**Learned:** lab tests with a damp cloth do not replace real rain.

### 3 October: test series with 220 kΩ
The oscillator stayed stable in each test: dry ~100 pF, spray mist ~270, three drops ~290, heavy spray ~600, soaked cloth 870–1240 pF. The firmware now detects drizzle and rain by rate of rise, with a rain-end timer and a short heater test.

### 3 October: false rain alert *(setback)*
A notification fired without rain because the automations listened to "humid" instead of "rain". I switched them to the rain sensor.

### 4 October: night behaviour and first fog morning
I removed the short "unknown" states after each wake; the firmware restores the last weather state across sleep. The heater no longer runs while dew or frost forms, which saves energy. I logged the first fog morning: capacitance stayed flat at ~187 pF while the plate warmed a little. I added morning drying, one short heat pulse a day once the surface is above the dew point. In fog the surface got wet again within ten minutes of a heat pulse (about 7 pF/min) although it was above the dew point; I noted that re-wetting as a candidate for fog detection.

### 8 October: Rev A arrives, oscillator stalls in steady rain *(setback)*
The assembled boards came with 1 MΩ for R1, so I changed it to 220 kΩ as on the prototype. In steady rain the prototype oscillator dropped to 0 Hz and ran again after I wiped the plate. Water had reached the solder pads at the edge of the sensor.

**Learned:** seal the back and the edge of the element as well as the face.

### 9 October: rain only, no dew logic
I took dew, frost, fog and morning drying out of the firmware. They needed outdoor temperature and humidity and misjudged too often. The firmware detects drizzle and rain by rate of rise and heats when the surface is wet; it needs no outdoor data and no blueprint.

**Learned:** each weather state added a way to be wrong.

### 9–10 October: battery empty overnight *(setback)*
The heater ran at dew level and kept trying to dry a stalled oscillator until the battery was flat. I raised the heating threshold above the dew level (300 pF) and capped heating against a stalled oscillator at 10 minutes per episode.

**Learned:** a heating rule needs a limit that holds when the reading is wrong.

### 10 October: water inside the sensor head *(setback)*
Runoff collected under the sensor on the lid and crept into the box by capillary action. A silica pad went in as a stopgap. The new head had to leave no gap below the sensor.

### 11 October: false drizzle from passing clouds *(setback)*
Clouds after sunshine cooled the plate, it took up humidity and the firmware read that as drizzle. The firmware now blocks the drizzle latch while the plate cools (2 K below the peak of the last 5–10 minutes). I tried a 30-second median against dew noise and dropped it, because it would have hidden real drizzle too.

**Learned:** blocking drizzle during cooling works better than smoothing the signal.

### 12 October: frost melt stalls the sensor, prototype taken down *(setback)*
At −1 °C the heater melted frost. The water ran to the edge of the flat holder and stalled the oscillator. Heating did not dry it; wiping did. The same night exposed a firmware bug: the oscillator ran while the plate was hot, which reset the 10-minute limit, so the heater came on at each wake. The limit now resets once the plate has cooled. I took the prototype down.

**Learned:** the holder must give water no place to stand, and a drying limit has to judge a cooled plate.

### 12 October: 45° tilt
In a drop test a drop stayed at 20°, slid from about 30° and at 45° smaller drops slid too. A steeper angle adds little and loses catch area for drizzle. Turning the sensor onto a corner made no difference.

### 13–14 October: new sensor holder
The sensor sits proud on a pedestal a little smaller than the element, so water drips off all four edges. Gutters and side shields run beside it without touching it, and the cable slot sits at the lower edge. The holder is white ASA-GF, primed and painted. Sikaflex bonds the sensor and seals the whole back instead of potting; it stays elastic while the plastic expands with heat.

### 15 October: Rev A in service
I flashed the board once over UART; the API key now encrypts OTA updates. Home Assistant moved the existing device onto the new board ("migrate" in the name-conflict dialog) and kept entity IDs, dashboard and history. Battery voltage reads correctly. An aluminium plate 2 cm behind the antenna reflects the WiFi signal towards the access point.

### 17 October: bench test on Rev A
With the same cable as on the prototype, the dry frequency rose from 14.6 to 35 kHz. The board carries less stray capacitance at the oscillator than the perfboard did. A wet surface reads 31 times the dry value instead of 10 times, and a single drop doubles the reading. The heater warmed the plate from 23 to 45 °C in 30 seconds. While it runs, the oscillator stops. The firmware skips readings during heating and pauses the heater for a clean one.

**Learned:** stray capacitance in the wiring dilutes the signal more than the cable does.

### Next
See [Roadmap](Roadmap.md).
