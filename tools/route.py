import sys, subprocess, os, re
import pcbnew
S=os.environ.get("ROUTE_WORKDIR", ".")  # work dir; put freerouting-2.1.0.jar here
src, dst = sys.argv[1], sys.argv[2]
b = pcbnew.LoadBoard(src)
dsn = f"{S}/r.dsn"; ses = f"{S}/r.ses"
pcbnew.ExportSpecctraDSN(b, dsn)
t = open(dsn).read()
# drop GND from routing (poured on both layers)
i = t.index("    (net GND\n"); j = t.index("    )\n", i) + 6
t = t[:i] + "    (net GND\n      (pins )\n    )\n" + t[j:]
t = t.replace("/VBAT_IN /VIN_RAW GND", "/VBAT_IN GND")
t = re.sub(r"(class kicad_default \"\" )\+12V \+3V3 \+5V ", r"\1", t)
t = t.replace("/HEAT_GATE /HEAT_RET /IO0", "/HEAT_GATE /IO0").replace("/SCL /SDA /SW /UART_RXD", "/SCL /SDA /UART_RXD").replace("/VBAT_IN /VIN_RAW", "/VBAT_IN")
t = t.replace("(class Power\n", "(class Power +5V /VIN_RAW +12V /SW /HEAT_RET\n").replace("(class Power33\n", "(class Power33 +3V3\n")
t = t.replace("(width 600)", "(width 500)")
open(dsn, "w").write(t)
subprocess.run(["java","-jar",f"{S}/freerouting-2.1.0.jar","-de",dsn,"-do",ses,"-mp","40","--gui.enabled=false"] , check=False, timeout=900)
b = pcbnew.LoadBoard(src)
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import ses_import; print("import", ses_import.import_ses(b, ses))
b.Save(dst)
