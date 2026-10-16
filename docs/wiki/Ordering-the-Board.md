# Ordering the board

1. **PCB.** Upload `fabrication/regensensor_gerbers.zip`: 2 layers, 1.6 mm, lead-free HASL is fine.
2. **Assembly.** Enable SMT assembly, top side. The ESP32 module (C701341, or C701344 for the UE variant) is only offered with **Standard PCBA** (one-time setup fee per side; JLCPCB adds edge rails, which break off).
3. **BOM and CPL.** Upload `fabrication/bom_jlcpcb.csv` and `fabrication/cpl_jlcpcb.csv`. For an external antenna (ESP32-WROOM-32UE, u.FL socket) take `bom_jlcpcb_ue.csv` and `cpl_jlcpcb_ue.csv` instead; the Gerbers stay the same. The UE module costs more: about 20 $ for five boards against about 17 € for the 32E (JLCPCB, 2026-10). Check that every line has stock; swap a part with the magnifier if not.
4. **Check the placement preview.** The magenta dot marks pin 1. In the CPL, U2 and U3 (SOT-23-5/-6) are rotated by 270° because JLCPCB's models are turned against KiCad's footprints; Q1 and Q2 (SOT-23) use 180°. Verify U1–U4, Q1, Q2 and D1 anyway; for the UE variant check that U1 sits on its pads.
5. **Shipping.** Product description e.g. *Sensor / Rain gauge* (HS 901590). To Germany, EuroPacket is a good compromise; check that import VAT is included at checkout.
6. **Hand soldering.** The through-hole parts (J1, J2, J3, J6 screw terminals; J4, J5, J7, J8 headers) are not in the BOM; [Parts](Parts.md#parts-to-solder-yourself) lists type, pitch and hole size.
