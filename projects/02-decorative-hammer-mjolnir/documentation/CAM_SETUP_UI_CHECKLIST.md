# CAM Setup — WCS configured 100% via API (no UI step)

> **Update 2026-05-02 (cleanup pass)**: 14 setups. H0a–H0d are now
> standalone face-mill PREP setups (no longer first ops of H1/H3);
> they skim 0.5 mm off each long flank to give a flat, repeatable
> Anchor-1 reference for H1–H4. H5 "top of tenon up" stays dropped —
> 240 mm handle vs 130 mm Z envelope, wedge kerf is hand-saw.
>
> **Setup roster:** H0a / H0b / H0c / H0d (PREP face-mills) +
> H1 / H2 / H3 / H4 (handle long flanks) + A1 / A2 / A3 / A4 / A5 / A6
> (head) = 14 setups, 41 ops, 38 posted .cnc files (1 suppressed,
> intentional gap until A1 chamfer chain is re-picked in the UI).
>
> WCS axes (orientation) configured via `_set_value` axis bindings
> on 2026-05-01 — works as documented below. **WCS origin** had a
> separate bug (see "Origin gotcha" below) — fixed 2026-05-02 by
> switching all setups to `wcs_origin_mode = 'stockPoint'` +
> `wcs_origin_boxPoint = 'top 1'`, putting WCS X0 Y0 Z0 at the
> front-left-top corner of the stock (where the operator probes).
> The earlier `modelOrigin + job_positionOffset` workaround
> documented below is no longer in use; left here as the historical
> record of the API limitation.

## Origin gotcha (and the fix)

The `_set_value` axis-binding sets WCS axes correctly but leaves the
WCS origin position broken: stock-corner reference in the matrix
ends up 10x larger than the underlying stock dimensions. Symptoms:

- `wcs_origin_mode = 'stockPoint' + boxPoint = 'top 1'` puts origin
  at world ~(-150, +285, -300) mm for handle (10x the body bbox).
- `wcs_origin_mode = 'modelPoint'` snaps to model bbox corner — also
  10x off.
- Binding a construction point via `wcs_origin_point._set_value([cp])`
  yields a matrix translation = `cp_position * 10`.
- `surfaceXHigh/Low` (used internally for stock placement) ALSO
  exhibits the 10x bug but with a different scale factor than the
  matrix translation, so they can't both be "correct" for the same cp.

**The working fix** (applied to all 10 setups):

```python
# 1. Set origin mode to modelOrigin (origin at world 0,0,0).
#    This makes surface bounds + stock placement self-consistent.
setup.parameters.itemByName('wcs_origin_mode').expression = "'modelOrigin'"

# 2. Apply per-setup translation via job_positionXOffset/Y/Z so that
#    the stock corner appears at G-code (0, 0, 0). This is a clean,
#    bug-free Fusion mechanism that runs at post time.
#    Compute by transforming the desired stock-corner world point to
#    WCS coords (via the inverse WCS matrix), then negate.
setup.parameters.itemByName('job_positionXOffset').expression = '<X> mm'
setup.parameters.itemByName('job_positionYOffset').expression = '<Y> mm'
setup.parameters.itemByName('job_positionZOffset').expression = '<Z> mm'
```

After this, body in G-code coords is:

| # | Setup | G-code body X | Y | Z |
|---|---|---|---|---|
| 0 | H1 | 30..270 | 1..29 | -45..-5 |
| 1 | H2 | 30..270 | 1..29 | -45..-5 |
| 2 | H3 | 30..270 | 8.5..41.5 | -29..-1 |
| 3 | H4 | 30..270 | 8.5..41.5 | -29..-1 |
| 4 | A1 | 0..100 | 0..50 | -50..0 |
| 5 | A2 | 0..100 | 0..50 | -50..0 |
| 6 | A3 | 0..100 | 0..50 | -50..0 |
| 7 | A4 | 0..100 | 0..50 | -50..0 |
| 8 | A5 | 0..50 | 0..50 | -100..0 |
| 9 | A6 | 0..50 | 0..50 | -100..0 |

All positive X/Y, negative Z — matches the project convention
("posted G-code uses positive X, Y values that stay inside
X = 0..stock_X_mm and Y = 0..stock_Y_mm" per CAM_PLAN.md).

## Convention reminder (still valid)

- **Stock as mounted:** lower-left front corner of stock against the
  Anchor 1 pins. WCS X0 Y0 = lower-left front. WCS Z0 = top of stock
  (re-probed each setup with the XYZ probe + 3.175 mm test rod).
- **Spindle direction:** approaches the part from **WCS Z+**. So the
  face picked as "Z up" for each setup is the one currently facing
  the spindle.

## What was actually done (2026-05-01 commit)

For each setup, the API picks the right face/edge by world-direction
filter and binds it. Concretely:

| Setup | "Z up" entity (binds `wcs_orientation_axisZ`) | "X along" entity (binds `wcs_orientation_axisX`) |
|---|---|---|
| **H1 — +Y face up** | largest `+Y`-normal handle face (2932 mm², the bust side) | a 185-mm handle edge in `+Z` direction |
| **H2 — -Y face up** | largest `-Y`-normal handle face (back side) | same `+Z` edge |
| **H3 — +X face up** | largest `+X`-normal handle face | same `+Z` edge |
| **H4 — -X face up** | largest `-X`-normal handle face | same `+Z` edge |
| **H5 — top of tenon up** | the small `+Z`-normal tenon-top face (200–600 mm²) | largest `+X`-normal handle face |
| **A1 — head +Z up** | head's `+Z` face (3050 mm²) | head's `+X` face (1600 mm²) |
| **A2 — head -Z up** | head's `-Z` face | head's `+X` face |
| **A3 — head +Y up** | head's `+Y` face (3600 mm², Yggdrasil side) | head's `+X` face |
| **A4 — head -Y up** | head's `-Y` face | head's `+X` face |
| **A5 — head +X up** | head's `+X` strike face | head's `+Y` face |
| **A6 — head -X up** | head's `-X` strike face | head's `+Y` face |

After binding, every setup's `workCoordinateSystem` matrix matches
the expected orientation (verified post-save).

## Working API recipe

```python
setup = cam.setups.item(idx)

# 1. mode FIRST
setup.parameters.itemByName('wcs_orientation_mode').expression = "'axesZX'"

# 2. bind axes via _set_value
setup.parameters.itemByName('wcs_orientation_axisZ').value._set_value([z_face])
setup.parameters.itemByName('wcs_orientation_axisX').value._set_value([x_edge_or_face])

adsk.doEvents()

# 3. read matrix to verify
m = setup.workCoordinateSystem
xaxis = (m.getCell(0,0), m.getCell(1,0), m.getCell(2,0))   # WCS X in world
zaxis = (m.getCell(0,2), m.getCell(1,2), m.getCell(2,2))   # WCS Z in world
```

## What I tried that did NOT work (kept here for reference)

| Approach | Result |
|---|---|
| `param.expression = entityToken` | accepted but reads back as `"false"` |
| `param.expression = "true"` | same |
| `param.value.value.push_back(face_or_edge)` | size goes 0→1 in memory but rolls back to 0 on save |
| `setup.workCoordinateSystem = matrix` | property is read-only |
| `Component.constructionCoordinateSystems` | class doesn't exist in `adsk.fusion`/`adsk.core`/`adsk.cam` |
| `Selections.Set <path>` (text command) | sets UI selection but doesn't propagate to params |
| `Setup.SetWCS …` (text command) | no such command |
| `param.value._set_value([face])` + `mode='axesXZ'` | axisZ persists & matrix uses it; **axisX persists but matrix ignores it** (WCS X stays world `+X`) |
| **`param.value._set_value([face])` + `mode='axesZX'`** | ✅ **both axes persist AND matrix reflects both** |

The interaction between `_set_value` and the *correct* mode name
(`axesZX` not `axesXZ`) was the unblock.

## Long-term reference

This finding is saved in permanent Claude memory at
`memory/fusion_cam_wcs_api_limitation.md` (with the same title kept
for backwards link, even though it now describes a working path).
