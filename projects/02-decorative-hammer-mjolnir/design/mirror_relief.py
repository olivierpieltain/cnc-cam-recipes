"""
Create a Y-mirrored copy of the Odin relief so the back side of the
handle gets the same face protruding in -Y direction.
"""

from pathlib import Path
import numpy as np
import trimesh

HERE = Path(__file__).parent
src = HERE / "odin_relief_panel.stl"
dst = HERE / "odin_relief_panel_mirrored.stl"

mesh = trimesh.load_mesh(str(src))
print(f"Source: {len(mesh.faces):,} tris, bbox: {mesh.bounds[1] - mesh.bounds[0]}")

# Mirror across XZ plane (Y -> -Y)
mirror = trimesh.transformations.reflection_matrix([0, 0, 0], [0, 1, 0])
mesh.apply_transform(mirror)

# After mirror, face normals are inverted; trimesh fixes via face winding
mesh.fix_normals()

print(f"Mirrored: {len(mesh.faces):,} tris, bbox: {mesh.bounds[1] - mesh.bounds[0]}")
print(f"  Y range: [{mesh.bounds[0][1]:.2f}..{mesh.bounds[1][1]:.2f}]")
print(f"  watertight: {mesh.is_watertight}")

mesh.export(str(dst))
print(f"Saved: {dst.name} ({dst.stat().st_size/1e6:.1f} MB)")
