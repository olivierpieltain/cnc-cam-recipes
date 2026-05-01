"""
Fusion 360 script — apply a recipe (JSON) to selected CAM operations.

How to use this script (inside Fusion 360):

    1. Tools tab -> Add-Ins -> Scripts and Add-Ins
    2. Click the green '+' next to "My Scripts" and point at the folder that
       contains this file. Fusion looks for a function called `run(context)`.
    3. In the Manufacture workspace, multi-select one or more operations in
       the browser (Ctrl-click). Then run this script.
    4. A file picker opens — choose a .json recipe from `recipes/`.
    5. The script writes recipe parameters onto each selected operation and
       prints a per-op before/after report in the Text Commands panel.

Notes:
    * The script edits parameters by *name*. If a recipe field doesn't have a
      matching Fusion CAM parameter on the selected op, the field is logged
      and skipped — it's not an error.
    * Operations remain marked invalid after editing — you'll need to
      regenerate toolpaths in the usual way.
    * This script is parametric on purpose: it doesn't hard-code values for
      any specific machine, material, or tool. The recipe carries those.

The same JSON recipe schema is consumed by `cam_recipes.py` for offline
lookup outside Fusion.
"""

# pylint: disable=import-error
import json
import traceback
import os

import adsk.core
import adsk.fusion
import adsk.cam


# Map from recipe key -> (Fusion CAM parameter name, expression formatter)
# The formatter takes the raw recipe value and returns a Fusion expression
# string. Most are direct passthroughs with mm units appended for clarity.
def _mm(v):       return f"{v} mm"
def _mmpm(v):     return f"{v} mm/min"
def _bool(v):     return "true" if v else "false"
def _str_choice(v): return f"'{v}'"
def _passthrough(v): return f"{v}"

PARAM_MAP = {
    # adaptive / roughing
    "tolerance_mm":            ("tolerance",            _mm),
    "maximumStepdown_mm":      ("maximumStepdown",      _mm),
    "minimumStepdown_mm":      ("minimumStepdown",      _mm),
    "fineStepdown_mm":         ("fineStepdown",         _mm),
    "optimalLoad_mm":          ("optimalLoad",          _mm),
    "stepover_mm":             ("stepover",             _mm),
    "stockToLeave_mm":         ("stockToLeave",         _mm),
    "useStockToLeave":         ("useStockToLeave",      _bool),
    "useRestMachining":        ("useRestMachining",     _bool),
    "flatAreaMachining":       ("flatAreaMachining",    _bool),
    "boundaryMode":            ("boundaryMode",         _str_choice),
    "rampType":                ("rampType",             _str_choice),
    "rampClearanceHeight_mm":  ("rampClearanceHeight",  _mm),
    "direction":               ("direction",            _str_choice),

    # heights
    "topHeight_offset_mm":     ("topHeight_offset",     _mm),
    "bottomHeight_offset_mm":  ("bottomHeight_offset",  _mm),
    "clearanceHeight_offset_mm": ("clearanceHeight_offset", _mm),
    "retractHeight_offset_mm": ("retractHeight_offset", _mm),
    "feedHeight_offset_mm":    ("feedHeight_offset",    _mm),

    # tool feeds / RPM
    "tool_feedCutting_mm_min": ("tool_feedCutting",     _mmpm),
    "tool_feedPlunge_mm_min":  ("tool_feedPlunge",      _mmpm),
    "tool_feedRamp_mm_min":    ("tool_feedRamp",        _mmpm),
    "tool_feedEntry_mm_min":   ("tool_feedEntry",       _mmpm),
    "tool_feedExit_mm_min":    ("tool_feedExit",        _mmpm),
    "tool_spindleSpeed_RPM":   ("tool_spindleSpeed",    _passthrough),
}


def _apply_recipe_to_op(op, recipe, log):
    """Apply recipe['params'] to a single Operation. Append per-key log entries."""
    params = op.parameters
    rp = recipe.get("params", {})

    log.append(f"--- {op.name} ---")
    log.append(f"  strategy: {op.strategy}")
    for key, value in rp.items():
        mapping = PARAM_MAP.get(key)
        if mapping is None:
            log.append(f"  [skip] {key}: no Fusion mapping known")
            continue
        param_name, formatter = mapping
        try:
            it = params.itemByName(param_name)
            if it is None:
                log.append(f"  [skip] {key} -> {param_name}: not on this op (strategy may not support it)")
                continue
            old = it.expression
            it.expression = formatter(value)
            new = it.expression
            log.append(f"  {param_name:28s}: {old} -> {new}")
        except Exception as exc:
            log.append(f"  [fail] {key} -> {param_name}: {exc}")


def run(context):  # noqa: D401 — Fusion script entry point
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # 1) Get selected operations
        selected_ops = []
        for i in range(ui.activeSelections.count):
            ent = ui.activeSelections.item(i).entity
            op = adsk.cam.Operation.cast(ent)
            if op is not None:
                selected_ops.append(op)

        if not selected_ops:
            ui.messageBox(
                "Select one or more CAM operations in the Manufacture browser, then re-run.",
                "apply_recipe.py",
            )
            return

        # 2) Pick a recipe JSON
        dlg = ui.createFileDialog()
        dlg.title = "Choose a recipe (.json)"
        dlg.filter = "Recipe JSON (*.json)"
        dlg.isMultiSelectEnabled = False
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK:
            return
        recipe_path = dlg.filename

        with open(recipe_path, "r", encoding="utf-8") as f:
            recipe = json.load(f)

        # 3) Apply
        log = []
        log.append(f"Recipe : {os.path.basename(recipe_path)}")
        log.append(f"Name   : {recipe.get('name','?')}")
        log.append(f"Tool   : {recipe.get('tool','?')}")
        log.append(f"Material: {recipe.get('material','?')}")
        log.append(f"Operation hint: {recipe.get('operation','?')}")
        log.append(f"Selected ops: {len(selected_ops)}")
        log.append("")

        for op in selected_ops:
            _apply_recipe_to_op(op, recipe, log)
            log.append("")

        # 4) Show result
        text = "\n".join(log)
        # also print to text commands panel for copy/paste
        try:
            app.log(text)
        except Exception:
            pass
        ui.messageBox(text, "apply_recipe.py — done")

    except Exception:
        if ui:
            ui.messageBox(traceback.format_exc(), "apply_recipe.py — error")
