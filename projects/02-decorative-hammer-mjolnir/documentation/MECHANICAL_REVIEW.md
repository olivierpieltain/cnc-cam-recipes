# Mechanical Review — Project 02

**Status:** all hard constraints respected. Design is mechanically
credible (look-and-feel of a real tool) without being intended as a
working hammer.

## 1. Stock fit

### Head — 7075 aluminium block

| Stock dim | Body dim | Margin |
|---|---|---|
| 100 mm (X = strike axis) | 100 mm | 0 mm — exact fit |
| 50 mm (Y = depth) | 50 mm | 0 mm — exact fit |
| 50 mm (Z = eye axis) | 50 mm | 0 mm — exact fit |

Stock is exactly the body's bounding box. Decorations are V-bit
engraved (sub-1 mm depth) so no exterior protrusions; eye is a 25 × 22
through-pocket centered on origin.

**Fixturing implication:** 6-sided machining (4 long faces × ±Y, ±X
+ 2 end caps × ±X). Need indexable dowel-pin fixture; see
[MILLABILITY_REVIEW.md](MILLABILITY_REVIEW.md).

### Handle — American (white) oak

The handle is a **two-section profile**: chunky shaft + retracted
tenon to fit the head's eye unchanged.

| Stock dim | Used dim (shaft / tenon) | Margin |
|---|---|---|
| 50 mm (Y = relief axis) | 47 mm = 33 (shaft) + 7×2 (busts) | 3 mm clearance |
| 30 mm (X = grip width) | 28 mm (shaft) / 25 mm (tenon) | 2 mm shaft, 5 mm tenon |
| 300 mm (Z = length) | 240 mm (190 shaft + 50 tenon) | 60 mm — endgrain fixturing tab |

The Y-margin tightened from 14 mm to **3 mm** when the user requested
a chunkier handle; this is workable with a side-clamp fixturing strategy
(clamp on ±X faces while machining ±Y).

**Stock-Y check (handle):** 33 + 7 + 7 = 47 mm vs 50 mm available.

## 2. Joinery — shouldered tenon + wood wedge

### Eye geometry vs tenon cross-section

| | X | Y |
|---|---|---|
| Shaft (BRep, with R6 long-edge fillets) | 28 mm | 33 mm |
| Tenon (BRep, with R6 long-edge fillets) | 25 mm | 22 mm |
| Eye (rectangular pocket in head) | 25 mm | 22 mm |

The tenon's 25 × 22 dimensions exactly match the eye. The R6 fillets
on the tenon's long edges produce 4 corner gaps in the eye:

- Each gap is the area between an R6 quarter-circle (handle corner)
  and the eye's sharp 90° corner: ≈ R6² (1 − π/4) ≈ 7.7 mm² per corner,
  31 mm² total around the perimeter.
- These gaps are the volume the wedge expansion needs to fill to lock
  the head. With ~31 mm² of corner gap and 14 mm of upper-tenon wedge
  travel, the wedge needs to splay each tenon "lip" by ~0.5 mm
  outward — well within the elastic + plastic deformation range of
  white oak under hammer pressure.

### Shoulder seat at Z=190

- The 28 × 33 shaft can't pass through the 25 × 22 eye, so the head's
  bottom face rests on a **shoulder ledge** of wood at Z=190:
  - Y-direction: 5.5 mm shoulder per side (33 − 22 = 11 mm total).
  - X-direction: 1.5 mm shoulder per side (28 − 25 = 3 mm total).
- Shoulder area = (33×28) − (22×25) = 374 mm² of bearing surface for
  the head — plenty for a decorative piece.

### Wedge mechanism

```
                       ┌─ wedge kerf, 22 × 1.5 × 14 mm
                       │   (saw slot at top of tenon)
                       ▼
   tenon top ─────┬────┴───┬─── flush with top of head (Z=240)
                  │ 25×22  │
                  │        │ ← upper 14 mm of tenon splits into two
                  │        │   "lips" when wedge is hammered in
                  ├────────┤    (this is INSIDE the head's eye)
                  │        │
   ===Z=190===────┤        ├──── shoulder seat (28×33 shaft)
                  │        │     resting head on this ledge
                  │ 28×33  │
                  │ shaft  │ ← solid handle from Z=0..190
                  │        │
```

- **Kerf:** 22 mm long (X axis) × 1.5 mm wide (Y axis) × 14 mm deep
  (Z axis, from top of tenon down).
- **Wedge:** typically harder/contrasting wood (oak, walnut, brass).
  Approximate dimensions: 22 mm × 14 mm long × tapered 0.5 mm (bottom)
  to 3 mm (top). Driven down with a mallet; expands the lips into the
  4 corner gaps inside the eye.
- **Why 22 mm and not 25 mm kerf width:** the kerf intentionally stays
  inside the R6 fillets on the top edges (tenon top face is 25 × 22 mm
  with R6 corners). 22 mm leaves ~1.5 mm clearance from the rounded
  corners, so the kerf is always cutting through fully-flat top
  material.

### Strap hole

- Ø6 mm cross-bore through Y axis, centered at Z = 15 mm from bottom.
- Located 2 mm above the start of the R5 pommel curve (curve covers
  Z = 0..~5 mm).
- Located 65 mm below the start of the rune inscription (Z=20).
- Functional: leather strap or rawhide loop for wrist tether.

### Pommel

- R5 fillet on all 4 bottom-perimeter edges.
- Picked R5 over R8 (original spec) because the bottom face has 4
  short straight segments (after R6 long-edge fillets) of only 13 mm
  (X) and 10 mm (Y); R8 fillets would interfere with the existing R6
  fillets. R5 leaves clean transitions.

## 3. Mass + balance (informational)

|  | Volume (cm³) | Density (g/cm³) | Mass (g) |
|---|---|---|---|
| Head (7075 alu, eye removed) | ~232 | 2.81 | **~652 g** |
| Handle (oak: 28×33×190 shaft + 25×22×50 tenon, features removed) | ~196 | 0.75 | **~147 g** |
| **Total** | | | **~799 g** |

Decorative weight, balanced toward the head — consistent with a
hand-axe / war-hammer feel rather than a working sledge.

## 4. Constraints validated

| Constraint | Status |
|---|---|
| Both blanks fit Carvera Air work envelope (360 × 240 × 140 mm) | ✓ |
| 7075 + 1/8" tool: only light-DOC, narrow-WOC strategies allowed | acknowledged, see millability review |
| 3-axis only — every feature reachable from a flip | ✓ all decorations lie on flat or single-plane chamfer surfaces |
| White oak grain (~0.5–1 mm): no engraved feature smaller | ✓ runes are 5 mm cells, medallions ≥11 mm, kerf 1.5 mm (post-CNC hand-finished) |
| Stock-Y handle headroom (14 mm) | ✓ |
| Wedge kerf width vs 1/8" tool | ⚠ flagged — handled with a hand-finishing pass; see millability review |

## 5. Open mechanical questions

- **None blocking.** All features are dimensioned and verified within
  stock + structural envelopes.
