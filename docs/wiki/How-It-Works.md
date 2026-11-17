# How it works

## Measurement

The sensing capacitor sets the frequency of a relaxation oscillator: an SN74HC14 Schmitt trigger with R1 = 47 kΩ, and a 100 nF capacitor (C3) in series to the sensor. A wetter surface raises the capacitance and lowers the frequency. The ESP32 counts the pulses with its hardware pulse counter (PCNT) in 2-second windows and passes on the median of five, one reading every 10 s.

You measure your dry sensor once and enter the result as the dry frequency. The firmware sets that value to 100 pF and scales everything else from it (`C = f_dry × 100 / f`). Cable length, layout and the value of R1 drop out, so all thresholds stay in pF and carry over between boards.

C3 blocks direct current. A water film on the sensor face conducts between the electrodes, and on Rev A without C3 that leak pulled the oscillator input below its switching point and stopped it in light rain and in thawing frost. With C3 the oscillator ran through every rain and through a thawing frost film at 460 pF. If it stops anyway (broken wire, water at bare metal), the firmware reports *Oscillator Stalled*, holds the weather state and heats the plate for up to 10 minutes. After that the heater waits until the cooled plate reads below the heating threshold.

The firmware ignores the frequency while the heater runs and for 12 s after, and keeps the heater off for at least 25 s between pulses to get a clean reading. On Rev B the boost module and the heater MOSFET meet the logic ground only at the power terminal, so the heater current stays out of the oscillator. On Rev A the boost converter on the board stops the oscillator while it runs; the same rule covers that.

The dry reading moves a little with the air humidity (about 0.2 % per percentage point) and with the plate temperature (about 0.2 pF per kelvin). Rain moves it by tens of pF within a minute.

## Rain or not

The capacitance tells you how wet the plate is, not why. Dew, the film left after rain and light rain can read the same level. Steady heavy rain reads lower than light rain, because the water runs off the 45° face. The firmware looks at how the level moves instead:

| Signal | Dew, fog, resting film | Rain |
|---|---|---|
| Rate of rise | dew about 0.03 pF/min | 4–36 pF/min at the start on a dry plate |
| Steps: RMS of the 10-s changes over 2 min, without the largest | 0–0.3 pF | 0.7–1.8 pF light rain on a wet plate, 2–17 pF rain |
| Unrest: standard deviation over 5 min | below 1.5 pF | 2–50 pF |

Values from the Rev A board on the 45° holder.

**Start.** Rain begins when the level rises at *Precipitation Detection Threshold* (default 4 pF/min) or more, or when the steps reach *Rain Start Steps* (default 0.7 pF). The steps catch rain on a plate that is already wet. Three cases block a start:

- the first 3 minutes after heating;
- a drying plate: the level falls by more than 2 pF over 5 minutes without a single drop of 5 pF or more (sun and wind dry a film in small steps, rain washes it off in large ones);
- the frost lock (see below).

**End.** Rain ends once the unrest stays below 1.5 pF for *Rain End Threshold* (default 3 min). Below *Dry Below* (default 115 pF), calm and without a rise, the plate counts as dry at once.

**Night mode.** The sensor wakes every 5 minutes for 35 s. A wake counts as restless when its readings spread by 1.5 pF or more, or when the level moved by +6 or −3 pF since the last wake. Two restless wakes in a row start rain, two calm ones end it.

**Frost lock.** Below 1 °C plate temperature the firmware reports no rain, and it keeps the lock until the plate is above 1 °C and dry again. Thaw water from frost or snow moves like rain: on one morning the meltwater ran off for an hour after the thaw began, at a plate temperature of 8–10 °C in full sun. The plate cools below the air on clear nights, so the lock also covers frost at an air temperature above 0 °C. The sensor does not detect snow.

**One state for rain.** The weather state reports *dry*, *Rain* or *Stalled*. An earlier version split drizzle from rain by the steps. Heavy rain forms a smooth running film and read as drizzle, so the split did not follow the amount of rain. A tipping-bucket gauge gives you the amount.

On two days of steady rain the sensor reported the start 2–5 minutes before the first tip of a tipping-bucket gauge next to it, and the end at the real pauses.

## Heater

The heater stays off while it rains, so the sensor can see the rain. It runs in four cases:

- **Drying run.** 15 minutes after rain ends, it heats the plate for *Drying After Rain* (default 6 min). New rain cancels the run. You can switch it off with *Drying Run*.
- **Frost.** Below 1 °C plate temperature and above *Dew Heating* (default 200 pF) it heats in pulses until the level drops to 85 % of that threshold. A frost film thaws into a closed water film in the morning. Dew above 1 °C does not disturb the detection, so the heater leaves it alone.
- **Stalled oscillator.** One drying attempt of up to 10 minutes per stall.
- **By hand**, with *Auto Mode* off.

Safety: off at *Heating Temperature* (default 45 °C, at most 60 °C), back on 5 K below, checked every second; the plate heats by about 0.7 K/s. A single pulse stops after 300 s. The heating time counts against a budget: after *Max. Heating Time* (default 15 min) the heater locks for *Heating Lockout* (default 120 min), and each heating minute recovers after *Pause per Heating Minute* (default 6 min). Below 3.3 V battery voltage no new pulse starts, below 3.5 V no drying run. An implausible NTC reading switches the heater off, and it starts off after each reset.

## Night mode

Optional deep sleep with a 5-minute wake interval and about 35 s awake per cycle, set by *Night Mode From* / *Night Mode Until* (separate end time for weekends). Off by default. The sensor sleeps through the wait before a drying run and stays awake while the run heats.

The supply has to stay on while the ESP32 sleeps. The Waveshare Solar Power Manager (D) cuts its 5 V output at low load; a double click on its function button switches it to low-current mode, which keeps the output on. After a deep discharge it forgot that mode and needed the double click again.
