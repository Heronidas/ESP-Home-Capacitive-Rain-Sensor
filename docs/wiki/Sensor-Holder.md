# Sensor holder

`mechanical/sensor-holder.stl`, about 228 × 124 × 50 mm, fits a 256 mm bed. The file contains **three parts; split them in the slicer** (Bambu Studio: right click → Split → To Parts).

<p align="center"><img src="../sensor-holder.png" alt="Sensor holder" width="720"></p>

## Material and finish

- **ASA, white.** ASA is UV and weather resistant; white keeps the head from heating up in the sun. PLA and PETG are not suitable for permanent outdoor use.
- FDM prints are not watertight. Seal the printed parts with a clear, UV-stable outdoor lacquer. Keep the sensor face itself free of lacquer.

## Mounting the sensor

> [!IMPORTANT]
> The back of the RC-SPC1KA with the heater and NTC solder pads is not protected against corrosion. The bond must be sealed all around the sensor edge so no water reaches the rear.

- The prototype uses a transparent MS polymer adhesive (UHU Polymax Express) and Kapton tape over the pads on the back.
- Neutral-curing adhesives only. Acetic-acid silicone (vinegar smell) attacks solder joints and copper.
- Degrease the bonding surfaces (isopropanol) and let the adhesive cure fully before going outside.
- Keep glue off the sensor face and away from the edge where water runs off; a glue bead there holds a water film and reads as wet.
- Solder the wires and **test the sensor and the VEML7700 before gluing**; afterwards nothing can be reworked.
- Let the cable leave the holder downwards with a drip loop, and add strain relief. Use an outdoor-rated cable (plain LiYY is not UV resistant).
- If the VEML7700 sits behind a cover or lacquer, adjust *Glass Factor* (default 1.6); no reflash needed.
- Use stainless screws for wall mounting.
