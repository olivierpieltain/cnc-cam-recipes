# Adapting a project to your machine

The whole point of this repo: someone else's working CAM project should
become yours with a few targeted edits, not a from-scratch rebuild.

## The mental model

Every project is a **stack of replaceable layers**:

```
┌────────────────────────────────────────┐
│  Posted G-code (.cnc / .nc)             │  ← post-specific
├────────────────────────────────────────┤
│  Post processor (Carvera.cps, grbl.cps) │  ← swap for your machine
├────────────────────────────────────────┤
│  CAM operations (tools + parameters)    │  ← swap for your tools, your power
├────────────────────────────────────────┤
│  Setup (WCS, stock body, fixtures)      │  ← swap for your blank size
├────────────────────────────────────────┤
│  Source design (.f3d, model, sketches)  │  ← usually keep as-is
└────────────────────────────────────────┘
```

You change layers from the top until the result matches your hardware.
Most adaptations need 2–3 layers.

## Step 0 — Read the project README

Specifically the *"How to adapt this to your machine"* section. The
project author already lists the parameters most likely to need tuning.
You'll often find your specific case discussed.

## Step 1 — Open the Fusion source

Pull the `.f3d` from the project folder (or its linked release). Open in
Fusion 360.

If the project lists a machine profile, import it first
([`docs/setup.md`](setup.md) → *Machine profile*) and assign it to the
setup. The profile gives Fusion your envelope and rapid feed limits for
simulation.

## Step 2 — Tool numbers

Walk through every operation in the CAM browser. For each:

- Note the tool's diameter / type / flutes
- Set the operation's **tool number** to the slot in your tool changer
  that holds an equivalent tool (or the order you'll do manual changes)

If you don't have an equivalent tool, see *Step 4 — Tools*.

## Step 3 — Stock dimensions

Find the body named `STOCK_*` in the design tree.

- **Different blank dimensions:** edit the body's defining sketch (or
  if the body was created in direct mode, use Press-Pull / Move on a face,
  or Combine-Join with a slab to grow it).
- **Stock prep is different from the project's:** for example, the
  project assumes you faced both sides; if you'll surface on the machine
  instead, see the project README for guidance on adding surfacing ops.

The setup uses `job_stockMode = 'solid'`, so the new body bounds flow
into the CAM automatically when you regenerate toolpaths.

## Step 4 — Tools

If your tooling doesn't match exactly:

| Project tool | Closest you have | What to change |
|---|---|---|
| Same diameter / type | (nothing) | tool number only (Step 2) |
| Same diameter, different flute count | (nothing structural) | re-check chipload: `feed = chipload × RPM × flutes` |
| Same type, different diameter | tool diameter in op + recipe | redo math: see [`feeds-and-speeds.md`](feeds-and-speeds.md) |
| Different type (flat → ball, etc.) | reconsider the op | strategies expect specific tool types — don't substitute blindly |

For diameter swaps, the rule of thumb:

- **Stepdown** scales linearly with diameter
- **Optimal load (radial)** scales linearly with diameter
- **Feed** scales linearly with diameter (for the same chipload)

A recipe tuned for Ø3.175 with stepdown 1.5 mm becomes stepdown ~3 mm at
Ø6.35 — but check spindle power doesn't blow the budget.

## Step 5 — Feeds, speeds, and machine power

The recipe carries a `machine_floor` field — the minimum machine spec
it's safe on. If your machine is **at or above** that floor, the recipe
runs as-is. If it's significantly above, you can increase MRR for shorter
cycles:

- **More rigid frame** → up to 2× radial WOC (`optimalLoad`) safely
- **More spindle power** → proportional MRR increase. Recompute power
  budget per [`feeds-and-speeds.md`](feeds-and-speeds.md).
- **Higher RPM ceiling** → maintain chipload (raise feed proportionally
  to RPM)

Apply changes via `tools/apply_recipe.py` (creates a new recipe and
applies it) or by editing the operation parameters directly in Fusion.

## Step 6 — Post processor

Select your machine's post in Fusion's setup post-processing step. The
operations themselves are post-agnostic; only the final G-code emission
depends on the post.

If your machine has its own community post (Onefinity, Genmitsu, etc.),
use it. For Grbl-based machines, Autodesk's stock `grbl.cps` works well.

## Step 7 — Regenerate and validate

Right-click the setup → "Generate Toolpath" (or per-op). Wait for all
ops to mark valid.

Post:

```
right-click NC Program → Post Process → choose your post → output to local folder
```

Validate:

```bash
python tools/validate_cnc.py path/to/output.cnc \
    --max-depth <project's hard Z constraint> \
    --bounds <project's stock bounds>           \
    --high-feed <your machine's high feed>
```

The validator's `=== PASS ===` is necessary but not sufficient. Always
also do the human checklist in [`safety-rules.md`](safety-rules.md)
before sending the file to the machine.

## Step 8 — First-cut sanity run

For any non-trivial adaptation:

1. Mount a **scrap blank** of the same dimensions and mounting style as
   the real one.
2. Run the program with **air cuts** at 50% feed override (`M851 S50` on
   Carvera, or your machine's feed override) and the spindle off — verify
   motion stays where you expect.
3. Lower feed override to 100% and run with spindle on, watching the
   first minute closely.
4. If it looks right, proceed with the real material.

Adaptations that change tool diameter, machine, or post should always go
through this sanity run. Adaptations that only change tool number or feed
within the same recipe class can usually skip it.

## Common adaptation patterns

### "I have the same machine, different artwork"

Replace the model body in the design (mesh / BRep) with yours. Keep the
stock setup, operations, and recipes as-is. Regenerate, post, validate.

### "Same artwork, different stock dimensions"

Resize the stock body. Adjust each operation's `topHeight` /
`bottomHeight` to match the new top of stock and the new deepest cut.
Regenerate, post, validate.

### "Different machine, same artwork, same stock"

Swap post processor. Update tool numbers. Verify chipload still in window
for your spindle's RPM. Regenerate, post, validate.

### "Same everything, different material"

Update the recipe — different `Kc` and chipload window. Reapply via
`tools/apply_recipe.py`. Regenerate, post, validate. **Always sanity-run
on a scrap of the new material first.**
