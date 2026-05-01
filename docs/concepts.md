# Concepts

The handful of conventions every project in this repo assumes. None of these
are unique to this repo — they're standard CNC practice — but writing them
down once means each project README can stay short.

## Anchor 1 — the WCS used by every project here

Work Coordinate System (G54) origin = **front-left, top corner of the stock
as it sits clamped on the bed**:

```
         +Z
          |
          |    +Y
          |   /
          |  /
          | /
          +-----------+----- +X
        anchor 1
   (X0, Y0, Z0)
```

- **X0 Y0** = the front-left corner of the blank
- **Z0** = the top face of the blank
- **+X** = right
- **+Y** = away from the operator
- **+Z** = up

To run any project on your machine: jog to that corner, zero X/Y/Z, run.
This is the simplest origin to set up reliably with a probe or by hand.

If your shop normally uses a different reference (stock center, machine
home), Fusion lets you change `wcs_origin_boxPoint` on the setup — but the
toolpaths and the comments in the posted G-code assume anchor 1. Re-zero
after you switch.

## Stock body conventions

Each project's Fusion file contains a `STOCK_*` body sized to the **physical
blank you'll mount on the machine**. Setups use `job_stockMode = 'solid'`
which reads the stock from this body.

If the project's blank is hand-prepared first (jointed flat, planed to
thickness, faced on both sides), the body name reflects the *post-prep*
dimensions and the README's *Stock prep* section explains what was done.
You don't re-do that prep in CAM — you do it before you mount the stock.

> **Important caveat seen in Fusion's CAM cache:** the stock-bounds values
> shown in the setup parameters (`stockZLow`, etc.) can be stale if you
> resize the body after creating the setup. The G-code is still posted from
> the live body, so it's correct — the cached values just lag the display.
> See [`safety-rules.md`](safety-rules.md) for the validation step that
> catches any real divergence.

## Operation order

Standard 3-axis relief / pocket workflow used by the projects in here:

```
roughing (adaptive)         ← bulk material removal, leaves stockToLeave
flat-floor rework (horizontal) ← cleans flat horizontal areas left by adaptive
3D finishing (parallel / scallop / pencil) ← detail surfaces
contour / chamfer / detach  ← edges + cutoff (often a separate setup)
```

Each step is one or more operations. Roughing is typically split into
**slabs** (top→middle, middle→bottom) so adaptive doesn't have to plan one
giant volume — that speeds up generation and keeps cycle times bounded.

## stockToLeave handoff

Each operation specifies how much material it leaves behind for the next
operation:

| Op | Typical `stockToLeave` |
|---|---|
| Adaptive roughing | 0.3–0.5 mm |
| Flat-floor rework | 0.05–0.15 mm |
| 3D finish | 0 mm (cuts to model) |

The next op in line removes that allowance plus does its own work.

## Tool numbers

Tool numbers in operations need to **match the physical slot in your tool
changer** (or the order you do manual changes). When you adapt a project to
your machine, walk through every operation and verify:

- Same tool index → same physical tool installed
- Different tool index → tool change in the post (M6 T#)

A subtle gotcha: two operations using physically different tools but the
same `tool_number` will silently work in CAM but produce a broken G-code
where the second op runs against the wrong tool. The validator in
`tools/validate_cnc.py` flags this.

## Changing WCS reference

If you prefer a different origin (e.g., stock center for a symmetric part),
edit the setup's `WCS` tab → `Origin` dropdown. Toolpaths regenerate to the
new reference automatically. The posted G-code coordinates change to match.
Don't try to "shift in your head" — re-anchor in CAM and re-post.
