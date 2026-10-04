# Milestones

How the sensor got to where it is, including the dead ends. Each setback has a short note on what was learned, so others can skip the same mistakes.

### Early September 2026: a rain sensor that does not corrode
Affordable rain sensors use copper comb boards that corrode within a season. Coating one with gold leaf was considered and dropped (it does not bond and corrodes at every pore). A Zigbee comb sensor served as a stopgap. The model for the real solution was Magnus Thomé's capacitive rainmeter with the sealed, heated RC-SPC1KA element.

### Early September: a heater does not run on batteries *(setback)*
The first plan assumed battery power only, which rules out a heater. The answer was a small solar system: 18 V / 10 W panel, Waveshare Solar Power Manager, three 18650 cells, and a 5 V to 12 V boost converter that is switched off together with the heater.

**Learned:** the heater sets the power budget, everything else is small change.

### Mid September: dew point dropped, then back for free
An SHT31 for the dew point was planned, then dropped to save a sensor; the heater was to work on capacitance bands alone. Later the outdoor sensor already in Home Assistant supplied temperature and humidity, and the dew point came back without extra hardware.

**Learned:** use the data the smart home already has.

### Mid September: first build
Wemos D1 mini (ESP8266) on perfboard, capacitance measured as charge time through 1 MΩ as in the reference project. Sensor glued into a printed ASA holder, contacts on the back covered with Kapton tape.

### ~20 September: capacitance always "NaN" *(setback)*
The measurement never returned a value. Sensor, cable, GPIOs and every solder joint checked out fine; the only cause was the 1 MΩ charge resistor, too large for this measuring method.

### 24 September: charge-time measurement hits its limit *(setback)*
500 kΩ gave unstable samples, 100 kΩ worked but read ~166 pF dry, and drizzle stayed below the threshold. A small leakage at the measuring node keeps it from reaching the ESP8266 switching point at 75 % of the supply, and the larger the resistor, the worse it gets. The datasheet's reference circuit uses a Schmitt-trigger oscillator, which switches at about half the supply.

**Learned:** follow the measuring principle the manufacturer designed the element for.

### 25 September: frequency measurement on an ESP32
SN74HC14 Schmitt-trigger relaxation oscillator. On the ESP8266, software counting was disturbed whenever the I2C sensors were read, so the controller changed to an ESP32 whose hardware pulse counter (PCNT) counts independently. Capacitance is now relative to the measured dry frequency; no offset calibration needed.

**Learned:** hardware counting is far quieter than software interrupts.

### 26 September: night mode needed a different charge controller *(setback)*
The Waveshare Solar Power Manager (C) switched its output off at low load, so the ESP32 never woke from deep sleep. The (D) version keeps the output on in low-current mode. DHT11 replaced with HTU21D.

**Learned:** check that the supply stays on at a few mA before relying on deep sleep.

### 26 September: Rev A carrier board
Board designed in KiCad, ordered fully assembled from JLCPCB. Repository created.

### 27 September: weather state logic
Dew detection via the distance to the dew point, frost point below 0 °C, morning and evening dew, hysteresis against flickering states.

### 28 September: placement error caught before production *(setback)*
The JLCPCB preview showed U2 and U3 (SOT-23-5/6) rotated by 90°. Fixed in the CPL file.

**Learned:** always check pin 1 of every IC in the assembly preview.

### 1 October: standalone variant
Local web page and MQTT for FHEM, ioBroker and others; English firmware alongside German.

### 2 October: first real rain, oscillator stalled *(setback)*
The frequency dropped to 0 Hz. Water on the plate added a leakage path that the oscillator could not drive with a 1 MΩ feedback resistor. Before that, dew had read almost like rain, and rain was not detected reliably. R1 changed to 220 kΩ.

**Learned:** lab tests with a damp cloth do not replace real rain.

### 3 October: test series with 220 kΩ
Oscillator stable in every test: dry ~100 pF, spray mist ~270, three drops ~290, heavy spray ~600, soaked cloth 870–1240 pF. Drizzle and rain are now detected by rate of rise, with a rain-end timer and a short heater test.

### 3 October: false rain alert *(setback)*
A notification fired without rain: the automations listened to "humid" instead of "rain". They now use the rain sensor.

### 4 October: night behaviour and first fog morning
Short "unknown" states after each wake removed; the last weather state is restored across sleep. The heater no longer runs while dew or frost is forming, which saves energy. First fog morning logged: capacitance flat at ~187 pF while the plate warmed slightly. Morning drying added: one short heat pulse a day once the surface is above the dew point. In fog the surface wetted again within ten minutes of a heat pulse (about 7 pF/min) although it was above the dew point; this re-wetting is the candidate for fog detection.

### Next
See [Roadmap](Roadmap.md).
