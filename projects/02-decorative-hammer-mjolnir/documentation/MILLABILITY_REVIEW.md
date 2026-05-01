# Millability Review — Project 02

**Status:** millable end-to-end on the Carvera Air with 1/8" + V-bit
+ ball end mill, with one small hand-finishing step on the wedge kerf.

## 1. Tooling — confirmed

| Tool | Use | Notes |
|---|---|---|
| Ø3.175 mm (1/8") flat carbide end mill | All adaptive roughing, slot pockets, eye through-cut | Only flat tool available for both pieces. Light DOC + narrow WOC for 7075. |
| Ø3.175 mm (1/8") ball end mill | 3D adaptive + finish on Odin bust | Can also serve as a ball-finish for chamfered medallion borders. |
| 60° V-bit | All runic engravings + medallion line work | Pencil-pass operation; Carvera-friendly. |
| 90° V-bit (optional) | Wider/shallower engraving variant | Tradeoff: less depth = less resin retention; 60° is the default. |

**No 6 mm carbide flat available** — confirmed earlier in project. All
roughing/pocketing must run with 1/8".

**No coolant** — air assist only for both materials.

## 2. Fixturing strategy

### Head (aluminium, 6-sided — 4 long faces × ±Y, ±X + 2 ends)

- 4 dowel pins on the Carvera bed forming a 50 × 50 mm pocket; the
  head sits inside, indexed by 2 corner pins, held against by 2
  side pins or a side-mount toe clamp.
- Flip strategy: sides (1) → (2) → (3) → (4), then end (5) → (6).
  Reuse the same pin pattern; rotate the part 90° between flips.
- **Origin per setup:** stock corner at (X=0, Y=0, Z=stock-top). Use
  the dowel pin centerline as the X/Y datum so each flip lands on
  the same WCS.

### Handle (oak, 5 sides — 4 long faces + 1 bottom; top hidden in head)

- The 60 mm of extra Z stock (300 mm vs 240 mm part length) is the
  fixturing tab: clamp the bottom 30 mm in the Carvera vise jaws,
  cut all 4 long faces + bottom, then trim the tab off.
- Each flip rotates 90° around Z. Wood is forgiving on indexing (~0.1 mm
  is fine for engravings); the Odin bust is the most precision-critical
  feature → cut both bust faces in adjacent flips, NOT separated by
  multiple re-mounts.
- **Two-section profile (shaft 28×33 + tenon 25×22) requires either:**
  - **Option A (preferred):** a single contour pass that follows the
    Z=190 shoulder. The 1/8" tool steps in 1.5 mm (X) + 5.5 mm (Y) at
    that Z height to reduce to the tenon cross-section.
  - **Option B:** rough the entire 28×33 outer profile, then come back
    with a separate setup that pockets the tenon down to 25×22 from
    Z=190..240.

  Option A is fewer setups but the Z=190 shoulder transition is a
  small inside corner — needs a careful chamfer or fillet finish at
  the shoulder to avoid leaving a tool-witness mark.

## 3. Feature-by-feature feasibility

### Head decorations

| Feature | Tool | Strategy | Notes |
|---|---|---|---|
| Eye 25 × 22 through-pocket | 1/8" flat | 2D adaptive + spring pass | Through-cut from one end face, ~1.5 mm radii at corners (matches 1/8" tool). |
| 5 mm × 45° chamfer | 1/8" flat (chamfer pass) OR pre-chamfered stock | Stock arrives close to size; chamfer is a CAM finish pass. |  |
| Yggdrasil + Celtic medallions (long faces) | 60° V-bit | Pencil-pass tracing the imported DXFs | Sub-1 mm depth, paint-in. |
| Helm-of-Awe medallion (strike faces) | 60° V-bit | Same as above |  |
| Hávamál runic bands (top/bot chamfers) | 60° V-bit | Engrave on the angled chamfer face — needs the chamfer to be machined first so the surface is flat. |  |
| OLIVIER + HAMARR (side chamfers) | 60° V-bit | Same as above; vertical text orientation, runes are 5 mm cells |  |

### Handle decorations

| Feature | Tool | Strategy |
|---|---|---|
| 28 × 33 shaft outer profile | 1/8" flat | 2D contour rough + spring finish, Z=0..190 |
| 25 × 22 tenon outer profile | 1/8" flat | 2D contour rough at reduced cross-section, Z=190..240 |
| Z=190 shoulder transition | 1/8" flat | Slow-feed step pass between shaft and tenon contours |
| R6 long-edge fillets (shaft + tenon) | 1/8" ball | 3D contour finish — 8 long edges |
| HAMMER OF OLIVIER inscription (shaft ±X faces) | 60° V-bit | Pencil pass, 158 mm column of 17 cells |
| 3 small medallions (shaft ±Y faces) | 60° V-bit | Triquetra/Valknut/Celtic at Z=35/75/115 |
| Odin bas-relief (shaft ±Y faces) | 1/8" ball | 3D adaptive rough + parallel ball finish, 7 mm depth, 23.5 × 60 mm panel |
| Strap hole Ø6 cross-bore | 1/8" flat | Drill-style plunge + bore from each side |
| R5 pommel | 1/8" ball | 3D contour finish on 4 bottom edges |

### ⚠ Problem feature: wedge kerf 1.5 mm wide

**Issue:** The 1/8" tool is 3.175 mm in diameter, which cannot fit
into a 1.5 mm slot.

**Resolution — hybrid CNC + hand-finish:**

1. **CNC pass:** mill a 4 mm × 22 mm × 14 mm starter slot at the top of
   the handle (Z=226..240), centered on Y=0. This uses the 1/8" tool
   in a single linear pass.
2. **Hand pass:** finish the slot to its 1.5 mm final width with a
   fine-blade hand saw (e.g., Japanese pull saw or jeweler's saw).
   The 4 mm starter gives you a guided kerf to follow.

**Alternative if user wants pure-CNC:** widen the kerf design to
3.5 mm and use a fatter wedge to match. Cosmetic tradeoff: a 3.5 mm
wedge is more visible. *Decision: keep 1.5 mm + hand-finish for the
authentic Norse look.*

## 4. CAM operation order — proposed

### Head (per flip)

1. Face top of stock to clean reference (1/8" flat, 0.2 mm DOC)
2. Profile any side cut needed
3. **5 mm chamfer pass** on visible edges (1/8" flat, chamfer step-over)
4. **Eye pocket** (only on the flip where the strike axis is up — through-cut)
5. **Medallion engraving** (60° V-bit, pencil)
6. **Chamfer-band inscription engraving** (60° V-bit on chamfer surface)

### Handle (per flip)

1. Face stock side
2. Outer profile contour (1/8" flat)
3. R6 long-edge fillet (1/8" ball, 3D contour)
4. **HAMMER OF OLIVIER engraving** (±X face flips, 60° V-bit)
5. **Small medallions engraving** (±Y face flips)
6. **Odin bas-relief** (±Y face flips, 1/8" ball, 3D adaptive + parallel finish)
7. **Strap hole** (1/8" flat, drill-plunge)
8. **R5 pommel** (1/8" ball, 3D contour)
9. **Wedge kerf starter slot** (1/8" flat, top face only)
10. Trim fixturing tab (off the CNC, hand-saw)

## 5. Time budget — rough estimate

| Phase | Hours (est.) |
|---|---|
| Head — 6 flips, all roughing + finishing + engraving in 7075 | **8–12 h** |
| Handle — 5 flips, including 2 Odin reliefs (3D adaptive in oak) | **6–10 h** |
| Hand finishing (kerf, sanding, resin fill, polishing head) | **3–5 h** |
| **Total** | **17–27 h** of build time |

Aluminium dominates — 7075 with a 1/8" tool is slow by necessity
(0.05 mm DOC × 0.5 mm WOC × 1500 mm/min is typical conservative).

## 6. Open millability questions

- [ ] Confirm the Carvera Air 1/8" carbide stock you have on hand
  (uncoated vs AlTiN coating affects 7075 chip evac).
- [ ] Decide on V-bit angle: 60° (default) vs 90° for runic engravings
  — affects line crispness and resin retention.
- [ ] Validate the 4-dowel head fixture by simulating one flip on the
  posted G-code before cutting.
