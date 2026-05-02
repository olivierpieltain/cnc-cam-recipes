(H0d_01_T1_FACE_NX)
(T1  Spiral O 3.175*25mm  Makera    D=3.175 CR=0. - ZMIN=-0.5 - flat end mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 30. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -0.5 mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : 1. mm )
(   Y Offset   : 0. mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(H0d_T1_FACE_NX)
M6 T1 
(5)
M400
M851 S100
S13000 M3
G54
G0 X302.064 Y0.61
Z15.
G1 Z5. F600.
Z-0.183 F200.
X301.746 Z-0.5 F1000.
X301.598
X-1.597 F600.
G2 X-1.597 Y2.786 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y4.961 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y7.136 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y9.312 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y11.487 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y13.663 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y15.838 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y18.014 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y20.189 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y22.364 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y24.54 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y26.715 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y28.891 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y31.066 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y33.242 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y35.417 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y37.592 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y39.768 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y41.943 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y44.119 I0. J1.088 F1000.
G1 X-1.597 F600.
G2 X-1.597 Y46.294 I0. J1.088 F1000.
G1 X301.598 F600.
G3 X301.598 Y48.47 I0. J1.088 F1000.
G1 X-1.597 F600.
X-1.915 Z-0.183 F1000.
Z15. F600.
M5
M400
M852
G28
M30
