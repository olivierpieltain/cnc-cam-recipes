# CAM Setup — UI Checklist

> One-time, ~30 seconds per setup × 11 setups = **5-10 minutes total**.
>
> **Why this exists:** Fusion's CAM API in direct-modeling mode can't
> bind a face to `wcs_orientation_axisZ` programmatically (no
> `constructionCoordinateSystems` collection in this design type, and
> `CadObjectParameterValue` doesn't expose a working setEntities
> path). Rather than fight it for hours, we do the WCS orientation
> in the UI — UI is genuinely the right tool for "click a face."
> Everything else (stock, operations, tools, feeds, simulation,
> post) is API-driven and saved in this repo.

## Convention reminder

- **Stock as mounted:** lower-left front corner of stock against the
  Anchor 1 pins. WCS X0 Y0 = lower-left front. WCS Z0 = top of stock
  (re-probed each setup with the XYZ probe + 3.175 mm test rod).
- **Spindle direction:** approaches the part from **WCS Z+**. So the
  face you pick as "Z up" for each setup is the one currently facing
  the spindle.

## How to configure each setup's WCS in the UI

For each setup (in the CAM browser tree, double-click the setup to
edit it):

1. Switch to the **Manufacture** workspace if not there already.
2. **Setup tab** (the first tab of the setup dialog).
3. Under the **Work Coordinate System (WCS)** section, set
   **Orientation** to → **"Select Z axis/plane & X axis"**.
4. Click in the **Z Axis** field, then click the **face on the part
   that should be UP** for that setup (see the per-setup table below).
5. Click in the **X Axis** field, then click the face/edge that
   represents the long axis of the handle (or the head's strike axis)
   pointing in the **+X bed direction** (away from Anchor 1).
6. Under the same WCS section, **Origin** should be **"Stock Point"**,
   and the box-point should be **"top lower-left front"** (the corner
   touching Anchor 1 — visualised as a small dot on the corner of the
   stock outline in the viewport).
7. Click **OK**. The WCS triad will visibly rotate — confirm Z is up,
   X is along the bed length.

That's it. The setup is configured for the rest of the API-driven
work to take over.

## Per-setup table

### Handle (5 setups)

| Setup | "Z up" face on the part | "X along" axis |
|---|---|---|
| **H1 — Side A (+Y face up)** | the **+Y face of the handle shaft** (where the Odin bust protrudes — the face with the bust mesh on it) | the **+Z direction along the handle** (long edge from pommel to head) |
| **H2 — Side B (-Y face up)** | the **-Y face** (back side, mirror of H1) | same +Z handle direction |
| **H3 — Side C (+X face up)** | the **+X face of the handle** (one of the side faces with the HAMMER OF OLIVIER inscription — pick the +X side) | same +Z handle direction |
| **H4 — Side D (-X face up)** | the **-X face** (mirror of H3) | same +Z handle direction |
| **H5 — Top end (+Z face up)** | the **top of the tenon** (small 25 × 22 face at Z=240, where the wedge kerf sits) | the **+X face of the handle** (so the wedge kerf X axis aligns with bed X) |

### Head (6 setups)

The head is a 100 × 50 × 50 mm block. It sits on the bed in different
orientations to expose each face.

| Setup | "Z up" face | "X along" axis |
|---|---|---|
| **A1 — Top end (+Z up)** | top face of the head (the 100 × 50 face containing the eye exit) | one long edge along bed X |
| **A2 — Bottom end (-Z up)** | bottom face (other 100 × 50 face, eye entry) | same |
| **A3 — Long face +Y up** | +Y face of the head (the 100 × 50 face with Yggdrasil + Celtic medallions) | one long edge |
| **A4 — Long face -Y up** | -Y face (mirror of A3) | same |
| **A5 — Strike face +X up** | +X face of the head (50 × 50 face with Helm-of-Awe) | the head's other 50 mm direction |
| **A6 — Strike face -X up** | -X face (mirror of A5) | same |

## Why the UI step (not API) — definitive answer

The Fusion 360 Python API doesn't expose a working path to bind a
face/edge to a CAM Setup's WCS orientation axis. Tested extensively
during this project (May 2026):

| Approach | Result |
|---|---|
| `param.expression = entityToken` | ❌ accepted but reads back `"false"` |
| `param.expression = "true"` | ❌ same |
| `param.value.value.push_back(face_or_edge)` | ❌ size goes 0→1 in memory but rolls back to 0 on save |
| `setup.workCoordinateSystem = matrix` | ❌ property is read-only |
| `Component.constructionCoordinateSystems` | ❌ class doesn't exist in `adsk.fusion`/`adsk.core`/`adsk.cam` |
| Switch to parametric (`design.designType = 1`) | ✓ works but `constructionCoordinateSystems` still doesn't exist |
| `Selections.Set <path>` (text command) | ✓ sets UI selection but doesn't propagate to params |
| `Setup.SetWCS …` (text command) | ❌ no such command |

After a UI WCS click, the API can read the result. Specifically:

```python
setup = next(s for s in cam.setups if s.name == 'H1_HANDLE_SIDE_PY')
mode = setup.parameters.itemByName('wcs_orientation_mode').expression
axisZ_expr = setup.parameters.itemByName('wcs_orientation_axisZ').expression
axisZ_size = setup.parameters.itemByName('wcs_orientation_axisZ').value.value.size()
m = setup.workCoordinateSystem
print(f'mode={mode}  axisZ.expr={axisZ_expr}  axisZ.size={axisZ_size}')
for r in range(4):
    print([round(m.getCell(r, c), 3) for c in range(4)])
```

After the UI click, `mode` becomes `'axesXZ'`, `axisZ.expr` becomes
`'true'`, `axisZ.size` becomes 1, and the matrix reflects the new
orientation. **This is how I'll verify each setup once you're done.**

Long-term reference: this finding is also saved as
`memory/fusion_cam_wcs_api_limitation.md` in the user's permanent
Claude memory so future sessions don't re-do the same investigation.

## Confirmation step before API takes over

After you've configured all 11 setups, ping me in the chat with
something like *"WCS done"*. I'll then:

1. Verify each setup's `workCoordinateSystem` matrix matches the
   expected orientation (programmatic readback — no UI).
2. Add stock dimensions per setup (30 × 50 × 300 mm for handle;
   100 × 50 × 50 mm for head).
3. Add operations: tools, geometry, feeds-and-speeds (per
   `CAM_PLAN.md`).
4. Simulate every operation.
5. Post `.cnc` files split by tool (per the `splitFile = tool`
   decision).
6. Validate every `.cnc` against the project 01 safety scan rules.
7. Write a per-setup run sheet (operator notes) and a
   `VALIDATION_REPORT.md` matching the project 01 format.

## What if you'd rather skip the UI step?

Two alternatives:

- **Convert the design to parametric mode** (Modify menu → Capture
  Design History or similar). Then Fusion exposes
  `constructionCoordinateSystems` and I can configure WCS purely via
  API. Risk: parametric mode replays direct-modeling features as a
  timeline; sometimes that re-introduces ordering bugs (esp. with the
  many head/handle rebuilds we did). I'd rather not do this without
  your explicit OK.
- **Accept modelOrientation everywhere.** This means the spindle
  always approaches from design +Z (handle long axis). We can do
  *some* operations this way (the wedge kerf, eye through-cut, top
  chamfers), but engravings on the side faces and the Odin 3D bust
  would not work. I'd lose ~70 % of the operations.

The UI route is genuinely the cheapest path forward.
