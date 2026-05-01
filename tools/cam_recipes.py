#!/usr/bin/env python3
"""
Recipe lookup module — pure Python, no Fusion 360 dependency.

A "recipe" is a JSON file in `recipes/` that describes a known-safe set of
CAM parameters for a specific (machine, material, tool, operation type)
combination. This module loads recipes from disk and looks them up.

Usage as a library:

    from cam_recipes import load_recipes, get_recipe

    recipes = load_recipes("recipes")
    r = get_recipe(recipes,
                   material="pear", tool_diameter_mm=3.175,
                   tool_type="flat", operation="adaptive_roughing")
    print(r["params"]["maximumStepdown_mm"])

Usage as a CLI:

    python cam_recipes.py list
    python cam_recipes.py show pear-3175-flat-roughing-adaptive
    python cam_recipes.py find --material pear --tool-d 3.175 --op adaptive_roughing
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def load_recipes(folder: str | Path) -> list[dict]:
    """Load every *.json file in `folder` as a recipe. Returns list of dicts."""
    folder = Path(folder)
    recipes = []
    for p in sorted(folder.glob("*.json")):
        try:
            with open(p, "r", encoding="utf-8") as f:
                r = json.load(f)
            r["__file__"] = str(p)
            r.setdefault("name", p.stem)
            recipes.append(r)
        except Exception as e:
            print(f"warn: couldn't load {p}: {e}", file=sys.stderr)
    return recipes


def get_recipe(
    recipes: list[dict],
    material: str | None = None,
    tool_diameter_mm: float | None = None,
    tool_type: str | None = None,
    operation: str | None = None,
) -> dict | None:
    """Return the first recipe matching all provided fields. Case-insensitive."""

    def matches(r: dict) -> bool:
        if material and material.lower() not in r.get("material", "").lower():
            return False
        if tool_diameter_mm is not None:
            d = r.get("tool", {}).get("diameter_mm")
            if d is None or abs(d - tool_diameter_mm) > 0.001:
                return False
        if tool_type and tool_type.lower() not in r.get("tool", {}).get("type", "").lower():
            return False
        if operation and operation.lower() not in r.get("operation", "").lower():
            return False
        return True

    for r in recipes:
        if matches(r):
            return r
    return None


def list_recipes(recipes: list[dict]) -> None:
    print(f"{'name':<50} {'material':<20} {'tool':<22} {'operation':<22}")
    print("-" * 116)
    for r in recipes:
        tool = r.get("tool", {})
        tool_str = f"Ø{tool.get('diameter_mm','?')} {tool.get('type','?')}"
        print(
            f"{r.get('name','?'):<50} "
            f"{r.get('material','?')[:20]:<20} "
            f"{tool_str[:22]:<22} "
            f"{r.get('operation','?')[:22]:<22}"
        )


def show_recipe(r: dict) -> None:
    print(f"name      : {r.get('name')}")
    print(f"file      : {r.get('__file__')}")
    print(f"machine   : {r.get('machine','?')}")
    print(f"material  : {r.get('material','?')}")
    print(f"tool      : {r.get('tool','?')}")
    print(f"operation : {r.get('operation','?')}")
    print()
    print("params:")
    for k, v in r.get("params", {}).items():
        print(f"  {k:<30} = {v}")
    print()
    print("reasoning:")
    for k, v in r.get("reasoning", {}).items():
        print(f"  {k:<30} : {v}")


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    default_folder = os.path.normpath(os.path.join(here, "..", "recipes"))

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", default=default_folder, help="recipes folder (default: ../recipes)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list all recipes")

    show = sub.add_parser("show", help="show one recipe by name")
    show.add_argument("name", help="recipe name (filename without .json)")

    find = sub.add_parser("find", help="search recipes by criteria")
    find.add_argument("--material", default=None)
    find.add_argument("--tool-d", type=float, default=None, help="tool diameter (mm)")
    find.add_argument("--tool-type", default=None)
    find.add_argument("--op", default=None, help="operation strategy")

    args = ap.parse_args()

    recipes = load_recipes(args.folder)

    if args.cmd == "list":
        list_recipes(recipes)
        return 0

    if args.cmd == "show":
        for r in recipes:
            if r.get("name") == args.name:
                show_recipe(r)
                return 0
        print(f"recipe not found: {args.name}", file=sys.stderr)
        return 1

    if args.cmd == "find":
        r = get_recipe(
            recipes,
            material=args.material,
            tool_diameter_mm=args.tool_d,
            tool_type=args.tool_type,
            operation=args.op,
        )
        if r is None:
            print("no recipe matched the given criteria", file=sys.stderr)
            return 1
        show_recipe(r)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
