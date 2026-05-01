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

| ID | Tool | Material | Operation |
|---|---|---|---|
| **T1** | 3.175 mm × 22 mm 2F flat | Oak | Handle outer profile + shaft / tenon contour |
| **T2** | 3.175 mm × 22 mm 2F ball | Oak | R6 long-edge fillets, R5 pommel, Odin bust 3D finish |
| **T3** | 60° / 0.1 mm V-bit (wood) | Oak | All handle engravings |
| **T4** | 1.5 mm × 6 mm 2F flat | Oak | Wedge kerf (final dimension), small-radius corners |
| **T5** | 3 mm TiN drill | Oak | Strap hole Ø6 — drill in 2× from each side at Ø3, then bore out to Ø6 with T1 |
| **T6** | 3.175 mm × 12 mm spiral O 1F (metal) | 7075 alu | Head outer profile + eye pocket roughing |
| **T7** | 3.175 mm × 42 mm spiral O 1F (metal, long) | 7075 alu | Eye through-cut (deep reach, project 01 tool) |
| **T8** | 90° chamfer bit | 7075 alu | 5 mm head chamfer |
| **T9** | 30° / 0.2 mm V-bit (metal) | 7075 alu | All head engravings |
| **T10** | 3.175 mm × 22 mm 2F ball | 7075 alu | Optional fine finish on chamfer band edges |

T7 was the project 01 roughing tool — well-characterised on this machine,
known feeds-and-speeds. We get to reuse what's already trusted.

## Notes

- **Coatings:** the metal tools are TiN-coated; the wood tools we'll
  pick uncoated where available (TiN doesn't help in wood and adds cost).
- **Length stick-out:** keep stick-out ≤ 1.5× flute length whenever
  possible — these are 1/8" shanks and deflect under load. Project 01
  lessons-learned has the deflection numbers.
- **The 1/8" shank metal V-bit at 30° / 0.2 mm tip** is the highest-
  precision tool here. Treat it gently — light DOC, no plunges, short
  stick-out.
