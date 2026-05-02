(H2_03_T8_STRAP_CHAMFER)
(T8  Chamfering Bit - 1/8AcA?A3 Shank      D=3.175 CR=0. TAPER=45deg - ZMIN=-0.5 - chamfer mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 50. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -0.5 mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : 45. mm )
(   Y Offset   : -29.999 mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(H2_T8_STRAP_CHAMFER)
M6 T8 
(8)
M400
M851 S100
S12000 M3
G54
G0 X45.318 Y10.998
Z15.
G1 Z5. F400.
Z0.635 F133.3
Z-0.183
Y11.315 Z-0.5 F400.
Y11.632
X45. Y11.95
G2 X45. Y18.05 I0. J3.05
X45. Y11.95 I0. J-3.05
G1 X44.682 Y11.632
Y11.315
Y10.998 Z-0.183
Z15.
M5
M400
M852
G28
M30
