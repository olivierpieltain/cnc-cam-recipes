(A6_01_T8_CHAMFER_5MM)
(T8  Chamfering Bit - 1/8AcA?A3 Shank      D=3.175 CR=0. TAPER=45deg - ZMIN=-1. - chamfer mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 100. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -1. mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : -75. mm )
(   Y Offset   : 215. mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(A6_T8_CHAMFER_5MM)
M6 T8 
(8)
M400
M851 S100
S12000 M3
G54
G0 X25. Y3.632
Z15.
G1 Z5. F600.
Z2. F200.
Z-1.
Y3.95 F600.
X5.
G2 X3.95 Y5. I0. J1.05
G1 Y45.
G2 X5. Y46.05 I1.05 J0.
G1 X45.
G2 X46.05 Y45. I0. J-1.05
G1 Y5.
G2 X45. Y3.95 I-1.05 J0.
G1 X25.
Y3.632
Z15.
M5
M400
M852
G28
M30
