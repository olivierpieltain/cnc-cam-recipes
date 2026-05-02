(A1_03_T6_EYE_FINISH)
(T6  Spiral O Metal 3.175*12mm  Makera    D=3.175 CR=0. - ZMIN=-26. - flat end mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 50. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -26. mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : 0. mm )
(   Y Offset   : 0. mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(A1_T6_EYE_FINISH)
M6 T6 
(5)
M400
M851 S100
S15000 M3
G54
G0 X34.96 Y25.317
Z15.
G1 Z5. F800.
Z0.635 F150.
Z-25.683
X35.278 Z-26. F500.
X35.595
X35.912 Y25.
Y14. F800.
G3 X37.5 Y12.413 I1.588 J0.
G1 X62.5
G3 X64.088 Y14. I0. J1.587
G1 Y36.
G3 X62.5 Y37.588 I-1.588 J0.
G1 X37.5
G3 X35.912 Y36. I0. J-1.588
G1 Y25.
X35.595 Y24.683 F500.
X35.278
X34.96 Z-25.683
Z15. F800.
M5
M400
M852
G28
M30
