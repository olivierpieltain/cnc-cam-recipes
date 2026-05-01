# Feeds & Speeds — the math behind the recipes

The recipes in [`recipes/`](../recipes/) aren't magic numbers. Each value
comes from one of four equations. Knowing them lets you **derive your own
recipe for your machine, your material, your tool** instead of copy-pasting
hoping it's safe.

## 1. Chipload (feed per tooth)

How much material each cutting flute carries per pass.

```
chipload [mm/tooth] = feed [mm/min] / (RPM × number_of_flutes)
```

Why it matters: too low and the tool **rubs** instead of cutting (heat,
work-hardening, fast wear). Too high and the tool **deflects or breaks**.

Typical chipload windows for a Ø3.175 mm (1/8") 2-flute spiral O endmill:

| Material | Chipload (mm/tooth) |
|---|---|
| Soft wood (pine, basswood) | 0.04–0.08 |
| Medium hardwood (cherry, walnut, pear) | 0.025–0.05 |
| Hard wood (oak, maple, ipe) | 0.015–0.03 |
| Acrylic (PMMA) | 0.02–0.04 |
| Aluminium 6061 | 0.012–0.025 |
| Soft brass | 0.015–0.025 |

**Verify your recipe's chipload** before committing:
`chipload = feed_mm_min / (RPM × flutes)`. If it's outside the window,
either bump the feed (preferred) or drop the RPM.

## 2. Material removal rate (MRR)

How fast you're throwing chips, in volume per time.

```
MRR [mm³/min] = stepdown [mm] × stepover [mm] × feed [mm/min]
```

This is the load the spindle has to drive.

## 3. Spindle power required

```
P_required [W] = (MRR [mm³/s]) × (Kc [N/mm²]) / efficiency
                = (MRR [mm³/min] / 60) × Kc / 0.7    (typical efficiency)
```

`Kc` (specific cutting force) is the energy per unit volume of material
removal — material constant.

| Material | Kc (N/mm² ≈ J/mm³) |
|---|---|
| Soft wood | 1.5–2.5 |
| Medium hardwood | 4–5 |
| Hard wood | 5–7 |
| Acrylic | 5–10 |
| Aluminium 6061 | 700–900 |
| Mild steel | 1500–2200 |

If `P_required > P_spindle_continuous`, you'll either stall, bog the
spindle (poor surface), or trip a current limit. **Stay below 70% of
continuous spindle power for a comfortable buffer.**

## 4. Spindle power budget

The Carvera Air's continuous spindle power is **about 200 W**. Pick any
recipe and you should be well below that:

```
P_spindle_budget = 200 W × 0.7 = 140 W
```

For pear (Kc ≈ 5):

```
MRR_max ≈ 140 [W] × 60 / 5 [N/mm²] = 1680 mm³/min
```

So any combination of `stepdown × stepover × feed` that stays under
~1.7 cm³/min in pear is comfortably within budget. The recipe in
[`recipes/pear-3175-flat-roughing-adaptive.json`](../recipes/pear-3175-flat-roughing-adaptive.json)
sits at ~320 mm³/min — about a fifth of budget — because we'd rather waste
spindle than break a 1/8" tool.

## 5. Where adaptive bends the rules

Conventional roughing engages the tool for the full slot width: high MRR,
high engagement, short tool life if you push too hard. **Adaptive clearing
("trochoidal")** keeps radial engagement *narrow* (10–25 % of tool diameter)
and axial engagement *deep* (≥ 1× tool diameter):

- Same MRR with way less radial force on the tool
- More of the flute length engaged → wears evenly
- Stays within spindle power even at 1× tool-diameter stepdown

The recipes here lean heavily on this: stepdown is around 50 % of tool
diameter, optimalLoad (= radial WOC) is around 16 %. That's conservative;
many setups can push to 1× DOC × 25 % WOC.

## 6. Plunge feed

A separate feed for vertical entry. Always lower than cutting feed because
end-mills are bad at plunging.

```
plunge_feed ≈ cutting_feed × 0.15 to 0.30
```

For a 1/8" tool: 60 mm/min plunge for 430 mm/min cutting is ~14 % — toward
the conservative end. **Use helical (G2/G3 helical) ramp entries instead of
straight plunges** wherever the strategy supports it. End-mills with no
center-cutting geometry will rub or break on a vertical plunge.

## 7. Putting it all together — worked example

The "1/8" pear roughing" recipe in this repo:

```
tool       = Ø3.175 mm, 2 flutes, flat
material   = pear (medium hardwood, Kc ≈ 5 N/mm²)
RPM        = 13 000
feed       = 430 mm/min
plunge     = 60 mm/min
stepdown   = 1.5 mm     (47 % of D)
stepover   = 0.5 mm     (16 % of D, "optimalLoad" in Fusion)
```

Verify:

```
chipload = 430 / (13000 × 2) = 0.0165 mm/tooth   → safe for pear (window 0.025–0.05; we're slow side, OK)
MRR      = 1.5 × 0.5 × 430   = 322 mm³/min       → ≈ 5.4 mm³/s
P_req    = 5.4 × 5 / 0.7     ≈ 38 W              → ~20% of 200 W budget ✓
```

Then you can **scale up if your machine has more spindle**: e.g., on a
500 W router, double the MRR (raise feed, stepover, or stepdown) and stay
within budget. See [`adapting-projects.md`](adapting-projects.md) for the
full adaptation flow.
