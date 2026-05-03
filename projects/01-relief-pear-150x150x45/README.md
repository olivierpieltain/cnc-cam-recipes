# 01 — Relief in pear, 150 × 150 × 45 mm

Three-slab adaptive roughing of a 3D relief into a small pear blank,
followed by horizontal flat-floor rework, a Ø3.175 ball-nose main 3D
finish, a Ø2.0 ball-nose detail rest pass, a 60° V-bit pencil pass for
the crispest valleys, and a final 2D contour trim around the relief
silhouette to free the part from the stock perimeter.

## Artwork credit

> The relief STL used in this project is **["Sylvan Dragoness — Relief
> Sculpture"](https://makerworld.com/fr/models/2478075-sylvan-dragoness-relief-sculpture)**
> on MakerWorld, model ID `2478075`.
>
> The artwork is **not redistributed in this repo** — please download it
> directly from MakerWorld under the creator's license. To reproduce
> this project with the actual STL: import the downloaded mesh into
> Fusion at the same position the project's `RELIEF_*_STL` body
> currently sits (X[2..148] mm, Y[2..148] mm, Z[0..−35] mm), and
> regenerate.
>
> If you swap in your own relief mesh of comparable size
> (~146 × 146 × 35 mm), the rest of the CAM works as-is.

## Machine

> Tested on a **[Makera Carvera Air](https://www.makera.com/products/carvera-air)** — stock 200 W spindle,
> 15 000 RPM ceiling, ~360 × 240 × 140 mm work envelope, 4-slot ATC.
> Manual tool change behavior in the post is `carvAirMtc` (Stock Air).

If your machine matches or exceeds the Carvera Air's specs, the
toolpaths in this project run as-is. See *How to adapt* below for
larger machines or different post processors.

## Stock prep — done by hand BEFORE mounting

This project assumes the blank arrives at the machine already squared:

1. Start from a **150 × 150 × 50 mm rough pear blank**.
2. **Hand-face both 150 × 150 faces down to 45 mm** with a thickness
   planer or drum sander. Even thickness end-to-end, parallel faces.
3. Square the side edges if needed.
4. Mount in vise, front-left of the bed, jaws flush with the blank's
   front edge.

> Why hand-prep? On a Carvera Air with a 1/8" tool, surfacing
> 150 × 150 × 2.5 mm takes ~70 minutes — bad use of machine time when a
> planer does it in seconds. The "Adapting: surfacing on the machine"
> section below covers what to do if you don't have a planer.

## Tooling

All tools share a 1/8" (3.175 mm) shank — fits the Carvera Air's stock
collet without changes.

| Slot | Tool | Spec | Used in | Source |
|---|---|---|---|---|
| **T1** | Spiral O single-flute (long) | Ø3.175 × **42** mm flute, 60 mm OAL | roughing slabs + flat-floor rework | [Makera 1/8″ Spiral O single-flute](https://www.makera.com/products/spiral-o-single-flute-bit-1-8-shank) (long-flute variant) |
| **T2** | 2-flute ball nose | Ø3.175 × **22** mm flute, 38 mm OAL | main 3D finish | [Makera 1/8″ 2-flute ball nose](https://www.makera.com/products/two-flute-ball-nose-bit-1-8-shank) |
| **T3** | 2-flute ball nose | Ø**2.0** × **12** mm flute, ~38 mm OAL | detail rest finish | same Makera 1/8" 2-flute ball-nose family, smaller cutter (Ø2.0 reduced-shank) |
| **T4** | V-bit / engraving | 60° × 0.1 mm tip, Ø3.175 × 8 mm flute (Makera `Single Flute Engraving Metal 60 deg*.1mm`) | pencil pass | engraving bit set, 1/8" shank |

> Photos of the actual bits used live in [`photos/`](photos/) — the
> "Tool inventory" album below explains which Chinese label means what.

### Why these specific bits

- **T1 long-flute spiral O** — single-flute means each cutting edge has
  the full chip pocket to itself; great chip evacuation in wood, lets
  us cut deeper without packing the kerf. 42 mm flute reaches 35 mm of
  relief depth comfortably.
- **T2 Ø3.175 × 22 mm ball** — the standard "main 3D finish" bit for
  any 1/8"-class CNC. Big enough to cover a lot of area at moderate
  stepover; small enough to follow most relief features.
- **T3 Ø2.0 × 17 mm 2-flute ball nose** — long-flute relative to
  diameter (8.5x), so it deflects under load. We compensate with
  conservative parameters (0.4 mm stepdown, 280 mm/min feed) to keep
  load low on the 200 W spindle and avoid chatter. 17 mm flute reaches
  most of the relief depth comfortably.
- **T4 60° × 0.1 mm V-bit** — pointed tip reaches into inside corners that
  no ball nose can (every ball leaves a fillet of unreached material at
  inside corners — radius = the ball's radius). Pencil strategy follows
  those V-shaped valleys and removes the fillet, defining crisp scale-
  edge / wing-line / eye-detail shadows. Switch to 30° × 0.2 mm only if
  your relief has tighter internal corners (more fragile tip, sharper
  angles reachable).
- **Final contour trim** uses **T1** again — no extra tool — to outline
  the 146 × 146 relief silhouette at full stock depth (Z = 0 → −40.3 mm
  including 0.3 mm into a sacrificial spoilboard) and free the part
  from the surrounding 2 mm border of stock.

## Operation order

| # | Op | Strategy | Tool | Recipe | Role |
|---|---|---|---|---|---|
| 01A | `01A_…_ROUGHING_…_SLAB_1_Z0_TO_Z-12` | adaptive | T1 | [`pear-3175-flat-roughing-adaptive`](../../recipes/pear-3175-flat-roughing-adaptive.json) | rough top slab, leave 0.5 mm |
| 01B | `01B_…_ROUGHING_…_SLAB_2_REST_Z-12_TO_Z-24` | adaptive (rest) | T1 | same | middle slab |
| 01C | `01C_…_ROUGHING_…_SLAB_3_REST_Z-24_TO_Z-35` | adaptive (rest) | T1 | same | bottom slab |
| 02 | `02_…_FLAT_FLOOR_REWORK_…` | horizontal | T1 | (defaults) | clean flats left by 1.5 mm stepdown |
| 03 | `03_…_FINITION_RELIEF_BOULE_3175x22` | parallel | **T2** | [`pear-3175-ball-finishing-main`](../../recipes/pear-3175-ball-finishing-main.json) | main 3D finish |
| 04 | `04_…_FINITION_DETAIL_REPRISE_BOULE_2x17_CROSSHATCH` | parallel + rest, `passAngle=90°` (cross-hatched against op 03) | **T3** Ø2.0 × 17 mm flute | [`pear-2mm-ball-finishing-detail-rest`](../../recipes/pear-2mm-ball-finishing-detail-rest.json) | clean what T2 couldn't reach. Cross-hatch (90° from op 03) catches detail in both directions. |
| 05 | `05_…_FINITION_PENCIL_VBIT_60deg` *(suppressed)* | pencil | **T4** (60° V-bit) | (defaults) | would sharpen inside corners — but **suppressed** in the current Fusion file: the relief STL has 1.46M triangles, well past Fusion's pencil edge-filter feasibility. Decimate the mesh to ~100k tri (Mesh → Reduce) before un-suppressing. |
| 06 | `06_…_CONTOUR_DECOUPE_PERIMETRE_3175x42` | 2D contour | **T1** (back) | (built inline — full-depth outer trim around 146 × 146 silhouette) | free part from 2 mm stock border |

## How to adapt this to your machine

### Tool numbers

The Fusion file uses **T1 / T2 / T3 / T4** as four physically different
tools — T1 (Spiral O 3.175×42 mm) is reused by the roughing slabs, the
flat-floor rework AND the final contour trim, so only three tool changes
happen across the eight files (T1→T2→T3→T4→T1). If your changer's slots
are different, walk through each operation and edit the tool's
`tool_number` to match. Verify by posting and grepping the output:

```bash
grep -n "M6 T" path/to/output.cnc
```

You should see **four** distinct tool numbers across the whole job.

### Stock dimensions

If your blank isn't 150 × 150 × 45:

1. Open `design/*.f3d` in Fusion.
2. Find the body named `STOCK_*` in the design tree. Resize it
   (Move/Press-Pull, or Combine-Join with a slab).
3. The CAM setup uses `job_stockMode = 'solid'` and reads bounds
   directly from the body — toolpaths follow the new bounds when you
   regenerate.

### Feeds / RPM

Recipe values are tuned for Carvera Air-class spindle (200 W). On a
more rigid 500 W+ machine you can roughly **double the radial WOC**
(`optimalLoad`) and maintain the same cycle time at higher MRR. Or
keep WOC and increase feed. See
[`docs/feeds-and-speeds.md`](../../docs/feeds-and-speeds.md).

### Post processor

Replace the post in Fusion's setup post-process step with the post for
your machine. The Fusion design itself has no post-specific data — the
operations are post-agnostic.

### Adapting: surfacing on the machine

If you can't pre-face the blank with a planer, add two surfacing ops to
the front of the CAM tree:

| # | Strategy | Z range | Settings |
|---|---|---|---|
| 00A | adaptive | 0 → −2.5 mm | optimalLoad 0.6, maxStepdown 2.5, useStockToLeave **false** |
| 00B | adaptive | −2.5 → −5 mm | same |

**Touch off Z=0 at the top of the 50 mm raw blank.** All other ops
shift down by 5 mm:

- Roughing tops/bottoms: 0/−12/−24/−35 → −5/−17/−29/−40
- Move the relief mesh body down by −5 mm in the design tree

If you have a Ø6 mm flat or face mill, use it for surfacing only — much
faster than a 1/8" flat for that big a flat area.

### Re-enabling the pencil pass (op 05)

Op 05 is in the CAM tree but **suppressed** because the Sylvan
Dragoness STL is 1.46M triangles — Fusion's pencil edge-filter is
roughly O(n²) on edge count and silently hangs at this density (no
error, no progress). To make pencil viable:

1. **Decimate the mesh.** Mesh workspace → Modify → Reduce. Target
   ~100k triangles. Visual loss is negligible for a relief at this
   resolution. Save before/after.
2. **Or convert to BRep.** Mesh workspace → Convert Mesh → Faceted
   BRep. May fail at this density — back up the mesh body first.
3. **Un-suppress op 05** in the Manufacture browser.
4. **Re-generate.** Should now complete in seconds rather than hang.
5. Re-post → `05_T4_PENCIL_VBIT_60deg.cnc`. Run after file 6 (detail
   rest) and before file 7 (contour trim) — same WCS, only adds a
   tool change at T3 → T4 → T1.

If you want to swap to a different V-bit (e.g., 30° × 0.2 mm for
tighter internal angles), edit op 05's tool before re-generating.

### Why op 04 is cross-hatched

A single parallel-direction finishing pass (e.g., op 03 running
along X) leaves a directional bias — features parallel to X get
smoothed along their length, but features perpendicular to X get
crossed at every step and captured cleanly. Op 04 runs at
`passAngle = 90°` (parallel to Y, perpendicular to op 03's 0°), so
each pass cleans what the other smeared. Visible improvement on
reliefs with mixed-orientation detail — comparable to what pencil
would have added for inside corners, but spread across the whole
surface. Cycle time is unchanged vs a same-direction rest pass.

### About op 06 (perimeter contour trim)

Op 06 is the final operation. It cuts a 2 mm-wide trench around the
146 × 146 relief silhouette from Z = 0 to Z = −40.3 mm — through the
full 40 mm stock plus 0.3 mm into a sacrificial spoilboard. This frees
the relief from the surrounding stock border that adaptive roughing
left in place beneath the relief depth.

**Required for op 06**:
- A sacrificial spoilboard under the part (the bit goes 0.3 mm into it).
- Heavy double-sided tape on the entire bottom of the blank (no
  fixturing — clamps would interfere with the perimeter cut). Tape must
  hold the part AND the four 2 mm × 5 mm × 150 mm strips that get
  freed in the final passes.
- Conservative parameters are already set: 0.75 mm stepdown (8 passes),
  400 mm/min cut feed, 100 mm/min plunge, single-direction climb on the
  air side / conventional on the part side (force pushes outward away
  from part — gentle on tape grip).

## Hard constraints

- **Z lowest cut:** −40.3 mm (op 06 contour trim through full stock +
  0.3 mm into spoilboard). For ops 01–05 the lowest cut is −35 mm
  (relief depth). Validator: `--max-depth 35` for ops 01–05,
  `--max-depth 41` for op 06.
- **XY excursion:** within roughly `0,0` → `150,150` ± tool radius
  (~1.6 mm). Adaptive deliberately overshoots the stock outline by a
  tool-radius at boundaries. Op 06 lead-in/out also goes ~0.5 mm past
  the stock edge in air. Mount with ≥ 5 mm clearance on every side.
- **T1 flute length:** 42 mm. Max engaged depth must be ≤ 42 mm. Op 06
  engages 5.3 mm of cut depth (Z = −35 → −40.3) starting from above
  cleared roughing zone — well within reach.
- **T2 reach:** 22 mm flute on a 1/8" shank. Reaches 22 mm into the
  relief; deeper background is the roughing leftover (acceptable —
  relief background is usually flat).
- **T3 reach:** Ø2.0 × **17 mm** flute is the version the user physically
  owns and what the Fusion file is configured for. The recipe
  ([`pear-2mm-ball-finishing-detail-rest.json`](../../recipes/pear-2mm-ball-finishing-detail-rest.json)) was originally tuned for a
  12 mm flute (stiffer, less deflection), but the Makera library only
  has 12 mm and the boxed kit's only Ø2 ball is the 17 mm version. The
  Fusion T3 tool was re-edited to flute=17 mm to match physical reality.
  Expect slightly more deflection than the recipe nominally allows —
  scale the Carvera feed-override down if it chatters. Broken Ø2 mm bits
  are easy, so be conservative on entry the first time.
- **T4 V-bit fragility:** 0.1 mm tip carbide. Plunge feed kept at
  50 mm/min. Don't override on the machine. A snapped tip can pull
  fibres out of the relief surface.
- **Stock backing for ops 01–05:** ≥ 5 mm under deepest cut. The 40 mm
  blank with Z = −35 deepest cut leaves 5 mm. Op 06 then cuts THROUGH
  this 5 mm — that's intended, the spoilboard is below.
- **Spoilboard for op 06:** must be present under the entire 150 × 150
  footprint. Bit drops to Z = −40.3 = 0.3 mm into the spoilboard.
  Don't run op 06 without a spoilboard.
- **Air assist:** `M7` on (the Carvera post enables this automatically).
  Roughing pear without air packs the kerf and stalls.

## Validation

After posting each op:

```bash
# Roughing slabs + flat-floor (T1 only, max-depth 35)
python tools/validate_cnc.py nc/01A_T1_ROUGHING_SLAB_1_Z0_TO_Z-12.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/01B_T1_ROUGHING_SLAB_2_REST_Z-12_TO_Z-24.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/01C_T1_ROUGHING_SLAB_3_REST_Z-24_TO_Z-35.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/02_T1_FLAT_FLOOR_REWORK_3175x42.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
# Finishing passes
python tools/validate_cnc.py nc/03_T2_FINISH_BALL_3175x22.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/04_T3_DETAIL_REST_BALL_2x17.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
# (op 05 V-bit pencil is suppressed — see "Re-enabling the pencil pass" above)
# Final perimeter trim — deeper limit, T1 returns
python tools/validate_cnc.py nc/06_T1_CONTOUR_TRIM_PERIMETER.cnc \
    --max-depth 41 --bounds 0,0,150,150 --high-feed 3000
```

Each should print `=== PASS ===`. Tools should be **only T1** for
01A/B/C/02/06, **only T2** for 03, **only T3** for 04.

## Finishing the part (after CNC)

The off-the-machine surface from a Ø2 ball-nose finish in pear is very
smooth (sub-µm scallop, finer than the wood grain) but it has machining
"fuzzies" — fibres that the cutter laid over instead of cleanly slicing.
A few hours of light handwork transforms the result from "carved wood"
to "finished sculpture."

### Step 1: Initial cleanup

1. **Blow off / vacuum** all chips and dust from the relief, especially
   the deep valleys. Compressed air from a few inches away works well.
2. **Stiff brass-bristle brush** (or a brass detail brush) — gently
   work over the entire relief. Knocks off the standing fuzz fibres.
   Brass is soft enough not to scratch pear; steel wool would be too
   harsh and leaves iron specks that react with future oil finish.

### Step 2: Sanding

**Grit progression — don't skip grits:**

| Grit | What it does | Time on this relief |
|---|---|---|
| 220 | Removes mill marks, scallops, remaining fuzzies. ~80% of the work. | ~30 min |
| 320 | Smooths the 220 scratch pattern. ~15%. | ~15 min |
| 400 | Final polish before finish. ~5%. | ~10 min |

You can stop at 400 for an oil finish; going to 600+ is overkill on
oil-finished hardwood and can actually *reduce* oil absorption.

**Tools (in order of use):**

- **Foam sanding sponges** (the angled-corner kind from any hardware
  store, ~3M Pro Grade or Norton equivalent) — primary tool for the
  3D surface. They conform to curves. Get fine + extra-fine
  (≈220 / 320 grit equivalent).
- **Folded sandpaper** (1/4 sheet folded into thirds) — for the flat
  146 × 146 backing edges and the perimeter band from the contour cut.
- **Sanding cord** or **strips wrapped on a thin dowel** — for tight
  valleys (scale shadows, eye outlines, mouth detail).
- **Optional: rotary tool** with a soft felt buffing tip + 320-grit
  paste — for very fine detail in deep crevices.

**Technique — light pressure is critical:**

- Let the abrasive do the work; don't press. Pressing harder rounds
  off relief detail (especially the dragon's high points: eye, snout,
  scale tips).
- Keep strokes consistent direction (along grain when possible) and
  *don't dwell* in one spot — even passes give an even surface.
- **Vacuum / blow off dust between grits.** Stray 220 grit on a 320
  pass leaves 220 scratches.
- **Inside corners — be gentle.** The Ø2 ball's natural 1 mm fillet
  at corners disappears under oil finish; trying to sand them sharper
  usually rounds the relief itself instead.

**Where to be lightest:**
- High points (eye, snout, scale tips, claw tips)
- Inside corners and the silhouette boundary
- Anywhere you see crisp detail — easy to lose

**Where you can press a bit firmer:**
- The flat 5 mm backing perimeter (no detail to lose)
- The cut edges from the perimeter trim — slight rounding looks
  intentional and nicer than a sharp edge that'll splinter

### Step 3: Raise-the-grain trick (recommended on pear)

After the 220 pass:

1. **Lightly damp** the surface with a wet (not soaked) cloth.
2. **Let dry fully** — 1 hour, or until the wood feels at room
   temperature again.
3. **Re-sand at 220** — kills the fibres the water raised. They won't
   come back when oil is applied.

Skip this and the first oil coat will go fuzzy as the oil swells the
remaining standing fibres. Do this once, and the surface stays smooth
under any finish.

### Step 4: Oil finish — basic clear

Pear takes oil beautifully. The simplest, most forgiving finish:

1. **Pure tung oil** or **boiled linseed oil** (BLO) or **wipe-on
   poly** — choose one. Tung is most natural-looking; BLO ambers
   (yellows) the wood slightly; wipe-on poly is most durable.
2. **Apply with a lint-free rag.** Liberally — flood the surface, let
   it sit 10 minutes, **then wipe off all excess** with a clean rag.
3. **Wait 24 hours** for cure between coats.
4. **Lightly buff** between coats with 0000 steel wool or a grey
   Scotch-Brite pad. Then dust off.
5. **2–3 coats** is usually enough. Stop when the wood looks
   satisfied (no more absorption, surface has a soft sheen).

> **Safety:** oil-soaked rags **spontaneously combust** as the oil
> oxidizes. Spread used rags flat on concrete to dry, or submerge in
> water in a sealed metal can before discarding. Never bunch up and
> toss in trash.

### Step 5 (optional): Two-oil contrast — accentuate the deep relief

To make the dragon "pop" — darker valleys, lighter high points,
giving the relief much more visual depth than uniform color:

**The technique** (sometimes called *highlighting* or *antiquing*):

1. **Pre-seal with thinned shellac.** Pear is a *blotchy* wood — it
   absorbs stain unevenly. A 1-lb-cut shellac wash (1 part shellac,
   4 parts denatured alcohol) wiped on first creates an even
   absorption surface. Let dry 1 hour, lightly scuff with 400 grit,
   dust off.
2. **Dark oil first.** Apply a tinted dark oil — *Watco Danish Oil
   Dark Walnut*, or *General Finishes Java*, or a dye-based option
   like *Mohawk Light Walnut Penetrating Stain*. Brush or rag-apply
   liberally; **let it pool in the valleys for 5 minutes.**
3. **Wipe the high points before it dries.** Use a *clean folded
   cloth* — drag it across the high points only, leaving the dark
   color in the recesses. Pressure controls the effect: lighter
   wipe = subtle highlighting; firmer wipe = strong contrast.
4. **Let dry 24 hours.**
5. **Top with clear oil over everything.** Tung or natural Danish
   oil, applied as in Step 4 above. This unifies the finish and
   protects the dark color in the recesses.
6. **Optional 2nd dark coat** if you want even darker valleys —
   repeat steps 2–4 before the final clear coat.

**Two-oil pairing recommendations** (common, beginner-friendly):

| Effect | Dark coat | Clear top |
|---|---|---|
| Subtle aged warmth | Watco Danish Oil — Medium Walnut | Watco Danish Oil — Natural |
| Strong dramatic depth | Watco Danish Oil — Dark Walnut | Pure tung oil |
| Almost-black valleys | General Finishes — Java gel stain (very thin coat, wipe quickly) | Wipe-on satin poly |
| Warm honey glow | Watco — Medium Walnut | Boiled linseed oil |

**Tips for relief specifically:**

- **Don't oversaturate.** A thin pooling is enough — too much dark
  oil migrates into the wood far past the valley bottoms and looks
  muddy.
- **Test on a scrap.** Cut a small piece of the same blank or use a
  hidden corner of the perimeter; try the technique there first.
- **The wipe-off is the most important step.** Dark oil left on high
  points reads as muddy, not contrasty. Wipe firmly enough to expose
  the lighter wood under the high spots.
- **Don't press with the wipe.** Drag flat — the goal is to remove
  surface oil, not to push it deeper into the wood.

After the final oil cures (a week for full hardness), a single coat of
**paste wax** (clear or tinted) buffed out gives a final hand-rubbed
sheen and adds tactile smoothness.

## Lessons learned

See [`lessons-learned.md`](lessons-learned.md) — including the
adaptive-vs-mesh slowness, Fusion's stale CAM stock cache, the Fusion
API `push_back` trap, and what `setup.operations.item(0)` actually means.
