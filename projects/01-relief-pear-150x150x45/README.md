# 01 — Relief in pear, 150 × 150 × 45 mm

Three-slab adaptive roughing of a 3D relief into a small pear blank, with
horizontal flat-floor rework and a parallel ball-nose finish to follow.

This is the project that produced the recipe in
[`recipes/pear-3175-flat-roughing-adaptive.json`](../../recipes/pear-3175-flat-roughing-adaptive.json).

## What this project does

The design imports a relief mesh (STL, ~146 × 146 × 35 mm) sitting at the
top of a 150 × 150 × 45 mm pear blank. The CAM tree is:

1. **Roughing** — adaptive, 3 slabs (Z 0 → −12, −12 → −24, −24 → −35).
   Bulk-removes everything outside the relief in three depth passes,
   leaves 0.5 mm everywhere.
2. **Flat floor rework** — horizontal strategy, 0.1 mm tolerance, picks
   up the flat horizontal areas left by adaptive's 1.5 mm stepdown.
3. **3D finish** — parallel scallop with a Ø3.175 ball-nose, 0.25 mm
   stepover, cuts to model.

The roughing leaves 5 mm of stock under the deepest cut as backing — the
blank doesn't get cut through.

## What I used

- **Machine:** Makera Carvera Air, stock 200 W spindle, 15 000 RPM ceiling,
  ~360 × 240 × 140 mm work envelope, 4-slot ATC.
- **Stock:** 150 × 150 × **45 mm** pear, **both faces pre-surfaced** down
  from a 50 mm raw blank by hand (planer / drum sander) before mounting.
  See *Stock prep* below.
- **Tools:**
  - **T1**: 1/8" (Ø3.175 mm) 2-flute flat spiral O endmill, 42 mm flute,
    60 mm overall length. Used for roughing slabs and flat-floor rework.
  - **T2**: 1/8" (Ø3.175 mm) 2-flute ball-nose endmill, 22 mm flute,
    38 mm overall length. Used for parallel finishing only.

  > Note on tool numbers: in the original Fusion document both tools were
  > assigned `T1` (a leftover from copy-paste). On a machine with ATC this
  > is a real problem — the post will emit `M6 T1` for both and the
  > controller won't change tools. Fix tool numbers per op before you
  > post any program that includes both tools.

- **Hold-down:** vise on the front-left of the bed, jaws flush with the
  blank's front edge.
- **WCS:** anchor 1 — X0 Y0 = front-left top corner of the blank;
  Z0 = top face of the blank.
- **Post processor:**
  [`Carvera.cps`](https://github.com/MakeraInc/CarveraProfiles) — Makera
  Carvera Community Post v1.4.3. Output extension `.cnc`.

## Stock prep (before mounting)

The recipes in this repo assume the blank is already squared up:

1. Start from a 150 × 150 × **50 mm** rough pear blank.
2. **Hand-face both 150 × 150 faces down to 45 mm** with a thickness
   planer or drum sander. Even thickness end-to-end, parallel faces.
3. Square the side edges if needed.
4. Mount in vise.

We surface by hand outside the machine because the Carvera Air's 1/8"
tool (the only flat we used) takes ~70 minutes to surface 150 × 150 ×
2.5 mm — not a good use of machine time when you have a planer on the
bench. If you don't have one, see *Adapting: surfacing on the machine*
below.

## Operation order

| # | Op name | Strategy | Tool | Recipe |
|---|---|---|---|---|
| 01A | `01A_ANCHOR1_ROUGHING_LONG_3175x42_SLAB_1_Z0_TO_Z-12` | adaptive | T1 | [`cam/recipe-roughing.json`](cam/recipe-roughing.json) |
| 01B | `01B_ANCHOR1_ROUGHING_LONG_3175x42_SLAB_2_REST_Z-12_TO_Z-24` | adaptive (rest) | T1 | same |
| 01C | `01C_ANCHOR1_ROUGHING_LONG_3175x42_SLAB_3_REST_Z-24_TO_Z-35` | adaptive (rest) | T1 | same |
| 02 | `02_ANCHOR1_FLAT_FLOOR_REWORK_LONG_3175x42` | horizontal | T1 | (uses operation-default values) |
| 03 | `03_ANCHOR1_RELIEF_FINISH_BALL_3175x22_VERIFY_EXIT` | parallel | T2 | (uses operation-default values) |

## How to adapt this to your machine

Things that almost always need changing:

### Tool numbers

If your tool changer's slots differ, walk through every operation in the
Fusion file's CAM tree and edit the tool number on each. Verify by
posting and grepping for `M6 T`:

```bash
grep -n "M6 T" path/to/output.cnc
```

You should see one line per physical tool change.

### Stock dimensions

If your blank isn't 150 × 150 × 45:

1. Open `design/*.f3d` in Fusion.
2. Find the body named `STOCK_*` in the design tree. Resize it (edit a
   sketch, or use Move/Press-Pull).
3. The CAM setup uses `job_stockMode = 'solid'` and reads the body
   directly — toolpaths follow the new bounds when you regenerate.

### Feeds / RPM

Recipe values are tuned for ~200 W spindle. On a more rigid machine with
500 W+ you can roughly **double the radial WOC** (`optimalLoad`) and
maintain the same cycle time at higher MRR; or keep WOC and increase
feed. See [`docs/feeds-and-speeds.md`](../../docs/feeds-and-speeds.md)
for the math.

### Post processor

Replace the post in Fusion's setup post-process step with the post for
your machine. The Fusion design itself has no post-specific data.

### Adapting: surfacing on the machine

If you can't pre-face the blank, add two surfacing operations to the
front of the CAM tree before roughing:

| # | Strategy | Top → Bottom | Notes |
|---|---|---|---|
| 00A | adaptive | 0 → −2.5 mm | `optimalLoad` 0.6, `maximumStepdown` 2.5, `useStockToLeave` false |
| 00B | adaptive | −2.5 → −5 mm | same params as 00A |

Touch off Z=0 at the **top of the 50 mm raw blank** and *all* operations
shift down by 5 mm:

- Roughing: 0/−12/−24/−35 → −5/−17/−29/−40
- Adjust the relief mesh's Z position by −5 mm in the design tree

A larger surfacing tool (Ø6 mm flat or face mill) is far faster than a
1/8" flat for this — if you have one, use it for the surfacing ops only.

## Hard constraints

- **Z lowest cut:** −35 mm. Validator: `--max-depth 35`. Below −35 means
  cutting into the 5 mm of intentional backing.
- **XY excursion:** within roughly `0,0` → `150,150` ± tool radius
  (~1.6 mm). Adaptive deliberately overshoots the stock outline by a
  tool-radius at boundaries. Check posted `.cnc` with
  `--bounds 0,0,150,150`.
- **Tool flute length:** T1 = 42 mm flute → max engaged depth must be
  ≤ 42 mm. We use 12 mm slabs deliberately to keep deflection bounded.
- **Stock backing:** ≥ 5 mm under deepest cut. With 45 mm stock and Z=−35
  cut, backing is 10 mm — comfortable.
- **Air assist:** `M7` on. The Carvera post enables this automatically.
  Roughing pear without air packs the kerf and stalls the spindle.

## Validation

After posting:

```bash
python tools/validate_cnc.py nc/01_T1_ROUGHING_3175x42.cnc \
    --max-depth 35 --bounds 0,0,150,150 --high-feed 3000
```

Expected: PASS. Tools: `[1]`. Z range: `−35.0 .. 15.0`. Feeds: `60, 150,
430`. Spindle: `13000`.

## Lessons learned

See [`lessons-learned.md`](lessons-learned.md) — including some real
gotchas with adaptive on mesh bodies, Fusion's stale CAM stock cache,
and a Fusion API trap that costs you an hour the first time you hit it.

## License / attribution

The CAM setup, recipes, and all written content in this folder are MIT.
The relief mesh artwork itself is **not** redistributed in this repo —
substitute your own STL of comparable size (~146 × 146 × 35 mm).
