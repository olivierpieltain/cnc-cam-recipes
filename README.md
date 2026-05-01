# CNC CAM Recipes

An open library of CNC milling projects, parametric recipes, and helper tooling.
Each project ships with the **Fusion 360 source design** so you can open it,
adapt it to your machine, regenerate toolpaths, and run.

## Who this is for

Hobbyists and makers running small-format CNC mills with **at least
Carvera Air-class capability**:

- Working envelope ≥ 360 × 240 × 140 mm
- Spindle ≥ 200 W continuous, ≥ 15 000 RPM
- Reasonably rigid frame (cast / steel-reinforced gantry)
- 3-axis minimum (4-axis projects will be tagged when added)

If your machine is *more* capable, the recipes here are conservative starting
points — see [`docs/feeds-and-speeds.md`](docs/feeds-and-speeds.md) for the
math to scale up. If it's *less* capable, expect to scale stepdown / stepover
down and the recipes may not be safe as-is.

## What's in here

| Folder | What it is |
|---|---|
| [`projects/`](projects/) | **Worked examples.** Each project = Fusion source + CAM recipe + the machine/material/tool context + lessons learned. Some include posted G-code where rights allow. |
| [`recipes/`](recipes/) | Parametric feed / speed / DOC / WOC tables for common `(material, tool, operation)` combinations. Each recipe carries inline reasoning so you can derive your own. |
| [`tools/`](tools/) | Python helpers: G-code safety validator, Fusion 360 recipe applier, recipe lookup module. |
| [`docs/`](docs/) | One-time setup guide, machining concepts, the math, and hard safety constraints. Read once, then every project in here is just "open and adapt." |

## Quickstart

1. **Set up once** — [`docs/setup.md`](docs/setup.md): install Fusion 360, your
   machine's post processor, and the tool library you'll use.
2. **Pick a project** from [`projects/`](projects/) and read its README, especially
   the *"How to adapt to your machine"* section.
3. **Open the .f3d** in Fusion 360 (large source files may be attached to a
   GitHub Release — see the project's README for the link).
4. **Regenerate toolpaths** with your tool numbers / feeds / speeds.
5. **Post and validate** — `python tools/validate_cnc.py path/to/file.cnc`
   — before sending to the machine.

## What this repo is *not*

- Not a redistribution of vendor post processors or tool libraries — those
  belong with their authors (links in [`docs/setup.md`](docs/setup.md)).
- Not opinionated about brand. The author tests on a Makera Carvera Air;
  recipes are framed against that as the *minimum* capability floor, not the
  only target.
- Not a substitute for verifying every G-code file before you run it. Always
  validate on your machine. Broken bits and crashed spindles are expensive.

## License

MIT — see [LICENSE](LICENSE). The recipes, scripts, and docs are free to copy,
adapt, and redistribute. Third-party artwork, models, or vendor files
referenced from a project must follow their own licenses.

## Contributing

Adding a project, recipe, or tool? See
[`projects/README.md`](projects/README.md) for the project template and
[`recipes/README.md`](recipes/README.md) for the recipe schema. PRs welcome.
