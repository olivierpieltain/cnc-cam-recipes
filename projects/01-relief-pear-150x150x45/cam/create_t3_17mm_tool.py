"""Create a new Ø2.0 × 17mm flute ball nose tool, derived from Makera 2*12mm.

Why: the Makera Carvera Tools v1.4.0 library only ships a Ø2 ball nose
with a 12 mm flute, but the boxed Makera kit's only Ø2 ball is the
17 mm version. Modifying the library tool inline and saving the Fusion
doc does NOT persist — Fusion reverts to the library default on every
load. The reliable workaround is to clone the library tool into a NEW
tool definition (its own GUID, its own description) in a custom local
library, then assign that custom tool to op 04.

Run once: writes
  %LOCALAPPDATA%/Autodesk/CAM360/libraries/Local/Custom/Olivier Custom Tools.json

Then in Fusion: open the project, select op 04, change tool to the new
"2 Flute Ball Nose 2*17mm (Olivier physical)" tool from Local > Custom.
Save the doc — this assignment persists across sessions.
"""
import json, copy, os, uuid
from pathlib import Path

src = Path(r"C:\Users\olivier\AppData\Roaming\Autodesk\CAM360\libraries\Local\Makera Carvera Tools v1.4.0\Makera Ball Endmills.json")
data = json.loads(src.read_text(encoding='utf-8'))

# Find the 2*12mm wood ball (description "2 Flute Ball Nose 2*12mm")
src_tool = None
for t in data["data"]:
    desc = t.get("description", "")
    geo = t.get("geometry", {})
    if "2*12" in desc and geo.get("DC") == 2.0:
        src_tool = t
        break

if not src_tool:
    # Fallback: any Ø2 ball
    for t in data["data"]:
        if t.get("geometry", {}).get("DC") == 2.0:
            src_tool = t
            break

print(f"Source tool: {src_tool['description']}")
print(f"  flute (LCF): {src_tool['geometry']['LCF']}, body (LB): {src_tool['geometry']['LB']}, OAL: {src_tool['geometry']['OAL']}")

# Clone it
new_tool = copy.deepcopy(src_tool)
new_tool["guid"] = str(uuid.uuid4())
new_tool["description"] = "2 Flute Ball Nose 2*17mm (Olivier physical)"
# Update geometry
new_tool["geometry"]["LCF"] = 17       # length cutting flute
new_tool["geometry"]["LB"] = 24        # length body (shoulder)
new_tool["geometry"]["OAL"] = 38       # overall length
new_tool["geometry"]["shoulder-length"] = 17  # match flute
# Update expressions
exprs = new_tool["expressions"]
exprs["tool_description"] = "'2 Flute Ball Nose 2*17mm (Olivier physical)'"
exprs["tool_fluteLength"] = "17 mm"
exprs["tool_shoulderLength"] = "17 mm"
# bodyLength stays via expression
# Update shaft segment heights so the geometry is realistic (flute=17 means shaft starts at 17 from tip)
# Actually shaft segments describe the smooth shank above the flute; total OAL=38, flute=17, so smooth shank = 21
new_tool["shaft"] = {
    "segments": [
        {"height": 21, "lower-diameter": 3.175, "upper-diameter": 3.175}
    ],
    "type": "shaft"
}

# Write the new tool to a NEW library file
out_dir = Path(r"C:\Users\olivier\AppData\Roaming\Autodesk\CAM360\libraries\Local\Custom")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "Olivier Custom Tools.json"

# Wrap in proper Fusion library format
lib = {
    "version": data.get("version", 3),
    "data": [new_tool]
}
out_path.write_text(json.dumps(lib, indent=2), encoding='utf-8')
print(f"Wrote: {out_path}")
print(f"GUID: {new_tool['guid']}")
