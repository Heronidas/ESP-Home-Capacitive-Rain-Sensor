"""Single source of truth for the rain sensor carrier board (schematic + PCB + BOM).

Net names: power nets are global (GND, +5V, +3V3, +12V). Every other net is a local label,
which KiCad exports as "/NAME".
"""

W, H = 72.0, 56.0            # board size in mm
ESP_X, ESP_Y = 36.0, 9.2     # ESP32 module origin (antenna overhangs the top edge)

PWR = {"GND", "+5V", "+3V3", "+12V"}

# fields: ref -> dict(sym=(lib,name), value, fp=(lib,name), lcsc, pins={pin: net or None}, pcb=(x,y,rot), sch=(x,y,rot), block)
C = {}


def add(ref, sym, value, fp, pins, pcb, sch, lcsc="", block="", dnp_note="", **kw):
    C[ref] = dict(ref=ref, sym=sym, value=value, fp=fp, pins=pins, pcb=pcb, sch=sch, lcsc=lcsc,
                  block=block, note=dnp_note, **kw)


R0805 = ("Resistor_SMD", "R_0805_2012Metric")
C0805 = ("Capacitor_SMD", "C_0805_2012Metric")

# ------------------------------------------------------------------ connectors
TERM3 = ("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_PT-1,5-3-3.5-H_1x03_P3.50mm_Horizontal")
TERM4 = ("TerminalBlock_Phoenix", "TerminalBlock_Phoenix_PT-1,5-4-3.5-H_1x04_P3.50mm_Horizontal")

add("J1", ("Connector_Generic", "Conn_01x03"), "5V_IN_GND_BAT", TERM3,
    {1: "/VIN_RAW", 2: "GND", 3: "/VBAT_IN"}, (4, 47, 0), (40, 40, 0), "C474893", "power")
add("J6", ("Connector_Generic", "Conn_01x04"), "I2C_SENSOR", TERM4,
    {1: "+3V3", 2: "GND", 3: "/SDA", 4: "/SCL"}, (17, 47, 0), (40, 200, 0), "C42400616", "i2c")
add("J3", ("Connector_Generic", "Conn_01x03"), "RC-SPC1KA_HEATER", TERM3,
    {1: "GND", 2: "/HEAT_RET", 3: "+12V"}, (32, 47, 0), (40, 130, 0), "C474893", "sensor")
add("J2", ("Connector_Generic", "Conn_01x03"), "RC-SPC1KA_SENSE", TERM3,
    {1: "/OSC_CAP", 2: "GND", 3: "/NTC_ADC"}, (45, 47, 0), (40, 150, 0), "C474893", "sensor")

add("J4", ("Connector_Generic", "Conn_01x04"), "I2C_BREAKOUT_SOCKET",
    ("Connector_PinSocket_2.54mm", "PinSocket_1x04_P2.54mm_Vertical"),
    {1: "+3V3", 2: "GND", 3: "/SCL", 4: "/SDA"}, (67, 23, 0), (40, 220, 0), "", "i2c")
add("J5", ("Connector_Generic", "Conn_01x04"), "QWIIC",
    ("Connector_JST", "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal"),
    {1: "GND", 2: "+3V3", 3: "/SDA", 4: "/SCL"}, (66.5, 40, 90), (40, 240, 0), "C160404", "i2c")
add("J7", ("Connector_Generic", "Conn_01x05"), "UART_PROG",
    ("Connector_PinHeader_2.54mm", "PinHeader_1x05_P2.54mm_Vertical"),
    {1: "GND", 2: "/UART_TXD", 3: "/UART_RXD", 4: "/IO0", 5: "/EN"}, (54, 3, 0), (40, 60, 0), "", "esp")
add("J8", ("Connector_Generic", "Conn_01x08"), "EXPANSION",
    ("Connector_PinHeader_2.54mm", "PinHeader_1x08_P2.54mm_Vertical"),
    {1: "+3V3", 2: "GND", 3: "/IO32", 4: "/IO33", 5: "/IO26", 6: "/IO27", 7: "/IO14", 8: "/IO4"},
    (3.5, 21.5, 90), (40, 80, 0), "", "esp")

# ------------------------------------------------------------------ ESP32 module
esp_pins = {p: None for p in range(1, 40)}
esp_pins.update({1: "GND", 15: "GND", 38: "GND", 39: "GND", 2: "+3V3", 3: "/EN", 6: "/NTC_ADC",
                 7: "/VBAT_ADC", 8: "/IO32", 9: "/IO33", 10: "/OSC_OUT", 11: "/IO26", 12: "/IO27",
                 13: "/IO14", 16: "/HEAT_CTRL", 25: "/IO0", 26: "/IO4", 33: "/SDA", 34: "/UART_RXD",
                 35: "/UART_TXD", 36: "/SCL"})
add("U1", ("RF_Module", "ESP32-WROOM-32"), "ESP32-WROOM-32E-N4", ("RF_Module", "ESP32-WROOM-32"),
    esp_pins, (ESP_X, ESP_Y, 0), (140, 60, 0), "C701341", "esp")

# ------------------------------------------------------------------ power
add("Q1", ("Device", "Q_PMOS_GSD"), "AO3401A", ("Package_TO_SOT_SMD", "SOT-23"),
    {1: "GND", 2: "+5V", 3: "/VIN_RAW"}, (7, 41, 0), (100, 40, 0), "C15127", "power")
add("C1", ("Device", "C"), "22u/25V", C0805, {1: "+5V", 2: "GND"}, (11, 36, 90), (130, 40, 0), "C45783", "power")
add("C2", ("Device", "C"), "10u/25V", C0805, {1: "+5V", 2: "GND"}, (15, 36, 90), (150, 40, 0), "C15850", "power")

add("U2", ("Regulator_Linear", "AP2112K-3.3"), "AP2112K-3.3", ("Package_TO_SOT_SMD", "SOT-23-5"),
    {1: "+5V", 2: "GND", 3: "+5V", 4: None, 5: "+3V3"}, (22, 30, 0), (100, 100, 0), "C51118", "ldo")
add("C3", ("Device", "C"), "10u/25V", C0805, {1: "+3V3", 2: "GND"}, (27, 30, 90), (130, 100, 0), "C15850", "ldo")

add("U3", ("Regulator_Switching", "MT3608"), "MT3608", ("Package_TO_SOT_SMD", "SOT-23-6"),
    {1: "/SW", 2: "GND", 3: "/FB", 4: "/HEAT_CTRL", 5: "+5V", 6: None}, (14, 28, 0), (100, 150, 0), "C84817", "boost")
add("L1", ("Device", "L"), "22u/1.8A", ("Inductor_SMD", "L_Bourns_SRN6045TA"), {1: "+5V", 2: "/SW"},
    (14, 22, 90), (140, 150, 0), "C354622", "boost")
add("D1", ("Device", "D_Schottky"), "SS34", ("Diode_SMD", "D_SMA"), {1: "+12V", 2: "/SW"},
    (22, 40, 0), (170, 150, 0), "C8678", "boost")
add("C10", ("Device", "C"), "22u/25V", C0805, {1: "+12V", 2: "GND"}, (28, 40, 90), (200, 150, 0), "C45783", "boost")
add("C11", ("Device", "C"), "22u/25V", C0805, {1: "+12V", 2: "GND"}, (31, 40, 90), (220, 150, 0), "C45783", "boost")
add("R4", ("Device", "R"), "180k", R0805, {1: "+12V", 2: "/FB_T"}, (17, 33, 90), (100, 190, 0), "C17501", "boost")
add("R5", ("Device", "R"), "10k", R0805, {1: "/FB_T", 2: "/FB"}, (17, 36, 90), (120, 190, 0), "C17414", "boost")
add("R6", ("Device", "R"), "10k", R0805, {1: "/FB", 2: "GND"}, (10, 30, 90), (140, 190, 0), "C17414", "boost")

add("Q2", ("Device", "Q_NMOS_GSD"), "AO3400A", ("Package_TO_SOT_SMD", "SOT-23"),
    {1: "/HEAT_GATE", 2: "GND", 3: "/HEAT_RET"}, (34, 40, 0), (100, 220, 0), "C20917", "heater")
add("R7", ("Device", "R"), "100k", R0805, {1: "/HEAT_CTRL", 2: "GND"}, (40, 36, 90), (130, 220, 0), "C96346", "heater")
add("R8", ("Device", "R"), "100R", R0805, {1: "/HEAT_CTRL", 2: "/HEAT_GATE"}, (37, 36, 90), (150, 220, 0), "C17408", "heater")

# ------------------------------------------------------------------ ESP support
add("C4", ("Device", "C"), "10u/25V", C0805, {1: "+3V3", 2: "GND"}, (23, 3.5, 90), (180, 40, 0), "C15850", "esp")
add("C5", ("Device", "C"), "100n", C0805, {1: "+3V3", 2: "GND"}, (23, 7, 90), (200, 40, 0), "C49678", "esp")
add("R13", ("Device", "R"), "10k", R0805, {1: "+3V3", 2: "/EN"}, (20, 3.5, 90), (220, 40, 0), "C17414", "esp")
add("C9", ("Device", "C"), "1u", C0805, {1: "/EN", 2: "GND"}, (20, 7, 90), (240, 40, 0), "C28323", "esp")
add("R14", ("Device", "R"), "10k", R0805, {1: "+3V3", 2: "/IO0"}, (48, 20.5, 0), (260, 40, 0), "C17414", "esp")
add("SW1", ("Switch", "SW_Push"), "BOOT", ("Button_Switch_SMD", "SW_SPST_TL3342"),
    {1: "/IO0", 2: "GND"}, (62, 8, 0), (280, 40, 0), "C2886898", "esp")
add("SW2", ("Switch", "SW_Push"), "RESET", ("Button_Switch_SMD", "SW_SPST_TL3342"),
    {1: "/EN", 2: "GND"}, (62, 15, 0), (300, 40, 0), "C2886898", "esp")

# ------------------------------------------------------------------ rain sensor front end
u4 = {p: None for p in range(1, 15)}
u4.update({1: "/OSC_CAP", 2: "/OSC_OUT", 3: "GND", 5: "GND", 9: "GND", 11: "GND", 13: "GND", 7: "GND", 14: "+3V3"})
add("U4", ("74xx", "74HC14"), "SN74HC14DR", ("Package_SO", "SOIC-14_3.9x8.7mm_P1.27mm"),
    u4, (47, 36, 0), (100, 260, 0), "C6820", "sensor")
add("R1", ("Device", "R"), "1M", R0805, {1: "/OSC_CAP", 2: "/OSC_OUT"}, (53, 33, 0), (140, 260, 0), "C17514", "sensor")
add("C6", ("Device", "C"), "100n", C0805, {1: "+3V3", 2: "GND"}, (52, 40, 90), (160, 260, 0), "C49678", "sensor")
add("R2", ("Device", "R"), "5.6k", R0805, {1: "/NTC_PU", 2: "/NTC_ADC"}, (58, 40, 90), (180, 260, 0), "C4382", "sensor")
add("R3", ("Device", "R"), "5.6k", R0805, {1: "/NTC_PU", 2: "/NTC_ADC"}, (61, 40, 90), (200, 260, 0), "C4382", "sensor")
add("C7", ("Device", "C"), "100n", C0805, {1: "/NTC_ADC", 2: "GND"}, (58, 44, 90), (220, 260, 0), "C49678", "sensor")
add("SJ1", ("Jumper", "SolderJumper_3_Bridged12"), "NTC_PULLUP",
    ("Jumper", "SolderJumper-3_P1.3mm_Bridged12_RoundedPad1.0x1.5mm"),
    {1: "+3V3", 2: "/NTC_PU", 3: "/IO32"}, (64, 44, 0), (240, 260, 0), "", "sensor")

# ------------------------------------------------------------------ battery monitor
add("R9", ("Device", "R"), "100k", R0805, {1: "/VBAT_IN", 2: "/VBAT_ADC"}, (5, 32, 90), (100, 300, 0), "C96346", "batt")
add("R10", ("Device", "R"), "100k", R0805, {1: "/VBAT_ADC", 2: "/BAT_LOW"}, (5, 28, 90), (120, 300, 0), "C96346", "batt")
add("SJ2", ("Jumper", "SolderJumper_2_Bridged"), "BAT_SENSE",
    ("Jumper", "SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm"), {1: "/BAT_LOW", 2: "GND"},
    (5, 24, 90), (140, 300, 0), "", "batt")
add("C8", ("Device", "C"), "100n", C0805, {1: "/VBAT_ADC", 2: "GND"}, (9, 30, 90), (160, 300, 0), "C49678", "batt")

# ------------------------------------------------------------------ I2C pull-ups
add("R11", ("Device", "R"), "4.7k", R0805, {1: "+3V3", 2: "/SDA"}, (62, 27, 90), (100, 340, 0), "C17673", "i2c")
add("R12", ("Device", "R"), "4.7k", R0805, {1: "+3V3", 2: "/SCL"}, (62, 30, 90), (120, 340, 0), "C17673", "i2c")

# ------------------------------------------------------------------ test points / mounting
for i, (net, x, y) in enumerate([("+5V", 20, 47.5), ("+3V3", 30, 25), ("+12V", 28, 46), ("GND", 24, 47.5), ("/OSC_OUT", 55, 25)], 1):
    add(f"TP{i}", ("Connector", "TestPoint"), net.strip("/"), ("TestPoint", "TestPoint_Pad_D1.5mm"),
        {1: net}, (x, y, 0), (100 + 20 * i, 380, 0), "", "misc")
for i, (x, y) in enumerate([(3.5, 3.5), (W - 3.5, 3.5), (3.5, H - 3.5), (W - 3.5, H - 3.5)], 1):
    add(f"H{i}", ("Mechanical", "MountingHole"), "M3", ("MountingHole", "MountingHole_3.2mm_M3"), {},
        (x, y, 0), (100 + 20 * i, 400, 0), "", "misc")
add("FLG1", ("power", "PWR_FLAG"), "PWR_FLAG", None, {1: "+5V"}, None, (200, 380, 0), "", "misc")
add("FLG2", ("power", "PWR_FLAG"), "PWR_FLAG", None, {1: "GND"}, None, (220, 380, 0), "", "misc")

add("FLG3", ("power", "PWR_FLAG"), "PWR_FLAG", None, {1: "+12V"}, None, (240, 380, 0), "", "misc")

BLOCK_TITLES = {}
