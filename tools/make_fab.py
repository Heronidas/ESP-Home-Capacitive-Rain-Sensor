import sys, os, csv, re, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from design import C
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = f"{ROOT}/hardware"
pcb = f"{H}/regensensor.kicad_pcb"
out = f"{ROOT}/fabrication"
shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{out}/gerbers")
layers = "F.Cu,B.Cu,F.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts"
subprocess.run(["kicad-cli","pcb","export","gerbers","--layers",layers,"--no-x2","--use-drill-file-origin","--subtract-soldermask","-o",f"{out}/gerbers/",pcb],check=True)
subprocess.run(["kicad-cli","pcb","export","drill","--format","excellon","--drill-origin","plot","--excellon-separate-th","--generate-map","--map-format","gerberx2","-o",f"{out}/gerbers/",pcb],check=True)
b = pcbnew.LoadBoard(pcb)
ROT = [(r"^SOT-23", 180), (r"^SOT-23-[56]", 90), (r"^SOIC-", 270), (r"^ESP32", 270)]
NO_ASSY = {"J1","J2","J3","J6","J4","J7","J8"}  # through-hole parts: hand-solder
rows = {}; cpl = []
for fp in b.GetFootprints():
    ref = fp.GetReference(); c = C.get(ref)
    if not c or not c["lcsc"] or ref in NO_ASSY: continue
    key = (c["value"], str(fp.GetFPID().GetLibItemName()), c["lcsc"])
    rows.setdefault(key, []).append(ref)
    pos = fp.GetPosition(); name = str(fp.GetFPID().GetLibItemName())
    rot = fp.GetOrientationDegrees()
    for pat, add in ROT:
        if re.match(pat, name): rot = (rot + add) % 360
    cpl.append((ref, round(pcbnew.ToMM(pos.x) - 100, 4), round(136 - pcbnew.ToMM(pos.y), 4), "Top", rot))
with open(f"{out}/bom_jlcpcb.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
    for (v, fpn, l), refs in sorted(rows.items(), key=lambda kv: kv[1][0]):
        w.writerow([v, ",".join(sorted(refs, key=lambda r: (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0)))), fpn, l])
with open(f"{out}/cpl_jlcpcb.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
    for r in sorted(cpl): w.writerow([r[0], f"{r[1]}mm", f"{r[2]}mm", r[3], r[4]])
shutil.make_archive(f"{out}/regensensor_gerbers", "zip", f"{out}/gerbers")
print(os.listdir(f"{out}/gerbers")); print(open(f"{out}/bom_jlcpcb.csv").read())
