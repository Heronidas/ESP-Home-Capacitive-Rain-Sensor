# Known limitations

- Rev B is designed but not yet built. The firmware, the heater circuit, the ground layout and the series capacitor C3 ran on the Rev A board with an external XL6009 module. Rev B uses R1 = 47 kΩ instead of the 38.7 kΩ on Rev A; the oscillator runs about 18 % slower, and the dry frequency absorbs that.
- The sensor reports rain or no rain. It cannot measure the amount: heavy rain runs off the 45° face and reads lower than drizzle.
- Very light rain on a plate that is already wet (one tip of a 0.07 mm gauge in 10 minutes) moves the level so little that the sensor can miss it.
- Below 1 °C plate temperature the sensor reports no rain, and it stays quiet until the plate is dry again. It does not detect snow or freezing rain.
- In night mode the sensor checks every 5 minutes, so a start or end can come up to 5 minutes late.
- The footprints for the ESP32 D1 mini and the XL6009 module come from measured modules. Clones differ: check the pin rows of your D1 mini (inner rows 22.86 mm apart) and the IN/OUT holes of your XL6009 (41 × 18 mm module) against [Board reference](Board-Reference.md#dimensions) before soldering.
- The terminal footprint is the Phoenix MKDS 1,5 5.08 mm; KF128/DG128-type terminals fit, other brands may not.
- The NTC pull-up draws about 0.9 mA unless you use the GPIO32 option (relevant for deep sleep on battery). The D1 mini's regulator and USB chip also draw current in deep sleep.
- DRC reports the courtyards of R11/R12 under the D1 mini; they sit there on purpose, below the module. ERC shows library-mismatch warnings for the generated symbols.
- The files use KiCad 8 formats; newer versions upgrade them on opening. Save once and re-run DRC.
