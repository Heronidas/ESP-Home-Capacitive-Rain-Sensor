import sys, os, csv, re, subprocess, shutil
sys.path.insert(0, os.path.dirname(__file__))
import pcbnew
from design import C, H as BH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = f"{ROOT}/hardware"
pcb = f"{H}/regensensor.kicad_pcb"
out = f"{ROOT}/fabrication"
shutil.rmtree(out, ignore_errors=True); os.makedirs(f"{out}/gerbers")
layers = "F.Cu,B.Cu,F.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts"
subprocess.run(["kicad-cli","pcb","export","gerbers","--layers",layers,"--no-x2","--use-drill-file-origin","--subtract-soldermask","-o",f"{out}/gerbers/",pcb],check=True)
subprocess.run(["kicad-cli","pcb","export","drill","--format","excellon","--drill-origin","plot","--excellon-separate-th","--generate-map","--map-format","gerberx2","-o",f"{out}/gerbers/",pcb],check=True)
b = pcbnew.LoadBoard(pcb)
# Most specific pattern first; the loop below stops at the first match.
ROT = [(r"^SOT-23-[56]", 270), (r"^SOT-23$", 180), (r"^SOIC-", 270), (r"^ESP32", 270)]
NO_ASSY = {"J1","J2","J3","J6","J4","J5","J7","J8"}  # through-hole parts: hand-solder
rows = {}; cpl = []
for fp in b.GetFootprints():
    ref = fp.GetReference(); c = C.get(ref)
    if not c or not c["lcsc"] or ref in NO_ASSY: continue
    key = (c["value"], str(fp.GetFPID().GetLibItemName()), c["lcsc"])
    rows.setdefault(key, []).append(ref)
    pos = fp.GetPosition(); name = str(fp.GetFPID().GetLibItemName())
    rot = fp.GetOrientationDegrees()
    for pat, add in ROT:
        if re.match(pat, name):
            rot = (rot + add) % 360
            break
    cpl.append((ref, round(pcbnew.ToMM(pos.x) - 100, 4), round(80 + BH - pcbnew.ToMM(pos.y), 4), "Top", rot))
def write(sfx, rows, cpl):
    with open(f"{out}/bom_jlcpcb{sfx}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        merged = {}  # JLCPCB rejects one LCSC part on two BOM lines (BOOT/RESET)
        for (v, fpn, l), refs in rows.items():
            m = merged.setdefault((fpn, l), [[], []]); m[0].append(v); m[1] += refs
        for (fpn, l), (vs, refs) in sorted(merged.items(), key=lambda kv: kv[1][1][0]):
            v = "/".join(vs)
            w.writerow([v, ",".join(sorted(refs, key=lambda r: (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0)))), fpn, l])
    with open(f"{out}/cpl_jlcpcb{sfx}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for r in sorted(cpl): w.writerow([r[0], f"{r[1]}mm", f"{r[2]}mm", r[3], r[4]])
write("", rows, cpl)
# UE variant (u.FL antenna): same Gerbers; module body 6.3 mm shorter on the antenna side, so its centre sits 3.15 mm lower
ue_rows = {(("ESP32-WROOM-32UE-N4", k[1], "C701344") if r == ["U1"] else k): r for k, r in rows.items()}
# JLCPCB's UE model sits 90° turned against the 32E model
ue_cpl = [(r[0], r[1], round(r[2] - 3.15, 4), r[3], (r[4] + 90) % 360) if r[0] == "U1" else r for r in cpl]
write("_ue", ue_rows, ue_cpl)
shutil.make_archive(f"{out}/regensensor_gerbers", "zip", f"{out}/gerbers")
print(os.listdir(f"{out}/gerbers")); print(open(f"{out}/bom_jlcpcb.csv").read())
