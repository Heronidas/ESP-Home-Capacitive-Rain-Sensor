"""Generate regensensor.kicad_sch from design.py (KiCad 7 format, opens fine in KiCad 8/9/10)."""
import re, uuid, math, sys
from kiutils.symbol import SymbolLib
import design as D

SYMDIR = "/usr/share/kicad/symbols"
ROOT = str(uuid.uuid4())
PROJECT = "regensensor"
_libs = {}


def uid():
    return str(uuid.uuid4())


def load(lib):
    if lib not in _libs:
        _libs[lib] = SymbolLib.from_file(f"{SYMDIR}/{lib}.kicad_sym")
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
                if c["sym"][1] in ("Conn_01x03", "Conn_01x04", "Conn_01x05", "Conn_01x08"):
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
    "J1": (45.72, 55.88), "Q1": (101.6, 55.88), "C1": (139.7, 55.88), "C2": (162.56, 55.88),
    "FLG1": (185.42, 55.88), "FLG2": (200.66, 55.88), "FLG3": (215.9, 55.88),
    "U2": (60.96, 132.08), "C3": (129.54, 132.08),
    "U3": (60.96, 190.5), "L1": (116.84, 177.8), "D1": (144.78, 190.5), "C10": (172.72, 190.5),
    "C11": (195.58, 190.5), "R4": (116.84, 208.28), "R5": (139.7, 208.28), "R6": (162.56, 208.28),
    "Q2": (60.96, 246.38), "R7": (116.84, 246.38), "R8": (139.7, 246.38),
    "R9": (60.96, 279.4), "R10": (86.36, 279.4), "SJ2": (111.76, 279.4), "C8": (137.16, 279.4),
    "J4": (241.3, 35.56), "J5": (274.32, 35.56), "J6": (307.34, 35.56), "R11": (335.28, 35.56), "R12": (355.6, 35.56),
    "U1": (312.42, 116.84),
    "C4": (378.46, 66.04), "C5": (396.24, 66.04), "R13": (378.46, 96.52), "C9": (396.24, 96.52),
    "R14": (378.46, 127), "SW1": (378.46, 152.4), "SW2": (396.24, 152.4),
    "J7": (241.3, 96.52), "J8": (241.3, 132.08),
    "R1": (370.84, 195.58), "C6": (391.16, 195.58), "R2": (302.26, 236.22), "R3": (322.58, 236.22), "C7": (342.9, 236.22),
    "SJ1": (368.3, 236.22), "J2": (392.43, 215.9), "J3": (392.43, 236.22),
    "TP1": (210.82, 269.24), "TP2": (223.52, 269.24), "TP3": (236.22, 269.24), "TP4": (248.92, 269.24), "TP5": (210.82, 284.48),
    "H1": (223.52, 284.48), "H2": (236.22, 284.48), "H3": (248.92, 284.48), "H4": (259.08, 284.48),
}
U4_UNITS = {1: (243.84, 190.5), 2: (243.84, 205.74), 3: (243.84, 220.98), 4: (289.56, 190.5), 5: (289.56, 205.74),
            6: (289.56, 220.98), 7: (335.28, 205.74)}

for ref, (x, y) in LAYOUT.items():
    D.C[ref]["sch"] = (x, y, 0)
D.C["U4"]["sch"] = (243.84, 190.5, 0)
D.C["U4"]["unit_pos"] = U4_UNITS

ORDER = [r for r in D.C]


def build(path):
    for ref in ORDER:
        place(ref)
    titles = [("5 V input, reverse-polarity protection, battery-sense input", 20, 30),
              ("3.3 V LDO", 20, 105), ("12 V boost converter for the sensor heater (MT3608)", 20, 155),
              ("Heater switch (low side)", 20, 225), ("Battery voltage monitor (100k / 100k divider, optional)", 20, 262),
              ("I2C connectors and pull-ups", 225, 25), ("Programming / expansion headers", 225, 80),
              ("ESP32-WROOM-32E", 280, 62), ("ESP32 support", 370, 55),
              ("Rain sensor front end: SN74HC14 oscillator, NTC pull-up, sensor terminals", 225, 172),
              ("Test points and mounting holes", 208, 262)]
    for t, x, y in titles:
        text(t, x, y)
    libtxt = "\n".join(sym_text(l, n) for (l, n) in used_libsyms)
    for pn in ("GND", "+3V3", "+5V", "+12V", "PWR_FLAG"):
        libtxt += "\n" + sym_text("power", pn)
    libtxt = re.sub(r"^", "  ", libtxt, flags=re.M)
    s = (
        f'(kicad_sch (version 20230121) (generator eeschema)\n\n  (uuid {ROOT})\n\n  (paper "A3")\n\n'
        f'  (title_block\n    (title "Rain sensor board")\n    (date "2026-09-26")\n    (rev "A")\n'
        f'    (comment 1 "ESP32 carrier for the RC-SPC1KA capacitive rain sensor")\n'
        f'    (comment 2 "5 V in, on-board 3.3 V LDO and 12 V heater boost")\n  )\n\n'
        f'  (lib_symbols\n{libtxt}\n  )\n\n'
        + "\n".join(out_wires + out_labels + out_nc + out_texts + out_syms) +
        f'\n\n  (sheet_instances\n    (path "/" (page "1"))\n  )\n)\n'
    )
    open(path, "w").write(s)


if __name__ == "__main__":
    build(sys.argv[1])
    print("wrote", sys.argv[1])
