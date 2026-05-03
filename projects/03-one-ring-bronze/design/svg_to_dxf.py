"""
Convert the canonical Wikimedia Ring inscription SVG to a DXF for Fusion import.

Source: https://commons.wikimedia.org/wiki/File:One_Ring_inscription.svg
ViewBox: 0 0 4538 1275

The SVG has 4 <path> elements. Sample each into polylines, scale to fit
the ring (target width 70mm to wrap the 24mm OD outer band ~75mm circumference),
and write a valid R12 ASCII DXF.
"""

from pathlib import Path
import xml.etree.ElementTree as ET
import re
from svgpathtools import parse_path, Path as SvgPath

SVG_PATH = Path(__file__).parent / "one_ring_inscription.svg"
DXF_PATH = Path(__file__).parent / "ring_inscription_official.dxf"

TARGET_WIDTH_MM = 70.0   # fits ring's ~75mm circumference with ~5mm headroom
SAMPLES_PER_SEGMENT = 12 # polyline samples per Bezier segment


def main():
    tree = ET.parse(SVG_PATH)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Strip namespace
    paths = []
    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "path":
            d = elem.get("d")
            if d:
                paths.append(d)
    print(f"Found {len(paths)} <path> elements")

    # Get viewBox
    vb = root.get("viewBox", "0 0 4538 1275").split()
    vb_x, vb_y, vb_w, vb_h = map(float, vb)
    print(f"viewBox: {vb_x},{vb_y} {vb_w}x{vb_h}")

    # SVG has two stacked lines (top = outer inscription, bottom = inner).
    # Use only the top line. Empirical y-split lives in [320, 620] gap.
    Y_SPLIT = 450.0

    all_polylines = []
    for d_str in paths:
        svg_path = parse_path(d_str)
        current = []
        prev_end = None
        for seg in svg_path:
            if prev_end is not None and abs(seg.start - prev_end) > 1e-6:
                if len(current) >= 2:
                    all_polylines.append(current)
                current = []
            if not current:
                current.append((seg.start.real, seg.start.imag))
            for i in range(1, SAMPLES_PER_SEGMENT + 1):
                t = i / SAMPLES_PER_SEGMENT
                pt = seg.point(t)
                current.append((pt.real, pt.imag))
            prev_end = seg.end
        if len(current) >= 2:
            all_polylines.append(current)

    # Top/bottom lines are stacked but some SVG paths span both. Split each polyline
    # wherever it enters the gap region (y in [Y_GAP_LO, Y_GAP_HI]); keep only segments
    # whose first point is above the gap (top line).
    Y_GAP_LO, Y_GAP_HI = 320.0, 620.0

    def split_at_gap(pl):
        runs = []
        cur = []
        for p in pl:
            in_gap = Y_GAP_LO <= p[1] <= Y_GAP_HI
            if in_gap:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) >= 2:
            runs.append(cur)
        return runs

    cleaned = []
    for pl in all_polylines:
        for run in split_at_gap(pl):
            mean_y = sum(p[1] for p in run) / len(run)
            if mean_y < Y_SPLIT:
                cleaned.append(run)
    print(f"After splitting: {len(cleaned)} top-line runs (was {len(all_polylines)})")
    all_polylines = cleaned

    print(f"Total polylines: {len(all_polylines)}")
    print(f"Total vertices: {sum(len(p) for p in all_polylines)}")

    # Scale + flip Y (SVG is y-down, DXF is y-up)
    scale = TARGET_WIDTH_MM / vb_w
    print(f"scale: {scale:.5f} mm/unit")

    transformed = []
    for pl in all_polylines:
        new_pl = [(p[0] * scale, -p[1] * scale) for p in pl]
        transformed.append(new_pl)

    # Compute bbox and center
    xs = [x for pl in transformed for x, y in pl]
    ys = [y for pl in transformed for x, y in pl]
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    print(f"Final size: {width:.2f} x {height:.2f} mm")
    print(f"Centering shift: ({-cx:.2f}, {-cy:.2f})")

    centered = [[(x - cx, y - cy) for x, y in pl] for pl in transformed]

    # SVG fill paths are implicitly closed — force-close every polyline.
    for pl in centered:
        if len(pl) >= 2 and (abs(pl[0][0] - pl[-1][0]) > 1e-3 or abs(pl[0][1] - pl[-1][1]) > 1e-3):
            pl.append(pl[0])

    # Even-odd nesting filter: only keep "outer" contours (those NOT enclosed by an
    # odd number of others). Embossing inner holes would conflict with outer recesses
    # and Fusion errors with "Cannot emboss near some features".
    def point_in_poly(px, py, poly):
        # Ray casting; assumes poly is a list of (x,y) and closed
        inside = False
        n = len(poly)
        j = n - 1
        for i in range(n):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-12) + xi):
                inside = not inside
            j = i
        return inside

    def centroid(pl):
        n = len(pl)
        return (sum(p[0] for p in pl) / n, sum(p[1] for p in pl) / n)

    outers = []
    for i, pl in enumerate(centered):
        cx_i, cy_i = centroid(pl)
        depth = 0
        for j, other in enumerate(centered):
            if i == j: continue
            # Quick bbox cull
            xs2 = [p[0] for p in other]; ys2 = [p[1] for p in other]
            if not (min(xs2) <= cx_i <= max(xs2) and min(ys2) <= cy_i <= max(ys2)):
                continue
            if point_in_poly(cx_i, cy_i, other):
                depth += 1
        if depth % 2 == 0:  # even depth = filled region
            outers.append(pl)
    print(f"After even-odd filter: {len(outers)} outer contours kept (was {len(centered)})")
    centered = outers

    # Write R12 DXF
    L = []
    def code(c, v):
        L.append(str(c))
        L.append(str(v))

    code(0, "SECTION"); code(2, "HEADER")
    code(9, "$ACADVER"); code(1, "AC1009")
    code(9, "$INSBASE"); code(10, 0); code(20, 0); code(30, 0)
    code(9, "$EXTMIN"); code(10, -100); code(20, -100); code(30, 0)
    code(9, "$EXTMAX"); code(10, 100); code(20, 100); code(30, 0)
    code(0, "ENDSEC")

    code(0, "SECTION"); code(2, "TABLES")
    code(0, "TABLE"); code(2, "LAYER"); code(70, 1)
    code(0, "LAYER"); code(2, "INSCRIPTION"); code(70, 0); code(62, 7); code(6, "CONTINUOUS")
    code(0, "ENDTAB")
    code(0, "ENDSEC")

    code(0, "SECTION"); code(2, "BLOCKS"); code(0, "ENDSEC")

    code(0, "SECTION"); code(2, "ENTITIES")
    for pl in centered:
        if len(pl) < 2:
            continue
        code(0, "POLYLINE")
        code(8, "INSCRIPTION")
        code(66, 1)
        code(70, 1 if pl[0] == pl[-1] else 0)
        code(10, 0); code(20, 0); code(30, 0)
        for x, y in pl:
            code(0, "VERTEX")
            code(8, "INSCRIPTION")
            code(10, f"{x:.4f}")
            code(20, f"{y:.4f}")
            code(30, "0.0")
        code(0, "SEQEND"); code(8, "INSCRIPTION")
    code(0, "ENDSEC")
    code(0, "EOF")

    DXF_PATH.write_text("\n".join(L), encoding="ascii")
    print(f"Wrote {DXF_PATH}")


if __name__ == "__main__":
    main()
