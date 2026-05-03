# 03 — The One Ring, bronze

> **Status: design imported, sized to spec. CAM next.**

## Goal

A replica of Sauron's One Ring from Tolkien's *Lord of the Rings* — wedding-band proportions, bronze, with the canonical Black Speech inscription engraved around the outer face. The inscription is the iconic two-line "Ash nazg durbatulûk…" Tengwar text Sauron forged into the Ring; this design uses the **outer line only** (the visible inscription on the band, not the inner one that appears in fire).

## Stock

| Part | Material | Stock dimensions | Orientation |
|---|---|---|---|
| Ring | Bronze (alloy TBD) | TBD round bar / disc | Z = ring axis (vertical when machining) |
| Fixture | PLA 3D print | matches ring inner Ø | mandrel — ring slides over it for outer-face work |

## Design — final

- **Form:** ring band, **Ø24 mm OD × 8 mm tall**, rounded outer profile (chamfered shoulders top + bottom, central flat band carries the inscription).
- **Inscription:** canonical Tengwar Black Speech, top line of the Ring inscription, engraved into the outer surface, wrapping ~360° around the band. Geometry is part of the source mesh, not a parametric feature.
- **Source mesh:** [`design/theonering_source.stl`](design/theonering_source.stl) — community model imported and scaled uniformly **×0.780** to land at exactly Ø24 × 8 mm, then translated to center on origin (Z range −4 … +4).
- **Fixture:** `Inner_fixture_3Dprint` occurrence in the Fusion design — a 3D-printed mandrel sized to the ring's inner diameter, used as workholding for outer-face engraving. PLA, printable on any FDM machine.

## Files in `design/`

| File | What it is |
|---|---|
| `OneRing_v2.f3d` | Fusion archive. Contains: scaled mesh body (`theonering_source`), parametric `OneRing_band` body (hidden, kept as historical reference), inner fixture occurrence, construction plane `OD_tangent_+X`, and the `INSCRIPTION` sketch (canonical Wikimedia Tengwar curves, kept as backup geometry). |
| `theonering_source.stl` | Community-sourced STL of the One Ring with full inscription engraved. Imported as-is; scaled in-Fusion. Original file ~30.77 mm OD × 10.25 mm tall. |
| `one_ring_inscription.svg` | Wikimedia Commons [`File:One_Ring_inscription.svg`](https://commons.wikimedia.org/wiki/File:One_Ring_inscription.svg) (CC-BY-SA). Canonical two-line inscription. Kept as a backup reference for an alternate parametric/CAM workflow. |
| `svg_to_dxf.py` | Converter: extracts the top line of the SVG, splits stacked-line geometry, applies even-odd fill rule, writes a Fusion-importable R12 ASCII DXF. Used for the parametric inscription experiment. |
| `ring_inscription_official.dxf` | Output of `svg_to_dxf.py`: 39 outer Tengwar contours, ~59 × 4 mm, ready to import as a sketch. |
| `generate_inscription_dxf.py` | Earlier experiment using `fontTools` + Tengwar Annatar TTF to render the inscription. Did not produce film-faithful glyphs — kept for reference only. Superseded by `svg_to_dxf.py`. |
| `tengwar_inscription.dxf` | Output of the superseded font-based generator. Reference only. |

## Why mesh instead of parametric

The film inscription is hand-drawn cursive Tengwar with connected glyphs and stacked tehtar (vowel marks) above consonants. Reproducing it parametrically in Fusion ran into multiple issues:

- Tengwar fonts aren't visible to Fusion's `SketchText` mid-session (font cache built at startup; restart required).
- Generated DXF curves either had open contours (didn't form profiles) or, once closed, hit Fusion's `Emboss` "cannot emboss near features" error wherever connected letters' outer + inner contours overlapped after engraving.
- Cleaning up the failed attempts repeatedly hung Fusion (timeline recompute storms).

The community mesh has the inscription baked into the geometry as triangles. No emboss feature, no profile detection, no recompute storms. The trade-off is that the inscription is no longer parametric — re-sizing or repositioning the text means editing the mesh externally.

## Hard constraints — verified

- **Inscription lives on a curved outer face** — this is exactly the case Fusion's `Emboss` feature struggles with for connected text. Use mesh-baked geometry or wrap-via-CAM, not Emboss-on-cylinder.
- **Mesh fidelity:** source has 282k triangles; after 0.78 scale the visible inscription detail is ≥0.1 mm — finer than any reasonable engrave V-bit tip can resolve. Mesh is over-spec for the milled part.
- **Inner Ø:** TBD by the wearer's ring size; current STL has ID **~18.5 mm** (after scale, before any clearance allowance for a press-fit on the fixture mandrel).

## Documentation

- TBD — mechanical review, fixture print + size adjustment, bronze-specific tooling notes.

## Pending before CAM

1. **Confirm wearer ring size** → final ID, regenerate fixture mandrel diameter to suit.
2. **Decide on engrave strategy** — the mesh's engraved surface is geometric, so a 3D parallel finish + V-bit pencil over the inscription valleys is the natural recipe (analogous to project 02's runic engravings).
3. **Bronze tooling** — alloy choice (PB1 / SAE 660 / silicon-bronze) drives spindle speed and tool selection. Carvera Air's 200 W spindle ceiling makes light DOC + slow feeds mandatory.
4. **Fixture print** — slice and print the inner-fixture mandrel; verify slip fit before committing to the cut.
5. **Build CAM setups** — minimum two: outer-face engrave (ring on mandrel, axis vertical), inner-face cleanup (ring inverted, edges chamfered).

## Folder layout

```
03-one-ring-bronze/
├── BRIEF.md           this file
├── design/            Fusion .f3d + source mesh + inscription generators
├── cam/               recipe snapshots, post settings (TODO)
├── nc/                posted .cnc files (TODO)
├── documentation/     reviews, fixture sizing notes (TODO)
└── photos/            build photos, fixture photos (TODO)
```

## References

- Source mesh — community STL of The One Ring (downloaded by user; original creator credit TBD when uploader is identified).
- Inscription artwork — [Wikimedia Commons: One Ring inscription](https://commons.wikimedia.org/wiki/File:One_Ring_inscription.svg) (CC-BY-SA), used as the canonical reference for the parametric backup workflow.
- [Project 02 — decorative Mjolnir hammer](../02-decorative-hammer-mjolnir/) — same engrave-via-CAM-on-curved-surface pattern, but Norse runes on flat chamfers rather than Tengwar on a cylinder.

## Decisions taken (closed)

- **Parametric inscription: dropped.** Tengwar transcription via `fontTools` produced disjoint glyphs (tehtar with zero advance width landed in the wrong slots); Wikimedia SVG curves embossed correctly but Fusion's Emboss feature errored on 60+ of 98 nested profiles. Switched to the community mesh.
- **Mesh size: scaled uniformly to Ø24 × 8 mm** (×0.780). Source was Ø30.77 × 10.25 mm.
- **Original parametric body kept hidden, not deleted** — `OneRing_band` (revolved cross-section, 24 mm OD) remains in the timeline for traceability and as a fallback if the mesh approach hits issues at CAM time.
