# 02 — Decorative Mjolnir-style hammer

> **Status: design locked, modeling next.**

## Goal

A decorative hammer that's mechanically credible — looks and feels
like a real tool, but isn't intended for use. Mjolnir-inspired
polished-aluminium head, carved oak handle with a sculpted Odin
bas-relief.

## Stock

| Part | Material | Stock dimensions |
|---|---|---|
| Head | 7075 aluminium | 50 × 50 × 100 mm |
| Handle | American (white) oak | 50 × 30 × 300 mm |

## Design — locked

### Head (aluminium)

- **Silhouette:** Mjolnir clean-block — square 50 × 50 × 100, edges
  chamfered (~3 mm × 45°), top/bottom symmetric. Polished finish
  post-machining.
- **Long-face decoration (×2):**
  - Central circular knotwork medallion (Norse / Celtic interlace)
    — sourced motif, embedded as engraving.
  - One **triquetra** at each of the four corners of the face.
  - One **deep blind-hole "stone"** per face, drilled and filled
    with black epoxy resin (reads as polished onyx).
- **End-face decoration (×2):** matching circular knotwork medallion
  + one blind-hole stone each.
- **Through-eye:** rectangular tenon hole through the 50 mm width,
  sized for the handle tenon. Friction fit + Viking wedge.
- **All V-bit engravings filled with black resin / blackwash** post-
  machining — engravings stand out crisply against polished
  aluminium.

### Handle (white oak)

- **Cross-section:** flattened oval, ~25 × 22 mm shaft.
- **Top section** (~30 mm, just below head): Norse knotwork band.
- **Middle section** (~70–80 mm): **Odin bas-relief** (helmet, single
  eye, mustache, braided beard) on a flattened front panel. Sourced
  bas-relief STL — Anciensmithy-style Odin reference is the visual
  target. ~5–8 mm relief depth.
- **Bottom section** (grip end / pommel): **runic engraving of
  OLIVIER in Elder Futhark — `ᛟᛚᛁᚹᛁᛖᚱ`**, V-bit, filled with black
  resin or India ink wash. Reads as a maker's mark / signature.
- Handle tenon at the head-end: rectangular, dimensioned for friction
  fit through the head's eye. Saw kerf in the tenon end for the wedge.

### Joinery — locked

**Friction tenon + Viking wood wedge.** No glue. Most authentic, most
mechanically credible, removable. Wedge is hand-fitted and tapped in
after dry-assembly.

### Inscription content

- **Head central medallion:** Norse knotwork (geometric / interlace),
  not text. Pure ornament.
- **Handle bottom:** `ᛟᛚᛁᚹᛁᛖᚱ` — Olivier in Elder Futhark, 7 runes,
  reads left-to-right.

## Machining strategy

**Both parts on dowel-registered fixtures, single machine zero across
top + bottom setups.**

- **Head:** 2-sided flip (top + bottom). The four long faces' rune /
  knotwork bands done as part of the top + bottom ops via shallow
  Z-engagement on the chamfered transition zone.
- **Handle:** 2-sided flip (front + back of the curve profile). Dowel
  holes through waste tabs at each end of the 300 mm blank — tabs cut
  off in a final pass.

## Tooling

| Slot | Tool | Used for |
|---|---|---|
| **T1** | Ø6 mm carbide flat (TBD — to confirm with operator) or Ø3.175 spiral O | Aluminium roughing, oak roughing |
| **T2** | Ø3.175 ball nose 22 mm | Main 3D finish on Odin relief + head medallions |
| **T3** | Ø2.0 ball nose 17 mm | Detail rest finish (Odin's beard strands, tight features) |
| **T4** | V-bit (60° × 0.1 mm or 30° × 0.2 mm) | Pencil pass on engravings, runes, knotwork |
| **T5** | Drill bit Ø~6 mm | Stone blind holes |

## What's needed (next steps)

1. **Source the Odin bas-relief STL** — search MakerWorld / Cults3D /
   MyMiniFactory for a single-sided ~5–8 mm depth Odin head /
   Allfather relief. License-compatible.
2. **Source / draw the knotwork medallion + triquetra patterns** —
   either as STL relief or as 2D vector for V-bit engraving.
3. **Confirm aluminium tooling** — does the operator have a Ø6 mm
   aluminium-rated carbide end mill? Air assist only or mist coolant?
4. **CAD modeling in Fusion** — head + handle, embedded reliefs and
   engravings.
5. **Carvera bed layout** — locate dowel positions in the bed/fixture
   plate (via Fusion MCP screenshot).
6. **CAM setups** with dowel-flip registration.
7. **Validation, post, run.**

## Hard constraints

- Carvera Air work envelope ~360 × 240 × 140 mm — both blanks fit
  comfortably.
- 200 W spindle ceiling. 7075 aluminium with a 1/8" tool is the
  limiting factor — light DOC, narrow WOC, plenty of patience. A
  Ø6 mm carbide flat would roughly halve roughing time.
- No 4th axis — handle Odin is on a single front panel (3-axis
  bas-relief), not 360° wrap.
- White oak grain (~0.5–1 mm) sets a practical lower bound on
  engraved feature size; sub-mm beard strands may soften.

## Folder layout

```
02-decorative-hammer-mjolnir/
├── BRIEF.md          (this file — design locked)
├── design/           (Fusion .f3d once modeling starts)
├── cam/              (recipe snapshots, post settings)
├── nc/               (posted .cnc files)
├── documentation/    (validation reports, instructions)
└── photos/           (build photos, fixture photos)
```

## References

- Visual target — head: [AncientSmithy Viking hammer history & craftsmanship](https://ancientsmithy.com/blogs/news/the-viking-hammer-myth-history-and-modern-craftsmanship)
- Visual target — handle Odin: same article, carved Odin handle detail.
- [Project 01 — Sylvan Dragoness pear relief](../01-relief-pear-150x150x45/)
  — same flow basis (3D adaptive + ball + V-bit pencil).
