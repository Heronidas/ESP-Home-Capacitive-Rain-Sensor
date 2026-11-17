# Ordering the board

1. **PCB.** Upload `fabrication/regensensor_gerbers.zip`: 2 layers, 1.6 mm, lead-free HASL is fine.
2. **Assembly.** Enable SMT assembly, top side. Economic PCBA is enough: all parts are small SMD parts. Two of them are extended parts (SN74HC14DR, AOD4184A), each with a small setup fee.
3. **BOM and CPL.** Upload `fabrication/bom_jlcpcb.csv` and `fabrication/cpl_jlcpcb.csv`. Check that every line has stock; swap a part with the magnifier if not.
4. **Check the placement preview.** The magenta dot marks pin 1. The CPL already corrects the rotations where JLCPCB's models are turned against KiCad's footprints (HTU21D U3 by 270°). Verify U3, U4 and Q1 anyway.
5. **Shipping.** Product description e.g. *Sensor / Rain gauge* (HS 901590). To Germany, EuroPacket is a good compromise; check that import VAT is included at checkout.
6. **Hand soldering.** The D1 mini sockets, the XL6009 pins, the screw terminals, the headers and the optional C1 are not in the BOM; [Parts](Parts.md#parts-to-solder-yourself) lists type, pitch and hole size.
