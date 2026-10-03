# Silkscreen labels: (text, x, y, size) in board coordinates (mm)
L = [("RC-SPC1KA Rain Sensor rev A", 15.5, 1.6), ("CC BY-NC-SA 4.0", 11.5, 4.2)]
def block(x0, pitch, func, num, title):
    for n, (f, k) in enumerate(zip(func, num)):
        L.append((f, x0 + n * pitch, 52.75, 0.65 if len(f) > 4 else 0.8)); L.append((k, x0 + n * pitch, 53.9))
    L.append((title, x0 + pitch * (len(func) - 1) / 2, 55.05))
block(10.3, 3.5, ["5V", "GND", "BAT"], ["1", "2", "3"], "POWER IN")
block(23.5, 3.5, ["3V3", "GND", "SDA", "SCL"], ["1", "2", "3", "4"], "I2C")
block(40.1, 3.5, ["GND", "HEAT-", "12V"], ["-", "#2", "#5"], "HEATER #=pin")
block(53.2, 3.5, ["OSC", "GND", "NTC"], ["#6", "#1+4", "#3"], "SENSOR #=pin")
L += [("BOOT", 60.5, 11.3), ("RESET", 60.5, 18.7), ("HTU21D", 68, 17.6),
      ("UART", 54, 1.0), ("EXPANSION", 8, 6.7), ("OSC", 52, 26.9)]
L += [(t, 70.4, 20 + 2.54 * k, 0.65) for k, t in enumerate(["3V3", "GND", "SCL", "SDA"])]
L += [(t, 51.3, 3 + 2.54 * k) for k, t in enumerate(["GND", "TX", "RX", "IO0", "EN"])]
L += [(t, 7.3, 9 + 2.54 * k) for k, t in enumerate(["3V3", "GND", "32", "33", "26", "27", "14", "4"])]
L += [(t, x, 25.9) for t, x in [("5V", 30), ("3V3", 33), ("12V", 36), ("GND", 39)]]

L += [(t, 68.6, 30.6 + k, 0.7) for k, t in enumerate(["QWIIC", "4 SCL", "3 SDA", "2 3V3", "1 GND"])]
