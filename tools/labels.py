# Silkscreen labels: (text, x, y, size) in board coordinates (mm)
L = [("RC-SPC1KA Rain Sensor", 52.5, 22.0), ("Heronidas  rev B", 52.5, 24.6)]
def block(x0, pitch, func, num, title):
    for n, (f, k) in enumerate(zip(func, num)):
        L.append((f, x0 + n * pitch, 54.75, 0.65 if len(f) > 4 else 0.8)); L.append((k, x0 + n * pitch, 55.9))
    L.append((title, x0 + pitch * (len(func) - 1) / 2, 57.05))
block(10.24, 5.08, ["5V", "GND", "BAT"], ["1", "2", "3"], "POWER IN")
block(26.68, 5.08, ["3V3", "GND", "SDA", "SCL"], ["1", "2", "3", "4"], "I2C")
block(48.2, 5.08, ["GND", "HEAT-", "12V"], ["-", "#2", "#5"], "HEATER #=pin")
block(64.64, 5.08, ["OSC", "GND", "NTC"], ["#6", "#1+4", "#3"], "SENSOR #=pin")
L += [("BOOT", 73.5, 12.0), ("RESET", 73.5, 19.4), ("HTU21D", 81, 19.1), ("I2C", 75.4, 25.31, 0.8, 90),
      ("UART", 67, 1.0), ("EXPANSION", 8, 6.7), ("OSC", 65, 26.9)]
L += [(t, 83.4, 21.5 + 2.54 * k, 0.65) for k, t in enumerate(["3V3", "GND", "SCL", "SDA"])]
L += [(t, 64.3, 3 + 2.54 * k) for k, t in enumerate(["GND", "TX", "RX", "IO0", "EN"])]
L += [(t, 7.3, 9 + 2.54 * k) for k, t in enumerate(["3V3", "GND", "32", "33", "26", "27", "14", "4"])]
L += [(t, x, 25.9) for t, x in [("5V", 30), ("3V3", 33), ("12V", 36), ("GND", 39)]]
# bottom side: logo, name, licence (centre x, y; mirrored so it reads from below)
LOGO = (42.5, 21.0, 26.0)
BOTTOM = [("Heronidas", 42.5, 37.5, 2.0), ("\u00a9 2026 \u00b7 CC BY-NC-SA", 42.5, 41.0, 1.2)]
