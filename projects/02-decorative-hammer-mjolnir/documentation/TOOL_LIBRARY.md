# Tool Library — available stock for project 02

Photographed inventory (2026-05-01). All shanks are **Ø3.175 mm
(1/8")** unless noted. This is what we have on hand and can pick from
for the CAM plan; we don't need to buy anything new.

## Flat end mills (spiral, single-flute "O" — for aluminium)

These are the 7075-friendly tools: single-flute O-geometry handles
chip evacuation in soft aluminium without coolant.

| Tool | Diameter | Flute | OAL | Use case |
|---|---|---|---|---|
| Spiral O 1F – metal, mini | 1.0 mm | 3 mm | ~38 mm | Tight inside corners on the head, fine eye-corner relief |
| Spiral O 1F – metal | 3.175 mm | 12 mm | ~38 mm | Aluminium roughing (eye, pocket, side passes) at moderate DOC |
| Spiral O 1F – metal, long | 3.175 mm | 42 mm | ~60 mm | Reach-through on the eye (50 mm depth) — same tool used in project 01 |

## Flat end mills (two-flute set — for oak)

Two-flute geometry has lower chip-evac ceiling but better surface
finish in oak. Use these on the handle.

| Tool | Diameter | Flute | OAL |
|---|---|---|---|
| 2F flat | 1.0 mm | 4 mm | ~38 mm |
| 2F flat | 1.5 mm | 6 mm | ~38 mm |
| 2F flat | 2.0 mm | 12 mm | ~38 mm |
| 2F flat | 2.5 mm | 17 mm | ~38 mm |
| 2F flat | 3.175 mm | 22 mm | ~38 mm |
| 2F flat (spiral, longer) | 3.175 mm | 32 mm | ~55 mm |

**Critical:** the **1.5 mm flat** is exactly the width of the wedge kerf
on the handle — we can cut the kerf to final dimension on the machine.
**No hand-saw step needed** (the millability review previously said it
would be required because we thought 1/8" was the smallest flat).

## Ball nose end mills (two-flute)

For 3D adaptive finish (the Odin bust) and any radius transition.

| Tool | Diameter | Flute | OAL |
|---|---|---|---|
| 2F ball | 1.0 mm | 4 mm | ~38 mm |
| 2F ball | 1.5 mm | 6 mm | ~38 mm |
| 2F ball | 2.0 mm | 17 mm | ~38 mm |
| 2F ball | 2.5 mm | ~12 mm | ~38 mm |
| 2F ball | 3.175 mm | 10 mm (metal) | ~38 mm |
| 2F ball | 3.175 mm | 22 mm | ~38 mm |

## V-bits and engraving bits

| Tool | Tip angle | Tip diameter | Use |
|---|---|---|---|
| Triangle V-bit set | 20°, 30°, 45°, 60°, 90° | 0.1 mm | Wood pencil engravings (rune lines, medallion outlines) |
| Single-flute engraving (metal) | 30° | 0.2 mm | Aluminium engravings (head Hávamál + medallions) |
| Single-flute engraving (metal) | 60° | 0.1 mm | Aluminium engravings — wider line / less depth alternative |

The 30° / 0.2 mm metal V-bit is the right pick for the aluminium
head's runic bands — narrow and consistent line, good resin retention.
The 60° / 0.1 mm wood V-bit is the right pick for the oak handle's
wider-line decorations.

## Chamfer + drill + thread bits

| Tool | Spec | Use |
|---|---|---|
| Chamfering bit | 90°, 1/8" shank | The 5 mm × 45° head chamfers (fast pass, vs ramping a flat) |
| TiN drill | Ø1.0 / Ø2.0 / Ø2.5 / Ø3.0 mm | Strap hole start + corn-bit follow-up |
| TiN corn bit | 1 mm, 2 mm | Cleaning out narrow slots |
| Thread mills | M3 / M4 / M5 | Not needed for project 02 |

## Tools we'll actually use on project 02 — short list

Mapped to specific entries in the **Makera Carvera Tools v1.4.0**
library (installed at `%APPDATA%/Autodesk/CAM360/libraries/Local/Makera Carvera Tools v1.4.0/`):

| ID | Library | Tool Name | D × Flute | Material | Operation |
|---|---|---|---|---|---|
| **T1** | O Flute Bits | `Spiral O 3.175*22mm` | 3.175 × 22 | Oak | Handle profile, shoulder, tenon contour |
| **T2** | Ball Endmills | `2 Flute Ball Nose 3.175*22` | 3.175 × 22 | Oak | R6 fillets, R5 pommel, Odin 3D finish |
| **T3** | Engraving Bits | `Single Flute Engraving Metal 60 deg*.1mm` | 3.175 × 8 (60° tip 0.1) | Oak | All handle engravings |
| **T4** | O Flute Bits | `Spiral O Metal 1.5*6mm` | 1.5 × 6 | Oak | Wedge kerf — final 1.5 mm width |
| **T5** | Drill Bits | `3*12mm Drill` | 3 × 12 | Oak | Strap hole Ø3 pilot (2× from each side) |
| **T6** | O Flute Bits | `Spiral O Metal 3.175*12mm` | 3.175 × 12 | 7075 alu | Head profile, eye pocket rough |
| **T7** | O Flute Bits | `Spiral O 3.175*42mm` | 3.175 × 42 | 7075 alu | Eye through-cut (project 01 tool) |
| **T8** | Other Tools | `Chamfering Bit - 1/8" Shank` | 3.175 × 3 (90°) | 7075 alu | 5 mm head chamfer |
| **T9** | Engraving Bits | `Single Flute Engraving Metal 30 deg*.2mm` | 3.175 × 9 (30° tip 0.2) | 7075 alu | Head engravings |

**Important:** the metal-spec engraving bit (T3) is being used in oak.
Functionally fine — tip geometry is what matters for V-engraving, and
single-flute O-geometry handles wood chips well. The metal coating is
over-spec but doesn't hurt.

**T7 (Spiral O 3.175*42mm)** was the roughing tool used in project 01
— same spindle, same well-characterised feeds-and-speeds. Reusing
trusted parameters.

### How Fusion sees this library

Fusion's API URL pattern works:

```
toollibraryroot://Local/Makera Carvera Tools v1.4.0/<filename>.json
```

There's a known issue where `Local.json` (the index file Fusion expects
at `libraries/Local.json`) is missing — only the subfolder
`libraries/Local/` exists. The browser tree won't auto-populate, but
direct URL access reads each library file individually. We assign tools
in CAM operations by URL.

## Notes

- **Coatings:** the metal tools are TiN-coated; the wood tools we'll
  pick uncoated where available (TiN doesn't help in wood and adds cost).
- **Length stick-out:** keep stick-out ≤ 1.5× flute length whenever
  possible — these are 1/8" shanks and deflect under load. Project 01
  lessons-learned has the deflection numbers.
- **The 1/8" shank metal V-bit at 30° / 0.2 mm tip** is the highest-
  precision tool here. Treat it gently — light DOC, no plunges, short
  stick-out.
