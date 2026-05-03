"""
Generate a DXF of the One Ring inscription using Tengwar Annatar Italic.
Outputs flat curves on the XY plane to be imported into Fusion 360.

Encoding: Dan Smith / Tengwar Annatar
Mode: Black Speech (Quenya-style tehtar-on-following-consonant)
"""

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
import math
import sys
from pathlib import Path

FONT_PATH = Path.home() / "AppData/Local/Microsoft/Windows/Fonts/tngani.ttf"

# Black Speech transcription of the One Ring inscription.
# Quenya-style: tehtar (vowels) sit on the FOLLOWING consonant.
# Word breakdown:
#   ash         = d + a-tehta             (harma + a)
#   nazg        = n + (z + a-tehta) + g   (numen, esse+a, ungwe)
#   durbatuluuk = d + (r+u) + b + (t+a) + (l+u) + (k+u)
#   gimbatul    = g + (m+i) + b + (t+a) + (l+u)         [b standalone, not mb-ligature]
#   thrakatuluk = th + r + (k+a) + (t+a) + (l+u) + (k+u)
#   agh         = (g+a) + h
#   burzum      = b + (r+u) + z + (m+u)
#   ishi        = (sh+i) + carrier+i
#   krimpatul   = k + r + (m+i) + p + (t+a) + (l+u)
#
# Dan Smith consonants: 1=tinco 2=ando 3=thule 5=numen 6=ore 7=romen
#   d=harma(sh) k=esse(z) g=ungwe(g) w=umbar(b) t=malta(m) j=lambe(l) z=quesse(k)
#   q=parma(p) x=anga... wait: anga=s, ungwe=x. Let me recheck.
# Actually per kriskowal/tengwarjs/dan-smith.js:
#   tinco=1 parma=q calma=a quesse=z
#   ando=2 umbar=w anga=s ungwe=x
#   thule=3 formen=e harma=d hwesta=c
#   numen=5 malta=t noldo=g nwalme=b
#   ore=6 vala=y anna=h wilya=n
#   romen=7 arda=u lambe=j alda=m
#   silme=8 silme-nuq=i esse=k esse-nuq=,
#   hyarmen=9 hwesta-sind=o yanta=l ure=.
# Tehtar: a=E e=R i=T o=Y u=U  (also #/$/%/^/& as alt positions)
# Carriers: short=` long=~

# Build the Tengwar Annatar string for the Black Speech inscription.
# Using upper-position tehtar (E R T Y U) which is typical for italic.
INSCRIPTION = (
    "dE 5kEx "                  # Ash nazg
    "26Uw1EjUzU, "              # durbatuluuk  (long uu approximated as repeated U)
    "dE 5kEx "                  # ash nazg
    "xw%1EjU, "                 # gimbatul   (using % for i alt position to avoid clash)
    "dE 5kEx "                  # ash nazg
    "37zE1EjUzU, "              # thrakatuluuk
    "xE9 "                      # agh
    "w6Uk tU-"                  # burzum (split for spacing) - on second thought leave together
)

# Re-do as a clean single string:
INSCRIPTION = (
    "dE 5kEx 26Uw1EjUzU, "
    "dE 5kEx xwTbU1EjU, "       # gimb: x + (w+i) + b... actually mb is one char (umbar=w)
    "dE 5kEx 37zE1EjUzU, "
    "xE9 w6UktU-dT`T z7tTq1EjU"
)
# Simpler attempt -- use only base consonants + tehta upper-position E/R/T/Y/U:
INSCRIPTION = (
    "dE 5kEx 26Uw1EjUzU, "       # ash nazg durbatulûk,
    "dE 5kEx xwT1EjU, "          # ash nazg gimbatul,
    "dE 5kEx 37zE1EjUzU, "       # ash nazg thrakatulûk,
    "xE9 w6UktU-dT`T z7tT1EjU"  # agh burzum-ishi krimpatul
)


def glyph_to_polylines(glyf, glyph_name, scale, x_offset, y_offset):
    """Decompose a glyph's outline into polylines (lists of (x,y) points)."""
    pen = DecomposingRecordingPen(glyf)
    glyph = glyf[glyph_name]
    glyph.draw(pen, glyf)

    polylines = []
    current = []
    pen_pos = (0, 0)

    for op, args in pen.value:
        if op == "moveTo":
            if current:
                polylines.append(current)
            current = [args[0]]
            pen_pos = args[0]
        elif op == "lineTo":
            current.append(args[0])
            pen_pos = args[0]
        elif op == "qCurveTo":
            # quadratic bezier - approximate with 8 segments
            pts = [pen_pos] + list(args)
            for i in range(1, len(pts) - 1):
                p0 = pts[i-1] if i == 1 else pts[i-1]
                p1 = pts[i]
                p2 = pts[i+1]
                if i < len(pts) - 2:
                    # implied on-curve point at midpoint
                    p2 = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
                # sample p0 -> p2 via control p1
                for s in range(1, 9):
                    t = s / 8.0
                    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t*t * p2[0]
                    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t*t * p2[1]
                    current.append((x, y))
            pen_pos = args[-1]
        elif op == "curveTo":
            pts = [pen_pos] + list(args)
            for i in range(0, len(pts) - 3, 3):
                p0, p1, p2, p3 = pts[i], pts[i+1], pts[i+2], pts[i+3]
                for s in range(1, 9):
                    t = s / 8.0
                    x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0]
                    y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]
                    current.append((x, y))
            pen_pos = args[-1]
        elif op == "closePath":
            if current and current[0] != current[-1]:
                current.append(current[0])
            polylines.append(current)
            current = []
        elif op == "endPath":
            if current:
                polylines.append(current)
            current = []

    if current:
        polylines.append(current)

    out = []
    for pl in polylines:
        scaled = [(x_offset + p[0]*scale, y_offset + p[1]*scale) for p in pl]
        out.append(scaled)
    return out


def main(out_path: Path, target_width_mm: float = 70.0, height_mm: float = 4.0):
    font = TTFont(str(FONT_PATH))
    cmap = font.getBestCmap()
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    units_per_em = font["head"].unitsPerEm

    # Choose scale so that 1em = height_mm
    scale = height_mm / units_per_em

    # First pass: lay out and find total width
    cursor = 0.0
    placements = []  # (glyph_name, x_offset)
    for ch in INSCRIPTION:
        codepoint = ord(ch)
        if codepoint not in cmap:
            print(f"WARN: char {ch!r} (U+{codepoint:04X}) not in font cmap; skipping", file=sys.stderr)
            continue
        glyph_name = cmap[codepoint]
        adv, lsb = hmtx[glyph_name]
        placements.append((glyph_name, cursor))
        cursor += adv * scale

    total_width = cursor
    print(f"Natural width at height {height_mm}mm: {total_width:.2f} mm")

    # Second pass: scale horizontally to target_width_mm if it's wider
    if target_width_mm and total_width > 0:
        h_scale = target_width_mm / total_width
        print(f"Scaling horizontally by {h_scale:.3f} to fit {target_width_mm}mm")
    else:
        h_scale = 1.0

    # Generate polylines
    all_polylines = []
    for glyph_name, x_off in placements:
        # We don't horizontally scale the glyph itself, just space them out.
        # (Better: scale uniformly. Let's keep glyphs un-distorted and adjust spacing only
        # if we'd otherwise stretch letters. Actually we should uniformly scale.)
        pass

    # Re-layout with uniform scaling
    final_scale = scale * h_scale
    cursor = 0.0
    all_polylines = []
    for ch in INSCRIPTION:
        codepoint = ord(ch)
        if codepoint not in cmap:
            continue
        glyph_name = cmap[codepoint]
        adv, lsb = hmtx[glyph_name]
        polylines = glyph_to_polylines(glyf, glyph_name, final_scale, cursor, 0.0)
        all_polylines.extend(polylines)
        cursor += adv * final_scale

    # Compute final bounds
    if all_polylines:
        xs = [x for pl in all_polylines for x,y in pl]
        ys = [y for pl in all_polylines for x,y in pl]
        print(f"Final bbox: x=[{min(xs):.2f},{max(xs):.2f}] y=[{min(ys):.2f},{max(ys):.2f}]")
        print(f"Width: {max(xs)-min(xs):.2f} mm, Height: {max(ys)-min(ys):.2f} mm")

    # Center the layout horizontally and vertically
    if all_polylines:
        cx = (min(xs) + max(xs)) / 2
        cy = (min(ys) + max(ys)) / 2
        all_polylines = [[(x-cx, y-cy) for x,y in pl] for pl in all_polylines]

    # Write proper R12 ASCII DXF with HEADER, TABLES, BLOCKS, ENTITIES sections
    L = []
    def code(c, v):
        L.append(str(c))
        L.append(str(v))

    # HEADER
    code(0,"SECTION"); code(2,"HEADER")
    code(9,"$ACADVER"); code(1,"AC1009")
    code(9,"$INSBASE"); code(10,0); code(20,0); code(30,0)
    code(9,"$EXTMIN"); code(10,-100); code(20,-100); code(30,0)
    code(9,"$EXTMAX"); code(10,100); code(20,100); code(30,0)
    code(0,"ENDSEC")

    # TABLES (minimum: LAYER table)
    code(0,"SECTION"); code(2,"TABLES")
    code(0,"TABLE"); code(2,"LAYER"); code(70,1)
    code(0,"LAYER"); code(2,"INSCRIPTION"); code(70,0); code(62,7); code(6,"CONTINUOUS")
    code(0,"ENDTAB")
    code(0,"ENDSEC")

    # BLOCKS (empty)
    code(0,"SECTION"); code(2,"BLOCKS"); code(0,"ENDSEC")

    # ENTITIES — use POLYLINE entities (R12 standard, more compatible than LWPOLYLINE)
    code(0,"SECTION"); code(2,"ENTITIES")
    for pl in all_polylines:
        if len(pl) < 2:
            continue
        code(0,"POLYLINE")
        code(8,"INSCRIPTION")
        code(66,1)        # vertices follow
        code(70, 1 if pl[0] == pl[-1] else 0)  # closed flag
        code(10,0); code(20,0); code(30,0)
        for x, y in pl:
            code(0,"VERTEX")
            code(8,"INSCRIPTION")
            code(10, f"{x:.4f}")
            code(20, f"{y:.4f}")
            code(30, "0.0")
        code(0,"SEQEND"); code(8,"INSCRIPTION")
    code(0,"ENDSEC")
    code(0,"EOF")
    lines = L

    out_path.write_text("\n".join(lines), encoding="ascii")
    print(f"Wrote {out_path} ({len(all_polylines)} polylines)")


if __name__ == "__main__":
    out = Path(__file__).parent / "tengwar_inscription.dxf"
    main(out, target_width_mm=70.0, height_mm=4.5)
