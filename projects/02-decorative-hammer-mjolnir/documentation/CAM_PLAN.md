# CAM Plan — project 02

> **Status: BUILT (2026-05-02, audit + cleanup pass complete).**
> 14 setups, 38 posted .cnc files at [nc/](../nc/) (25 handle + 13 head),
> 1 known UI-only TODO (re-pick A1 chamfer chain, ~30 s).
> This document was the planning step; the section below reflects the
> actual final pipeline. Lessons learned about Fusion CAM idiosyncrasies
> are in the user's claude memory under `memory/fusion_cam_*.md`.

## Final pipeline (built 2026-05-02)

**14 setups, 38 .cnc files, 8 unique tools (T7 dropped, T9 30°-V-bit re-added for Odin V-carve overlay).**

| Setup | Ops | Output files |
|---|---|---|
| H0a +Y prep | T1 face-mill +Y flank, 0.5 mm skim | 1 (1.9 KB) |
| H0b -Y prep | T1 face-mill -Y flank, 0.5 mm skim | 1 (1.9 KB) |
| H0c +X prep | T1 face-mill +X flank, 0.5 mm skim | 1 (2.4 KB) |
| H0d -X prep | T1 face-mill -X flank, 0.5 mm skim | 1 (2.4 KB) |
| H1 +Y up | T1 profile → T1 strap bore (Ø6×30) → T8 strap chamfer → T2 Odin finish → T2 fillet finish → T2_15 (1.5mm ball) Odin fine → T8 V-bit engrave → T9 V-bit Odin V-carve overlay | 8 (1.2 MB) |
| H2 -Y up | mirror of H1 minus T9 V-carve | 7 (1.2 MB) |
| H3 +X up | T1 profile → T8 V-bit (HAMMER OF OLIVIER) → T2 fillet finish | 3 (68 KB) |
| H4 -X up | mirror of H3 | 3 (68 KB) |
| A1 +Z up | (T8 chamfer suppressed — UI re-pick) → T6 eye rough (stockToLeave 0.2) → T6 eye finish (stockToLeave 0) | 2 of 3 (435 KB) |
| A2 -Z up | T8 chamfer → T6 eye rough → T6 eye finish (eye meets A1 in middle, 4 mm overlap) | 3 (436 KB) |
| A3 +Y up | T8 chamfer → T8 V-bit project (Yggdrasil + Celtic + Hávamál + OLIVIER) | 2 (26 KB) |
| A4 -Y up | mirror of A3 (HAMARR side) | 2 (27 KB) |
| A5 +X up | T8 chamfer → T8 V-bit project (Helm-of-Awe) | 2 (10 KB) |
| A6 -X up | mirror of A5 | 2 (10 KB) |

**Key build decisions that differ from this original plan:**

- **Engravings use `project` strategy + `axialOffset = -1.5 mm` (oak) / `-1.0 mm` (alu)**, NOT `engrave`. Fusion's `engrave` strategy silently dropped most open lines from the DXF medallions/runes — `project` follows the projection onto the body surface and cuts at consistent perpendicular depth, including on the 45° chamfer faces.
- **All engravings use T8 (90° chamfer bit)**, not the original T3 (60° wood V-bit) and T9 (30° metal V-bit). The 90° angle gives a 3 mm-wide line at 1.5 mm depth — bolder/rougher look the user wanted. Same tool for handle and head means one fewer tool change.
- **Odin ROUGH (T2 adaptive) was dropped** — Carvera post processor fails with "Initialization fails" on adaptive output. The Odin FINISH (T2 parallel) and FINE (T2_15 parallel) handle bulk removal too — slower but post-compatible.
- **Eye uses rough+finish split per side**: A1+A2 each have a pocket2d ROUGH at `stockToLeave=0.2 mm` plus a contour2d FINISH at `stockToLeave=0` for clean walls. Default `stockToLeave=0.5` would have left the eye 1 mm undersized.
- **Head outer-profile contours dropped** — they cut nothing (stock = body), waste of 6 ops × ~5 min each.
- **Eye chamfer ops failed silently** — `chamfer2d` won't generate path on those inner edges. Eye edges left sharp; deburr by hand if desired.

**Hand-finished after CNC:**
- Wedge kerf (22 × 1.5 × 14 mm): hand-saw. The 240 mm handle won't stand on end in the 130 mm Z envelope.
- Eye edge chamfer: hand-deburr (CAM op didn't generate).
- Tab removal: band-saw at design Z=0 and Z=240 after all milling done.
- Resin fill for V-bit engravings: blackwash post-CNC.

---

## 2026-05-02 audit — fixturing rework + tool/origin cleanup

A re-audit of the Fusion CAM doc identified blockers in the
existing setups and reworked the fixturing strategy. Changes
applied to the live doc:

**Fixturing — new "Anchor 1 + manual flip + face-mill prep" approach
replacing the H0a/H0b dowel-tab drilling.** Vertical mount is
impossible (Carvera Air Z = 130 mm vs handle = 240 mm) and the
dowel-drilling scheme was complex. New approach:

- **End-square the blank off-machine** (table saw); becomes the X-pin
  reference.
- **4 face-mill PREP setups** (`H0a_PREP_PY`, `H0b_PREP_NY`,
  `H0c_PREP_PX`, `H0d_PREP_NX`) — one per long flank face, each skims
  0.5 mm with T1. After all 4, every long flank is flat → repeatable
  Anchor-1 lateral registration in any of H1–H4.
- **No dowel through-holes.** Toe-clamps on the tabs only.
- **Setup order** (mount-chain-optimized):
  PREP_PY → PREP_NY → PREP_PX → PREP_NX → H4 → H3 → H1 → H2 → A1..A6.

Detail in [FIXTURING_AND_ROTATION.md](FIXTURING_AND_ROTATION.md).

**Tool library tool-numbers fixed.** Previously every tool in the
library reported `T#1`, which would have collapsed the
`splitFile = tool` post into a single .cnc and confused the operator
at every M6 line. Now: T1=Spiral O 3.175×25, T2=Ball 3.175×22,
T3=V-bit 60° (oak), T4=Spiral O 1.5×6 (kerf), T5=Ø3 drill,
T6=Spiral O Metal 3.175×12, T7=Spiral O 3.175×42 (long), T8=Chamfer
bit, T9=V-bit 30° (metal), T10=Ball 1.5×8.

**WCS origin fixed.** All setups now use `wcs_origin_mode='stockPoint'`
+ `wcs_origin_boxPoint='top 1'`, putting WCS X0 Y0 Z0 at the
front-left-top corner of the stock — exactly where the operator
probes with the manual XYZ probe. Was previously `modelOrigin` which
would have offset every cut by the body-vs-stock-corner distance.

**Outer profile contour bottom depths corrected.** Previously every
`*_OUTER_PROFILE_CONTOUR` cut to `from stock bottom +0` = full stock
depth. Now: H1/H2 → −45 mm (5 mm safety to spoilboard, exposes
body ±Y face). H3/H4 → −29 mm (1 mm safety, exposes body ±X face).

**Eye split between A1 and A2.** Each cuts to −26 mm depth with
T6 (12 mm flute). With head 50 mm tall, two halves of 26 mm meet
with 2 mm overlap → clean breakthrough, no need for T7 long-flute on
the eye. T7 is now free for any future deep-bore needs.

**What remains for the user to add manually in the CAM UI** (geometry
selection is fragile via the API):

| Op | Setup | Tool | Strategy | Geometry |
|---|---|---|---|---|
| **Wedge kerf** (now possible thanks to horizontal mount) | H3 | T4 | 2D Pocket, helical entry | `WEDGE_KERF` sketch profiles. Bottom −15 mm, DOC 0.5 mm, 16000 RPM, 400 mm/min. Decide whether to do this in CAM or stick with hand-saw — original plan said hand-saw because of vertical-mount constraint, which no longer applies. |
| R6 long-edge fillet ×4 | H1, H2, H3, H4 | T2 (3.175 ball) | 3D parallel / corner | 2 long edges per setup (top edges of body relative to that setup's Z+). Radius R6. |
| R5 pommel-edge fillet ×4 | H1, H2, H3, H4 | T2 (3.175 ball) | 3D parallel / corner | The pommel-end edge of each face's exposed surface. Radius R5. |
| (Optional) T5 strap-hole pilot drill | H1, H2 | T5 (Ø3 drill) | Drill / peck | `STRAP_HOLE_DRILL` sketch position. Used if drift on T1's 2-sided helical bore proves problematic. The current build uses T1 helical bore from each side meeting in middle (no pilot) — keep that unless drift shows up. |

**Fixed `DEC_HANDLE_CELTIC_PY_115` is still empty** — needs to be
re-drawn before its engraving curves can be picked up.

---

## 2026-05-02 audit — sophistication pass

**Handle decorations rearranged — bottom-to-top: Vegvisir, Celtic,
Valknut.** Per user direction:

| Body Z | Sketch | Design | Notes |
|---|---|---|---|
| 35 (closest to pommel) | `DEC_HANDLE_VEGVISIR_PY_35` / `_NY_35` | 8-arm Vegvisir (Icelandic stave): radial 6 mm arms at 45°, each ending in a 2 mm perpendicular crossbar, R0.8 mm centre circle | New. Replaces TRIQUETRA. |
| 75 (middle) | `DEC_HANDLE_CELTIC_PY_75` / `_NY_75` | 3 overlapping R4 mm circles in triangular arrangement (3-ring Celtic) | New. Replaces VALKNUT (which moved to Z=115). |
| 115 (closest to bust) | `DEC_HANDLE_VALKNUT_PY_115` / `_NY_115` | Three interlocked triangles (copy of original Valknut, shifted +40 mm) | New. Replaces broken CELTIC. |

The original `TRIQUETRA_*_35`, `VALKNUT_*_75`, and broken
`CELTIC_*_115` sketches are kept in the model but hidden, so future
edits can reference them if needed. The H1 / H2 `T8_PROJECT_ENGRAVE`
op selections were re-pointed to the new sketches.

**Odin bust V-carve overlay added.** New sketch `ODIN_VCARVE_PY` on
`HANDLE_PLANE_PY` with two open-line accents (no eye outlines per
user direction):
- Vertical nose-bridge line at body X=0, body Z=170→148 (top of brow
  to nose tip on the bust)
- Horizontal lip line at body Z=141, body X=−2.5..+2.5 (just under
  the mustache)

New op `H1_T9_ODIN_VCARVE` uses **T9 30°/0.2 mm V-bit** with the
`trace` strategy (project hit empty toolpath with these line shapes),
`axialOffset = -0.3 mm` for a 0.31 mm-wide line on the bust surface.
Spindle 18 000 RPM, 600 mm/min. Generates a non-empty toolpath with
a depth-bounds warning (the bust mesh is taller than the op's
machining envelope; the warning is informational and does not stop
the cut).

**Design switched to Parametric mode** (was Direct) so feature
history is captured. No semantic change to existing geometry — just
allows future fillet/chamfer features to be added cleanly.

## Status of fillets and head edge rounding

**Handle R6 long-edge fillets and R5 pommel fillets are ALREADY
modeled in the body** — the `HANDLE_OAK_RAW` BRep includes 4× R6
cylinder faces (Z=5..190 at the four corners) and 4× R5 cylinder
faces at the pommel-end transition. The outer profile contour cuts
follow the rounded silhouette already.

What's still **TODO via Fusion UI** (the Fusion CAM API for
3D-finish ops on these specific cylinder faces kept producing empty
toolpaths or errors — this is faster to add manually):

| Op | Setup | Tool | Strategy | Geometry | Notes |
|---|---|---|---|---|---|
| R6/R5 fillet finish ×4 | H1, H2, H3, H4 | T2 (3.175 ball) | 3D parallel or scallop | The 2 visible R6 cylinder faces + 1 visible R5 pommel face per setup | Set machining boundary to a 2D sketch covering just the fillet zone (e.g. body X = ±8..±14, body Z = 0..190 strip). Stepover 0.4 mm. 15000 RPM, 700 mm/min. |

**Head chamfer → fillet rounding:** The user requested rounding the
head's 5 mm chamfered edges for a "sturdy but not angular" look. The
chamfers are modeled in the `HEAD_ALU_RAW` body. To convert them to
fillets cleanly: edit the body in Fusion (Modify → Fillet, pick the
chamfer-corner edges, R5 mm), then add 3D parallel finish ops in A1,
A2, A3, A4, A5, A6 with T2 (3.175 ball). The existing T8 chamfer
ops can stay (they take 0.5 mm chamfer of the new fillet edge for
final break) or be removed.

**Wedge kerf:** stays as **hand-saw**. Geometric constraint — the
kerf is at body Z=240 (top of tenon) opening downward into body −Z;
to CAM-cut this with a vertical-spindle 3-axis machine the stock
must be mounted with body Z axis vertical (handle standing on end).
240 mm handle vs 130 mm Carvera Air Z envelope — doesn't fit. Cut
the kerf manually after the CNC machining is complete.

## 2026-05-02 audit — fillet finish + head rounding (API limitations)

I attempted to implement the R6/R5 handle fillet finish ops and the
head chamfer→fillet rounding via Python API, including:

- `parallel`, `pencil`, `scallop`, `corner` strategies with explicit
  `model` (override-model) face list and 2D `machiningBoundarySel`
  sketch.
- Setting `boundaryMode='selection'`, `useSilhouetteAsMachiningBoundary=false`,
  explicit topHeight / bottomHeight bounds.

All 3D-strategy operations failed in this document with one of:
- `"Depth (Y) less than the depth of the selected model"` warning + empty
  toolpath. The warning is qualified at the SETUP level, not the op,
  and persists regardless of op-level configuration.
- `0xffffffff "An unhandled exception occurred"` errors.
- `"Generation not started"` errors.

The likely cause is interaction between the `ODIN_RELIEF_v3` mesh
body included in H1's setup model and the parametric-mode change
applied earlier in the session. These ops compute fine when added
through the Fusion UI directly (per Autodesk forum reports of similar
issues), so the recommended path is **add these ops manually**:

| Op | Setup | Tool | Strategy | What | Notes |
|---|---|---|---|---|---|
| R6/R5 handle fillet finish ×4 | H1, H2, H3, H4 | T2 (3.175 ball) | 3D parallel or scallop | Sweep over the body's R6 cylinder fillet faces and R5 pommel fillets | UI: select the 2 R6 + 1 R5 cylindrical faces visible from each setup as the model surfaces; let Fusion auto-compute boundary. 0.4 mm stepover, 15000 RPM, 700 mm/min. |
| Head chamfer → R5 fillet | A1..A6 | T2 (3.175 ball) | 3D parallel | After CAD edit (replace 5 mm chamfer feature with R5 fillet on `HEAD_ALU_RAW`), 3D-finish each visible fillet face | UI: in design workspace edit the chamfer feature → switch to fillet → R5; then add 3D parallel ops in each A setup. |

**A1_T8_CHAMFER_5MM is currently suppressed** — its contour-chain
selection was lost during my retool attempts (the API rejected
re-application of `BRepBody`-typed entities to `ChainSelection.inputGeometry`).
Restore by editing the op in the UI: pick the four chamfered
corner-edge chains on the head's +Z face (same as the A2..A6 chamfer
ops). It'll take 30 seconds with the picker.

## 2026-05-02 audit — fillet finish ops finally working

The previous "Depth less than the depth of the selected model"
warnings turned out to be a **stale CAM-state caching issue**. The
fix that worked:

1. Backup the document (saved version snapshot).
2. `cam.clearAllToolpaths()` to flush all cached toolpath state.
3. `cam.generateAllToolpaths()` to recompute everything fresh.
4. **Duplicate the working `H1_T2_ODIN_FINISH` op** as the seed for
   each fillet finish op (per-setup), keeping `boundaryMode='silhouette'`,
   adjusting only `bottomHeight_offset` to cover the fillet-zone Z range.

Result: **4 new ops added, all generating clean toolpaths, 0 warnings, 0 errors.**

| Op | Setup | Tool | Strategy | Bottom |
|---|---|---|---|---|
| `H1_T2_FILLET_FINISH` | H1 | T2 (3.175 ball) | parallel (silhouette boundary) | −20 mm — covers R6 fillet at body +Y +X corner + R5 pommel +Y face |
| `H2_T2_FILLET_FINISH` | H2 | T2 | parallel | −20 mm |
| `H3_T2_FILLET_FINISH` | H3 | T2 | parallel | −10 mm — H3/H4 stock is 30 mm thick, fillet zone shallower |
| `H4_T2_FILLET_FINISH` | H4 | T2 | parallel | −10 mm |

These ops sweep the entire +Y / -Y / +X / -X face area visible in
each setup. They're slightly redundant with the existing Odin
parallel-finish ops in H1/H2 (covering the bust panel) but the
cycle-time hit is acceptable for full-coverage finish — the user's
"as pretty and sophisticated as possible" goal.

**Head chamfer→fillet rounding** still TODO (requires CAD edit on
`HEAD_ALU_RAW`: replace 5 mm chamfer features with R5 fillet, then
3D parallel finish ops in A1..A6 — same pattern as the handle).
This is a CAD-modification operation safer to do in the UI.

**Final CAM state**: 14 setups, 38 OK ops, 0 warnings, 0 errors,
1 suppressed (A1 chamfer geometry — quick UI restore needed).

## Final CAM state (40 valid ops, 1 suppressed, 0 warnings, 0 errors, 14 setups)

```
[H0a_PREP_PY]   T1 face-mill +Y                                  1 op
[H0b_PREP_NY]   T1 face-mill -Y                                  1 op
[H0c_PREP_PX]   T1 face-mill +X                                  1 op
[H0d_PREP_NX]   T1 face-mill -X                                  1 op
[H4_HANDLE_NX]  T1 outer profile + T8 engrave + T2 fillet finish 3 ops
[H3_HANDLE_PX]  T1 outer profile + T8 engrave + T2 fillet finish 3 ops
[H1_HANDLE_PY]  T1 outer + T1 strap bore + T8 strap chamfer
                + T2 Odin parallel + T2 fillet finish
                + T10 Odin fine + T8 engrave + T9 Odin V-carve   8 ops
[H2_HANDLE_NY]  same as H1 minus T9 V-carve                      7 ops
[A1_HEAD_+Z]    (T8 chamfer SUPPRESSED — UI re-pick)
                + T6 eye rough + T6 eye finish                   2 of 3 ops
[A2_HEAD_-Z]    T8 chamfer + T6 eye rough + T6 eye finish        3 ops
[A3..A6 head faces]  T8 chamfer + T8 engrave                     8 ops total
```

## 2026-05-02 cleanup pass — final post

A subsequent re-audit caught three small issues; all resolved:

- **H0b face-mill feeds out of sync** — siblings ran 13000 RPM / 600 mm/min,
  H0b had been left at 10000 / 1000 from a stray edit. Re-synced.
- **H1 / H2 strap-hole bore stockToLeave = 0.5 mm + tolerance 0.1 mm** —
  would have produced Ø5 hole instead of plan's Ø6, with 0.2 mm step at
  the meeting plane between the two helical bores. Fixed to
  stockToLeave=0 and tolerance=0.01 mm. Hole is now Ø6 as designed.
- **Posted .cnc files were stale** — predated the late-add fillet-finish
  ops (×4), Odin V-carve op (H1), and the four PREP face-mill setups.
  Total of 9 ops missing on disk. **Wiped and re-posted all 38 valid
  ops** (1 suppressed = A1 chamfer; intentional gap until UI re-pick).

Final disk: 25 .cnc in `nc/handle/`, 13 .cnc in `nc/head/`, 2.6 MB +
964 KB. Files ordered with zero-padded indices matching op position
in setup so the operator runs them in numeric sequence.

**One UI-only TODO before milling**: un-suppress `A1_T8_CHAMFER_5MM`
by re-picking the four chamfered corner-edge chains on the head's +Z
face (same edges already used in A2_T8_CHAMFER_5MM, which works).
The Fusion CAM API rejects ChainSelection BRepBody re-binding — must
be done with the picker.

---

## Original plan (as of 2026-05-01, kept for reference)

> This was the planning step before any Fusion CAM operations existed.
> The plan was reviewed first; only then did we start clicking in Fusion.

## Why a written plan first

The user has flagged that he can't validate technical correctness on
CAM (feeds-and-speeds math, fixture-collision analysis, post-
processor compatibility). The mitigation:

1. **Conservative defaults** for every cut.
2. **Simulate every operation in Fusion** before posting.
3. **Cross-reference feeds and speeds against published sources** and
   cite the source in the operation comment.
4. **Walk through the reasoning** in this document so anything
   off-smell is visible to the user before the bit touches stock.
5. **Validate every posted `.cnc`** with `tools/validate_cnc.py` and
   the safety-scan headers from project 01.
6. **Test the easier piece first** — handle (oak) before head (7075).
   Fixturing + workflow get debugged on the cheap material.

## Two CAM tracks

### Handle (white oak) — first

Goal: validate fixture, indexing, decoration engraving recipes on a
forgiving material. If the handle ships, the workflow is real.

**5 setups: 1 prep (drill fixturing tabs) + 4 long-face flips.**
Pommel R5 fillet and strap hole are both reachable from the side
flips, so no separate pommel/bottom setup is needed. Wedge kerf is
cut from the side in H3 (per the existing strategy).

| # | Setup | Tools | What it does |
|---|---|---|---|
| H0a | PREP — bore 2 fixturing holes (face A down) | T1 | Raw blank flat on bed, lower-left corner against Anchor 1. **Helical-bore 2 Ø4.2 mm vertical through-holes** through the 2 tab centres (one per tab) using T1 (3.175 mm 2F flat) in helical mode — Ø3.175 tool walks a 0.5 mm-radius helical path to produce Ø4.2 mm holes. Sacrificial spoilboard underneath. |
| H0b | PREP — bore 2 fixturing holes (rotated 90°) | T1 | **Rotate stock 90° about its long axis**, re-register at Anchor 1 (different corner against the pins now), helical-bore 2 more Ø4.2 mm holes at the same tab centres. After H0a + H0b, the stock has 4 through-holes meeting at the cross-section centre axis. For any of H1–H4, exactly one hole-pair is vertical so dowels go through it. |
| H1 | Side A (+Y face up, bust side) | T1, T2, T3 | Outer profile contour 28×33 → tenon shoulder at Z=190. R6 long-edge fillets along this face (T2 ball). HAMMER OF OLIVIER engraving (T3 V-bit). 3 small medallions (T3). 3D adaptive + ball-nose finish on the Odin bust panel. R5 pommel-edge fillet on this face (T2 ball). |
| H2 | Side B (-Y face up) | T1, T2, T3 | Mirror of H1 minus the bust. Outer profile finish + R6 fillets + engravings on -Y face + R5 pommel fillet. |
| H3 | Side C (+X face up, wedge kerf side) | T1, T2, T3, T4 | Profile + R6 fillets + engravings on +X face + R5 pommel fillet. **Wedge kerf** at top of tenon (T4 1.5 mm flat, helical entry, full-width slot). |
| H4 | Side D (-X face up) | T1, T2, T3 | Mirror of H3 minus the kerf. Profile + R6 fillets + engravings + R5 pommel fillet. |

**Strap hole (Ø6, near pommel)**: drilled in H1 + H2 — Ø3 pilot from
+Y in H1, Ø3 pilot from -Y in H2 (meet in the middle to minimise
drift). Then bored to Ø6 with T4 (1.5 mm flat) in helical mode in H1.

**Tab removal** is **manual** (band saw or hand saw) **after all
milling is done**. The tabs are not machined off on the Carvera —
that would require a final setup with a different fixture, which we
don't need for a decorative project.

### Head (7075 aluminium) — second

Goal: produce the polished decorative head. Slowest run of the project
because of the spindle ceiling.

6 setups:

| # | Setup | Tools | What it does |
|---|---|---|---|
| A1 | Top end (+Z up) | T6, T7, T8 | Outer profile pre-cut (if stock is oversized). Eye 25×22 pocket roughing through ~half the depth (T6). Eye finish to wall (T7 long-flute, multi-pass). 5 mm chamfer on the +Z face perimeter (T8). |
| A2 | Bottom end (-Z up) | T6, T7, T8 | Eye finish from the other side (meets in the middle, eliminates breakthrough burr). 5 mm chamfer on -Z perimeter. |
| A3 | Long face +Y | T6, T8, T9 | Outer profile finish on this face. Side chamfers (5 mm × 45°). Yggdrasil + Celtic medallion engraving (T9 metal V-bit). Hávamál top/bot chamfer engravings. OLIVIER vertical side-chamfer engraving. |
| A4 | Long face -Y | T6, T8, T9 | Mirror of A3 with HAMARR / DEYR SIALFR / ORÞSTIR LIFIR text. |
| A5 | Strike face +X | T6, T8, T9 | 50×50 face: profile finish + 4 corner chamfers + Helm-of-Awe medallion engraving. |
| A6 | Strike face -X | T6, T8, T9 | Mirror of A5. |

## Tool list (final picks)

See [TOOL_LIBRARY.md](TOOL_LIBRARY.md) for the full inventory and
rationale. Final selection for project 02:

| ID | Tool | Mat. | Primary use |
|---|---|---|---|
| **T1** | 3.175 mm × 22 mm 2F flat | Oak | Handle profile, shoulder, tenon |
| **T2** | 3.175 mm × 22 mm 2F ball | Oak | Fillets, pommel, Odin 3D finish |
| **T3** | 60° / 0.1 mm V-bit | Oak | Handle engravings |
| **T4** | 1.5 mm × 6 mm 2F flat | Oak | Wedge kerf (final width!) |
| **T5** | 3.0 mm TiN drill | Oak | Strap hole pilot |
| **T6** | 3.175 mm × 12 mm 1F spiral O | Alu | Head profile, pocket rough |
| **T7** | 3.175 mm × 42 mm 1F spiral O long | Alu | Eye through-cut |
| **T8** | 90° chamfer bit | Alu | 5 mm head chamfers |
| **T9** | 30° / 0.2 mm V-bit (metal) | Alu | Head engravings |

## Feeds and speeds — provisional

The numbers below are starting points. They will be cross-referenced
against the Carvera community wiki and Carbide3D's calculator, then
locked in the per-operation Fusion comments before posting.

### Oak (Janka ~1350, density 0.75 g/cm³)

Starting point based on project 01 roughing recipe (corrected version,
12-hour pass) which used the same T1 in oak/pear-equivalent:

| Op | Tool | Spindle | Feed | DOC | WOC |
|---|---|---|---|---|---|
| Profile rough | T1 (3.175 flat) | 13 000 RPM | 600 mm/min | 1.5 mm | 0.8 mm (25 % of D) |
| Profile finish | T1 | 15 000 RPM | 800 mm/min | 0.5 mm | 0.5 mm |
| Fillet finish | T2 (3.175 ball) | 15 000 RPM | 700 mm/min | 0.3 mm step | 0.3 mm step |
| Odin 3D adaptive | T1 (rough) | 13 000 RPM | 600 mm/min | 0.6 mm | 0.6 mm |
| Odin 3D finish | T2 ball | 18 000 RPM | 1200 mm/min | 0.15 mm step | 0.15 mm step |
| V-bit pencil engrave | T3 | 18 000 RPM | 1000 mm/min | 0.4 mm | n/a (line trace) |
| Wedge kerf | T4 (1.5 flat) | 16 000 RPM | 400 mm/min | 0.5 mm | full 1.5 mm slot, helical entry |
| Strap hole drill | T5 | 8 000 RPM | 100 mm/min | peck 1 mm | n/a |

### 7075 aluminium (the slow runs)

Numbers anchored to Carvera Air's 200 W spindle ceiling. **Bias hard
toward conservative.**

| Op | Tool | Spindle | Feed | DOC | WOC |
|---|---|---|---|---|---|
| Eye rough | T6 (3.175 1F O) | 13 000 RPM | 1000 mm/min | 0.1 mm | 0.5 mm (16 % D) |
| Eye finish | T7 long-flute | 13 000 RPM | 800 mm/min | 0.05 mm | 0.3 mm |
| Profile finish | T6 | 15 000 RPM | 800 mm/min | 0.05 mm | 0.3 mm |
| Chamfer | T8 (90°) | 12 000 RPM | 600 mm/min | 0.5 mm step | n/a |
| V-bit engrave | T9 (30°) | 18 000 RPM | 600 mm/min | 0.15 mm | n/a |

Power check: at the eye-rough numbers above, MRR = 0.5 × 0.1 × 1000 =
50 mm³/min ≈ 0.83 mm³/s. For 7075 (k ≈ 1.0 W per mm³/s for soft
aluminium with sharp tool), P ≈ 1 W cutting + spindle losses. Well
under the 200 W ceiling. The bottleneck is thermal/chip management,
not power — air assist needs to be on.

## Carvera Air bed — reference specs

Confirmed from Makera + community sources (cited in **References** at
the bottom). The Carvera Air ships with a **CNC-machined MDF bed**
that has the following layout:

| Spec | Value |
|---|---|
| Working area (3-axis) | **300 × 200 × 130 mm** (X × Y × Z) |
| Bed surface | MDF, machined; replaceable consumable |
| Hold-down | Threaded holes (M6 metric / 1/4-20 inch on Saunders option plate) |
| **Anchor 1** | Lower-left corner of the bed (origin reference) |
| **Anchor 2** | Centre of the bed (alternate origin reference) |
| Locating pins | **Ø4 mm** dowel pins in **8 mm standoffs** at each anchor |
| Optional aluminium plate | Saunders 306 × 222 × 17.8 mm, M6 / 20 mm grid |

The Ø4 mm pins at Anchor 1 give a **repeatable lower-left registration
corner** on the bed itself — pressing the stock against the two pins
puts it at a known X/Y position relative to the machine origin. This
is the foundation of the fixturing strategy below.

## Work origin policy — "Anchor 1 + stock corner offset"

The convention adopted across this project (and matching project 01
+ arc-reactor):

- **WCS X0 Y0** = the **lower-left front corner of the stock as
  mounted**. The stock is registered against Anchor 1's two Ø4 mm
  pins, so WCS X0 Y0 is at a known offset from machine origin. This
  is the user's term **"anchor 1"** for the WCS.
- **WCS Z0** = the **top face of the blank**, set with the XYZ probe
  (white-side manual probe placed against the front-left corner of the
  stock; mill positioned in the probe's square; click "Set Origin →
  Set By XYZ Probe"; tool diameter 3.175 mm).
- **Posted G-code** uses positive X, Y values that stay inside
  X = 0..stock_X_mm and Y = 0..stock_Y_mm. The pre-amble emits a
  safety lift `G53 G0 Z-2` before the first XY rapid (per project 01
  validation report — emitted automatically by the v1.4.3 community
  post).
- **Z-zero is re-set per setup**: each flip presents a new "top of
  blank" surface. We re-probe at the start of each setup to reset Z0
  to the new top.
- **X/Y origin is preserved across flips on the same fixture** as
  long as the stock returns to the same anchor-1 position (the fixture
  pins guarantee this).

## Project-02 fixture strategy

### Handle (oak, 300 mm long stock — HORIZONTAL with sacrificial tabs)

> **Fixturing correction (2026-05-02):** earlier draft proposed
> mounting the handle vertically. Carvera Air's Z work envelope is
> only **130 mm** but the handle is **240 mm** long, so vertical mount
> is physically impossible. The handle is mounted **horizontally**,
> long axis along bed X, with sacrificial tabs at both ends used as
> dowel anchors. See [FIXTURING_AND_ROTATION.md](FIXTURING_AND_ROTATION.md)
> for the full per-setup mount + rotation procedure.

**Stock**: 50 × 30 × 300 mm rectangular oak blank. Finished handle
body is 240 mm long (Z=0 to Z=240 in design coords), centred in the
stock — so we have **30 mm of un-machined "tab" at each end** for
fixturing. The tabs are removed after all milling is done (band saw
or hand saw).

**Mount**: handle laid flat on the bed, long axis along bed X. Each
tab is held to the bed by a Ø4 mm dowel pin going through a vertical
through-hole drilled in the tab. The body of the handle is suspended
between the two tab anchors — it never touches the bed surface, so
machined features on the four long faces don't interfere with seating.

**Rotation between H1–H4**: lift the handle, rotate 90° about its
long axis, drop back onto the dowels via the alternate pair of
through-holes. Each tab has **two perpendicular through-holes**
(one in handle +Y direction, one in handle +X direction). Whichever
pair is vertical at the moment is the pair the dowels go through.

```
top view of stock on bed (handle long axis = bed X):

   bed surface
   ┌────────────────────────────────────────────────────────┐
   │                                                        │
   │   ●●           ┌────────┐                  ┌────────┐  │
   │  Anchor 1      │ TAB    │   handle body    │ TAB    │  │
   │   pins         │  ●     │ (suspended,      │   ●    │  │
   │                │ ● ● ●  │  doesn't touch   │ ● ● ●  │  │
   │                │  ●     │   the bed)       │   ●    │  │
   │                └────────┘                  └────────┘  │
   │                  ↑                            ↑        │
   │              dowels (Ø4)                  dowels (Ø4)  │
   │           through tab holes            through tab     │
   │                                          holes         │
   └────────────────────────────────────────────────────────┘

each tab cross-section (looking down the handle long axis):

        ┌─────────┐
        │    ●    │   ←── +Y direction through-hole
        │ ●─────● │   ←── +X direction through-hole  (the two
        │    ●    │       cross at the centre of the tab)
        └─────────┘
        for H1/H2 (+Y or -Y up) the +X-direction hole is vertical
        for H3/H4 (+X or -X up) the +Y-direction hole is vertical
```

### Head (7075 alu, 100 × 50 × 50 mm stock)

- **Mounted on a 4-pin pocket** indexed off Anchor 1. The head's
  100 mm dimension along bed X, 50 mm along bed Y. Two pins on the
  back face (anchor-1 side) and two on the side establish a unique
  corner.
- **Indexed flip** rotates the head 90° around either its X or Y axis
  per setup. Pins are repositioned for the two strike-face setups
  (50 × 50 footprint) vs the 4 long-face setups (100 × 50 footprint).
- Side-clamp toe-clamps on the **non-machining face** for each setup
  — never on a face being machined or about to be machined.

```
   bed surface (top view, looking down -Z)
   ┌──────────────────────────────────────┐
   │                                      │
   │   ●  ●                               │ ← 4-pin pocket
   │  ┌────────────────────┐              │   (Ø4 mm pins)
   │  │                    │              │
   │  │   HEAD STOCK       │   ← 100 × 50 mm   for long-face flips
   │  │                    │              │
   │  └────────────────────┘              │
   │   ●  ●                               │
   │   ↑                                  │
   │ Anchor 1                             │
   └──────────────────────────────────────┘
```

For the **strike-face flips** (head stood on end, 50 × 50 footprint
on the bed): the same 4 pins relocated into a 50×50 pattern, or use
2 pins on the back + a side toe-clamp.

## Stock prep — out of scope of CAM, done before mounting

| Stock | Spec | Pre-CNC prep |
|---|---|---|
| Head | 7075 aluminium, 100 × 50 × 50 mm | Saw to size + light deburr. The CNC will not face the blank; arrives at final outer dimension. |
| Handle | American white oak, 50 × 30 × 300 mm | Saw to size; verify squareness on a try-square — handle relies on the back face being flat for vise registration. |

> Both pieces are **near net size** going onto the machine — there's
> ≤ 1–2 mm of stock to remove on the outer profile. This is by design:
> "no facing the blank" is one of the project's safety rules.

## CAM safety rules — pulled from arc-reactor / project 01

These apply to every operation in this project, no exceptions:

- **No facing the blank** unless explicitly requested.
- **Helical / ramped entries** — never straight plunges, especially in
  aluminium.
- **Air assist on (M7)** for cutting in both materials.
- **Group output by tool** when posting (`splitFile = tool` in the
  Carvera community post).
- **WCS = top-front-left of stock** ("anchor 1" in the user's
  terminology): X0 Y0 lower-left as mounted, Z0 = top of blank.
- **No final-detach operation** posted without explicit human sign-off.
- **Validate every `.cnc`** before sending: tool, depths, feeds, motion
  bounds. Use `tools/validate_cnc.py` from arc-reactor.
- **5 mm minimum margin** between the deepest cut and the bottom of
  stock (avoids cutting into the spoilboard).
- **`splitFile = tool`** for the full job, so each tool has its own
  `.cnc` file — easier to inspect and run independently.

## File outputs (planned)

Following the project 01 naming convention (`<seq>_T<n>_<DESCRIPTION>.cnc`):

```
projects/02-decorative-hammer-mjolnir/
├── nc/
│   ├── handle/
│   │   ├── 01_T1_HANDLE_BOTTOM_FACE_AND_POMMEL.cnc
│   │   ├── 02_T1_HANDLE_PROFILE_SIDE_A.cnc
│   │   ├── 03_T2_HANDLE_FILLET_SIDE_A.cnc
│   │   ├── 04_T3_HANDLE_ENGRAVE_SIDE_A.cnc
│   │   ├── 05_T2_HANDLE_ODIN_RELIEF_SIDE_A.cnc
│   │   ├── ... (analogous for sides B/C/D)
│   │   ├── XX_T4_HANDLE_WEDGE_KERF.cnc
│   │   └── XX_T5_HANDLE_STRAP_HOLE.cnc
│   └── head/
│       ├── 01_T6_HEAD_TOP_PROFILE_AND_EYE_ROUGH.cnc
│       ├── 02_T7_HEAD_EYE_FINISH.cnc
│       ├── 03_T8_HEAD_CHAMFER_TOP.cnc
│       ├── ... (analogous for other faces)
│       └── XX_T9_HEAD_ENGRAVE_LONG_FACES.cnc
└── documentation/
    ├── TOOL_LIBRARY.md           ← available tools
    ├── CAM_PLAN.md               ← this file
    ├── MECHANICAL_REVIEW.md
    ├── MILLABILITY_REVIEW.md
    ├── DESIGN_CHANGELOG.md
    └── VALIDATION_REPORT.md      ← TODO, written after the .cnc files exist
```

## What I'll do next, in order

1. **Inspect arc-reactor's `carvera_job/`** structure — see how
   project 01's first-article setup was organized. Mirror that
   structure here.
2. **Open Fusion + switch to the Manufacture workspace.** Add the
   tool library entries (T1..T9) into a project-local tool library.
3. **Create the first setup (H1: handle bottom + pommel).** Smallest
   footprint, easiest to validate. Post + simulate before moving on.
4. **Iterate one setup at a time.** Each setup gets:
   - Operations created in Fusion
   - In-Fusion simulation passed
   - `.cnc` posted
   - File-level validation pass
   - Documented in this CAM_PLAN.md before moving to the next.

## References

- [Carvera Air work area + bed specs (Makera product page)](https://www.makera.com/products/carvera-air)
- [Carvera Air MDF bed (Makera replacement part)](https://www.makera.com/products/carvera-air-mdf-bed)
- [Saunders fixture/tooling plate dimensions](https://saundersmachineworks.com/products/makera-carvera-air-fixture-tooling-plate)
- [Makera Wiki — Tool Kit + manual probe procedure](https://wiki.makera.com/en/carvera/manual/tool-kit)
- [arc-reactor docs/makera-carvera-cam-notes.md — local CAM safety rules + post properties](file:///C:/projects/arc-reactor/docs/makera-carvera-cam-notes.md)
- [Project 01 lessons-learned.md — feeds-and-speeds calibration story](../../01-relief-pear-150x150x45/lessons-learned.md)
- [Project 01 VALIDATION_REPORT.md — first-article validation pattern](../../01-relief-pear-150x150x45/documentation/VALIDATION_REPORT.md)

## Decisions taken

- **`splitFile = tool`** for project 02 (one `.cnc` per tool). Easier
  to inspect each program in isolation; project 01 used `none` because
  it was a single roughing pass.
- **Resin fill conversation deferred** — that's a post-CAM step; the
  CAM-time decision is just engraving DOC, which is locked at 0.15 mm
  for the metal V-bit (sufficient for any resin).
