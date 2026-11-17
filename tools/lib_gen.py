"""Project footprints and symbols for parts without a KiCad library entry (rev B).

ESP32_MiniKit: MH-ET LIVE MiniKit style "ESP32 D1 mini", 4 rows x 10 pins, top view, antenna end up.
Pad n: rows 1-10 from the antenna end; pads 1-10 left outer, 11-20 left inner, 21-30 right inner,
31-40 right outer. Inner rows 22.86 mm apart, outer rows 2.54 mm further out.
XL6009_Module: boost module carried on four pin-header pins through its IN/OUT holes (41 x 18 mm).
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRETTY = f"{ROOT}/hardware/rain-sensor.pretty"
SYMLIB = f"{ROOT}/hardware/rain-sensor.kicad_sym"

MINIKIT = {
    "LO": ["GND", "NC", "IO39", "IO35", "IO33", "IO34", "IO14", "NC", "SD2", "CMD"],
    "LI": ["RST", "IO36", "IO26", "IO18", "IO19", "IO23", "IO5", "3V3", "IO13", "SD3"],
    "RI": ["TXD", "RXD", "IO22", "IO21", "IO17", "IO16", "GND", "VCC", "IO15", "SD0"],
    "RO": ["GND", "IO27", "IO25", "IO32", "IO12", "IO4", "IO0", "IO2", "SD1", "CLK"],
}
COLX = {"LO": -13.97, "LI": -11.43, "RI": 11.43, "RO": 13.97}
COLS = ["LO", "LI", "RI", "RO"]
ROW0 = -11.43                      # row 1 (antenna end)
BOARD_W, ANT_END, USB_END = 31.3, -18.93, 20.03


def pad_num(col, row):
    return COLS.index(col) * 10 + row


def minikit_pins():
    return {pad_num(c, r + 1): MINIKIT[c][r] for c in COLS for r in range(10)}


def f(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def line(x1, y1, x2, y2, layer, w=0.12):
    return f'  (fp_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) (stroke (width {w}) (type solid)) (layer "{layer}"))'


def rect(x1, y1, x2, y2, layer, w=0.12):
    return "\n".join(line(*a, layer, w) for a in [(x1, y1, x2, y1), (x2, y1, x2, y2), (x2, y2, x1, y2), (x1, y2, x1, y1)])


def text(t, x, y, layer, size=1.0, kind="user"):
    if kind == "user":
        return f'  (fp_text user "{t}" (at {f(x)} {f(y)}) (layer "{layer}") (effects (font (size {size} {size}) (thickness 0.15))))'
    return f'  (fp_text {kind} "{t}" (at {f(x)} {f(y)}) (layer "{layer}") (effects (font (size {size} {size}) (thickness 0.15))))'


def thp(num, x, y, drill, size, shape="circle"):
    return (f'  (pad "{num}" thru_hole {shape} (at {f(x)} {f(y)}) (size {size} {size}) (drill {drill}) '
            f'(layers "*.Cu" "*.Mask"))')


def minikit_fp():
    hw = BOARD_W / 2
    o = ['(footprint "ESP32_MiniKit" (version 20221018) (generator lib_gen) (layer "F.Cu")',
         '  (descr "ESP32 D1 mini (MH-ET LIVE MiniKit layout), 4x10 pins 2.54 mm, inner rows 22.86 mm apart")',
         '  (attr through_hole)',
         text("REF**", 0, ANT_END - 1.5, "F.SilkS", kind="reference"),
         text("ESP32_MiniKit", 0, USB_END + 1.5, "F.Fab", kind="value")]
    for c in COLS:
        for r in range(10):
            n = pad_num(c, r + 1)
            o.append(thp(n, COLX[c], ROW0 + 2.54 * r, 1.0, 1.7, "rect" if n == 1 else "circle"))
    o.append(rect(-hw, ANT_END, hw, USB_END, "F.Fab", 0.1))
    o.append(rect(-hw - 0.25, ANT_END - 0.25, hw + 0.25, USB_END + 0.25, "F.CrtYd", 0.05))
    o.append(rect(-hw, ANT_END, hw, USB_END, "F.SilkS"))
    o.append(line(-hw, ANT_END + 6.4, hw, ANT_END + 6.4, "F.SilkS"))
    o.append(text("ANTENNA", 0, ANT_END + 3.2, "F.SilkS", 1.0))
    o.append(text("USB", 0, USB_END - 2.0, "F.SilkS", 1.0))
    o.append(")")
    return "\n".join(o) + "\n"


XL_PADS = {1: ("IN+", 0, 0), 2: ("IN-", 0, 18), 3: ("OUT+", 41, 0), 4: ("OUT-", 41, 18)}


def xl_fp():
    o = ['(footprint "XL6009_Module" (version 20221018) (generator lib_gen) (layer "F.Cu")',
         '  (descr "XL6009 boost module on four pin-header pins through its IN/OUT holes, 41 x 18 mm")',
         '  (attr through_hole)',
         text("REF**", 20.5, -3.2, "F.SilkS", kind="reference"),
         text("XL6009_Module", 20.5, 9, "F.Fab", kind="value")]
    for n, (name, x, y) in XL_PADS.items():
        o.append(thp(n, x, y, 1.0, 2.2, "rect" if n == 1 else "circle"))
        o.append(text(name, x + (3.2 if x == 0 else -3.6), y, "F.SilkS", 1.0))
    o.append(rect(-1.5, -1.5, 42.5, 19.5, "F.SilkS"))
    o.append(rect(-1.75, -1.75, 42.75, 19.75, "F.CrtYd", 0.05))
    o.append(text("XL6009", 20.5, 9, "F.SilkS", 1.5))
    o.append(")")
    return "\n".join(o) + "\n"


def sym_pin(num, name, x, y, ang, etype="passive"):
    return (f'      (pin {etype} line (at {f(x)} {f(y)} {ang}) (length 5.08)\n'
            f'        (name "{name}" (effects (font (size 1.27 1.27))))\n'
            f'        (number "{num}" (effects (font (size 1.27 1.27)))))')


def symbol(name, ref, fp, pins, h):
    o = [f'  (symbol "{name}" (in_bom yes) (on_board yes)',
         f'    (property "Reference" "{ref}" (at 0 {f(h + 2.54)} 0) (effects (font (size 1.27 1.27))))',
         f'    (property "Value" "{name}" (at 0 {f(-h - 2.54)} 0) (effects (font (size 1.27 1.27))))',
         f'    (property "Footprint" "rain-sensor:{fp}" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
         f'    (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
         f'    (symbol "{name}_0_1"',
         f'      (rectangle (start -10.16 {f(h)}) (end 10.16 {f(-h)}) (stroke (width 0.254) (type default)) (fill (type background)))',
         '    )', f'    (symbol "{name}_1_1"'] + pins + ['    )', '  )']
    return "\n".join(o)


def etype(name):
    return {"GND": "power_in", "VCC": "power_in", "3V3": "power_out"}.get(name, "bidirectional" if name.startswith("IO") else "passive")


def build():
    os.makedirs(PRETTY, exist_ok=True)
    open(f"{PRETTY}/ESP32_MiniKit.kicad_mod", "w").write(minikit_fp())
    open(f"{PRETTY}/XL6009_Module.kicad_mod", "w").write(xl_fp())
    mp = minikit_pins()
    pins = []
    for n in range(1, 41):
        left = n <= 20
        i = (n - 1) % 20
        y = 24.13 - 2.54 * i
        pins.append(sym_pin(n, mp[n], -15.24 if left else 15.24, y, 0 if left else 180, etype(mp[n])))
    s1 = symbol("ESP32_MiniKit", "U", "ESP32_MiniKit", pins, 26.67)
    xp = [sym_pin(1, "IN+", -15.24, 2.54, 0, "passive"), sym_pin(2, "IN-", -15.24, -2.54, 0, "passive"),
          sym_pin(3, "OUT+", 15.24, 2.54, 180, "power_out"), sym_pin(4, "OUT-", 15.24, -2.54, 180, "passive")]
    s2 = symbol("XL6009_Module", "U", "XL6009_Module", xp, 5.08)
    open(SYMLIB, "w").write("(kicad_symbol_lib (version 20220914) (generator lib_gen)\n" + s1 + "\n" + s2 + "\n)\n")


if __name__ == "__main__":
    build()
    print("ok")
