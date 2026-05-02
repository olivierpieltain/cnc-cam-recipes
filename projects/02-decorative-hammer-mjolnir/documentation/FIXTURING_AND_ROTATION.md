# Fixturing & Rotation — per-setup mount procedure

Companion to [CAM_PLAN.md](CAM_PLAN.md). This is what the operator
follows at the machine: which face is up, where to clamp, how to
rotate between setups, and where to re-probe Z0.

## Strategy summary

- **Anchor 1 + manual flip + toe-clamps** — no dowel through-holes.
  The stock corner is pressed against Anchor 1's two Ø4 mm pins for
  X/Y registration. Toe-clamps on the tabs hold it down. Between
  setups the stock is unmounted, rotated, re-pressed against Anchor 1,
  re-clamped, re-probed.
- **One face-mill prep per long flank face** (4 prep setups total)
  before any main ops. After prep, all 4 long flank faces are flat
  → repeatable Anchor-1 lateral registration in any of H1–H4.
- **End-square the blank off-machine** (table saw / hand-square)
  before mounting. The squared end becomes the X-pin reference; the
  CAM doesn't square the end (the Carvera Air's vertical-spindle,
  300 mm bed makes end-face milling impractical with a 300 mm-long
  blank).

## Bed-coordinate convention

- **Anchor 1** = the lower-left corner of the Carvera bed, with two
  Ø4 mm dowel pins in 8 mm standoffs that act as the X+Y corner stop.
- **WCS X0 Y0** = the **front-left-top corner of the stock as
  mounted** (against Anchor 1's two pins). **WCS Z0** = top of stock,
  re-probed with the manual XYZ probe at the start of each setup.
- All positions in this doc are stock-local (X, Y, Z relative to that
  front-left-top corner) unless stated otherwise.

## Stock and tab geometry

**Stock**: 50 × 30 × 300 mm rectangular oak blank.
- Stock **50 mm** dimension = aligned with **body Y** (the bust
  side). Milled down to body's 33 mm Y extent.
- Stock **30 mm** dimension = aligned with **body X** (the narrow
  handle width). Milled down to body's 28 mm X extent.
- Stock **300 mm** dimension = aligned with **body Z** (handle long
  axis). Body is 240 mm; tabs are 30 mm at each end. Tabs are
  **removed manually** with a band saw or hand saw after all
  machining is done.

**Tab geometry** (un-machined material at each end):
- Tab 1 spans body Z = -30..0 (pommel-side). Centre at body Z = -15.
- Tab 2 spans body Z = +240..+270 (tenon-side). Centre at body Z = +255.

## Off-machine prep — square one end of the blank

Before mounting on the Carvera:
- Cut the 300 mm-long oak blank to length on a table saw or chop saw,
  ensuring **one end face is square** (perpendicular to long axis).
  This squared end becomes the X-pin reference.
- Verify the end is square with a try-square or combination square.
  ±0.5° is fine for decorative work.
- The blank's long flanks can be sawn-rough — the in-machine PREP
  setups will face-mill them flat.

## H0 — face-mill prep (4 setups, one per long flank)

Goal: produce 4 flat parallel long-flank reference faces so Anchor-1
lateral registration is repeatable across all the H setups. Each prep
setup mounts the stock with one of the 4 long flanks UP, then
face-mills 0.5 mm off it.

| Setup | Face up | Face down | Z0 (top of stock) | Tool | Op |
|---|---|---|---|---|---|
| `H0a_PREP_PY` | body +Y | body -Y | 50 mm above bed | T1 | `H0a_T1_FACE_PY` |
| `H0b_PREP_NY` | body -Y | body +Y | 50 mm above bed | T1 | `H0b_T1_FACE_NY` |
| `H0c_PREP_PX` | body +X | body -X | 30 mm above bed | T1 | `H0c_T1_FACE_PX` |
| `H0d_PREP_NX` | body -X | body +X | 30 mm above bed | T1 | `H0d_T1_FACE_NX` |

**Each prep op**: 2D Face strategy, T1 (3.175 mm 2F flat), 13 000 RPM,
600 mm/min, **0.5 mm DOC** in one pass, full step-over of the stock
top. ~30 seconds of cutting per face.

**Mount sequence** (chained — stock rotates between consecutive
setups, never goes back to a previous orientation):

```
1. Mount body +Y up against Anchor 1 → run H0a_PREP_PY
   (clamp tabs only; toe-clamps lightly; stock rests on the bed
    via the body's -Y face which is sawn-rough → tolerable for prep)

2. Flip 180° about long axis (body -Y up) → run H0b_PREP_NY
   (now body +Y is on the bed, freshly milled flat from step 1
    → stock sits flat-on-flat against the bed)

3. Rotate 90° about long axis (body +X up) → run H0c_PREP_PX
   (body -Y is on the bed-Y pin face, freshly milled flat → great
    lateral registration. Body -X on bed.)

4. Flip 180° about long axis (body -X up) → run H0d_PREP_NX
   (body +X now on the bed, freshly milled flat from step 3.)
```

After H0d, all 4 long flanks are flat. The stock is currently in body
**-X up** orientation — naturally chains into H4.

## Bed-coordinate convention for H1–H4

After PREP, the operator re-presses the stock against Anchor 1
between every setup. The stock corner against the pins is **always
the same physical corner of the (now-trimmed) blank** — the corner
where: (a) the squared end face touches the bed-X pin, (b) the
freshly-milled long flank touches the bed-Y pin, (c) the bed surface
supports the stock from below.

Because all 4 long flanks are flat post-PREP, any of them can serve
as the bed-Y reference depending on which orientation the stock is in.

## H4 — Side D (-X face up, after H0d)

| Item | Spec |
|---|---|
| Stock orientation | body -X up (same as H0d_PREP_NX → no remount) |
| Probe Z0 | top of stock = body's -X face (post-prep at body X = -14.5), 30 mm above bed |
| Hold-down | toe-clamps on the tab tops |
| WCS | bed +Z = body -X, bed +X = body +Z (long axis), bed +Y = body +Y |
| Operations (current) | T1 outer profile contour, T3 V-bit engrave on -X face |
| **Operations to add (UI)** | T2 R6 long-edge fillets on this face's two long edges; T2 R5 pommel-edge fillet on the pommel-end edge of this face |

## H3 — Side C (+X face up, flip from H4)

| Item | Spec |
|---|---|
| Stock orientation | unmount H4, **flip 180° about long axis** (body +X up). Re-press against Anchor 1. |
| Probe Z0 | top of stock = body +X face (post-prep at body X = +14.5), 30 mm above bed |
| Hold-down | toe-clamps on the tab tops |
| WCS | bed +Z = body +X, bed +X = body +Z, bed +Y = body -Y |
| Operations (current) | T1 outer profile contour, T3 V-bit engrave on +X face |
| **Operations to add (UI)** | **T4 wedge kerf** (1.5 mm flat, helical entry, full-width slot, depth -15 mm); T2 R6 fillets on this face's two long edges; T2 R5 pommel-edge fillet on this face |

## H1 — Side A (+Y face up, bust side, rotate 90° from H3)

| Item | Spec |
|---|---|
| Stock orientation | unmount H3, **rotate 90° about long axis** (body +Y up). Re-press against Anchor 1. |
| Probe Z0 | top of stock = body +Y face (post-prep at body Y = +24.5; mesh body extends bbox so stock top in CAM = body Y +28.5), 50 mm above bed |
| Hold-down | toe-clamps on the tab tops; body +Y is up → bust will be carved here, body -Y face on the bed (freshly milled flat) |
| WCS | bed +Z = body +Y, bed +X = body +Z, bed +Y = body +X |
| Operations (current) | T1 outer profile contour, T7 strap-hole bore through (Ø6, helical, depth -42 mm), T8 strap-hole chamfer, T2 Odin parallel finish (3.175 ball), T10 Odin fine finish (1.5 ball), T3 V-bit engrave on +Y face |
| **Operations to add (UI)** | T1 (or T2) Odin **3D adaptive rough** before the parallel finishes; T2 R6 fillets on this face's two long edges; T2 R5 pommel-edge fillet on this face; T5 strap-hole pilot drill (Ø3, peck, partial depth from +Y) BEFORE the T7 bore-out |

## H2 — Side B (-Y face up, flip from H1)

| Item | Spec |
|---|---|
| Stock orientation | unmount H1, **flip 180° about long axis** (body -Y up). Re-press against Anchor 1. |
| Probe Z0 | top of stock = body -Y face (post-prep), 50 mm above bed |
| Hold-down | toe-clamps on the tab tops; body -Y is up → bust face from H1 is now down, suspended above bed (no contact, body +Y face was machined). **Verify ≥5 mm clearance during dry run** since the bust relief sticks out below the body's nominal -Y line. |
| WCS | bed +Z = body -Y, bed +X = body +Z, bed +Y = body -X |
| Operations (current) | T1 outer profile contour, **(SUPPRESSED)** T1 strap hole bore (H1 now bores through), T8 strap chamfer, T2 back-relief parallel finish, T10 fine finish, T3 V-bit engrave on -Y face |
| **Operations to add (UI)** | T2 R6 fillets on this face's two long edges; T2 R5 pommel-edge fillet on this face; T5 strap-hole pilot drill (Ø3, partial depth from -Y face, only if the H1 T7 through-bore proves insufficient — keep optional) |

## After all handle setups

1. Unclamp, lift stock off the bed.
2. Cut off both tabs with a band saw at body Z = 0 (pommel side) and
   Z = 240 (tenon side).
3. Light hand-sanding to clean up the saw cuts; the tab cuts are not
   on a finished face so a 0.5 mm sanding margin is fine.
4. Inspect: outer profile, strap hole, wedge kerf, bust relief,
   engravings, fillets.

## Operator quick-reference (handle, in run order)

| # | Setup | Face up | Z0 above bed | Pin contact face | Notes |
|---|---|---|---|---|---|
| 1 | H0a_PREP_PY | +Y | 50 mm | -X (sawn) | first mount |
| 2 | H0b_PREP_NY | -Y | 50 mm | +X (sawn) | flip 180° |
| 3 | H0c_PREP_PX | +X | 30 mm | -Y (now flat) | rotate 90° |
| 4 | H0d_PREP_NX | -X | 30 mm | +Y (now flat) | flip 180° |
| 5 | H4 | -X | 30 mm | +Y (now flat) | no remount |
| 6 | H3 | +X | 30 mm | -Y (now flat) | flip 180° |
| 7 | H1 | +Y | 50 mm | -X (now flat) | rotate 90° |
| 8 | H2 | -Y | 50 mm | +X (now flat) | flip 180° |

Re-probe Z0 every setup. X/Y origin is set against Anchor 1 every
remount (the sawn-flat reference faces guarantee it returns to the
same position to within the lumber's straightness).

## Head fixturing — preview

The head is 100 × 50 × 50 mm — small enough that a simple toe-clamp
holds it in any of the 6 orientations needed for A1–A6. Per-setup
detail (which face is up, which face touches the X-pin, etc.) follows
the same Anchor-1 + flip pattern.

Head stock arrives at finished outer dimension (no facing the blank);
verify squareness with a try-square before mounting. Each A setup
re-probes Z0.
