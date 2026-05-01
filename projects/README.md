# projects

Each subfolder is a complete worked example. The directory is **the
project** — Fusion source design, recipe used, machine and material
context, lessons learned, and (when rights allow) the posted G-code.

## Index

| # | Project | Material | Stock | Tools | Status |
|---|---|---|---|---|---|
| 01 | [`01-relief-pear-150x150x45`](01-relief-pear-150x150x45/) | pear (medium hardwood) | 150 × 150 × 45 mm, both faces pre-surfaced from a 50 mm raw blank | T1: Ø3.175 flat 42 mm flute · T2: Ø3.175 ball 22 mm flute | roughing posted, finishing pending |

## Project folder template

```
NN-short-descriptive-name/
├── README.md            # ← REQUIRED: see template below
├── design/              # ← Fusion source (.f3d). >50 MB → GitHub Release
├── source/              # ← STL / DXF / images the design references
├── cam/                 # ← Optional notes about the CAM setup
│   └── recipe-*.json    # ← The recipes used for each op (copies)
├── nc/                  # ← Optional: posted .cnc for popular machines
│   └── 01_T1_*.cnc
└── photos/              # ← Optional: reference photos of the result
```

## README.md template (drop into every new project)

```markdown
# <Project name>

One-line description.

## What this project does

A few paragraphs of context — what's being made, why it's interesting as
a worked example.

## What I used

- Machine: <make / model — exact spindle / envelope numbers>
- Stock: <dimensions, material, prep done before mounting>
- Tools:
  - T1: <exact tool spec, source, part number if relevant>
  - T2: ...
- Hold-down: <vise / clamps / tape / fixture description>
- WCS: anchor 1 (front-left top corner of stock; X+ right, Y+ away, Z+ up)
- Post processor: <name / version / source>

## Operation order

| # | Op | Strategy | Tool | Recipe | Notes |
|---|---|---|---|---|---|
| 01A | … | adaptive | T1 | `cam/recipe-roughing.json` | … |
| ... |

## How to adapt this to your machine

The most common parameters you'll need to change:

- **Tool numbers** if your changer has different slots
- **Stock dimensions** if your blank differs (edit the `STOCK_*` body in
  the Fusion file; CAM picks up the new bounds)
- **Feeds / RPM** if your spindle differs from the recipe's `machine_floor`
- **Post processor** if you're not on the listed machine

For each, see the relevant section below.

## Hard constraints

- Z lowest cut: <value> mm (validator: `--max-depth <value>`)
- XY excursion: <value> outside <bounds> mm (tool radius excursion)
- Tool flute length must be ≥ <value> mm (deepest cut + ramp)
- Stock backing must be ≥ <value> mm under the cut (rigidity / detach safety)

## Lessons learned

See [`lessons-learned.md`](lessons-learned.md).

## License / attribution

If the design references third-party artwork or models, list the source
and rights here. Don't redistribute artwork you don't have rights to.
```

## Sharing large source files

GitHub doesn't love files > 50 MB. Two options:

1. **GitHub Releases** — upload the `.f3d` as a release asset. The project
   README links to the release. Best for stable, versioned snapshots.
2. **Git LFS** — works for design files in active development. Requires
   contributors to install LFS. Costs against your LFS bandwidth quota.

For a single worked example, prefer Releases.

## Contributing a new project

1. Copy the directory template above into a new `NN-short-name/` folder.
2. Fill in the README, lessons-learned, and any recipe copies.
3. If the design file is < 50 MB, commit it under `design/`. Otherwise
   note in the README that it's attached to release `<tag>`.
4. Open a PR.
