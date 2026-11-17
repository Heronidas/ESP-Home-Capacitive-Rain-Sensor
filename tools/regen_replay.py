#!/usr/bin/env python3
"""Replay the rain detection of firmware/regensensor_de.yaml over a device log.

Reads the 10-s "Kapazität" states from an ESPHome log (lines with
"[S][sensor]: 'Kapazität' >> 123 pF") and prints when the weather state
would change. Day logic only: no night wakes, no heater lockout. Frost lock from the
"Oberflächentemperatur" states.
Mirror of the control loop (section 0a): change both together.

    python3 tools/regen_replay.py ~/regensensor-logs/2026-11-17.log
"""
import math
import re
import sys

RATE_START = 4.0     # "Schwelle Niederschlagserkennung", pF/min
SPR_START = 0.7      # "Sprünge Regenbeginn", pF
ENDE_S = 180         # "Schwelle für Regenende", s
TROCKEN_BIS = 115.0  # "Trocken bis", pF
UNRUHE_RUHIG = 1.5
PEGEL_FALL = 2.0
ABLAUF_SPRUNG = 5.0
FROST_GRENZE = 1.0

pat = re.compile(r"\[(\d\d):(\d\d):(\d\d)\.\d+\]\[S\]\[sensor\]: '(Kapazität|Oberflächentemperatur)' >> (\S+) ")
samples = []
temp = math.nan
for line in open(sys.argv[1], errors="ignore"):
    m = pat.search(line)
    if not m or m.group(5) == "nan":
        continue
    if m.group(4) == "Oberflächentemperatur":
        temp = float(m.group(5))
        continue
    h, mi, s = map(int, m.group(1, 2, 3))
    samples.append((h * 3600 + mi * 60 + s, float(m.group(5)), temp))

uv, ut, rates = [], [], []
prev = None
regen, frost, ruhig_seit, last = False, False, 0, None
for t, c, tp in samples:
    if tp < FROST_GRENZE:
        frost = True
    elif c < TROCKEN_BIS:
        frost = False
    if ut and t - ut[-1] > 15:      # gap (heater, reboot): window starts over
        uv, ut = [], []
    uv.append(c); ut.append(t)
    del uv[:-40], ut[:-40]
    if prev and 0 < t - prev[0] <= 900:
        rates = (rates + [(c - prev[1]) * 60 / (t - prev[0])])[-6:]
    prev = (t, c)
    rr = sum(rates) / len(rates) if rates else math.nan

    w = [(v, tt) for v, tt in zip(uv, ut) if t - tt <= 300]
    n = len(w)
    steps = [(w[i][0] - w[i - 1][0], w[i][1]) for i in range(1, n) if w[i][1] - w[i - 1][1] <= 15]
    kurz = [d * d for d, tt in steps if t - tt <= 120]
    un = math.sqrt(max(sum(v * v for v, _ in w) / n - (sum(v for v, _ in w) / n) ** 2, 0)) if n >= 24 else math.nan
    sk = math.sqrt((sum(kurz) - max(kurz)) / len(kurz)) if len(kurz) >= 6 else math.nan
    pg = c - w[0][0] if n >= 24 else math.nan
    abfall = -min([0.0] + [d for d, _ in steps])

    steigt = not math.isnan(rr) and rr >= RATE_START
    trocknet = not math.isnan(pg) and pg < -PEGEL_FALL and abfall < ABLAUF_SPRUNG
    if not regen and (steigt or (not math.isnan(sk) and sk >= SPR_START and not trocknet)):
        regen, ruhig_seit = True, 0
    if frost:
        regen = False
    if c < TROCKEN_BIS and not steigt and not un >= UNRUHE_RUHIG:
        regen = False
    if math.isnan(un) or un >= UNRUHE_RUHIG:
        ruhig_seit = 0
    elif ruhig_seit == 0:
        ruhig_seit = t
    elif t - ruhig_seit >= ENDE_S:
        regen = False

    st = "Regen" if regen else "trocken (Frost)" if frost else "trocken"
    if st != last:
        print(f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}  {st}")
        last = st
