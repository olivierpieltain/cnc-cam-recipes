"""
Convert each Norse decoration SVG into a DXF normalized to a target
bounding box in millimeters. The output DXF imports cleanly into Fusion
via sketch.importDXF() at 1:1 scale and lands centered on origin.

Why DXF and not direct SVG import:
  - Fusion's sketch.importSVG has unpredictable scale (depends on the
    SVG's viewBox + transforms) and lands at sketch local origin.
  - DXF carries explicit mm units. We pre-normalize content to a known
    box, so importing at scale=1.0 yields exactly that size.

Strategy:
  1. Parse SVG (svgelements flattens transforms and resolves viewBox).
  2. Walk every path, sample to polyline points (curves -> N segments).
  3. Compute combined bbox; translate to center on (0,0); scale uniformly
     so the longer side fits TARGET_SIZE_MM.
  4. Write LWPOLYLINE entities to DXF with INSUNITS=4 (mm).
"""

from __future__ import annotations

from pathlib import Path
import sys
import math

import ezdxf
from svgelements import SVG, Path as SvgPath, Shape, PathSegment


HERE = Path(__file__).parent
TARGET_SIZE_MM = 30.0  # longer side of bounding box, after normalization
CURVE_SAMPLES = 64     # samples per non-linear path segment

# (svg_filename, output_dxf_filename, optional override target size)
JOBS = [
    # head decoration (long faces)
    ("yggdrasil.svg",            "yggdrasil.dxf",      25.0),
    ("vegvisir.svg",             "vegvisir.dxf",       25.0),
    ("valknut-borromean.svg",    "valknut.dxf",        25.0),
    ("helm-of-awe.svg",          "helm-of-awe.dxf",    30.0),
    ("triquetra.svg",            "triquetra.dxf",      15.0),
    ("celtic-knot-insquare.svg", "celtic-knot.dxf",    25.0),
    # handle decoration (smaller, fit on 13 mm flat band of filleted face)
    ("triquetra.svg",            "triquetra-small.dxf",   11.0),
    ("valknut-borromean.svg",    "valknut-small.dxf",     11.0),
    ("celtic-knot-insquare.svg", "celtic-knot-small.dxf", 11.0),
]


def sample_path(p: SvgPath, samples: int = CURVE_SAMPLES) -> list[list[tuple[float, float]]]:
    """Return one or more polylines as lists of (x,y) tuples.

    A 'Move' splits the path into subpaths -> separate polylines.
    """
    polylines: list[list[tuple[float, float]]] = []
    current: list[tuple[float, float]] = []

    for seg in p:
        cls = seg.__class__.__name__
        if cls == "Move":
            if len(current) >= 2:
                polylines.append(current)
            current = [(seg.end.x, seg.end.y)]
        elif cls == "Line":
            current.append((seg.end.x, seg.end.y))
        elif cls == "Close":
            if current:
                # close the subpath by repeating the start point
                current.append(current[0])
                polylines.append(current)
            current = []
        else:
            # Curve types: CubicBezier, QuadraticBezier, Arc — sample
            for i in range(1, samples + 1):
                t = i / samples
                pt = seg.point(t)
                current.append((pt.x, pt.y))

    if len(current) >= 2:
        polylines.append(current)
    return polylines


def collect_polylines(svg_path: Path) -> list[list[tuple[float, float]]]:
    svg = SVG.parse(str(svg_path), reify=True)
    polys: list[list[tuple[float, float]]] = []
    for elem in svg.elements():
        if isinstance(elem, Shape):
            try:
                p = SvgPath(elem)
            except Exception:
                continue
            if not len(p):
                continue
            polys.extend(sample_path(p))
    return polys


def normalize(polys: list[list[tuple[float, float]]], target: float) -> list[list[tuple[float, float]]]:
    if not polys:
        return polys
    xs = [x for poly in polys for x, _ in poly]
    ys = [y for poly in polys for _, y in poly]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    width = xmax - xmin
    height = ymax - ymin
    if width <= 0 or height <= 0:
        return polys
    # SVG y-axis points down; flip so DXF/CAD-style (y up).
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    scale = target / max(width, height)
    out: list[list[tuple[float, float]]] = []
    for poly in polys:
        out.append([((x - cx) * scale, -(y - cy) * scale) for x, y in poly])
    return out


def write_dxf(polys: list[list[tuple[float, float]]], dst: Path) -> None:
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = ezdxf.units.MM  # INSUNITS = 4
    msp = doc.modelspace()
    for poly in polys:
        # use polyline; closed if first == last (within tolerance)
        is_closed = len(poly) >= 3 and math.dist(poly[0], poly[-1]) < 1e-6
        pts = poly[:-1] if is_closed else poly
        msp.add_lwpolyline(pts, close=is_closed)
    doc.saveas(str(dst))


def main() -> None:
    for svg_name, dxf_name, target in JOBS:
        src = HERE / svg_name
        dst = HERE / dxf_name
        if not src.exists():
            print(f"SKIP {svg_name} (not found)")
            continue
        polys = collect_polylines(src)
        polys = normalize(polys, target)
        if not polys:
            print(f"WARN {svg_name}: no usable paths")
            continue
        write_dxf(polys, dst)
        n_segs = sum(len(p) - 1 for p in polys)
        xs = [x for p in polys for x, _ in p]
        ys = [y for p in polys for _, y in p]
        bbox_w = max(xs) - min(xs)
        bbox_h = max(ys) - min(ys)
        print(f"OK   {svg_name:30s} -> {dxf_name:24s}"
              f"  polys={len(polys):3d} segs={n_segs:5d}"
              f"  bbox={bbox_w:5.1f} x {bbox_h:5.1f} mm")


if __name__ == "__main__":
    main()
