# One-Time Setup

Read this once. Every project in this repo assumes the conventions below.

## 1. Fusion 360

Install Fusion 360 (Personal or Subscription both work). On the Personal tier,
Fusion limits rapid feed (G0) to cutting feed — projects here are written so
this is harmless; just expect slightly longer cycle times.

## 2. Post processor for your machine

Pick the post for your specific CNC. The `.f3d` source designs in this repo
are post-agnostic — only the final post step depends on your machine.

| Machine | Source | Output extension |
|---|---|---|
| Makera Carvera / Carvera Air | https://github.com/MakeraInc/CarveraProfiles → `Carvera.cps` | `.cnc` |
| Onefinity / Masso | Vendor download or Autodesk's stock posts | `.nc` |
| Grbl-based (3018, OpenBuilds, etc.) | Autodesk's `grbl.cps` | `.nc` |
| Industrial (Haas, Tormach, etc.) | Vendor or Autodesk Post Library | varies |

**Install in Fusion:** Manage → Post Library → My Posts → Local → Import.

> Vendor post processors are not redistributed in this repo — they belong with
> their original authors. Always download the latest from the source.

## 3. Tool library

Import the tool library that matches the tooling you actually own. For Carvera
users, the libraries in
[`MakeraInc/CarveraProfiles/Tool Files/`](https://github.com/MakeraInc/CarveraProfiles)
cover all standard Makera bits.

If you adapt a project to a different tool, edit the operations' tool
selection in Fusion before regenerating.

## 4. Machine profile (optional but recommended)

A machine profile gives Fusion the work envelope, axis directions, and any
machine-specific quirks for simulation.

For Makera, import the matching `.f3d` from `MakeraInc/CarveraProfiles`
(`Makera.Carvera.Air.3-axis.Community.Version.1.17.f3d` etc.) via Fusion's
Machine Library.

> **Known issue:** assigning a machine to a setup via Fusion's Python API
> sometimes fails with *"The requested document is not accessible."* If you
> hit this, assign the machine through the UI — it works there. Don't loop
> retries through the API; it can destabilize Fusion.

## 5. WCS convention used by every project here

Every project sets the work coordinate system at **anchor 1**:

- **X0 Y0** = front-left corner of the stock as it sits clamped on the bed
- **Z0** = top face of the stock

To run a project on your machine: jog to the front-left top corner of your
mounted blank, zero X / Y / Z there, and you're aligned. The CAM origin
inside Fusion uses the same reference, so what you see in simulation is what
the machine cuts.

If your usual workflow uses a different reference (e.g., stock center, or
machine home), see [`concepts.md`](concepts.md) → *Changing WCS reference*.

## 6. File-naming convention

Posted G-code follows `<seq>_T<n>_<DESCRIPTION>.<ext>`:

- `seq` — two-digit sequence in run order (`01`, `02`, …)
- `T<n>` — tool number used by that program
- `DESCRIPTION` — `ALL_CAPS_UNDERSCORES`, identifiable across the shop
- `ext` — `.cnc` for Carvera, `.nc` for most others

Example: `01_T1_ROUGHING_3175x42.cnc`.

## 7. Optional: drive Fusion 360 from scripts / Claude Code

The recipe-applier script in [`tools/apply_recipe.py`](../tools/apply_recipe.py)
runs *inside* Fusion (Tools → Add-Ins → Scripts → green +). If you want to
drive Fusion *from outside* (CI, Claude Code, etc.), the
[fusion360-mcp-bridge](https://github.com/ndoo/fusion360-mcp-bridge) add-in
exposes a local HTTP MCP server.

Entirely optional. Every workflow in this repo also works through the Fusion
UI alone.
