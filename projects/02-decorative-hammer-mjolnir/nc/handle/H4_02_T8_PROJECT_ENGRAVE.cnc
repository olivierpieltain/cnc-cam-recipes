(H4_02_T8_PROJECT_ENGRAVE)
(T8  Chamfering Bit - 1/8AcA?A3 Shank      D=3.175 CR=0. TAPER=45deg - ZMIN=-2.5 - chamfer mill)
( =================================================== )
(   Z Origin Set To   : Stock Top )
(   Stock Height                    : 30. mm )
(   Toolpath Z Maximum from Stock Top: 15. mm )
(   Toolpath Z Min from Stock Top: -2.5 mm )
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

(H4_T8_PROJECT_ENGRAVE)
M6 T8 
(8)
M400
M851 S100
S12000 M3
G54
G0 X208. Y28.
Z15.
G1 Z1. F400.
Z-2.5 F133.3
X200. F400.
Z5.
Y23.8
Z1.
Z-2.5 F133.3
X208. F400.
Z5.
X205.6 Y28.
Z1.
Z-2.5 F133.3
X202.4 Y23.8 F400.
Z5.
X198. Y28.
Z1.
Z-2.5 F133.3
X190. F400.
Z5.
X197.6
Z1.
Z-2.5 F133.3
X196.4 Y23.8 F400.
Z5.
X194.
Z1.
Z-2.5 F133.3
X195.2 Y28. F400.
Z5.
X184. Y23.8
Z1.
Z-2.5 F133.3
X188. Y28. F400.
X180.
Z5.
X184.
Z1.
Z-2.5 F133.3
X188. Y23.8 F400.
X180.
Z5.
X174.
Z1.
Z-2.5 F133.3
X178. Y28. F400.
X170.
Z5.
X174.
Z1.
Z-2.5 F133.3
X178. Y23.8 F400.
X170.
Z5.
X160.
Z1.
Z-2.5 F133.3
X168. F400.
X165.6 Y25.9
X168. Y28.
X160.
Z5.
X150.
Z1.
Z-2.5 F133.3
X158. F400.
X155.6 Y23.8
X154. Y28.
X150. Y23.8
Z5.
X147.1 Y24.4
Z1.
Z-2.5 F133.3
X145.9 F400.
Y25.6
X147.1
Y24.4
Z5.
X143. Y25.9
Z1.
Z-2.5 F133.3
X140.6 Y23.8 F400.
X138.6 Y25.9
X140.6 Y28.
X143. Y25.9
Z5.
X140.6 Y28.
Z1.
Z-2.5 F133.3
X135. Y23.8 F400.
Z5.
Y28.
Z1.
Z-2.5 F133.3
X140.6 Y23.8 F400.
Z5.
X133. Y28.
Z1.
Z-2.5 F133.3
X125. F400.
Z5.
X131.8
Z1.
Z-2.5 F133.3
X133. Y23.8 F400.
Z5.
X130.6
Z1.
Z-2.5 F133.3
X129.4 Y28. F400.
Z5.
X122.1 Y25.6
Z1.
Z-2.5 F133.3
Y24.4 F400.
X120.9
Y25.6
X122.1
Z5.
X118. Y25.9
Z1.
Z-2.5 F133.3
X115.6 Y23.8 F400.
X113.6 Y25.9
X115.6 Y28.
X118. Y25.9
Z5.
X115.6 Y28.
Z1.
Z-2.5 F133.3
X110. Y23.8 F400.
Z5.
Y28.
Z1.
Z-2.5 F133.3
X115.6 Y23.8 F400.
Z5.
X105.6 Y25.
Z1.
Z-2.5 F133.3
X108. Y28. F400.
X100.
Z5.
X98.
Z1.
Z-2.5 F133.3
X90. F400.
Z5.
X88.
Z1.
Z-2.5 F133.3
X80. F400.
Z5.
X86.8
Z1.
Z-2.5 F133.3
X88. Y23.8 F400.
Z5.
X85.6
Z1.
Z-2.5 F133.3
X84.4 Y28. F400.
Z5.
X78.
Z1.
Z-2.5 F133.3
X70. F400.
Z5.
X60.
Z1.
Z-2.5 F133.3
X68. F400.
X65.6 Y25.9
X68. Y23.8
X60.
Z5.
X50.
Z1.
Z-2.5 F133.3
X54. Y28. F400.
X55.6 Y23.8
X58. Y28.
X50.
Z15.
M5
M400
M852
G28
M30
