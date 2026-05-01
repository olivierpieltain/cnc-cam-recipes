# recipes

Each `.json` file in this folder is a self-contained recipe: a known-safe
set of CAM parameters for a specific `(machine_floor, material, tool,
operation)` combination, with the *reasoning* recorded inline so you can
understand and adapt rather than copy blindly.

## Recipe schema

```json
{
  "name": "pear-3175-flat-roughing-adaptive",
  "version": 1,
  "machine_floor": {
    "min_envelope_mm": [360, 240, 140],
    "min_spindle_W_continuous": 200,
    "min_spindle_RPM": 15000,
    "rigidity": "small-format desktop CNC (Carvera Air-class or better)"
  },
  "material": "free-text description, including density and Kc when relevant",
  "tool": {
    "diameter_mm": 3.175,
    "type": "flat endmill",
    "flutes": 2,
    "flute_length_mm": 42,
    "geometry_notes": "free text"
  },
  "operation": "adaptive_roughing | horizontal_finishing | parallel_finishing | ...",
  "params": {
    "tolerance_mm": 0.1,
    "maximumStepdown_mm": 1.5,
    "optimalLoad_mm": 0.5,
    "stockToLeave_mm": 0.5,
    "useRestMachining": true,
    "flatAreaMachining": false,
    "tool_feedCutting_mm_min": 430,
    "tool_feedPlunge_mm_min": 60,
    "tool_spindleSpeed_RPM": 13000
  },
  "reasoning": {
    "maximumStepdown_mm": "1.5 mm = 47% of tool diameter — within...",
    "optimalLoad_mm":     "0.5 mm radial = 16% of D — adaptive's strength is..."
  },
  "verification": {
    "MRR_mm3_min": 322,
    "spindle_power_required_W": 38,
    "spindle_power_budget_W": 140,
    "chipload_mm_per_tooth": 0.0165
  },
  "see_also": ["docs/feeds-and-speeds.md", "docs/safety-rules.md"]
}
```

### Required fields

- `name` — used as the recipe identifier (`tools/cam_recipes.py show <name>`)
- `material` — at least the common name and Kc estimate
- `tool` — at minimum `diameter_mm` and `type`
- `operation` — the CAM strategy this recipe is for
- `params` — the actual parameters (key naming follows
  `tools/apply_recipe.py`'s `PARAM_MAP`)
- `reasoning` — one short sentence per non-obvious value

### Optional but recommended

- `machine_floor` — the minimum machine spec the recipe is safe on; helps
  others know whether to scale up or down for their machine
- `verification` — derived numbers (MRR, spindle power, chipload) so a
  reviewer can sanity-check without redoing the math
- `see_also` — links to relevant docs

## Naming convention

```
<material>-<tool_diameter_x10>-<tool_geometry>-<operation>.json
```

Examples:

- `pear-3175-flat-roughing-adaptive.json`
- `walnut-6mm-flat-finishing-horizontal.json`
- `acrylic-3175-ball-finishing-parallel.json`

Tool diameter is encoded as the integer mm × 10 (e.g., `3175` for 3.175 mm)
to keep filenames sortable across mixed metric tooling.

## How to add a new recipe

1. Copy an existing `.json` that's close to what you want.
2. Edit `material`, `tool`, `operation`, and `params`.
3. Update `reasoning` — every value worth a sentence gets one. **The
   reasoning is the point of this folder. A recipe without explanations is
   just a magic number.**
4. Run `tools/cam_recipes.py show <name>` to verify it parses cleanly.
5. Open a project in Fusion 360, multi-select the matching operations,
   run `tools/apply_recipe.py`, and verify it applies without errors.
6. Open a PR.

## How to *use* a recipe

In Fusion: select operations → run `tools/apply_recipe.py` → pick the JSON.

Outside Fusion: `python tools/cam_recipes.py show <name>` reads the values
into your terminal, so you can hand-enter them or feed another tool.

For the math behind any specific value, see
[`docs/feeds-and-speeds.md`](../docs/feeds-and-speeds.md).
