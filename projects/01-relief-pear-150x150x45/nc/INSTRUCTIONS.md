# Sylvan Dragoness — Run Instructions

Posted G-code for the relief in pear, 150 × 150 × 45 mm blank,
mounted at the front-left of the Carvera Air bed (anchor 1 = X0 Y0 at
the front-left corner of the blank, Z0 at the top of the blank).

> **Stock prep is hand-done before mounting**: 50 mm raw pear blank
> faced down to 45 mm on a planer, both 150 × 150 faces parallel.

## Run order — six files, one tool slot per file

Each roughing slab is its own file so you can stop, inspect, and
resume between Z-layers if you want. All four T1 files use the same
bit (no tool change between them); only files 5 and 6 require a swap.

| # | File | Tool | Z range | Notes |
|---|---|---|---|---|
| 1 | `01A_T1_ROUGHING_SLAB_1_Z0_TO_Z-12.cnc`         | **T1** Ø3.175 spiral O, 42 mm flute | 0 → −12 mm | top slab — bulk material removal |
| 2 | `01B_T1_ROUGHING_SLAB_2_REST_Z-12_TO_Z-24.cnc`  | **T1** (no change)                  | −12 → −24 mm | middle slab, rest machining off slab 1 |
| 3 | `01C_T1_ROUGHING_SLAB_3_REST_Z-24_TO_Z-35.cnc`  | **T1** (no change)                  | −24 → −35 mm | bottom slab, rest machining off slab 2 |
| 4 | `02_T1_FLAT_FLOOR_REWORK_3175x42.cnc`           | **T1** (no change)                  | 0 → −29.9 mm | cleans the 1.5 mm steps left by slabs |
| 5 | `03_T2_FINISH_BALL_3175x22.cnc`                 | **T2** Ø3.175 ball nose, 22 mm flute | 0 → −31.5 mm | main 3D finish |
| 6 | `04_T3_DETAIL_REST_BALL_2x17.cnc`               | **T3** Ø2.0 ball nose, 17 mm flute  | 0 → −31.5 mm | detail rest pass on what T2 couldn't reach |

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

You're keeping the **same X / Y / Z workpiece zero across all six
files**. Only thing that changes is the tool, and only at file 5 and 6.

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
4. After a tool change, **re-probe TOOL LENGTH only** — the Carvera
   auto-routine handles this. **Do NOT re-touch the workpiece Z** — the
   workpiece zero is unchanged.
5. Load the next file and run.

## Tool slots — the actual bits

These are the same Makera-family bits the project README describes.
Make sure each slot in the changer holds the correct one before you
start file 1.

| Slot | Bit | Description on the box |
|---|---|---|
| **T1** | Ø3.175 single-flute spiral O, **42 mm flute** | yellow-capped tube, "Spiral 'O' Single Flute Bit – 1/8" Shank, 3.175mm × 42mm" |
| **T2** | Ø3.175 2-flute ball nose, **22 mm flute** | "双刃球头铣刀 3.175*22*38" / "Two Flute Ball Nose – 3.175 × 22 mm" |
| **T3** | Ø2.0 2-flute ball nose, **17 mm flute** | "双刃球头铣刀 3.175*2.0-17" — **the 17 mm flute version, not 12 mm** |

> The 12 mm flute Ø2.0 in your set is a **flat** endmill (in the
> 2-flute flat-endmill set `双刃平头铣刀套装`). For finishing we want
> the **ball nose** — that's the 17 mm one.

## What's left on the part between operations

| After file | What's left on the model |
|---|---|
| 1 (slab 1) | top 12 mm of the relief is roughed, 0.5 mm offset everywhere |
| 2 (slab 2) | middle 12 mm roughed, 0.5 mm offset |
| 3 (slab 3) | bottom roughed, 0.5 mm offset everywhere |
| 4 (flat-floor rework) | 0.1 mm on flats, 0.5 mm everywhere else |
| 5 (main 3D finish) | ~0 mm except where the Ø3.175 ball couldn't reach corners |
| 6 (detail rest) | ~0 mm everywhere within reach of the Ø2.0 ball, 17 mm deep |

Optional: a V-bit pencil pass after file 6 sharpens the deepest
valleys that even the small ball couldn't reach. Not provided in this
run — add manually in Fusion when you're ready.

## If the bit looks too high or off in XY at the start of a file

- **Z too high** → check your Carvera workpiece-thickness setting. If
  it says 50 mm, change to 45 mm and re-probe Z.
- **XY off by ~2 mm** → you may have zeroed at the relief corner
  (mesh inset 2 mm) instead of the physical blank corner. Re-zero on
  the actual blank corner.

## Safety reminders

- **Keep the cover closed** during cuts.
- **Watch the first minute** of every file — most failures show up
  immediately.
- **Air assist on** for all wood cuts.
- **Don't pause-and-resume mid-job** unless you're sure the resume
  point is correct. Restart the file from the beginning if in doubt.
