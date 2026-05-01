# tools

Three small Python utilities. None of them depend on anything outside the
standard library (the Fusion script depends on `adsk.*` because it runs
inside Fusion).

## `validate_cnc.py` — G-code safety scan

Standalone validator for posted G-code (`.cnc` / `.nc`). Parses the file,
extracts X/Y/Z bounds, tool numbers, feeds, spindle speeds, M/G codes, and
section markers. Then runs configurable safety checks.

```bash
python validate_cnc.py path/to/file.cnc                    # report only
python validate_cnc.py file.cnc --max-depth 35             # fail if Z < -35
python validate_cnc.py file.cnc --bounds 0,0,150,150       # check XY excursion
python validate_cnc.py file.cnc --high-feed 3000           # cap feed
```

Exit code is 0 (pass) or 1 (one or more checks failed). Suitable for CI or
pre-flight automation.

## `cam_recipes.py` — recipe lookup (offline)

Loads recipes from `recipes/` and lets you list / show / search them
without opening Fusion 360.

```bash
python cam_recipes.py list
python cam_recipes.py show pear-3175-flat-roughing-adaptive
python cam_recipes.py find --material pear --tool-d 3.175 --op adaptive_roughing
```

Also usable as a library:

```python
from cam_recipes import load_recipes, get_recipe

r = get_recipe(load_recipes("recipes"),
               material="pear", tool_diameter_mm=3.175,
               operation="adaptive_roughing")
print(r["params"]["maximumStepdown_mm"])
```

## `apply_recipe.py` — Fusion 360 script

Runs **inside** Fusion 360. Multi-select one or more CAM operations in the
Manufacture browser, run the script, pick a recipe JSON, and the
parameters get written onto each selected op (with a per-key log of what
changed).

Install:

1. Tools tab → Add-Ins → Scripts and Add-Ins
2. Click `+` next to "My Scripts" → browse to this folder
3. Run from the Scripts panel

The script edits parameters by *name*. If a recipe field doesn't apply to
a selected op (e.g., `optimalLoad` on a parallel-strategy op), it's logged
as `[skip]` and the rest of the recipe still applies. This lets you keep
one recipe file even when applying it to mixed operation types.
