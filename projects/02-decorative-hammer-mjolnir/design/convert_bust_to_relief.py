"""
Convert the Viking-bust STL into a bas-relief suitable for the hammer
handle panel. Steps:

  1. Load the STL.
  2. Translate so the bust is centered horizontally and standing on Z=0.
  3. Detect which horizontal direction the face points (auto-orient).
  4. Slice off everything behind a plane ~12 mm into the face from the
     front-most point. Result: a "front shell" of the head.
  5. Cap the back of the slab with a flat plane => watertight relief.
  6. Scale to fit the handle panel target box (~30 W x 70 H x 7 D mm).
  7. Save the result; print the final bounding box.

Run with the source STL path as a positional argument or place it next
to this script.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh


SRC = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else r"C:\Users\olivier\AppData\Local\Temp\viking_bust_inspect\obj_1_VIking Head.stl_A.stl"
)
OUT_DIR = Path(__file__).parent
TARGET_W = 25.0   # X (width of handle panel)
TARGET_H = 60.0   # Z (height down the handle)
TARGET_D = 14.0   # Y (depth into handle, post-cap) — dramatic bas-relief
SLICE_DEPTH_MM = 25.0  # take a deep slab of the front so we keep helmet/nose volume

# Override the auto-detected front axis. For this bust the face is on
# -Y in the native frame: the bust has a long beard flowing down the
# chest, which shifts the geometric centroid forward (toward the face),
# making "+Y protrusion past centroid" look LARGER on the back side.
# Counter-intuitive but verified visually in Fusion after import.
MANUAL_FRONT_AXIS = "-Y"

# Pre-slice cropping. The full bust includes a wide shoulder/cape that
# extends past the head's silhouette, which forces the X-scale to
# collapse the head when we fit to a narrow handle panel. Crop to the
# central column (head + helmet + beard + neck) before slicing.
CROP_Z_FRAC = 0.25   # keep top (1 - CROP_Z_FRAC) of bust height
CROP_X_HALF = 35.0   # keep |X| <= CROP_X_HALF mm in original frame


def detect_face_axis(mesh: trimesh.Trimesh) -> tuple[str, int]:
    """Return ('+Y' / '-Y' / '+X' / '-X', axis_index_for_front_dir).

    Heuristic: the nose protrudes furthest from the centroid in the
    "front" direction. We take the centroid (mean of vertices), measure
    how far the bounding box extends past it on each horizontal axis,
    and pick the longest extent. Works for any normal portrait bust.
    """
    centroid = mesh.vertices.mean(axis=0)
    bb_min = mesh.vertices.min(axis=0)
    bb_max = mesh.vertices.max(axis=0)
    # protrusion past centroid on each axis (X and Y only, Z is height)
    extents = {
        "+X": bb_max[0] - centroid[0],
        "-X": centroid[0] - bb_min[0],
        "+Y": bb_max[1] - centroid[1],
        "-Y": centroid[1] - bb_min[1],
    }
    front = max(extents, key=extents.get)
    print(f"  protrusion extents: {extents}")
    print(f"  detected front direction: {front}")
    return front


def slice_front(mesh: trimesh.Trimesh, front: str, depth_mm: float) -> trimesh.Trimesh:
    """Keep only the slab of the bust within `depth_mm` of the front-most point."""
    bb_min = mesh.vertices.min(axis=0)
    bb_max = mesh.vertices.max(axis=0)

    if front == "+Y":
        plane_origin = [0, bb_max[1] - depth_mm, 0]
        plane_normal = [0, -1, 0]   # keep what's on +Y side of the plane
    elif front == "-Y":
        plane_origin = [0, bb_min[1] + depth_mm, 0]
        plane_normal = [0, 1, 0]
    elif front == "+X":
        plane_origin = [bb_max[0] - depth_mm, 0, 0]
        plane_normal = [-1, 0, 0]
    elif front == "-X":
        plane_origin = [bb_min[0] + depth_mm, 0, 0]
        plane_normal = [1, 0, 0]
    else:
        raise ValueError(front)

    # invert the normal because slice_plane keeps the side the normal points away from
    sliced = mesh.slice_plane(plane_origin, np.array(plane_normal) * -1, cap=True)
    if sliced is None or sliced.is_empty:
        raise RuntimeError("Slice produced empty mesh")
    return sliced


def main() -> None:
    print(f"Loading {SRC.name} ({SRC.stat().st_size/1e6:.1f} MB) ...")
    mesh = trimesh.load_mesh(str(SRC))
    print(f"  triangles: {len(mesh.faces):,}")
    print(f"  bbox: {mesh.bounds[1] - mesh.bounds[0]}")

    # 1. center horizontally (X,Y) and stand on Z=0
    bb_min = mesh.vertices.min(axis=0)
    bb_max = mesh.vertices.max(axis=0)
    cx = (bb_min[0] + bb_max[0]) / 2
    cy = (bb_min[1] + bb_max[1]) / 2
    mesh.apply_translation([-cx, -cy, -bb_min[2]])
    print(f"  centered. new bbox: {mesh.bounds[0]} .. {mesh.bounds[1]}")

    # 1b. crop to central head/helmet column BEFORE slicing — this
    # removes wide shoulders that would otherwise force the X-scale
    # to collapse the head's facial features
    print(f"Cropping to head zone (top {(1-CROP_Z_FRAC)*100:.0f}% Z, |X|<={CROP_X_HALF})...")
    pre_crop_tris = len(mesh.faces)
    z_keep = mesh.bounds[1][2] * (1 - CROP_Z_FRAC) * 0 + mesh.bounds[0][2] + (mesh.bounds[1][2] - mesh.bounds[0][2]) * CROP_Z_FRAC
    # remove bottom slab
    mesh = mesh.slice_plane([0, 0, z_keep], [0, 0, 1], cap=True)
    # remove +X side past CROP_X_HALF
    mesh = mesh.slice_plane([CROP_X_HALF, 0, 0], [-1, 0, 0], cap=True)
    # remove -X side past -CROP_X_HALF
    mesh = mesh.slice_plane([-CROP_X_HALF, 0, 0], [1, 0, 0], cap=True)
    print(f"  triangles {pre_crop_tris:,} -> {len(mesh.faces):,}")
    print(f"  bbox after crop: {mesh.bounds[0]} .. {mesh.bounds[1]}")

    # 2. detect face direction (logged for transparency, but we use the
    # manual override since auto-detect is unreliable for full busts)
    print("Detecting face direction (auto, for reference only)...")
    auto_front = detect_face_axis(mesh)
    front = MANUAL_FRONT_AXIS
    if auto_front != front:
        print(f"  WARNING: auto-detected '{auto_front}' but using manual '{front}'")
    else:
        print(f"  auto and manual agree: {front}")

    # 3. rotate so front is +Y (handle convention: panel face = +Y)
    rot = {
        "+Y": np.eye(4),
        "-Y": trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]),
        "+X": trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 0, 1]),
        "-X": trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]),
    }[front]
    mesh.apply_transform(rot)
    print(f"  rotated. new bbox: {mesh.bounds[0]} .. {mesh.bounds[1]}")

    # 4. slice keeping only the front N mm of the (now +Y-facing) face
    print(f"Slicing front {SLICE_DEPTH_MM} mm slab...")
    relief = slice_front(mesh, "+Y", SLICE_DEPTH_MM)
    print(f"  triangles after slice+cap: {len(relief.faces):,}")
    print(f"  bbox after slice: {relief.bounds[0]} .. {relief.bounds[1]}")

    # 4b. drop disconnected components (chest fragment, isolated bits) —
    # keep only the largest connected body so the relief is one clean piece
    components = relief.split(only_watertight=False)
    if len(components) > 1:
        print(f"  found {len(components)} connected components; keeping largest")
        for i, c in enumerate(components):
            print(f"    [{i}] {len(c.faces):,} tris, vol {c.volume:.1f}")
        relief = max(components, key=lambda c: len(c.faces))
        print(f"  kept: {len(relief.faces):,} tris, vol {relief.volume:.1f}")

    # 5. scale to target panel dimensions
    cur_extents = relief.bounds[1] - relief.bounds[0]  # [W, D, H]
    sx = TARGET_W / cur_extents[0]
    sz = TARGET_H / cur_extents[2]
    # use the more restrictive of width/height to preserve aspect ratio
    s_xy = min(sx, sz)
    sy = TARGET_D / cur_extents[1]
    print(f"  scale factors: width={sx:.4f} height={sz:.4f} depth={sy:.4f}")
    print(f"  using uniform XZ scale {s_xy:.4f} (preserves face proportions)")
    print(f"  using independent Y scale {sy:.4f} (compresses depth into panel)")

    relief.apply_scale([s_xy, sy, s_xy])

    # re-center on origin
    bb_min = relief.bounds[0]
    bb_max = relief.bounds[1]
    relief.apply_translation([
        -(bb_min[0] + bb_max[0]) / 2,
        -bb_min[1],            # back of relief on Y=0
        -(bb_min[2] + bb_max[2]) / 2,
    ])

    print(f"\nFinal relief:")
    print(f"  triangles: {len(relief.faces):,}")
    print(f"  bbox: {relief.bounds[1] - relief.bounds[0]}")
    print(f"  is_watertight: {relief.is_watertight}")
    print(f"  volume: {relief.volume:.2f} mm^3")

    # 6. save full-resolution and a decimated preview
    out_full = OUT_DIR / "odin_relief_panel.stl"
    relief.export(str(out_full))
    print(f"\nSaved full-resolution relief to: {out_full.name}")
    print(f"  file size: {out_full.stat().st_size / 1e6:.1f} MB")

    # Optionally save a decimated copy for fast Fusion preview
    # (skipped if fast_simplification isn't installed — full mesh works fine)
    if len(relief.faces) > 50_000:
        try:
            decimated = relief.simplify_quadric_decimation(50_000)
            out_lite = OUT_DIR / "odin_relief_panel_lite.stl"
            decimated.export(str(out_lite))
            print(f"Saved decimated preview ({len(decimated.faces):,} tris) to: {out_lite.name}")
        except (ImportError, ModuleNotFoundError) as e:
            print(f"(decimation skipped: {e})")


if __name__ == "__main__":
    main()
