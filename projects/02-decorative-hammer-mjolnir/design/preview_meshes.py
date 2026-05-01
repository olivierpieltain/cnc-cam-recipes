"""
Render PNG previews of the original Viking bust and the converted relief
from 4 horizontal directions (+X, -X, +Y, -Y) so we can visually verify
which side is the "face" and whether the conversion preserved it.

Uses matplotlib's 3D plotting with face-color = Z-depth (depth shading)
for a quick silhouette + relief preview without needing OpenGL.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import trimesh


HERE = Path(__file__).parent

BUST = Path(r"C:\Users\olivier\AppData\Local\Temp\viking_bust_inspect\obj_1_VIking Head.stl_A.stl")
RELIEF = HERE / "odin_relief_panel.stl"


def render_views(mesh: trimesh.Trimesh, label: str, decimate_to: int | None = 30_000) -> None:
    if decimate_to and len(mesh.faces) > decimate_to:
        # subsample triangles uniformly (quick preview, no quadric decimation needed)
        stride = max(1, len(mesh.faces) // decimate_to)
        keep = np.arange(0, len(mesh.faces), stride)
        faces = mesh.faces[keep]
        verts = mesh.vertices
    else:
        verts = mesh.vertices
        faces = mesh.faces

    views = [
        ("+Y (front-default)", lambda v: (v[:, 0], v[:, 2]), lambda v: v[:, 1]),
        ("-Y (back)", lambda v: (-v[:, 0], v[:, 2]), lambda v: -v[:, 1]),
        ("+X (right)", lambda v: (-v[:, 1], v[:, 2]), lambda v: v[:, 0]),
        ("-X (left)", lambda v: (v[:, 1], v[:, 2]), lambda v: -v[:, 0]),
    ]

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    for ax, (title, project_uv, project_depth) in zip(axes, views):
        u, w = project_uv(verts)
        depth = project_depth(verts)

        # build face polygons in projected 2D
        face_uvs = np.column_stack([u[faces].reshape(-1, 1), w[faces].reshape(-1, 1)]).reshape(-1, 3, 2)
        face_depths = depth[faces].mean(axis=1)

        # paint front-facing triangles only (depth > 0 means in front of the centroid plane)
        order = np.argsort(face_depths)  # back to front for proper painter's algo
        sorted_polys = face_uvs[order]
        sorted_depths = face_depths[order]

        norm = plt.Normalize(vmin=sorted_depths.min(), vmax=sorted_depths.max())
        colors = cm.viridis(norm(sorted_depths))

        coll = PolyCollection(sorted_polys, facecolors=colors, edgecolors="none", linewidths=0)
        ax.add_collection(coll)
        ax.set_xlim(u.min() - 5, u.max() + 5)
        ax.set_ylim(w.min() - 5, w.max() + 5)
        ax.set_aspect("equal")
        ax.set_title(f"{label}\n{title}")
        ax.set_xticks([])
        ax.set_yticks([])

    out = HERE / f"preview_{label}.png"
    plt.tight_layout()
    plt.savefig(out, dpi=110, bbox_inches="tight")
    plt.close()
    print(f"  saved {out.name}")


def main() -> None:
    print("Rendering original bust (decimated for speed)...")
    bust = trimesh.load_mesh(str(BUST))
    bust.apply_translation(-bust.vertices.mean(axis=0))
    render_views(bust, "bust", decimate_to=80_000)

    print("Rendering converted relief...")
    relief = trimesh.load_mesh(str(RELIEF))
    relief.apply_translation(-relief.vertices.mean(axis=0))
    render_views(relief, "relief", decimate_to=None)


if __name__ == "__main__":
    main()
