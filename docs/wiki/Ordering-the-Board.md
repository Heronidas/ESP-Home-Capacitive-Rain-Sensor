# Ordering the board

1. **PCB.** Upload `fabrication/regensensor_gerbers.zip`: 2 layers, 1.6 mm, lead-free HASL is fine.
2. **Assembly.** Enable SMT assembly, top side. The ESP32 module (C701341) is only offered with **Standard PCBA** (one-time setup fee per side; JLCPCB adds edge rails, which break off).
3. **BOM and CPL.** Upload `fabrication/bom_jlcpcb.csv` and `fabrication/cpl_jlcpcb.csv`, then check that every line has stock; swap a part with the magnifier if not.
4. **Check the placement preview.** The magenta dot marks pin 1. In the CPL, U2 and U3 (SOT-23-5/-6) are rotated by 90° because JLCPCB's models are turned against KiCad's footprints; Q1 and Q2 (SOT-23) use 180°. Verify U1–U4, Q1, Q2, D1 and J5 anyway.
5. **Shipping.** Product description e.g. *Sensor / Rain gauge* (HS 901590). To Germany, EuroPacket is a good compromise; check that import VAT is included at checkout.
6. **Hand soldering.** The through-hole parts (J1, J2, J3, J6 screw terminals; J4, J7, J8 headers) are not in the BOM. J5 (Qwiic) and L1 are assembled.
