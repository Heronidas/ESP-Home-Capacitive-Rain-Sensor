"""Single source of truth for the rain sensor carrier board rev B (schematic + PCB + BOM).

Rev B follows the tested prototype: ESP32 D1 mini on headers, external XL6009 boost module on
pin headers, heater switched low side by an N-MOSFET on the module input. The heater return
(GNDPWR) has its own copper to the GND terminal of J1; it meets the logic GND only there (NT1).

Net names: power nets are global (GND, GNDPWR, +5V, +3V3). Every other net is a local label,
which KiCad exports as "/NAME".
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_gen import minikit_pins

W, H = 100.0, 70.0           # board size in mm
TERM_Y = 61.0                # terminal row (wire entry towards the bottom edge)
D1_X, D1_Y = 77.0, 19.43     # centre of the D1 mini pin field (antenna end up, USB end down)
XL_X, XL_Y = 8.0, 28.0       # XL6009 IN+ pad; IN- 18 mm below, OUT+/OUT- 41 mm to the right
HOLE = 3.5                   # mounting holes, centre distance from each edge

PWR = {"GND", "GNDPWR", "+5V", "+3V3"}

# fields: ref -> dict(sym=(lib,name), value, fp=(lib,name), lcsc, pins={pin: net or None}, pcb=(x,y,rot), sch=(x,y,rot), block)
C = {}


def add(ref, sym, value, fp, pins, pcb, sch=(0, 0, 0), lcsc="", block="", dnp_note="", **kw):
    C[ref] = dict(ref=ref, sym=sym, value=value, fp=fp, pins=pins, pcb=pcb, sch=sch, lcsc=lcsc,
                  block=block, note=dnp_note, **kw)


R0805 = ("Resistor_SMD", "R_0805_2012Metric")
R0603 = ("Resistor_SMD", "R_0603_1608Metric")
C0805 = ("Capacitor_SMD", "C_0805_2012Metric")
TERM = {n: ("TerminalBlock_Phoenix", f"TerminalBlock_Phoenix_MKDS-1,5-{n}-5.08_1x0{n}_P5.08mm_Horizontal") for n in (2, 3, 4)}
CONN = {n: ("Connector_Generic", f"Conn_01x0{n}") for n in (2, 3, 4, 8)}
R100K = ("100k", R0603, "C25803")

# ------------------------------------------------------------------ terminals (bottom row)
add("J1", CONN[3], "5V_IN_GND_BAT", TERM[3], {1: "+5V", 2: "GNDPWR", 3: "/VBAT_IN"}, (10.24, TERM_Y, 0), block="power")
add("J6", CONN[4], "I2C_SENSOR", TERM[4], {1: "+3V3", 2: "GND", 3: "/SDA", 4: "/SCL"}, (70.88, TERM_Y, 0), block="i2c")
add("J3", CONN[2], "RC-SPC1KA_HEATER", TERM[2], {1: "/HEAT_P", 2: "/HEAT_N"}, (27.48, TERM_Y, 0), block="heater")
add("J2", CONN[3], "RC-SPC1KA_SENSE", TERM[3], {1: "/OSC_SENSE", 2: "GND", 3: "/NTC_ADC"}, (50.64, TERM_Y, 0), block="sensor")

# ------------------------------------------------------------------ headers (top row)
add("J8", ("Connector_Generic", "Conn_01x08"), "EXPANSION",
    ("Connector_PinHeader_2.54mm", "PinHeader_1x08_P2.54mm_Vertical"),
    {1: "+3V3", 2: "GND", 3: "/IO32", 4: "/IO33", 5: "/IO26", 6: "/IO27", 7: "/IO14", 8: "/IO4"},
    (9.0, 5.0, 90), block="esp")
add("J5", CONN[4], "I2C_HEADER", ("Connector_PinHeader_2.54mm", "PinHeader_1x04_P2.54mm_Vertical"),
    {1: "+3V3", 2: "GND", 3: "/SCL", 4: "/SDA"}, (33.0, 5.0, 90), block="i2c")
add("J4", CONN[4], "I2C_SOCKET", ("Connector_PinSocket_2.54mm", "PinSocket_1x04_P2.54mm_Vertical"),
    {1: "+3V3", 2: "GND", 3: "/SCL", 4: "/SDA"}, (33.0, 9.0, 90), block="i2c")

# ------------------------------------------------------------------ ESP32 D1 mini (U1)
D1_NETS = {"GND": "GND", "VCC": "+5V", "3V3": "+3V3", "IO25": "/OSC_OUT", "IO34": "/NTC_ADC",
           "IO35": "/VBAT_ADC", "IO13": "/HEAT_CTRL", "IO21": "/SDA", "IO22": "/SCL",
           "IO32": "/IO32", "IO33": "/IO33", "IO26": "/IO26", "IO27": "/IO27", "IO14": "/IO14", "IO4": "/IO4"}
add("U1", ("rain-sensor", "ESP32_MiniKit"), "ESP32 D1 mini", ("rain-sensor", "ESP32_MiniKit"),
    {n: D1_NETS.get(name) for n, name in minikit_pins().items()}, (D1_X, D1_Y, 0), block="esp")

# ------------------------------------------------------------------ heater supply (as prototype)
add("U2", ("rain-sensor", "XL6009_Module"), "XL6009 module", ("rain-sensor", "XL6009_Module"),
    {1: "/VIN_HEAT", 2: "/HEAT_SW", 3: "/HEAT_P", 4: "/HEAT_N"}, (XL_X, XL_Y, 0), block="heater")
add("Q1", ("Device", "Q_NMOS_GDS"), "AOD4184A", ("Package_TO_SOT_SMD", "TO-252-2"),
    {1: "/HEAT_GATE", 2: "/HEAT_SW", 3: "GNDPWR"}, (14.0, 51.3, 180), lcsc="C99124", block="heater")
add("R8", ("Device", "R"), "100R", R0805, {1: "/HEAT_CTRL", 2: "/HEAT_GATE"}, (25.2, 52.5, 90), lcsc="C17408", block="heater")
add("R7", ("Device", "R"), R100K[0], R100K[1], {1: "/HEAT_GATE", 2: "GNDPWR"}, (23.1, 53.5, 90), lcsc=R100K[2], block="heater")
add("C2", ("Device", "C"), "100n", C0805, {1: "/VIN_HEAT", 2: "GNDPWR"}, (19.0, 15.5, 90), lcsc="C49678", block="heater")
add("C1", ("Device", "C_Polarized"), "1000u/16V", ("Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm"),
    {1: "/VIN_HEAT", 2: "GNDPWR"}, (8.0, 14.5, 0), block="heater", dnp_note="optional, hand-soldered")
add("NT1", ("Device", "NetTie_2"), "NetTie", ("NetTie", "NetTie-2_SMD_Pad0.5mm"),
    {1: "GNDPWR", 2: "GND"}, (22.3, 50.5, 0), block="power")
add("NT2", ("Device", "NetTie_2"), "NetTie", ("NetTie", "NetTie-2_SMD_Pad2.0mm"),
    {1: "/VIN_HEAT", 2: "+5V"}, (6.6, 58.0, 0), block="power")

# Heater current paths, fixed before autorouting: (net, width, [points]) on F.Cu.
# J1 5V -> NT2 -> XL IN+, XL IN- -> Q1 drain, Q1 source -> J1 GND, XL OUT -> J3.
PREROUTE = [
    ("+5V", 1.2, [(10.24, 61.0), (8.6, 58.0)]),
    ("/VIN_HEAT", 1.2, [(4.6, 58.0), (5.0, 57.6), (5.0, 30.0), (7.0, 28.0), (8.0, 28.0)]),
    ("/VIN_HEAT", 1.2, [(8.0, 28.0), (8.0, 14.5)]),
    ("/HEAT_SW", 1.5, [(8.0, 46.0), (8.0, 49.0), (10.3, 51.3), (13.0, 51.3)]),
    ("GNDPWR", 1.5, [(19.04, 49.02), (21.3, 49.02), (21.3, 55.5), (18.0, 55.5), (15.32, 58.18), (15.32, 61.0)]),
    ("/HEAT_P", 1.2, [(49.0, 28.0), (46.0, 31.0), (29.0, 31.0), (27.48, 32.52), (27.48, 61.0)]),
    ("/HEAT_N", 1.2, [(49.0, 46.0), (46.0, 49.0), (34.04, 49.0), (32.56, 50.48), (32.56, 61.0)]),
]

# ------------------------------------------------------------------ rain sensor front end
u4 = {p: None for p in range(1, 15)}
u4.update({1: "/OSC_CAP", 2: "/OSC_OUT", 3: "GND", 5: "GND", 9: "GND", 11: "GND", 13: "GND", 7: "GND", 14: "+3V3"})
add("U4", ("74xx", "74HC14"), "SN74HC14DR", ("Package_SO", "SOIC-14_3.9x8.7mm_P1.27mm"),
    u4, (60.0, 46.5, 0), lcsc="C6820", block="sensor")
# Deviation from rev A (220k || 47k = 38.7k, tested since 28.10.): 47k alone, a Basic part; the
# capacitance is read relative to the dry frequency, so only "Trockenfrequenz" changes (~125 kHz).
add("R1", ("Device", "R"), "47k", R0805, {1: "/OSC_CAP", 2: "/OSC_OUT"}, (53.0, 45.0, 90), lcsc="C17713", block="sensor")
# Cs in series to the sensor (tested on rev A since 07.11.): blocks the DC path of a water film
# from OSC to GND on face A, so the oscillator can no longer stall.
add("C3", ("Device", "C"), "100n", C0805, {1: "/OSC_SENSE", 2: "/OSC_CAP"}, (50.64, 51.0, 90), lcsc="C49678", block="sensor")
add("C6", ("Device", "C"), "100n", C0805, {1: "+3V3", 2: "GND"}, (67.0, 44.0, 90), lcsc="C49678", block="sensor")
add("R2", ("Device", "R"), "5.6k", R0805, {1: "/NTC_PU", 2: "/NTC_ADC"}, (59.0, 53.3, 0), lcsc="C4382", block="sensor")
add("R3", ("Device", "R"), "5.6k", R0805, {1: "/NTC_PU", 2: "/NTC_ADC"}, (55.5, 53.3, 0), lcsc="C4382", block="sensor")
add("C7", ("Device", "C"), "100n", C0805, {1: "/NTC_ADC", 2: "GND"}, (62.5, 53.3, 0), lcsc="C49678", block="sensor")
add("SJ1", ("Jumper", "SolderJumper_3_Bridged12"), "NTC_PULLUP",
    ("Jumper", "SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm"),
    {1: "+3V3", 2: "/NTC_PU", 3: "/IO32"}, (68.0, 49.5, 0), block="sensor")

# ------------------------------------------------------------------ battery monitor
add("R9", ("Device", "R"), R100K[0], R100K[1], {1: "/VBAT_IN", 2: "/VBAT_ADC"}, (56.5, 14.0, 90), lcsc=R100K[2], block="batt")
add("R10", ("Device", "R"), R100K[0], R100K[1], {1: "/VBAT_ADC", 2: "/BAT_LOW"}, (56.5, 18.0, 90), lcsc=R100K[2], block="batt")
add("SJ2", ("Jumper", "SolderJumper_2_Bridged"), "BAT_SENSE",
    ("Jumper", "SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm"), {1: "/BAT_LOW", 2: "GND"},
    (56.5, 22.0, 90), block="batt")
add("C8", ("Device", "C"), "100n", C0805, {1: "/VBAT_ADC", 2: "GND"}, (59.3, 15.5, 90), lcsc="C49678", block="batt")

# ------------------------------------------------------------------ I2C: pull-ups, on-board HTU21D
add("R11", ("Device", "R"), "4.7k", R0805, {1: "+3V3", 2: "/SDA"}, (84.0, 13.0, 90), lcsc="C17673", block="i2c")
add("R12", ("Device", "R"), "4.7k", R0805, {1: "+3V3", 2: "/SCL"}, (84.0, 17.0, 90), lcsc="C17673", block="i2c")
add("U3", ("Sensor_Humidity", "Si7021-A20"), "HTU21D", ("Package_DFN_QFN", "DFN-6-1EP_3x3mm_P1mm_EP1.5x2.4mm"),
    {1: "/SDA", 2: "GND", 3: None, 4: None, 5: "+3V3", 6: "/SCL", 7: "GND"}, (93.5, 47.0, 0), lcsc="C83479", block="i2c")
add("C9", ("Device", "C"), "100n", C0805, {1: "+3V3", 2: "GND"}, (89.5, 47.0, 90), lcsc="C49678", block="i2c")
# Slots around the sensor tongue keep board heat away (x1, y1, x2, y2 of each straight slot, 1 mm wide)
SLOTS = [(85.5, 40.5, 98.5, 40.5), (85.5, 53.5, 98.5, 53.5), (85.5, 40.5, 85.5, 43.5), (85.5, 50.5, 85.5, 53.5)]
# No copper below the D1 mini antenna
KEEPOUT = (61.0, 0.0, 93.0, 6.8)

# ------------------------------------------------------------------ test points / mounting
for i, (net, x, y) in enumerate([("+5V", 38, 22), ("+3V3", 41, 22), ("/HEAT_P", 44, 22), ("GND", 47, 22),
                                  ("/OSC_OUT", 53.0, 50.5)], 1):
    add(f"TP{i}", ("Connector", "TestPoint"), net.strip("/"), ("TestPoint", "TestPoint_Pad_D1.5mm"),
        {1: net}, (x, y, 0), block="misc")
for i, (x, y) in enumerate([(HOLE, HOLE), (W - HOLE, HOLE), (HOLE, H - HOLE), (W - HOLE, H - HOLE)], 1):
    add(f"H{i}", ("Mechanical", "MountingHole"), "M3", ("MountingHole", "MountingHole_3.2mm_M3"), {},
        (x, y, 0), block="misc")
for i, net in enumerate(["+5V", "GND", "GNDPWR"], 1):
    add(f"FLG{i}", ("power", "PWR_FLAG"), "PWR_FLAG", None, {1: net}, None, block="misc")

BLOCK_TITLES = {}
