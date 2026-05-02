(H1_08_T9_ODIN_VCARVE)
(T9  Single Flute Engraving Metal 30 deg*.2mm      D=3.175 CR=0. TAPER=15deg - ZMIN=-12.3 - chamfer mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 50. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -12.3 mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : 15. mm )
(   Y Offset   : 60. mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(H1_T9_ODIN_VCARVE)
M6 T9 
(8)
M400
M851 S100
S18000 M3
G54
G0 X178. Y15.
Z15.
G1 Z2. F600.
Z-12.3 F200.
X200. F600.
Z2. F500.
Z5. F600.
X171. Y17.5
Z2.
Z-12.3 F200.
Y12.5 F600.
Z2. F500.
Z15. F600.
M5
M400
M852
G28
M30
