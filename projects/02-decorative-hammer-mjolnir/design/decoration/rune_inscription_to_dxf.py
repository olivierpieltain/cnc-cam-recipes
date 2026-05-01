"""
Render Elder Futhark runic inscriptions as DXF line drawings.

Each rune is defined as a list of polylines in a unit cell [0,1] x [0,1].
At render time, runes are scaled to (cell_w x cell_h) mm, laid out
horizontally with `gap` mm between them, and a small square dot acts
as a word separator. Output is a DXF in mm with INSUNITS=4, importable
into Fusion at 1:1 scale.

Designed for V-bit pencil-pass engraving on the hammer head's long
faces (long 100x50 mm, 5 mm chamfer leaves ~90x40 mm flat zone).

Old Norse spelling conventions used:
  - Y -> ᛁ (Isa)             — Y vowel borrowed from Younger Futhark
  - Æ -> ᚨ (Ansuz)           — fronted A
  - Í/É/Á -> ᛁ/ᛖ/ᚨ            — long vowels collapse to short
  - Ð -> ᚦ (Thurisaz)        — voiced/unvoiced TH conflated in Elder
"""

from __future__ import annotations

from pathlib import Path
import ezdxf

HERE = Path(__file__).parent

# Each rune: list of polylines (each polyline = list of (x,y) points in [0,1]^2).
# Glyphs use a stem at x=0 with arms extending to x>0 where applicable.
RUNES: dict[str, list[list[tuple[float, float]]]] = {
    "F": [  # ᚠ Fehu — stem with two branches angled up-right, contained in cell
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.85), (0.7, 1.0)],
        [(0.0, 0.55), (0.7, 0.70)],
    ],
    "U": [  # ᚢ Uruz
        [(0.0, 0.0), (0.0, 1.0), (0.7, 0.85), (0.7, 0.0)],
    ],
    "TH": [  # ᚦ Thurisaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.7), (0.55, 0.5), (0.0, 0.3)],
    ],
    "A": [  # ᚨ Ansuz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.95), (0.7, 0.80)],
        [(0.0, 0.65), (0.7, 0.50)],
    ],
    "R": [  # ᚱ Raidho
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 1.0), (0.7, 0.7)],
        [(0.0, 0.5), (0.7, 0.7)],
        [(0.0, 0.5), (0.7, 0.0)],
    ],
    "K": [  # ᚲ Kaunan (K/C)
        [(0.0, 0.0), (0.6, 0.5), (0.0, 1.0)],
    ],
    "G": [  # ᚷ Gebo
        [(0.0, 0.0), (0.7, 1.0)],
        [(0.0, 1.0), (0.7, 0.0)],
    ],
    "W": [  # ᚹ Wunjo
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 1.0), (0.5, 0.7), (0.0, 0.4)],
    ],
    "H": [  # ᚺ Hagalaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.7, 0.0), (0.7, 1.0)],
        [(0.0, 0.7), (0.7, 0.3)],
    ],
    "N": [  # ᚾ Naudhiz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.4), (0.6, 0.7)],
    ],
    "I": [  # ᛁ Isa
        [(0.0, 0.0), (0.0, 1.0)],
    ],
    "J": [  # ᛃ Jera
        [(0.0, 0.55), (0.3, 1.0), (0.6, 0.55)],
        [(0.0, 0.45), (0.3, 0.0), (0.6, 0.45)],
    ],
    "EI": [  # ᛇ Eihwaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 0.85), (0.5, 1.0)],
        [(0.0, 0.15), (0.5, 0.0)],
    ],
    "P": [  # ᛈ Pertho
        [(0.0, 0.0), (0.0, 1.0), (0.6, 0.85), (0.6, 0.15), (0.0, 0.0)],
    ],
    "Z": [  # ᛉ Algiz
        [(0.0, 0.0), (0.35, 1.0)],
        [(0.7, 0.0), (0.35, 1.0)],
        [(0.35, 0.0), (0.35, 1.0)],
    ],
    "S": [  # ᛋ Sowilo
        [(0.0, 0.0), (0.5, 0.4), (0.0, 0.6), (0.5, 1.0)],
    ],
    "T": [  # ᛏ Tiwaz
        [(0.35, 0.0), (0.35, 1.0)],
        [(0.0, 0.7), (0.35, 1.0), (0.7, 0.7)],
    ],
    "B": [  # ᛒ Berkano
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.0, 1.0), (0.55, 0.85), (0.0, 0.5)],
        [(0.0, 0.5), (0.55, 0.15), (0.0, 0.0)],
    ],
    "E": [  # ᛖ Ehwaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.7, 0.0), (0.7, 1.0)],
        [(0.0, 1.0), (0.35, 0.7), (0.7, 1.0)],
    ],
    "M": [  # ᛗ Mannaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.7, 0.0), (0.7, 1.0)],
        [(0.0, 1.0), (0.7, 0.5)],
        [(0.7, 1.0), (0.0, 0.5)],
    ],
    "L": [  # ᛚ Laguz
        [(0.0, 0.0), (0.0, 1.0), (0.5, 0.7)],
    ],
    "NG": [  # ᛜ Ingwaz (diamond)
        [(0.35, 0.2), (0.0, 0.5), (0.35, 0.8), (0.7, 0.5), (0.35, 0.2)],
    ],
    "D": [  # ᛞ Dagaz
        [(0.0, 0.0), (0.0, 1.0)],
        [(0.7, 0.0), (0.7, 1.0)],
        [(0.0, 0.0), (0.7, 1.0)],
        [(0.0, 1.0), (0.7, 0.0)],
    ],
    "O": [  # ᛟ Othala — Anglo-Saxon "ēðel" crossed-legs variant
        # Diamond on top
        [(0.35, 0.45), (0.0, 0.7), (0.35, 1.0), (0.7, 0.7), (0.35, 0.45)],
        # Crossed legs from diamond side corners through opposite bottom corners,
        # forming an X under the diamond. The crossing point is centered at
        # (0.35, 0.35) — just below the diamond's bottom apex.
        [(0.0, 0.7), (0.7, 0.0)],
        [(0.7, 0.7), (0.0, 0.0)],
    ],
}


# ASCII letter -> rune key. Multi-char (TH, NG) handled in tokenizer.
CHAR_TO_RUNE = {
    "A": "A", "B": "B", "C": "K", "D": "D", "E": "E", "F": "F", "G": "G",
    "H": "H", "I": "I", "J": "J", "K": "K", "L": "L", "M": "M", "N": "N",
    "O": "O", "P": "P", "Q": "K", "R": "R", "S": "S", "T": "T", "U": "U",
    "V": "F", "W": "W", "X": "K", "Y": "I", "Z": "Z",
}


def tokenize(text: str) -> list[str]:
    """Convert ASCII text to a list of rune keys. Spaces become 'SEP'."""
    tokens: list[str] = []
    s = text.upper()
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == " ":
            tokens.append("SEP")
            i += 1
            continue
        if i + 1 < len(s) and s[i:i+2] in ("TH", "NG"):
            tokens.append(s[i:i+2])
            i += 2
            continue
        if ch in CHAR_TO_RUNE:
            tokens.append(CHAR_TO_RUNE[ch])
        i += 1
    return tokens


def render_inscription(
    text: str,
    cell_w: float = 5.0,
    cell_h: float = 6.0,
    gap: float = 1.0,
    sep_width: float = 2.0,
    sep_dot: float = 1.0,
) -> tuple[list[list[tuple[float, float]]], float]:
    """Lay out runes horizontally, centered on (0,0). Returns (polylines, total_width_mm)."""
    tokens = tokenize(text)
    # measure total width
    total = 0.0
    for t in tokens:
        total += sep_width if t == "SEP" else cell_w
        total += gap
    if tokens:
        total -= gap

    polylines: list[list[tuple[float, float]]] = []
    x = -total / 2
    y0 = -cell_h / 2

    for t in tokens:
        if t == "SEP":
            cx = x + sep_width / 2
            cy = 0.0
            half = sep_dot / 2
            polylines.append([
                (cx - half, cy - half), (cx + half, cy - half),
                (cx + half, cy + half), (cx - half, cy + half),
                (cx - half, cy - half),
            ])
            x += sep_width + gap
            continue
        if t not in RUNES:
            print(f"  warning: rune '{t}' not defined")
            x += cell_w + gap
            continue
        for poly in RUNES[t]:
            scaled = [(x + p[0] * cell_w, y0 + p[1] * cell_h) for p in poly]
            polylines.append(scaled)
        x += cell_w + gap

    return polylines, total


def render_inscription_vertical(
    text: str,
    cell_w: float = 5.0,
    cell_h: float = 5.0,
    gap: float = 0.5,
    sep_height: float = 1.0,
    sep_dot: float = 0.8,
) -> tuple[list[list[tuple[float, float]]], float]:
    """Lay out runes top-to-bottom in a single column, centered on (0,0).

    Runes stay upright (not rotated). First token is at the top; cursor descends.
    Returns (polylines, total_height_mm).
    """
    tokens = tokenize(text)
    total_h = 0.0
    for t in tokens:
        total_h += sep_height if t == "SEP" else cell_h
        total_h += gap
    if tokens:
        total_h -= gap

    polylines: list[list[tuple[float, float]]] = []
    y_cursor = total_h / 2  # start at top
    x0 = -cell_w / 2  # rune cell origin (left edge), centered horizontally

    for t in tokens:
        if t == "SEP":
            cy = y_cursor - sep_height / 2
            half = sep_dot / 2
            polylines.append([
                (-half, cy - half), (half, cy - half),
                (half, cy + half), (-half, cy + half),
                (-half, cy - half),
            ])
            y_cursor -= sep_height + gap
            continue
        if t not in RUNES:
            print(f"  warning: rune '{t}' not defined")
            y_cursor -= cell_h + gap
            continue
        # rune fills cell [x0..x0+cell_w] x [y_cursor - cell_h .. y_cursor]
        for poly in RUNES[t]:
            scaled = [(x0 + p[0] * cell_w, y_cursor - cell_h + p[1] * cell_h) for p in poly]
            polylines.append(scaled)
        y_cursor -= cell_h + gap

    return polylines, total_h


def write_dxf(polylines: list[list[tuple[float, float]]], dst: Path) -> None:
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for poly in polylines:
        is_closed = len(poly) >= 3 and poly[0] == poly[-1]
        pts = poly[:-1] if is_closed else poly
        msp.add_lwpolyline(pts, close=is_closed)
    doc.saveas(str(dst))


# Hávamál stanza 77 — Old Norse, transliterated:
#   Deyr fé,       (Cattle die,)
#   deyja frændr,  (kinsmen die,)
#   deyr sjálfr,   (you yourself die,)
#   en orðstír    (but renown)
#   lifir           (lives)
#
# Split across 4 bands (top + bottom of each ±Y face).
JOBS_HORIZONTAL = [
    ("inscription_PY_top.dxf", "DEYR FE"),
    ("inscription_PY_bot.dxf", "DEYJA FRAENDR"),
    ("inscription_NY_top.dxf", "DEYR SIALFR"),
    ("inscription_NY_bot.dxf", "ORTHSTIR LIFIR"),
]

# Side chamfers (vertical layout) — usable Z extent ~40 mm between top/bot corner chamfers.
# 5 mm cells + 0.5 mm gap → 7 runes = 38 mm; 6 runes = 32.5 mm.
JOBS_VERTICAL = [
    ("inscription_olivier_vertical.dxf", "OLIVIER", {}),
    ("inscription_hamarr_vertical.dxf",  "HAMARR",  {}),  # Old Norse for "hammer"
    # Full handle ±X-face inscription, larger cells to span the whole length.
    # 15 runes + 2 separators @ 8 mm cell + 2 mm gap ≈ 152 mm total height,
    # fits within ~170 mm usable Z range on the handle ±X face.
    ("inscription_handle_full.dxf", "HAMMER OF OLIVIER",
     {"cell_w": 6.0, "cell_h": 8.0, "gap": 2.0, "sep_height": 3.0, "sep_dot": 1.2}),
]


def main() -> None:
    for fname, text in JOBS_HORIZONTAL:
        polys, w = render_inscription(text)
        dst = HERE / fname
        write_dxf(polys, dst)
        n = sum(len(p) - 1 for p in polys)
        print(f"  H  {fname:38s} '{text:20s}' width={w:5.1f}mm  polys={len(polys):3d} segs={n:4d}")

    for fname, text, kwargs in JOBS_VERTICAL:
        polys, h = render_inscription_vertical(text, **kwargs)
        dst = HERE / fname
        write_dxf(polys, dst)
        n = sum(len(p) - 1 for p in polys)
        print(f"  V  {fname:38s} '{text:20s}' height={h:5.1f}mm polys={len(polys):3d} segs={n:4d}")


if __name__ == "__main__":
    main()
