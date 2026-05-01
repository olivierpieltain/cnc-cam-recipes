# Safety Rules — Hard Constraints

Run through this list **every time** before you load a `.cnc` file on the
machine. The validator in [`tools/validate_cnc.py`](../tools/validate_cnc.py)
automates most of it, but the human read-through is what catches the rest.

## Pre-run checklist

### Tool

- [ ] **Right tool in the slot.** The G-code's first `M6 T<n>` (or the
  ATC's tool table) must match the physical tool installed. A 1/8" flat
  endmill where the program expects a 1/8" ball will plow through the
  workpiece on the first depth pass.
- [ ] **Sharp.** Dull tools generate heat instead of chips and load the
  spindle harder than the math predicts.
- [ ] **Tool length recorded.** If your machine measures tool length
  automatically, run the probe before the program. If you do it manually,
  re-touch on every tool change.

### Stock

- [ ] **Mounted square.** Front-left corner of the blank lines up with
  X0 Y0 of the work envelope (or wherever you've moved your WCS).
- [ ] **Clamped firmly.** Vise jaws or hold-downs grip the part with at
  least the depth of the deepest cut + 5 mm safety margin still in the jaws.
- [ ] **Top face clearance.** Z = +highest_clearance_in_program above the
  blank top must be reachable without the spindle nose hitting anything.
- [ ] **Boundary clearance.** Adaptive toolpaths frequently excursion **up
  to 1 tool radius outside the stock outline** at boundaries. Check the
  validator output for X/Y range — make sure your fixtures aren't there.

### Program

- [ ] **Z lowest value ≥ −(stock_thickness − backing_min).** For a 45 mm
  blank with 5 mm backing minimum, Z must never go below −40 mm. The
  validator checks this if you pass `--max-depth`.
- [ ] **No surprise tool changes.** Count `M6` lines — should match the
  number of tools in your job package.
- [ ] **End sequence present.** File ends with spindle stop, dwell, home,
  and program-end (`M5`, `M400`, `G28`/equivalent, `M30`). A program that
  ends with the spindle still spinning is a fire risk on wood.
- [ ] **Feeds within machine limits.** Cutting feed should be below your
  machine's `highFeedrate` (typically 3000 mm/min). Plunge feed should be
  ≤ 1/3 of cutting feed.

### Mid-run

- [ ] **Air assist on** before the spindle starts (M7 in Carvera /
  Carvera Air). Wood machining without air assist packs the cut with
  chips and stalls.
- [ ] **First minute observed.** Don't walk away during the first minute
  of any new program — tool engagement is highest near the surface.
- [ ] **Sound check.** A loaded spindle has a particular pitch. Sudden
  changes (chatter, bog, squeal) mean stop, retract, inspect.

## Hard "don't"s

### Don't run a program you haven't validated

```bash
python tools/validate_cnc.py path/to/file.cnc
```

Look at every section of the report. If anything's flagged, understand why
**before** loading the file.

### Don't reuse a `.cnc` after editing the Fusion design

If you changed the stock body, the relief, the tool list, or any operation
parameter — the posted file is now wrong. Re-post.

### Don't bypass helical ramps

Operations with `rampType = 'helix'` are spec'd that way because the tool
can't plunge straight in. Don't change it to "plunge" because adaptive
doesn't always have room to ramp at the edges. If a ramp won't fit, expand
your stock or redesign the boundary, don't switch to a plunge.

### Don't disable air on wood

Without air, dust packs into the kerf, the tool loads up, the temperature
spikes, and you lose either the tool or your stock. The Carvera post turns
air on with `M7` automatically — leave it.

### Don't run finishing without proper roughing

A 0.25 mm-stepover ball-nose finish that suddenly hits 5 mm of unmilled
stock will deflect, chatter, or snap. The roughing pass is what makes
finishing safe.

### Don't post the cutoff without explicit approval

Final-detach operations that free the part from the stock are intentionally
the last thing you run. Post and run cutoff **only after** the rest of the
job has been inspected on the machine.

## Tool-rigidity envelope

For a long-flute endmill (flute length > 5× diameter), respect this:

- **Maximum DOC at full radial engagement** ≤ 1× tool diameter
- **Maximum DOC at adaptive engagement (≤ 25% radial)** ≤ flute length
  (but the tool deflects more — leave more `stockToLeave` for finishing)

The 3.175 × 42 mm tool used in the example projects is *very* long for its
diameter (13× flute-to-D ratio). It deflects measurably under load — that's
why the recipes leave 0.5 mm of stock for finishing. A short-flute tool
(say 3.175 × 12 mm) is stiffer and can hold tighter tolerance, but can't
reach 35 mm deep.

## When something feels wrong

Stop the spindle, retract Z, leave X/Y where they are, and inspect. The
operation can almost always be resumed from a checkpoint after you fix the
underlying problem (fixture moved, tool dulled, dust packed). Forcing
through a problem mid-program is how broken bits and ruined stock happen.
