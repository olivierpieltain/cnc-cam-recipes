"""
Convert an STL file into a JSON payload suitable for Fusion 360's
MeshBodies.addByTriangleMeshData(coords, faceIndices, normals, normalIndices).

Coordinates are emitted in centimeters (Fusion's internal unit). Normals
are face normals replicated to all three vertices of each triangle so we
have one normal per triangle.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path

import trimesh


def stl_to_json(stl_path: Path, out_json: Path, decimate_to: int | None = None) -> None:
    print(f"Loading {stl_path.name} ...")
    mesh = trimesh.load_mesh(str(stl_path))
    print(f"  {len(mesh.faces):,} triangles  bbox: {mesh.bounds[1]-mesh.bounds[0]} mm")

    if decimate_to and len(mesh.faces) > decimate_to:
        try:
            import fast_simplification
            import numpy as np
            target_reduction = 1.0 - decimate_to / len(mesh.faces)
            v_new, f_new = fast_simplification.simplify(
                np.asarray(mesh.vertices, dtype=np.float32),
                np.asarray(mesh.faces, dtype=np.int32),
                target_reduction=target_reduction,
            )
            mesh = trimesh.Trimesh(vertices=v_new, faces=f_new)
            print(f"  decimated to {len(mesh.faces):,} triangles")
        except Exception as e:
            print(f"  decimation skipped: {e}")

    # Convert vertices from mm to cm (Fusion internal units)
    verts_cm = (mesh.vertices / 10.0).tolist()
    coords: list[float] = []
    for v in verts_cm:
        coords.extend(v)

    face_indices: list[int] = []
    for f in mesh.faces:
        face_indices.extend(int(i) for i in f)

    # Per-face normals replicated to per-vertex
    normals_cm: list[float] = []
    for n in mesh.face_normals:
        normals_cm.extend(float(c) for c in n)

    payload = {
        "coords": coords,
        "face_indices": face_indices,
        "normals": normals_cm,
        "vertex_count": len(verts_cm),
        "triangle_count": len(mesh.faces),
        "bbox_mm": (mesh.bounds[1] - mesh.bounds[0]).tolist(),
    }
    with open(out_json, "w") as fp:
        json.dump(payload, fp)
    print(f"  saved {out_json.name}  ({out_json.stat().st_size/1e6:.1f} MB)")


def main() -> None:
    HERE = Path(__file__).parent
    jobs = [
        ("odin_relief_panel.stl",          "odin_relief_panel.json"),
        ("odin_relief_panel_mirrored.stl", "odin_relief_panel_mirrored.json"),
    ]
    for stl, js in jobs:
        stl_to_json(HERE / stl, HERE / js, decimate_to=40_000)


if __name__ == "__main__":
    main()
