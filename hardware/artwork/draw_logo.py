# Redraws the logo from simple shapes so every line and gap is >= 0.2 mm at 12 mm (2400 px canvas).
import math, numpy as np
from PIL import Image, ImageDraw
N=2400; B,W=0,255                      # B = printed (drawn black), W = no print
im=Image.new('L',(N,N),W); d=ImageDraw.Draw(im)
def disc(cx,cy,r,c): d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=c)
def stroke(pts,w,c):
    d.line(pts,fill=c,width=w,joint='curve')
    for x,y in (pts[0],pts[-1]): disc(x,y,w/2,c)
# ears, then a gap around the head, then head + chip tab + USB
d.ellipse((70,1080,470,1900),fill=B); d.ellipse((1930,1080,2330,1900),fill=B)
d.rounded_rectangle((316,716,2084,2304),264,fill=W)
d.rounded_rectangle((360,760,2040,2260),220,fill=B)
d.rounded_rectangle((750,640,1650,820),60,fill=B)
d.rounded_rectangle((1000,2160,1400,2360),60,fill=B)
d.rounded_rectangle((1080,2220,1320,2300),40,fill=W)          # USB opening
# antenna with two stripes
a0,a1=(1780,830),(1880,230); stroke([a0,a1],120,B)
for t in (0.18,0.82):
    x=a0[0]+(a1[0]-a0[0])*t; y=a0[1]+(a1[1]-a0[1])*t
    stroke([(x-80,y-13),(x+80,y+13)],44,W)
# steam
for i in range(401): disc(1150+70*math.sin(i/400*2*math.pi),560-i*1.25,35,B)
# meander on the chip tab, module window with WiFi
mx=[860,860,1010,1010,1130,1130,1270,1270,1390,1390,1540,1540]
my=[950,710,710,830,830,710,710,830,830,710,710,950]
stroke(list(zip(mx,my)),44,W)
d.rounded_rectangle((850,920,1550,1400),30,fill=W)
cx,cy=1200,1300
for r in (260,160): d.arc((cx-r,cy-r,cx+r,cy+r),225,315,fill=B,width=50)
disc(cx,cy,45,B)
# pin dots and four pads
for i in range(8):
    y=1000+i*165; disc(520,y,50,W); disc(1880,y,50,W)
for x,y in ((640,960),(1670,960),(640,2060),(1670,2060)): d.rectangle((x,y,x+90,y+90),fill=W)
# eyes and smile
for ex in (870,1530):
    disc(ex,1690,230,W); disc(ex,1690,180,B); disc(ex,1690,130,W); disc(ex,1690,75,B)
d.arc((1000,1620,1400,2020),40,140,fill=W,width=50)
a=np.array(im)<128
np.save('drawn.npy',a)
Image.fromarray(np.where(a,0,255).astype(np.uint8)).save('drawn_2400.png')
