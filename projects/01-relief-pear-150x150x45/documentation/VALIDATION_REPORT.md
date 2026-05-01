# Validation Report — Sylvan Dragoness pear relief, 150×150×45 mm

Generated against the CAM tree as of the run that's currently on the
machine. This document captures the safety checks done before the
files were copied to USB.

## Summary

| Check | Result |
|---|---|
| Fusion `cam.checkToolpath()` (all ops) | **PASS** all 6 |
| `tools/validate_cnc.py` on every posted `.cnc` | **PASS** all 6 |
| Tool flute reach vs cut depth | **OK** all ops |
| Stock-bottom margin | minimum **+10 mm** (op 01C at Z=−35; stock at Z=−45) |
| Tool-number conflicts | **None** — T1, T2, T3 distinct |
| End sequence per file | M5 / M400 / M852 / G28 / M30 ✓ |
| Visual top-view inspection | toolpaths cover full stock incl. 2 mm outer border ✓ |
| Visual iso inspection | clean Z-layering, no out-of-bounds cuts ✓ |

## Per-operation status

| # | Op | Tool | DOC | ZMIN | checkToolpath | hasError | hasWarning |
|---|---|---|---|---|---|---|---|
| 01A | rough slab 1 | T1 (Ø3.175 × 42) | 12 mm | −12 | ✓ | False | False |
| 01B | rough slab 2 (rest) | T1 | 12 mm | −24 | ✓ | False | False |
| 01C | rough slab 3 (rest) | T1 | 11 mm | −35 | ✓ | False | False |
| 02 | flat-floor rework | T1 | mesh-driven | −29.89 | ✓ | False | **True** ⚠ |
| 03 | main 3D finish | T2 (Ø3.175 ball × 22) | mesh-driven | −31.52 | ✓ | False | False |
| 04 | detail rest | T3 (Ø2.0 ball × 17) | mesh-driven | −31.55 | ✓ | False | False |

### The single warning (op 02)

> *"One or more pockets were not machined because they are too small to
> be reached with given ramping constraints."*

Not a collision, not a safety issue. Some very small flat pockets in
the relief are too tight for the helical-ramp entry of the horizontal
strategy with this tool. **Op 03 (parallel ball-nose finish) picks
those up** — the affected pockets just keep slightly more leftover
from op 02, which the ball-nose handles cleanly.

## File-level G-code safety scan (`validate_cnc.py`)

Run against each `.cnc` with `--max-depth 35 --bounds 0,0,150,150
--high-feed 3000`:

```
01_T1_ROUGHING_3175x42.cnc           PASS
02_T1_FLAT_FLOOR_REWORK_3175x42.cnc  PASS
03_T2_FINISH_BALL_3175x22.cnc        PASS
04_T3_DETAIL_REST_BALL_2x17.cnc      PASS
```

All files: single tool number per file, Z lowest within −35 mm,
feeds ≤ 3000 mm/min, end sequence present.

## Stock bottom safety margins

```
Op 01A   Z bottom -12 mm  margin +33 mm
Op 01B   Z bottom -24 mm  margin +21 mm
Op 01C   Z bottom -35 mm  margin +10 mm  ← deepest cut
Op 02    Z bottom -29.89  margin +15 mm
Op 03    Z bottom -31.52  margin +13 mm
Op 04    Z bottom -31.55  margin +13 mm
```

The blank's physical bottom is at Z=−45 mm (the stock body). A 5+ mm
margin is the rule of thumb for backing material; we have ≥ 10 mm
everywhere.

## Tool reach analysis

| Tool | Flute / OAL | Max DOC in any op | Verdict |
|---|---|---|---|
| T1 (3.175 spiral O) | 42 / 60 mm | 12 mm (slab 1) | 30 mm flute headroom — fine |
| T2 (3.175 ball) | 22 / 38 mm | mesh-driven, ZMIN −31.5 | reaches 22 mm of cutting flute; below that the 1/8" shank fits the cleared volume — fine |
| T3 (2.0 ball) | 17 / 38 mm | mesh-driven, ZMIN −31.5 | same logic; T3 is rest-only, never enters un-cleared volume — fine |

## Operator notes

- The 200 % feed-override workaround for the slow first-version
  roughing is documented in `lessons-learned.md` in the GitHub repo.
  Don't apply override to the finishing passes (op 03 / op 04).
- Carvera workpiece-thickness setting must be **45 mm**, not 50 mm
  (which was the raw blank before hand-facing).
- X / Y zero on the **physical blank corner** — not the relief edge,
  which is inset 2 mm at X=2, Y=2 in the design.

## Reference

- GitHub repo: <https://github.com/olivierpieltain/cnc-cam-recipes>
- Project: `projects/01-relief-pear-150x150x45/`
- Source artwork: <https://makerworld.com/fr/models/2478075-sylvan-dragoness-relief-sculpture> (not redistributed)
