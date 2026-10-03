import schemdraw, schemdraw.elements as e
from schemdraw import logic
schemdraw.config(fontsize=12, font='DejaVu Sans', lw=1.4)
def save(d,name):
    d.save(name+'.svg'); d.save(name+'.png', dpi=150)

# A) Oscillator
with schemdraw.Drawing(show=False) as d:
    d += (osc:=e.Dot().label('OSC', loc='top'))
    d += e.Line().right(1.5)
    d += (g:=logic.SchmittNot().right().label('U1A\n74HC14', loc='bottom', ofst=0.1))
    d.add(e.Label().at((g.in1.x-0.2, g.in1.y+0.25)).label('1', fontsize=9))
    d.add(e.Label().at((g.out.x+0.2, g.out.y+0.25)).label('2', fontsize=9))
    d += e.Line().right(1.2)
    d += (n2:=e.Dot())
    d += e.Line().right(1.8)
    d += e.Tag().right().label('GPIO25')
    d += e.Line().at(n2.center).up(2.0)
    d += e.Resistor().left().tox(osc.center).label('R1  220 kΩ')
    d += e.Line().down().toy(osc.center)
    d += e.Line().at(osc.center).left(1.5)
    d += (cs:=e.Capacitor().down(2.2).label('C sensor\nRC-SPC1KA\n6 → 1', loc='bottom', ofst=0.4))
    d += e.Ground()
    d.add(e.Label().at((osc.center[0]-1.6, -4.3)).label('U1: pin 14 → 3V3 with 100 nF to GND,  pin 7 → GND,  unused inputs 3, 5, 9, 11, 13 → GND', fontsize=10, halign='left'))
    save(d,'osc')

# B) NTC
with schemdraw.Drawing(show=False) as d:
    d += e.Vdd().label('3V3')
    d += e.Resistor().down(2.2).label('R2  2.8 kΩ\n(2 × 5.6 kΩ ∥)', loc='bottom', ofst=0.4)
    d += (n:=e.Dot())
    d += e.Line().right(2.0)
    d += e.Tag().right().label('GPIO34')
    d += e.Line().at(n.center).down(0.6)
    d += (j:=e.Dot())
    d += e.Line().left(2.8)
    d += e.Capacitor().down(1.8).label('C2\n100 nF', loc='bottom', ofst=0.4)
    d += e.Ground()
    d += e.Line().at(j.center).down(0.4)
    d += e.Thermistor().down(1.8).label('NTC 1 kΩ\nsensor 3 → 4', loc='bottom', ofst=0.4)
    d += e.Ground()
    save(d,'ntc')

# C) Heater
with schemdraw.Drawing(show=False) as d:
    q = e.NFet().at((0,0))
    d += q
    d.add(e.Label().at((q.drain[0]-0.5, q.gate[1])).label('Q1\nlogic-level\nN-MOSFET', halign='right', fontsize=11))
    d += e.Ground().at(q.source)
    d += e.Line().at(q.drain).up(0.5)
    d += e.Resistor().up(2.2).label('Heater ≈ 42 Ω\nsensor 5 → 2', loc='bottom', ofst=0.4)
    d += e.Vdd().label('12 V (boost OUT+)')
    d += e.Line().at(q.gate).right(0.8)
    d += (gn:=e.Dot())
    d += e.Resistor().right(2.2).label('R3  100 Ω')
    d += e.Tag().right().label('GPIO13')
    d += e.Line().at(gn.center).down(0.6)
    d += e.Resistor().down(1.8).label('R4\n100 kΩ', loc='bottom', ofst=0.4)
    d += e.Ground()
    save(d,'heater')

# C2) Power
with schemdraw.Drawing(show=False) as d:
    d += (b:=e.Ic(pins=[e.IcPin(name='IN+',side='left'), e.IcPin(name='IN−',side='left'),
                         e.IcPin(name='OUT+',side='right'), e.IcPin(name='OUT−',side='right')],
                   edgepadW=1.4, edgepadH=0.6, pinspacing=1.4, leadlen=1.0).label('MT3608\nboost module', 'center', ofst=(0,0.0), fontsize=11))
    d += e.Tag().at(b['IN+']).left().label('5 V')
    d += e.Ground().at(b['IN−'])
    d += e.Line().at(b['OUT+']).right(0.6); d += e.Tag().right().label('12 V')
    d += e.Ground().at(b['OUT−'])
    save(d,'power')

# D) Battery divider + I2C
with schemdraw.Drawing(show=False) as d:
    d += e.Vdd().label('BAT +')
    d += e.Resistor().down(2.0).label('R5\n100 kΩ', loc='bottom', ofst=0.4)
    d += (n:=e.Dot())
    d += e.Line().right(1.6); d += e.Tag().right().label('GPIO35')
    d += e.Resistor().at(n.center).down(2.0).label('R6\n100 kΩ', loc='bottom', ofst=0.4)
    d += e.Ground()
    save(d,'batt')
