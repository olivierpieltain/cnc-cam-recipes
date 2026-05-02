(H0b_01_T1_FACE_NY)
(T1  Spiral O 3.175*25mm  Makera    D=3.175 CR=0. - ZMIN=-0.5 - flat end mill)
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

(H0b_T1_FACE_NY)
M6 T1 
(5)
M400
M851 S100
S13000 M3
G54
G0 X302.064 Y0.58
Z15.
G1 Z5. F600.
Z-0.183 F200.
X301.746 Z-0.5 F1000.
X301.598
X-1.597 F600.
G2 X-1.597 Y2.725 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y4.871 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y7.016 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y9.161 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y11.307 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y13.452 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y15.598 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y17.743 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y19.888 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y22.034 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y24.179 I0. J1.073 F1000.
G1 X301.598 F600.
G3 X301.598 Y26.324 I0. J1.073 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y28.47 I0. J1.073 F1000.
G1 X301.598 F600.
X301.915 Z-0.183 F1000.
Z15. F600.
M5
M400
M852
G28
M30
