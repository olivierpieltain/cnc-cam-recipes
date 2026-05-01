# Design Changelog — Project 02

Key design pivots taken during the design phase, in chronological
order. The current state is documented in [BRIEF.md](../BRIEF.md).

---

## 1. Initial brief — locked
Decorative Mjolnir hammer, 7075 aluminium head + American oak handle,
twin Odin bas-reliefs, Norse runic engravings, friction-tenon + wedge
joinery.

## 2. Curvature — cancelled
**Decision:** keep the handle straight rather than add a curved
sweep.
**Rationale:** "Let's not overcomplicate things — it will already be
challenging to mill this." Multi-axis sweep curves would have meant
either a 4th-axis setup (not available) or a much longer 3-axis
strategy with worse surface finish at the curve transitions.

## 3. Aluminium tooling
**Decision:** 1/8" carbide flat + 1/8" ball + 60° V-bit, air assist,
no coolant.
**Rationale:** No 6 mm tool was available; 1/8" sets a hard floor on
roughing speed in 7075 (200 W spindle ceiling).

## 4. Norse decoration set — picked
- **Long faces (±Y):** Yggdrasil (left) + Celtic-knot (right) per
  face. Vegvisir was tried first but the sourced SVG was line-art
  with many disconnected short strokes — when converted to DXF it
  rendered as scattered fragments. Replaced with Celtic-knot, which
  has clean closed loops.
- **Strike faces (±X):** Helm-of-Awe centered.
- **Top/bot chamfers (±Y):** Hávamál stanza 77 split into 4 phrases
  (`DEYR FE` / `DEYJA FRAENDR` / `DEYR SIALFR` / `ORÞSTIR LIFIR`).
- **Side chamfers (±Y, vertical):** `OLIVIER` + `HAMARR` (Old Norse
  for "hammer"), one per side.
- **Handle ±X faces:** `HAMMER OF OLIVIER` runic inscription, full
  vertical length of the handle.
- **Handle ±Y faces:** Triquetra / Valknut / Celtic-knot small
  medallions (Z=35 / 75 / 115).

## 5. Head chamfer — bumped 3 mm → 5 mm
**Decision:** larger chamfer to host the runic inscription bands
visibly.
**Tradeoff:** loses ~2 mm of flat-face decoration zone per side.
Acceptable — the medallion pair fits in the remaining 90 × 40 mm
flat zone with margin.

## 6. Othala (ᛟ) glyph — fixed
**Issue:** the original rune library drew Othala with legs extending
*outside* the [0, 1]² cell box, which clipped weirdly when laid out
next to other runes.
**Fix:** redrew Othala as a clean diamond on two splayed legs, fully
contained in the cell.
**Then upgraded** to the Anglo-Saxon "ēðel" crossed-legs variant per
user pick — the legs cross at the bottom of the diamond, forming a
small X under the diamond. More ornate, ties visually with the X
shapes of Gebo and Dagaz already in the inscriptions.

## 7. Odin bust — flattened 14 mm → 7 mm
**Decision:** halve the protrusion of the bas-relief.
**Rationale:** at 14 mm the bust visually overpowered the handle
scale. 7 mm reads as a deliberate bas-relief rather than a
near-sculptural protrusion.
**Stock impact:** total handle Y now 22 + 7 + 7 = 36 mm out of 50 mm
stock — leaves 14 mm fixturing clearance instead of ~0 mm.

## 8. Handle inscription — extended
**Decision:** replace `OLIVIER` (7 runes, Z=20..88) with
`HAMMER OF OLIVIER` (15 runes + 2 separators, full handle length,
~Z=20..178). Cell size kept at ~8 mm × 6 mm, gap 2 mm.

## 9. Handle pass-through — full thickness
**Decision:** drop the tenon narrowing.
**Original:** handle 25 × 22 mm shaft → narrowed to 24 × 14 mm tenon
at Z=190..240, shouldering against the head's bottom face.
**New:** handle uniform 25 × 22 mm the whole 240 mm length. Eye
widened from 24 × 14 to 25 × 22 mm. Head is held by the wedge
expansion alone, no shoulder.
**Why:** matches the user's reference photo (rustic Norse / Viking
construction). The wedge mechanism is fully sufficient for a
decorative hammer; the shoulder was redundant.

## 10. Pommel R8 → R5
**Decision:** smaller pommel fillet.
**Rationale:** R8 conflicted with the existing R6 long-edge fillets
in Fusion (no clean fillet face could be generated). R5 is the largest
size that produces clean transitions on the 13 × 10 mm bottom-face
flats.

## 11. Handle resize — bigger shaft, retracted tenon
**Decision:** grow the handle to use more of the 30 × 50 mm stock,
while keeping the head's eye unchanged.
- **Shaft (Z=0..190):** 25 × 22 → **28 × 33 mm** — uses ~93 % of the
  X stock (was 83 %) and 66 % of the Y stock (was 44 %), fills the
  hand more like a real war-hammer.
- **Tenon (Z=190..240):** new 25 × 22 mm section, sized to the
  existing eye.
- **Sharp 90° shoulder at Z=190** seats the head on the shaft. Y-step
  5.5 mm/side, X-step 1.5 mm/side.

**Bust position shifts:** back of bust moves from Y=±11 to Y=±16.5
(handle face). Peak now at Y=±23.5 (still fits 50 mm Y-stock with 1.5
mm clearance each side).

**Decoration repositioning:** all handle decorations re-imported on
the new shaft faces (HANDLE_PLANE_PY/NY moved from Y=±11 to Y=±16.5;
±X-face inscription moved from X=±12.5 to X=±14).

**Why "retracted" instead of full pass-through:** lets the user keep
the head exactly as designed (eye 25 × 22 mm, walls 14 mm thick at
narrowest), while still getting a comfortable grip below.
