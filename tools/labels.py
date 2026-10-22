# Silkscreen labels: (text, x, y, size) in board coordinates (mm)
from design import TERM_Y, H
L = [("RC-SPC1KA Rain Sensor", 41.0, 13.5, 1.2), ("Heronidas  rev B", 41.0, 16.0)]
# fixed GPIO assignment of the D1 mini (free GPIOs are on J8)
L += [("GPIO", 24.0, 10.2, 0.8)]
L += [(t, 24.0, 11.8 + 1.4 * k, 0.8) for k, t in enumerate(
    ["25  OSC", "34  NTC", "35  BAT", "13  HEAT", "21  SDA", "22  SCL"])]
LY = TERM_Y + 5.4


def block(x0, pitch, func, num, title):
    for n, (f, k) in enumerate(zip(func, num)):
        L.append((f, x0 + n * pitch, LY, 0.8)); L.append((k, x0 + n * pitch, LY + 1.2))
    L.append((title, x0 + pitch * (len(func) - 1) / 2, LY + 2.4))


block(10.24, 5.08, ["5V", "GND", "BAT"], ["1", "2", "3"], "POWER IN")
block(70.88, 5.08, ["3V3", "GND", "SDA", "SCL"], ["1", "2", "3", "4"], "I2C")
block(27.48, 5.08, ["HEAT+", "HEAT-"], ["#5", "#2"], "HEATER #=pin")
block(50.64, 5.08, ["OSC", "GND", "NTC"], ["#6", "#1+4", "#3"], "SENSOR #=pin")
L += [(t, 9.0 + 2.54 * k, 2.4, 0.8) for k, t in enumerate(["3V3", "GND", "32", "33", "26", "27", "14", "4"])]
L += [("EXPANSION", 17.9, 7.4)]
L += [(t, 33.0 + 2.54 * k, 2.4, 0.8) for k, t in enumerate(["3V3", "GND", "SCL", "SDA"])]
L += [("I2C", 44.5, 7.2)]
L += [(t, x, 24.0, 0.8) for t, x in [("5V", 38), ("3V3", 41), ("12V", 44), ("GND", 47)]]
L += [("OSC", 53.0, 48.6, 0.8), ("HTU21D", 93.0, 51.5, 0.8)]
# bottom side: logo, name, licence (centre x, y; mirrored so it reads from below)
LOGO = (71.5, 35.0, 20.0)
BOTTOM = [("Heronidas", 71.5, 47.0, 2.0), ("© 2026 · CC BY-NC-SA", 71.5, 50.0, 1.2)]
