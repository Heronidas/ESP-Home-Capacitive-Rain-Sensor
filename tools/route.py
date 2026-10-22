"""Autoroute everything except GND (poured on both layers) with Freerouting, then import the result."""
import sys, subprocess, os, re
import pcbnew
S = os.environ.get("ROUTE_WORKDIR", ".")  # work dir; put freerouting-2.1.0.jar here
src, dst = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(src)
dsn = f"{S}/r.dsn"; ses = f"{S}/r.ses"
pcbnew.ExportSpecctraDSN(b, dsn)
t = open(dsn).read()
i = t.index("    (net GND\n"); j = t.index("    )\n", i) + 6
t = t[:i] + "    (net GND\n      (pins )\n    )\n" + t[j:]
t = re.sub(r"(\(class \w+[^\n]*?) GND( |\n)", r"\1\2", t)
POWER = ["+5V", "/VIN_HEAT", "GNDPWR", "/HEAT_P", "/HEAT_N", "/HEAT_SW"]
for n in POWER + ["+3V3"]:
    t = re.sub(r"(\(class kicad_default[^(]*?)\s" + re.escape(n) + r"(?=[\s)])", r"\1", t)
t = t.replace("(class Power\n", "(class Power " + " ".join(POWER) + "\n").replace("(class Power33\n", "(class Power33 +3V3\n")
open(dsn, "w").write(t)
subprocess.run(["java", "-jar", f"{S}/freerouting-2.1.0.jar", "-de", dsn, "-do", ses, "-mp", "60", "--gui.enabled=false"],
               check=False, timeout=1500)
b = pcbnew.LoadBoard(src)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import ses_import; print("import", ses_import.import_ses(b, ses))
b.Save(dst)
