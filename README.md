# CNC CAM Recipes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Target](https://img.shields.io/badge/target-desktop%20CNC%20%28Carvera%20Air--class%2B%29-blue.svg)

> **An open library of CNC milling projects, parametric feed-and-speed
> recipes, and helper tooling — written so you can pull a project, adapt
> the Fusion 360 source to your machine and material, and run.**

```
   recipes/                  projects/
       │                         │
       │  ◄─── reasoning ───►    │  ◄─── concrete examples ───►
       │       (the math)        │      (Fusion source +
       │                         │       lessons learned)
       ▼                         ▼
   ┌─────────────────────────────────────────────┐
   │   docs/   ◄──  one-time setup + concepts  ──►
   │   tools/  ◄──  apply_recipe / validate_cnc ──►
   └─────────────────────────────────────────────┘
                    │
                    ▼
              your machine
```

---

## Who this is for

Hobbyists and makers running small-format CNC mills with **at least
Carvera Air-class capability**:

- Working envelope ≥ 360 × 240 × 140 mm
- Spindle ≥ 200 W continuous, ≥ 15 000 RPM
- Reasonably rigid frame (cast or steel-reinforced gantry)
- 3-axis minimum (4-axis projects are tagged when added)

> [!NOTE]
> **More capable machine?** Recipes here are conservative starting points —
> see [`docs/feeds-and-speeds.md`](docs/feeds-and-speeds.md) for the math
> to scale up.
>
> **Less capable?** Expect to scale stepdown / stepover down. The recipes
> may not be safe as-is on machines below the floor above.

## What's in here

| Folder | What it is |
|---|---|
| [**`projects/`**](projects/) | **Worked examples.** Each project = Fusion source + CAM recipe + the machine/material/tool context + lessons learned. Some include posted G-code where rights allow. |
| [**`recipes/`**](recipes/) | Parametric feed/speed/DOC/WOC tables for common `(material, tool, operation)` combinations. Each recipe carries inline reasoning so you can derive your own. |
| [**`tools/`**](tools/) | Python helpers: G-code safety validator, Fusion 360 recipe applier, recipe lookup module. |
| [**`docs/`**](docs/) | One-time setup guide, machining concepts, the math, and hard safety constraints. Read once, then every project in here is just "open and adapt." |

## Quickstart

1. **Set up once** — [`docs/setup.md`](docs/setup.md): install Fusion 360,
   your machine's post processor, and the tool library you'll use.
2. **Pick a project** from [`projects/`](projects/) and read its README,
   especially the *"How to adapt to your machine"* section.
3. **Open the .f3d** in Fusion 360 (large source files may be attached to
   a GitHub Release — see the project's README).
4. **Regenerate toolpaths** with your tool numbers / feeds / speeds
   (use [`tools/apply_recipe.py`](tools/apply_recipe.py) to bulk-apply a
   recipe to selected operations).
5. **Post and validate** — `python tools/validate_cnc.py path/to/file.cnc`
   — before sending to the machine.

> [!WARNING]
> **Always validate every G-code file before you run it.** The validator
> in `tools/validate_cnc.py` flags common safety failures (Z-bounds, tool
> conflicts, missing program-end). Pair it with the human checklist in
> [`docs/safety-rules.md`](docs/safety-rules.md). Broken bits and crashed
> spindles are expensive.

## Featured projects

| | Project | Material | Stock | Tools | What's interesting |
|---|---|---|---|---|---|
| 🪵 | [01 — Relief in pear, 150×150×45](projects/01-relief-pear-150x150x45/) | medium hardwood | 150×150×45 mm pre-faced from 50 mm raw | T1 flat 3.175×42 · T2 ball 3.175×22 · T3 ball 2.0×12 · V-bit (carving) | three-slab adaptive roughing + 3-pass finishing (main / detail rest / pencil) |

## What this repo is *not*

- **Not a redistribution of vendor post processors or tool libraries** —
  those belong with their original authors. Links to sources in
  [`docs/setup.md`](docs/setup.md).
- **Not opinionated about brand.** The author tests on a Makera Carvera
  Air; recipes use that as the *minimum capability floor*, not the only
  target.
- **Not a substitute for verifying every G-code file before you run it.**

## Contributing

Adding a project, recipe, or tool? See:

- [`projects/README.md`](projects/README.md) for the project template
- [`recipes/README.md`](recipes/README.md) for the recipe schema
- [`tools/README.md`](tools/README.md) for what the helper scripts do

PRs welcome. The bar for a good contribution: another maker should be
able to reproduce your result without a phone call.

## License

[MIT](LICENSE) — recipes, scripts, and docs are free to copy, adapt, and
redistribute. Third-party artwork, models, or vendor files referenced
from a project must follow their own licenses.
