# 02 — Decorative Mjolnir-style hammer

> **Status: design draft locked. CAM prep next.**

## Goal

A decorative hammer that's mechanically credible — looks and feels
like a real tool, but isn't intended for use. Mjolnir-inspired
polished-aluminium head, carved oak handle with twin Odin bas-reliefs
and runic name engraving.

## Stock

| Part | Material | Stock dimensions | Orientation |
|---|---|---|---|
| Head | 7075 aluminium | 50 × 50 × 100 mm | 100 = strike axis (X) |
| Handle | American (white) oak | 50 × 30 × 300 mm | 50 = thickness (Y, relief axis), 30 = grip width (X), 300 = length (Z) |

## Design — locked

### Head (aluminium) — modelled

- **Body:** rectangular block, 100 × 50 × 50 mm
  - X = 100 mm (strike axis)
  - Y = 50 mm (depth)
  - Z = 50 mm (eye axis, vertical when assembled)
- **All 12 edges chamfered 3 mm × 45°** (Mjolnir clean-block silhouette).
- **Eye:** rectangular through-hole, **24 × 14 mm**, full Z (50 mm),
  centered on origin. Matches handle tenon for friction fit.
- **Decorations** (live in CAM, not BRep):
  - Long faces (×2, ±Y, 50 × 100 mm): central knotwork medallion +
    4 triquetras at corners + 1 deep blind-hole "stone" (filled with
    black resin for polished-onyx look).
  - End faces (×2, ±X, 50 × 50 mm strike faces): central knotwork
    medallion + 1 stone.
- All V-bit engravings **filled with black resin / blackwash** post-
  machining.

### Handle (white oak) — modelled

- **Length:** 220 mm (shorter than initial 250 to give 2.2:1 ratio
  vs. 100 mm head — reads as balanced).
- **Cross-section:** 25 × 22 mm, all 4 long edges filleted **R6**
  for an oval feel.
- **Top — Tenon:** 30 mm long, 24 × 14 mm cross-section. Centered.
  Z range 190–220 mm. Friction-fits into head's 24 × 14 eye.
- **Just under tenon — Odin reliefs (×2):** Z range 130–190 mm.
  - Front face (+Y) and back face (-Y), mirrored copies of the
    same Viking-warrior bust.
  - Source: user-provided `Viking+Bust+100%+248mm` STL, converted to
    bas-relief via `convert_bust_to_relief.py` (slice + cap + scale).
  - Final relief size: **23.5 × 14 × 60 mm** — deep dramatic relief.
  - Cap flush with handle face (Y = ±11 mm), face peak at Y = ±25 mm
    — exactly fills the 50 mm Y-stock available.
- **Smooth grip:** Z 80–130 mm.
- **Runic engraving (±X faces):** Z range 20–88 mm.
  - **`ᛟᛚᛁᚹᛁᛖᚱ`** in Elder Futhark, vertical column, 7 runes.
  - Cells **7 mm wide × 8 mm tall**, 2 mm gap, total column 68 mm.
  - Drawn as line segments (not text — Fusion's text engine doesn't
    have proper Runic glyphs). V-bit-ready for the pencil pass.
  - -X face is mirrored in sketch local frame so runes are readable
    from both sides of the handle.
- **Pommel:** rounded R8 at bottom.
- **Leather strap hole:** Ø6 mm cross-bore, Z = 15 mm from bottom.

### Joinery — locked

- **Friction tenon + Viking wood wedge** (no glue).
- Tenon enters head's eye from below; head rests on shaft shoulder
  at Z = 190 mm.
- Wedge kerf in tenon top: TODO — to be added before CAM.

## Files in `design/`

| File | What it is |
|---|---|
| `convert_bust_to_relief.py` | Slices the user's 248 mm bust into a 60 mm bas-relief panel. Manual front-axis override (face is on -Y in the source bust's native frame). |
| `mirror_relief.py` | Mirrors the relief across XZ to create the -Y handle copy. |
| `preview_meshes.py` | matplotlib renderer for visually verifying orientation. |
| `odin_relief_panel.stl` | Final relief, +Y orientation (front face). |
| `odin_relief_panel_mirrored.stl` | Same relief mirrored for -Y face. |
| `02-decorative-hammer-mjolnir.f3d` | TODO — needs interactive Save-As in Fusion. |

## Pending before CAM

1. **Curvature** — gentle bow (deferred per user; will rebuild handle
   as swept body once everything else is locked).
2. **Wedge kerf** in handle tenon (~1.5 × 14 × 20 mm slot at top).
3. **Knotwork patterns** for head decoration — to be sourced /
   drawn as 2D sketches for V-bit + drilled-stone pockets.
4. **Aluminium tooling decision** — is there a Ø6 mm carbide flat
   available? Air assist or mist coolant for 7075?
5. **Carvera bed layout** — dowel pin positions to support the
   2-sided flip strategy on both pieces.

## Hard constraints

- Carvera Air work envelope ~360 × 240 × 140 mm — both blanks fit
  comfortably even with dowel fixturing.
- 200 W spindle ceiling. 7075 with a 1/8" tool is the limiting
  factor — light DOC, narrow WOC, plenty of patience.
- No 4th axis — handle Odin is a single-side bas-relief on each ±Y
  face (3-axis flip strategy), not 360° wrap.
- White oak grain (~0.5–1 mm) sets a practical lower bound on
  engraved feature size.
- Stock-Y check (handle): handle thickness 22 mm + relief depth 14 mm
  = 36 mm total used out of 50 mm available — fits with 14 mm
  back clearance.

## Folder layout

```
02-decorative-hammer-mjolnir/
├── BRIEF.md          (this file — design locked)
├── design/           Fusion .f3d + STLs + conversion scripts
├── cam/              recipe snapshots, post settings
├── nc/               posted .cnc files
├── documentation/    validation reports, instructions
└── photos/           build photos, fixture photos
```

## References

- Visual target — head + handle: [AncientSmithy Viking hammer history & craftsmanship](https://ancientsmithy.com/blogs/news/the-viking-hammer-myth-history-and-modern-craftsmanship)
- [Project 01 — Sylvan Dragoness pear relief](../01-relief-pear-150x150x45/)
  — same flow basis (3D adaptive + ball + V-bit pencil).
