"""Generate regensensor.kicad_sch from design.py (KiCad 7 format, opens fine in KiCad 8/9/10)."""
import re, uuid, math, sys, os
from kiutils.symbol import SymbolLib
import design as D

SYMDIR = "/usr/share/kicad/symbols"
ROOT = str(uuid.uuid4())
PROJECT = "regensensor"
_libs = {}


def uid():
    return str(uuid.uuid4())


PROJ_SYMLIB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hardware", "rain-sensor.kicad_sym")


def load(lib):
    if lib not in _libs:
        _libs[lib] = SymbolLib.from_file(PROJ_SYMLIB if lib == "rain-sensor" else f"{SYMDIR}/{lib}.kicad_sym")
    return _libs[lib]


def find(lib, name):
    for s in load(lib).symbols:
        if s.entryName == name:
            return s
    raise KeyError((lib, name))


def set_prop(text, key, value):
    return re.sub(r'(\(property "%s" )"[^"]*"' % re.escape(key), lambda m: m.group(1) + '"' + value.replace('"', "'") + '"', text, count=1)


_symtext = {}


def sym_text(lib, name):
    k = (lib, name)
    if k in _symtext:
        return _symtext[k]
    s = find(lib, name)
    if s.extends:
        parent = find(lib, s.extends)
        t = parent.to_sexpr(indent=4).replace(parent.entryName, name)
        for pr in s.properties:
            if pr.key in ("Footprint", "Datasheet", "ki_description", "ki_keywords"):
                t = set_prop(t, pr.key, pr.value)
    else:
        t = s.to_sexpr(indent=4)
    t = t.replace(f'(symbol "{name}"', f'(symbol "{lib}:{name}"', 1)
    _symtext[k] = t
    return t


def sym_pins(lib, name):
    """Return {unit: [(number, name, x, y, angle, length)]} with unit 0 shared."""
    s = find(lib, name)
    if s.extends:
        s = find(lib, s.extends)
    out = {}
    for u in s.units:
        for p in u.pins:
            out.setdefault(u.unitId, []).append((p.number, p.name, p.position.X, p.position.Y, p.position.angle or 0, p.length))
    for p in s.pins:
        out.setdefault(0, []).append((p.number, p.name, p.position.X, p.position.Y, p.position.angle or 0, p.length))
    return out


def rot_pt(x, y, r):
    r = r % 360
    if r == 0:
        return x, y
    if r == 90:
        return -y, x
    if r == 180:
        return -x, -y
    if r == 270:
        return y, -x
    raise ValueError(r)


def f(v):
    return f"{v:.4f}".rstrip("0").rstrip(".")


out_wires, out_labels, out_nc, out_syms, out_texts = [], [], [], [], []
_pwr_n = [0]


def add_wire(x1, y1, x2, y2):
    out_wires.append(f'  (wire (pts (xy {f(x1)} {f(y1)}) (xy {f(x2)} {f(y2)})) (stroke (width 0) (type default)) (uuid {uid()}))')


def add_label(net, x, y, direction):
    # direction: outward unit vector (dx, dy) in schematic coords
    dx, dy = direction
    if dx < 0:
        ang, just = 180, "right bottom"
    else:
        ang, just = 0, "left bottom"
    out_labels.append(f'  (label "{net}" (at {f(x)} {f(y)} {ang}) (effects (font (size 1.27 1.27)) (justify {just})) (uuid {uid()}))')


def add_glabel(net, x, y, direction):
    dx, dy = direction
    ang, just = (180, "right") if dx < 0 else (0, "left")
    out_labels.append(
        f'  (global_label "{net}" (shape passive) (at {f(x)} {f(y)} {ang}) (fields_autoplaced) '
        f'(effects (font (size 1.27 1.27)) (justify {just})) (uuid {uid()})\n'
        f'    (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) (justify {just}) hide))\n  )')


def add_power(net, x, y, flip=False):
    _pwr_n[0] += 1
    ref = f"#PWR{_pwr_n[0]:03d}"
    rot = 0
    out_syms.append(
        f'  (symbol (lib_id "power:{net}") (at {f(x)} {f(y)} {rot}) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {uid()})\n'
        f'    (property "Reference" "{ref}" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))\n'
        f'    (property "Value" "{net}" (at {f(x)} {f(y + (3.5 if net == "GND" else -3.5))} 0) (effects (font (size 1.27 1.27))))\n'
        f'    (property "Footprint" "" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))\n'
        f'    (property "Datasheet" "" (at {f(x)} {f(y)} 0) (effects (font (size 1.27 1.27)) hide))\n'
        f'    (pin "1" (uuid {uid()}))\n'
        f'    (instances (project "{PROJECT}" (path "/{ROOT}" (reference "{ref}") (unit 1))))\n  )')


used_libsyms = {}


def place(ref):
    c = D.C[ref]
    lib, name = c["sym"]
    used_libsyms[(lib, name)] = True
    sx, sy, rot = c["sch"]
    pins = sym_pins(lib, name)
    units = sorted(k for k in pins if k != 0) or [0]
    nunits = max(units) if units != [0] else 1
    unit_pos = c.get("unit_pos", {})
    for unit in range(1, nunits + 1):
        ux, uy = unit_pos.get(unit, (sx, sy))
        plist = list(pins.get(unit, [])) + list(pins.get(0, []))
        pin_uuids = []
        seen = set()
        ys = [p[3] for p in plist] or [0]
        xs = [p[2] for p in plist] or [0]
        for (num, pname, px, py, pang, plen) in plist:
            rx, ry = rot_pt(px, py, rot)
            ax, ay = ux + rx, uy - ry
            # outward direction = opposite of pin direction (pin angle points from connection point toward body)
            dxl, dyl = math.cos(math.radians(pang)), math.sin(math.radians(pang))
            rdx, rdy = rot_pt(dxl, dyl, rot)
            outx, outy = -rdx, rdy          # to schematic coords (y flipped): body direction = (rdx, -rdy); outward = negation
            outx, outy = -rdx, rdy
            # body direction in sch coords is (rdx, -rdy) => outward is (-rdx, +rdy)
            net = c["pins"].get(int(num)) if str(num).isdigit() else None
            pin_uuids.append(num)
            if net is None:
                if c["sym"][1].startswith("Conn_01x") or (pname == "NC" and lib != "rain-sensor"):
                    continue
                out_nc.append(f'  (no_connect (at {f(ax)} {f(ay)}) (uuid {uid()}))')
                continue
            key = (round(ax, 2), round(ay, 2))
            if key in seen:
                continue
            seen.add(key)
            ex, ey = ax + 2.54 * outx, ay + 2.54 * outy
            add_wire(ax, ay, ex, ey)
            multi = len(plist) > 4 or c["sym"][1].startswith("Conn_")
            if net in D.PWR and multi:
                add_glabel(net, ex, ey, (outx if abs(outx) > 0.5 else 1, outy))
            elif net in D.PWR:
                add_power(net, ex, ey)
            else:
                add_label(net.lstrip("/"), ex, ey, (outx if abs(outx) > 0.5 else 1, outy))
        # instance
        pu = "".join(f'    (pin "{n}" (uuid {uid()}))\n' for n in pin_uuids)
        fp = f"{c['fp'][0]}:{c['fp'][1]}" if c["fp"] else ""
        is_ic = len(plist) > 4 and not c["sym"][1].startswith("Conn_")
        top = uy - max(ys) - 3.5 if is_ic else uy - 1.5
        bot = uy - min(ys) + 3.5 if is_ic else uy + 1.5
        rx_, ry_ = (ux + 4, uy - 1.5) if not is_ic else (ux - 5, top)
        vx_, vy_ = (ux + 4, uy + 1.5) if not is_ic else (ux - 5, bot)
        props = (
            f'    (property "Reference" "{ref}" (at {f(rx_)} {f(ry_)} 0) (effects (font (size 1.27 1.27)) (justify left)))\n'
            f'    (property "Value" "{c["value"]}" (at {f(vx_)} {f(vy_)} 0) (effects (font (size 1.27 1.27)) (justify left)))\n'
            f'    (property "Footprint" "{fp}" (at {f(ux)} {f(uy)} 0) (effects (font (size 1.27 1.27)) hide))\n'
            f'    (property "Datasheet" "~" (at {f(ux)} {f(uy)} 0) (effects (font (size 1.27 1.27)) hide))\n'
            f'    (property "LCSC" "{c["lcsc"]}" (at {f(ux)} {f(uy)} 0) (effects (font (size 1.27 1.27)) hide))\n'
        )
        in_bom = "no" if ref.startswith(("H", "TP", "FLG")) else "yes"
        out_syms.append(
            f'  (symbol (lib_id "{lib}:{name}") (at {f(ux)} {f(uy)} {rot}) (unit {unit}) (in_bom {in_bom}) (on_board yes) (dnp no) (uuid {uid()})\n'
            + props + pu +
            f'    (instances (project "{PROJECT}" (path "/{ROOT}" (reference "{ref}") (unit {unit}))))\n  )')


def text(s, x, y, size=2.0):
    out_texts.append(f'  (text "{s}" (at {f(x)} {f(y)} 0) (effects (font (size {size} {size})) (justify left bottom)) (uuid {uid()}))')


# ---------------------------------------------------------------- sheet layout (A3, 420 x 297 mm)
LAYOUT = {
    # power input and heater (left)
    "J1": (45.72, 55.88), "NT2": (88.9, 50.8), "NT1": (88.9, 66.04),
    "FLG1": (114.3, 40.64), "FLG2": (114.3, 81.28), "FLG3": (134.62, 81.28),
    "C1": (60.96, 116.84), "C2": (81.28, 116.84), "U2": (139.7, 116.84), "J3": (190.5, 116.84),
    "Q1": (101.6, 165.1), "R8": (66.04, 165.1), "R7": (83.82, 182.88),
    "R9": (50.8, 233.68), "R10": (73.66, 233.68), "SJ2": (96.52, 233.68), "C8": (119.38, 233.68),
    # ESP32 D1 mini and headers (middle)
    "U1": (264.16, 116.84), "J8": (215.9, 195.58),
    # I2C (right top)
    "J4": (340.36, 35.56), "J5": (365.76, 35.56), "J6": (391.16, 35.56), "R11": (340.36, 66.04), "R12": (360.68, 66.04),
    "U3": (370.84, 101.6), "C9": (340.36, 101.6),
    # sensor front end (right bottom)
    "R1": (370.84, 165.1), "C6": (391.16, 165.1), "R2": (325.12, 218.44), "R3": (345.44, 218.44), "C7": (365.76, 218.44),
    "SJ1": (391.16, 218.44), "J2": (391.16, 246.38),
    "TP1": (215.9, 256.54), "TP2": (228.6, 256.54), "TP3": (241.3, 256.54), "TP4": (254.0, 256.54), "TP5": (266.7, 256.54),
    "H1": (215.9, 274.32), "H2": (228.6, 274.32), "H3": (241.3, 274.32), "H4": (254.0, 274.32),
}
U4_UNITS = {1: (307.34, 165.1), 2: (307.34, 180.34), 3: (307.34, 195.58), 4: (337.82, 180.34), 5: (337.82, 195.58),
            6: (368.3, 195.58), 7: (391.16, 195.58)}

for ref, (x, y) in LAYOUT.items():
    D.C[ref]["sch"] = (x, y, 0)
D.C["U4"]["sch"] = U4_UNITS[1] + (0,)
D.C["U4"]["unit_pos"] = U4_UNITS

ORDER = [r for r in D.C]


def build(path):
    for ref in ORDER:
        place(ref)
    titles = [("5 V input; heater (GNDPWR) and logic (GND) meet only at J1 via NT1/NT2", 20, 30),
              ("Heater: XL6009 boost module, low-side switch AOD4184A (as prototype)", 20, 95),
              ("Battery voltage monitor (100k / 100k divider, optional)", 20, 215),
              ("ESP32 D1 mini (MiniKit layout) and expansion header", 205, 80),
              ("I2C connectors, pull-ups, on-board HTU21D", 330, 25),
              ("Rain sensor front end: SN74HC14 oscillator, NTC pull-up, sensor terminal", 290, 150),
              ("Test points and mounting holes", 205, 245)]
    for t, x, y in titles:
        text(t, x, y)
    libtxt = "\n".join(sym_text(l, n) for (l, n) in used_libsyms)
    for pn in ("GND", "GNDPWR", "+3V3", "+5V", "PWR_FLAG"):
        libtxt += "\n" + sym_text("power", pn)
    libtxt = re.sub(r"^", "  ", libtxt, flags=re.M)
    s = (
        f'(kicad_sch (version 20230121) (generator eeschema)\n\n  (uuid {ROOT})\n\n  (paper "A3")\n\n'
        f'  (title_block\n    (title "Rain sensor board")\n    (date "2026-10-21")\n    (rev "B")\n'
        f'    (comment 1 "ESP32 carrier for the RC-SPC1KA capacitive rain sensor")\n'
        f'    (comment 2 "5 V in, ESP32 D1 mini, external XL6009 heater boost module")\n  )\n\n'
        f'  (lib_symbols\n{libtxt}\n  )\n\n'
        + "\n".join(out_wires + out_labels + out_nc + out_texts + out_syms) +
        f'\n\n  (sheet_instances\n    (path "/" (page "1"))\n  )\n)\n'
    )
    open(path, "w").write(s)


if __name__ == "__main__":
    build(sys.argv[1])
    print("wrote", sys.argv[1])
