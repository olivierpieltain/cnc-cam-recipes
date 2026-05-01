# Lessons Learned — 01-relief-pear-150x150x45

Notes I wish I'd had before starting. None of these are deal-breakers,
but each cost time the first time around.

## "Conservative" is not the same as "right" — under-feeding doubles cycle time

The first version of the roughing recipe shipped with `optimalLoad =
0.5 mm` (16 % of tool diameter) and `tool_feedCutting = 430 mm/min`.
The thinking was "Carvera Air's small spindle, long-flute tool, better
to be safe." The result: an estimated **35-hour roughing pass**, which
the operator only noticed after the job had started.

The numbers were wrong in two compounding ways:

1. **`optimalLoad` 0.5 mm = 16 % of D.** Adaptive clearing's design
   point in wood is **20–30 % of D**. At 16 % the tool is making
   chips so thin they don't break — it rubs and burnishes more than it
   cuts. Bumping to **0.8 mm = 25 % of D** lands in the recipe's
   intended window.
2. **`tool_feedCutting` 430 mm/min.** With Ø3.175 / 2 flutes / 13 000
   RPM that's 0.0165 mm/tooth — the *bottom* of pear's chipload window
   (0.025–0.05 mm/tooth). Bumping to **600 mm/min** gives 0.023
   mm/tooth, mid-window. Same tool, same engagement, just feeding
   correctly.

Power check at the corrected numbers: MRR ≈ 2.0 × 0.8 × 600 = 960
mm³/min ≈ 16 mm³/s. P ≈ 16 × 5 / 0.7 ≈ **115 W** — under the 140 W
spindle budget. Comfortable.

**Net effect:** the corrected recipe roughs the same volume in roughly
**12 hours instead of 35.** Same machine, same tool, same stock.

> Why this matters beyond cycle time: a tool that's rubbing instead of
> cutting heats up, dulls fast, and makes worse surface finish. Slow
> isn't the same as gentle.

The recipe in [`recipes/pear-3175-flat-roughing-adaptive.json`](../../recipes/pear-3175-flat-roughing-adaptive.json)
now ships with the corrected numbers. The reasoning block in the
recipe carries inline notes about what the earlier version had so the
mistake isn't silently repeated.

**Operator workaround on the running job:** the Carvera's feed-override
slider scales feeds in real time. Setting it to **200 %** doubles 430
to 860 mm/min, which is *higher* than the corrected 600 but still
inside pear's chipload window (0.033 mm/tooth). On a job that's
already in flight with the slow .cnc, that's the only lever — and it
roughly halves the remaining time. Reset to 100 % before any
finishing pass.

## Adaptive against a mesh body is *much* slower than against BRep

The relief in this project is a triangle mesh (STL). Adaptive evaluates
tool engagement against every triangle inside the cut volume. For a dense
relief mesh (≈ 100 k faces) this is **5–10× slower than the same
operation against an analytic BRep**.

Before chasing CAM parameters to speed things up, check whether your
model is BRep or mesh. If it's mesh and you can convert (Fusion: Mesh
workspace → Convert Mesh → Faceted BRep), do it. Conversion fails on very
dense / non-manifold meshes — keep a backup of the mesh body.

## The CAM stock dimensions in the setup parameters are *cached*

If you resize the stock body after the setup is created, the values
shown under `setup.parameters` (e.g., `stockZLow`) can lag the body by
several minutes. The G-code itself is posted from the live body, so the
result is correct — but the header comment in the posted `.cnc` may say
`Stock Height: 40 mm` when the body is actually 45 mm. Cosmetic only.

To force a refresh: touch any stock-offset parameter (set it to its own
value). Fusion re-evaluates. Or just trust that the post reads from the
body, not the cache.

## Fusion API: `NCProgramInput.operations.push_back(op)` doesn't work

If you build CAM programs through the Python API, this trap is real:

```python
# DOESN'T POPULATE THE PROGRAM:
nc_input.operations.push_back(op)

# DOES:
nc_input.operations = [op1, op2, op3]      # list assignment
```

After `push_back`, the resulting NC program has `opsCount = 0` and posts
as an empty file. The pattern that works is documented in
[Autodesk's PostToolpaths sample](https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/PostToolpaths_Sample_Sample.htm).

## Adaptive cuts up to one tool-radius outside the stock outline

The first time you see X = 151.07 in a posted `.cnc` for a 150-wide blank
it looks alarming. It isn't — that's the tool *center* tracing a path
that puts the cutting edge at X = 152.65, in air, at the edge of an
adaptive arc. Normal.

Practical implication: leave at least 5 mm clearance between the blank
edge and any fixturing. Adaptive will reach a few mm past where you
think it should.

## `op.duplicate()` returns a `bool`, not the new operation

Easy trap if you assume Fusion's API is consistent with most "duplicate"
methods elsewhere:

```python
# DOESN'T do what you think:
new_op = op.duplicate()         # new_op is True/False

# Instead:
before = setup.operations.count
ok = op.duplicate()
new_op = setup.operations.item(setup.operations.count - 1)
```

The new operation is appended to the *end* of the operation list, not
adjacent to its template. Use `moveBefore` / `moveAfter` to reorder.

## `setup.operations.item(0)` is **not** necessarily what's drawn first

The `cam.allOperations` collection enumerates ops in *display* order
across all setups; `setup.operations.item()` enumerates by an internal
index that doesn't always match the browser order. Don't index by
position — look up ops by `name`.

## Long-flute 1/8" tools deflect under load

A Ø3.175 × 42 mm flute tool has a flute-length-to-diameter ratio of 13×.
That's *long*. Under any meaningful radial load it deflects measurably,
and the resulting surface has a tapered wall (more material left near the
top of the cut, less at the bottom).

Don't fight the deflection — leave 0.5 mm of stock-to-leave so the
finishing pass cleans it up. If you need flat walls within tight
tolerance, reach for a shorter (e.g., 12 mm flute) tool for the final
pass.

## Disable `flatAreaMachining` on adaptive when you have a separate flat-finish op

Adaptive's "flat area machining" inserts extra fine-stepdown passes on
detected flat regions. If you also have a horizontal-strategy op
specifically for flats, those passes are redundant — and they slow CAM
generation by 2–4×. Turn them off; let the flat-finish op do its job.

## `splitFile` in the Carvera post

The Makera Carvera community post has a property called `splitFile` with
options `none` / `tool` / `toolpath`:

- **none** — single `.cnc` for the whole job. Simplest.
- **tool** — one file per tool. Useful if you want to inspect each tool's
  program separately or run them independently.
- **toolpath** — one file per operation. Most flexibility, most files to
  manage.

For the roughing-only post in this project, `none` is right (3 ops, all
on T1). When the full job ships, `tool` is probably what you want so
finishing is its own file.

## Fusion's machine-assignment API is unreliable

Trying to assign a Carvera machine `.f3d` to the setup via Python's CAM
API has thrown `"The requested document is not accessible"` for me on
multiple sessions. Assign the machine through the UI; don't loop retries
in the API — Fusion can become unstable.

## When toolpath generation feels stuck at e.g. 60% for minutes

The progress meter in Fusion is non-linear. Adaptive's expensive phases
are computing the in-process model and resolving rest-machining sources;
once those are done the path itself comes out fast. **Don't cancel a
stuck-looking gen for at least 10 minutes** — odds are it's still
working.

You can sanity-check by looking at Fusion's CPU usage in Task Manager.
If it's pegged on one core, gen is alive.
