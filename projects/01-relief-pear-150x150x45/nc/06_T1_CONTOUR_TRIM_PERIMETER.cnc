(06_T1_CONTOUR_TRIM_PERIMETER)
(T1  Spiral O 3.175*42mm  Makera    D=3.175 CR=0. - ZMIN=-40.3 - flat end mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 40. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -40.3 mm )
(  )
( =================================================== )

( The following values are based on the part position info used in fusion and can be used to roughly align the machine offset from anchor 1 if you use that feature. )
(   X Offset   : -75. mm )
(   Y Offset   : -75. mm )

( =================================================== )

G90 G94
G17
G21
(When using Fusion for Personal Use, the feedrate of rapid)
(moves is reduced to match the feedrate of cutting moves,)
(which can increase machining time. Unrestricted rapid moves)
(are available with a Fusion Subscription.)

(06_ANCHOR1_CONTOUR_DECOUPE_PERIMETRE_3175x42)
M6 T1 
(5)
M400
M851 S100
S13000 M3
G54
G0 X145.46 Y74.683
Z15.
G1 Z-30. F400.
Z-34.365 F100.
Z-35.433
X145.777 Z-35.75 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-35.433
Z5. F400.
Y74.683
Z-30.
Z-35.115 F100.
Z-36.183
X145.777 Z-36.5 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-36.183
Z5. F400.
Y74.683
Z-30.
Z-35.865 F100.
Z-36.933
X145.777 Z-37.25 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-36.933
Z5. F400.
Y74.683
Z-30.
Z-36.615 F100.
Z-37.683
X145.777 Z-38. F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-37.683
Z5. F400.
Y74.683
Z-30.
Z-37.365 F100.
Z-38.433
X145.777 Z-38.75 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-38.433
Z5. F400.
Y74.683
Z-30.
Z-38.115 F100.
Z-39.183
X145.777 Z-39.5 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-39.183
Z5. F400.
Y74.683
Z-30.
Z-38.865 F100.
Z-39.583
X145.777 Z-39.9 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-39.583
Z5. F400.
Y74.683
Z-30.
Z-39.265 F100.
Z-39.983
X145.777 Z-40.3 F1000.
X146.095
X146.413 Y75.
Y146.413 F400.
X3.588
Y3.588
X146.413
Y75.
X146.095 Y75.317 F1000.
X145.777
X145.46 Z-39.983
Z15. F400.
M5
M400
M852
G28
M30
