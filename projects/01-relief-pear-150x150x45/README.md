# 01 — Relief in pear, 150 × 150 × 45 mm

Three-slab adaptive roughing of a 3D relief into a small pear blank,
followed by horizontal flat-floor rework, a Ø3.175 ball-nose main 3D
finish, and a Ø2.0 ball-nose detail rest pass. Optional V-bit pencil
pass after that for the crispest valleys.

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
| **T4** *(optional)* | V-bit / engraving | 60° × 0.1 mm tip (or 30° × 0.2 mm) | pencil pass | engraving bit set, 1/8" shank |

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
- **V-bit (optional)** — 60° × 0.1 mm is the default for pencil; switch
  to 30° × 0.2 mm only if your relief has very tight internal corners
  (more fragile tip, but reaches sharper angles).

## Operation order

| # | Op | Strategy | Tool | Recipe | Role |
|---|---|---|---|---|---|
| 01A | `01A_…_ROUGHING_…_SLAB_1_Z0_TO_Z-12` | adaptive | T1 | [`pear-3175-flat-roughing-adaptive`](../../recipes/pear-3175-flat-roughing-adaptive.json) | rough top slab, leave 0.5 mm |
| 01B | `01B_…_ROUGHING_…_SLAB_2_REST_Z-12_TO_Z-24` | adaptive (rest) | T1 | same | middle slab |
| 01C | `01C_…_ROUGHING_…_SLAB_3_REST_Z-24_TO_Z-35` | adaptive (rest) | T1 | same | bottom slab |
| 02 | `02_…_FLAT_FLOOR_REWORK_…` | horizontal | T1 | (defaults) | clean flats left by 1.5 mm stepdown |
| 03 | `03_…_RELIEF_FINISH_BALL_3175x22_…` | parallel | **T2** | [`pear-3175-ball-finishing-main`](../../recipes/pear-3175-ball-finishing-main.json) | main 3D finish |
| 04 | `04_…_RELIEF_DETAIL_REST_BALL_2x17` (Ø2 × **12**) | parallel + rest | **T3** | [`pear-2mm-ball-finishing-detail-rest`](../../recipes/pear-2mm-ball-finishing-detail-rest.json) | clean what T2 couldn't reach |
| 05 *(optional)* | `05_…_PENCIL_VBIT_…` | pencil | **T4** (V-bit) | (manual setup) | sharpen valleys |

> Op 05 isn't created by the API in this project — it's left to add via
> the Fusion UI once you've decided on V-bit angle. See *Adding the
> pencil pass* below.

## How to adapt this to your machine

### Tool numbers

The Fusion file already uses **T1 / T2 / T3** as four physically
different tools. If your changer's slots are different, walk through
each operation and edit the tool's `tool_number` to match. Verify by
posting and grepping the output:

```bash
grep -n "M6 T" path/to/output.cnc
```

You should see **three** distinct tool numbers across the whole job.

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

### Adding the pencil pass (op 05)

In Fusion:

1. Manufacture browser → right-click setup → New 3D Operation → Pencil.
2. Tool: select your V-bit (60° × 0.1 mm tip recommended; 30° × 0.2 mm
   for tighter internal angles).
3. Geometry: leave model selection auto.
4. Stepover / depth: ~0.05 mm depth-of-engagement.
5. (Optional) run [`tools/apply_recipe.py`](../../tools/apply_recipe.py)
   on the new op with a recipe of your choice.

## Hard constraints

- **Z lowest cut:** −35 mm. Validator: `--max-depth 35`. Below −35 cuts
  into the intentional 5 mm of stock backing.
- **XY excursion:** within roughly `0,0` → `150,150` ± tool radius
  (~1.6 mm). Adaptive deliberately overshoots the stock outline by a
  tool-radius at boundaries. Mount with ≥ 5 mm clearance on every side.
- **T1 flute length:** 42 mm. Max engaged depth must be ≤ 42 mm — easily
  satisfied with our 12 mm slab depths.
- **T2 reach:** 22 mm flute on a 1/8" shank. Reaches 22 mm into the
  relief; deeper background is the roughing leftover (acceptable —
  relief background is usually flat).
- **T3 reach:** 12 mm flute. **Picked deliberately for stiffness.**
  Don't switch to the 17 mm version unless you've verified your
  machine doesn't chatter on it — broken Ø2 mm bits are easy.
- **Stock backing:** ≥ 5 mm under deepest cut. Our 45 mm blank with
  Z = −35 cut leaves 10 mm — comfortable.
- **Air assist:** `M7` on (the Carvera post enables this automatically).
  Roughing pear without air packs the kerf and stalls.

## Validation

After posting each op:

```bash
python tools/validate_cnc.py nc/01_T1_ROUGHING_3175x42.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/03_T2_FINISH_BALL_3175x22.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
python tools/validate_cnc.py nc/04_T3_DETAIL_REST_BALL_2x17.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
```

Each should print `=== PASS ===`. Tools should be **only T1**, **only
T2**, **only T3** respectively.

## Lessons learned

See [`lessons-learned.md`](lessons-learned.md) — including the
adaptive-vs-mesh slowness, Fusion's stale CAM stock cache, the Fusion
API `push_back` trap, and what `setup.operations.item(0)` actually means.
