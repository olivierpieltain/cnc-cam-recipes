# Sylvan Dragoness — Run Instructions

Posted G-code for the relief in pear, 150 × 150 × 45 mm blank,
mounted at the front-left of the Carvera Air bed (anchor 1 = X0 Y0 at
the front-left corner of the blank, Z0 at the top of the blank).

> **Stock prep is hand-done before mounting**: 50 mm raw pear blank
> faced down to 45 mm on a planer, both 150 × 150 faces parallel.

## Run order — seven files, one tool slot per file

Each roughing slab is its own file so you can stop, inspect, and
resume between Z-layers if you want. All four T1 files at the start
use the same bit (no tool change between them); files 5–6 require
swaps; file 7 returns to T1 for the final perimeter trim.

| # | File | Tool | Z range | Notes |
|---|---|---|---|---|
| 1 | `01A_T1_ROUGHING_SLAB_1_Z0_TO_Z-12.cnc`         | **T1** Ø3.175 spiral O, 42 mm flute   | 0 → −12 mm    | top slab — bulk material removal |
| 2 | `01B_T1_ROUGHING_SLAB_2_REST_Z-12_TO_Z-24.cnc`  | **T1** (no change)                    | −12 → −24 mm  | middle slab, rest machining off slab 1 |
| 3 | `01C_T1_ROUGHING_SLAB_3_REST_Z-24_TO_Z-35.cnc`  | **T1** (no change)                    | −24 → −35 mm  | bottom slab, rest machining off slab 2 |
| 4 | `02_T1_FLAT_FLOOR_REWORK_3175x42.cnc`           | **T1** (no change)                    | 0 → −29.9 mm  | cleans the 1.5 mm steps left by slabs |
| 5 | `03_T2_FINISH_BALL_3175x22.cnc`                 | **T2** Ø3.175 ball nose, 22 mm flute  | 0 → −31.5 mm  | main 3D finish |
| 6 | `04_T3_DETAIL_REST_BALL_2x17.cnc`               | **T3** Ø2.0 × 17 mm flute ball nose    | 0 → −31.5 mm  | detail rest pass on what T2 couldn't reach. **Cross-hatched at 90° from op 03** — passes run along Y while op 03 ran along X, so each pass cleans what the other smeared (`useRestMachining=true`, source = file 5). |
| 7 | `06_T1_CONTOUR_TRIM_PERIMETER.cnc`              | **T1** (back) Ø3.175 spiral O, 42 mm flute | −35 → −40.3 mm | final perimeter trim — frees the 146 × 146 part from the 2 mm stock border. **Requires sacrificial spoilboard + heavy double-sided tape** (no fixturing). |

> **Note on the missing file numbered 05:** the Fusion CAM tree contains
> a planned op 05 (V-bit pencil pass with 60° × 0.1 mm tip) but it is
> currently **suppressed** — the relief STL has 1.46 million triangles,
> which is far past Fusion's pencil-strategy edge-filter feasibility
> threshold. Generation hangs without producing a toolpath. To run op 05
> you would first need to decimate the mesh (Mesh workspace → Modify →
> Reduce, target ~100k triangles) or convert it to a Faceted BRep, then
> regenerate op 05 and post a `05_T4_PENCIL_VBIT_60deg.cnc` file. The
> cross-hatch direction on op 04 (file 6 above) compensates for most of
> what pencil would have added — see project README for the why.

## Setup before file 1 (one-time)

1. **Mount the blank** in the vise, front-left of the bed, jaws flush
   with the front edge of the blank.
2. **Set X = 0, Y = 0** at the front-left corner of the **physical
   blank**. Not at the relief edge inside it (the relief is inset 2 mm,
   ignore that — zero on the actual board edge).
3. **Probe Z = 0** on the **top surface of the blank** with the Carvera
   Air probe routine.
   - If your probe routine uses the **stock-thickness setting** to
     compute Z, **set it to 45 mm** (NOT 50 mm — that was the raw blank
     before facing).
   - Easiest: use the routine that probes the actual top of the wood
     directly so stock thickness doesn't matter.
4. **Air assist on** (`M7` is in the file, but verify your air supply
   is open and the line is connected).

## Between files — DO NOT re-zero the workpiece

You're keeping the **same X / Y / Z workpiece zero across all eight
files** (with one exception: before file 8 you'll switch fixturing —
see *Re-fixturing before file 8* below). Tool changes happen at files
5, 6, 7, and 8.

After each file finishes:

1. Carvera returns to home and stops the spindle (the post writes
   `M5 / M400 / M852 / G28 / M30` at the end).
2. **(Optional) inspect** the work — between roughing slabs is a great
   time to vacuum chips, look for any unexpected steps, and confirm
   the cuts match the simulation.
3. **Change the tool** if the next file uses a different one:
   - Files 1 → 2 → 3 → 4: same T1, no change
   - File 4 → 5: T1 → **T2** (Ø3.175 ball)
   - File 5 → 6: T2 → **T3** (Ø2.0 ball)
   - File 6 → 7: T3 → **T1** back (Ø3.175 spiral O 42 mm flute)
4. After a tool change, **re-probe TOOL LENGTH only** — the Carvera
   auto-routine handles this. **Do NOT re-touch the workpiece Z** — the
   workpiece zero is unchanged.
5. Load the next file and run.

## Re-fixturing before file 8 (perimeter trim)

File 8 cuts a trench around the entire 146 × 146 silhouette of the
relief, going through the full stock thickness into a sacrificial
spoilboard. **Anchor pins / vise jaws would be in the toolpath**, so
fixturing must change for this final op.

1. **Pause after file 7 finishes.** Vacuum thoroughly.
2. **Lift the part off the anchor pins** carefully — the relief is
   already finished and visible.
3. **Place a sacrificial spoilboard** (MDF, scrap pine, or HDPE) on
   the bed where the part will sit. Spoilboard footprint should
   exceed 150 × 150 mm by at least 10 mm on every side.
4. **Apply heavy double-sided tape** to the entire bottom of the
   blank (carpet tape works well — full coverage, not just edges).
5. **Press the part down onto the spoilboard** at the same X / Y
   position it was in before. Front-left corner of the blank against
   X=0, Y=0 (or whatever your anchor-1 origin was). The CAM file
   uses the same WCS — workpiece zero must match.
6. **Re-probe Z = 0** on the top of the wood (it's now sitting on a
   spoilboard so its absolute height changed).
7. **Verify XY** by rapid-jogging the spindle to (75, 75) and
   eyeballing — you should be at the centre of the part.
8. Load file 8 and run.

## Tool slots — the actual bits

These are the same Makera-family bits the project README describes.
Make sure each slot in the changer holds the correct one before you
start file 1.

| Slot | Bit | Description on the box |
|---|---|---|
| **T1** | Ø3.175 single-flute spiral O, **42 mm flute** | yellow-capped tube, "Spiral 'O' Single Flute Bit – 1/8" Shank, 3.175mm × 42mm" |
| **T2** | Ø3.175 2-flute ball nose, **22 mm flute** | "双刃球头铣刀 3.175*22*38" / "Two Flute Ball Nose – 3.175 × 22 mm" |
| **T3** | Ø2.0 2-flute ball nose, **17 mm flute** | "双刃球头铣刀 3.175*2.0-17" — **the 17 mm flute version, not 12 mm** |
| **T4** | Ø3.175 single-flute V-bit, **60° tip, 0.1 mm tip Ø, 8 mm flute** | metal-rated engraving bit, "Single Flute Engraving Metal 60 deg × 0.1 mm" |

> **About T3:** Ø2.0 × **17 mm** flute is the physical bit you own and
> what the Fusion file is configured for. The Makera Carvera library only
> ships a 12 mm flute Ø2 ball, but the boxed Makera kit's only Ø2 *ball*
> is the 17 mm version (the 12 mm Ø2 in your kit is a **flat** endmill,
> in the 2-flute flat-endmill set `双刃平头铣刀套装`). The Fusion T3
> tool was edited to flute = 17 mm so this matches your reality. The
> recipe (`recipe-finishing-detail-rest.json`) was originally tuned for
> the stiffer 12 mm flute, so expect slightly more deflection than the
> recipe nominally allows — scale the Carvera feed override down if it
> chatters. Broken Ø2 mm bits are easy, so be conservative on entry the
> first time.

> **About T4:** Same metal-rated 60° V-bit used in project 02 for
> aluminium engravings. Coating is over-spec on wood but doesn't hurt.
> 0.1 mm tip is fragile — don't push the feed override.

## What's left on the part between operations

| After file | What's left on the model |
|---|---|
| 1 (slab 1) | top 12 mm of the relief is roughed, 0.5 mm offset everywhere |
| 2 (slab 2) | middle 12 mm roughed, 0.5 mm offset |
| 3 (slab 3) | bottom roughed, 0.5 mm offset everywhere |
| 4 (flat-floor rework) | 0.1 mm on flats, 0.5 mm everywhere else |
| 5 (main 3D finish) | ~0 mm except where the Ø3.175 ball couldn't reach corners |
| 6 (detail rest) | ~0 mm everywhere within reach of the Ø2.0 ball, 17 mm deep |
| 7 (V-bit pencil) | inside-corner fillets removed, scale-edge / wing-line / eye-detail shadows defined |
| 8 (perimeter trim) | part freed from surrounding stock — final 146 × 146 piece with relief on top + 5 mm flat backing below; four 2 mm × 5 mm × 150 mm strips fall off (or stay stuck to the spoilboard tape, peel them off after) |

## If the bit looks too high or off in XY at the start of a file

- **Z too high** → check your Carvera workpiece-thickness setting. If
  it says 50 mm, change to 45 mm and re-probe Z.
- **XY off by ~2 mm** → you may have zeroed at the relief corner
  (mesh inset 2 mm) instead of the physical blank corner. Re-zero on
  the actual blank corner.

## After the CNC: sanding + finish

The off-the-machine surface from the Ø2 ball-nose finish is very smooth
but has machining "fuzzies" — fibres laid over rather than cleanly
sliced. A few hours of light handwork transforms the result.

**Quick version:**
1. **Vacuum / blow off** dust thoroughly.
2. **Brass-bristle brush** over the relief to knock off standing fuzz.
3. **Sand 220 → damp surface lightly → let dry → sand 220 again →
   320 → 400.** Foam sanding sponges for the relief, folded paper for
   flats. **Light pressure** — the abrasive does the work; pressing
   harder rounds off the dragon's fine details (eye, snout, scale tips).
   Skip the "raise the grain" damp step and the first oil coat goes
   fuzzy.
4. **Oil finish.** Tung oil or boiled linseed oil, rag-applied,
   wipe excess after 10 min, 24 h between coats, 2–3 coats total.

**For dramatic depth — two-oil contrast finish:**

Apply a darker tinted oil first (e.g., Watco Danish Oil Dark Walnut),
let it pool in the valleys 5 minutes, wipe the high points with a
clean cloth (leaves dark in the recesses), let dry 24 h, then top with
clear oil over everything. Pre-seal pear with a 1-lb-cut shellac wash
first (it's a blotchy wood — without sealing, the dark stain absorbs
unevenly).

> **See the [project README "Finishing the part" section](../README.md#finishing-the-part-after-cnc)
> for the detailed breakdown** — grit choices, tool list, oil pairings,
> and where to be careful with relief detail.

> **Safety:** oil-soaked rags **spontaneously combust** as the oil
> oxidizes. Spread used rags flat on concrete to dry, or submerge in
> water in a sealed metal can before discarding. Never bunch and toss
> in the trash.

## Safety reminders

- **Keep the cover closed** during cuts.
- **Watch the first minute** of every file — most failures show up
  immediately.
- **Air assist on** for all wood cuts.
- **Don't pause-and-resume mid-job** unless you're sure the resume
  point is correct. Restart the file from the beginning if in doubt.
- **For file 7 (V-bit):** if the tool catches on a knot or grain
  reversal, the 0.1 mm tip will snap. Listen for any sudden change in
  cut sound and pause if it doesn't sound right.
- **For file 8 (perimeter trim) WITHOUT fixtures:** keep an eye on
  the four 2 mm strips as they get freed in the final passes. If a
  strip lifts toward the cutter, hit feed-hold immediately. With heavy
  tape coverage this should not happen, but it's the only failure
  mode where the tape is the only thing between you and a flying
  splinter.
