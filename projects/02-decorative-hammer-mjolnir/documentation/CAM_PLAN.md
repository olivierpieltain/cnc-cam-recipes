# CAM Plan — project 02

> **Status: in design.** This document is the planning step before any
> Fusion CAM operations exist. The plan is reviewed first; only then
> do we start clicking in Fusion. Updated as decisions are taken.

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

5 setups (4 long-face flips + 1 bottom + top decorations are merged
into one of the long-face flips since the wedge kerf and the bust are
on different faces):

| # | Setup | Tools | What it does |
|---|---|---|---|
| H1 | Bottom + side reference | T1 | Face the bottom of the stock to a clean Z=0 reference, mill the R5 pommel curve, mill one long-side flat to indexing. Optionally drill the strap hole pilot from one side. |
| H2 | Side A (+Y face up) | T1, T2, T3 | Outer profile contour 28×33 → 25×22 with shoulder at Z=190. R6 long-edge fillets (T2 ball). HAMMER OF OLIVIER engraving on this side (T3 V-bit). 3 small medallions (T3). 3D adaptive + ball-nose finish on the Odin bust panel. |
| H3 | Side B (-Y face up) | T1, T2, T3 | Mirror of H2. |
| H4 | Side C (+X face up) | T1, T2, T3, T4 | Profile contour from this side. HAMMER OF OLIVIER engraving on the +X face. Wedge kerf at top of tenon (T4 1.5 mm flat to final dimension). |
| H5 | Side D (-X face up) | T1, T2, T3 | Mirror of H4 minus the kerf (already done in H4). |

The strap hole (Ø6) is drilled in two passes — Ø3 starter from each
side (T5 drill), then bore out to Ø6 with the 1.5 mm flat in helical
mode in one of the side flips.

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

### Handle (oak, 300 mm long stock)

- **Mounted vertically — long axis along the bed's Y axis**, with the
  bottom 30 mm of stock clamped in the Carvera vise jaws (which sit
  against Anchor 1).
- The vise jaws give a flat reference plane; the stock's back face
  registers against the Ø4 mm pins at Anchor 1, and a parallel block
  along the side gives the X-axis register.
- **Free length above the vise: 270 mm.** Plenty of clearance for the
  spindle to reach the part's full Z range.
- **Indexed flip** rotates the part 90° around its long axis between
  setups (4 long-face flips). Re-probe Z0 each time. X/Y origin
  preserved by the vise + pin reference.

```
                    +Z (machine)
                     │
   bed surface   ┌───┴───┐  ← part top (free end, Z=240 of part)
        ┌────────┤       │
        │        │       │
        │ vise   │ part  │
        │ jaws   │       │
        │        │       │
        └────────┤       │
                 │       │  ← part Z=30 of part
                 └───────┘  ← bottom of stock (Z=0 of part = WCS Z=stock_top)
                  ↑        ↑
                Anchor 1  pin registers
                pin       (back face of stock)
```

WCS origin per setup: X = pin-distance, Y = vise-jaw-front-edge,
Z = top of part (re-probed). The 60 mm fixturing tab below Z=0 of the
part is **inside the vise**, machined off after the part is finished.

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
