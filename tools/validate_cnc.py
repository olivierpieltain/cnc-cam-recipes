#!/usr/bin/env python3
"""
Standalone G-code (.cnc / .nc) safety validator.

Parses a posted G-code file and checks the things that bite you:

  - Tool numbers used (and whether they're consistent)
  - Z range (lowest cut, highest retract)
  - X/Y range (motion excursion outside expected bounds)
  - Feed rates seen
  - Spindle speeds seen
  - M-codes and G-codes used
  - Section markers (tool changes, op boundaries)
  - Final program-end sequence

Usage:
    python validate_cnc.py PATH [--max-depth N] [--min-z N] [--bounds X1,Y1,X2,Y2]
                                [--high-feed N] [--quiet]

Examples:
    python validate_cnc.py work.cnc
    python validate_cnc.py work.cnc --max-depth 35   # error if any Z < -35
    python validate_cnc.py work.cnc --bounds 0,0,150,150 --high-feed 3000

Exit code 0 = all checks passed, 1 = one or more failures.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field

WORD_RE = re.compile(r"([XYZIJKFRSP])(-?\d+\.?\d*)")
TOOL_RE = re.compile(r"\bT(\d+)\b")
GCODE_RE = re.compile(r"\bG(\d+)\b")
MCODE_RE = re.compile(r"\bM(\d+)\b")


@dataclass
class Report:
    path: str
    size_bytes: int = 0
    line_count: int = 0
    x_min: float = float("inf")
    x_max: float = float("-inf")
    y_min: float = float("inf")
    y_max: float = float("-inf")
    z_min: float = float("inf")
    z_max: float = float("-inf")
    tools: set[int] = field(default_factory=set)
    feedrates: set[float] = field(default_factory=set)
    spindle_speeds: set[float] = field(default_factory=set)
    g_codes: set[int] = field(default_factory=set)
    m_codes: set[int] = field(default_factory=set)
    tool_change_lines: list[int] = field(default_factory=list)
    section_markers: list[tuple[int, str]] = field(default_factory=list)
    last_lines: list[str] = field(default_factory=list)


def parse(path: str) -> Report:
    rep = Report(path=path, size_bytes=os.path.getsize(path))

    tail = []
    with open(path, "r", errors="replace") as f:
        for line_no, raw in enumerate(f, start=1):
            rep.line_count += 1
            tail.append(raw.rstrip("\n"))
            if len(tail) > 10:
                tail.pop(0)

            stripped = raw.strip()
            if not stripped:
                continue

            # Parenthesized comment line — record as section if it looks like one
            if stripped.startswith("(") and stripped.endswith(")"):
                marker = stripped[1:-1].strip()
                if marker:
                    rep.section_markers.append((line_no, marker))
                continue

            # Strip inline comments
            line = re.sub(r"\(.*?\)", "", stripped)

            # Tool change lines
            if "M6" in line or "M06" in line:
                rep.tool_change_lines.append(line_no)

            # Word fields
            for letter, value in WORD_RE.findall(line):
                v = float(value)
                if letter == "X":
                    rep.x_min = min(rep.x_min, v); rep.x_max = max(rep.x_max, v)
                elif letter == "Y":
                    rep.y_min = min(rep.y_min, v); rep.y_max = max(rep.y_max, v)
                elif letter == "Z":
                    rep.z_min = min(rep.z_min, v); rep.z_max = max(rep.z_max, v)
                elif letter == "F":
                    rep.feedrates.add(v)
                elif letter == "S":
                    rep.spindle_speeds.add(v)

            for m in TOOL_RE.findall(line):
                rep.tools.add(int(m))
            for m in GCODE_RE.findall(line):
                rep.g_codes.add(int(m))
            for m in MCODE_RE.findall(line):
                rep.m_codes.add(int(m))

    rep.last_lines = tail
    return rep


def humanize(rep: Report) -> str:
    lines = []
    lines.append(f"file       : {rep.path}")
    lines.append(f"size       : {rep.size_bytes:,} bytes ({rep.size_bytes/1024/1024:.2f} MB)")
    lines.append(f"line count : {rep.line_count:,}")
    lines.append("")
    lines.append(f"X range    : {rep.x_min:.3f} .. {rep.x_max:.3f} mm")
    lines.append(f"Y range    : {rep.y_min:.3f} .. {rep.y_max:.3f} mm")
    lines.append(f"Z range    : {rep.z_min:.3f} .. {rep.z_max:.3f} mm")
    lines.append("")
    lines.append(f"tools      : {sorted(rep.tools)}")
    lines.append(f"M6 lines   : {len(rep.tool_change_lines)}  (lines: {rep.tool_change_lines[:5]}{' ...' if len(rep.tool_change_lines)>5 else ''})")
    lines.append(f"feeds (mm/min) : {sorted(rep.feedrates)}")
    lines.append(f"spindle (RPM)  : {sorted(rep.spindle_speeds)}")
    lines.append(f"G-codes seen   : {sorted(rep.g_codes)}")
    lines.append(f"M-codes seen   : {sorted(rep.m_codes)}")
    lines.append("")
    lines.append("section markers (first 10):")
    for ln, marker in rep.section_markers[:10]:
        lines.append(f"  line {ln:>8}  ({marker})")
    if len(rep.section_markers) > 10:
        lines.append(f"  ... +{len(rep.section_markers)-10} more")
    lines.append("")
    lines.append("last 6 lines (program-end sequence):")
    for ln in rep.last_lines[-6:]:
        lines.append(f"  {ln}")
    return "\n".join(lines)


def check(rep: Report, max_depth: float | None, min_z: float | None,
          bounds: tuple[float, float, float, float] | None,
          high_feed: float | None) -> list[str]:
    fails = []

    if max_depth is not None and rep.z_min < -max_depth - 1e-6:
        fails.append(
            f"Z lowest = {rep.z_min:.3f} mm — exceeds --max-depth {max_depth} mm"
        )
    if min_z is not None and rep.z_min < min_z - 1e-6:
        fails.append(f"Z lowest = {rep.z_min:.3f} mm — below --min-z {min_z}")

    if bounds is not None:
        x1, y1, x2, y2 = bounds
        # tool-radius excursion of ~2 mm is normal at adaptive boundaries
        margin = 5.0
        if rep.x_min < x1 - margin:
            fails.append(f"X min = {rep.x_min:.3f} mm — beyond {x1} - {margin} mm tolerance")
        if rep.x_max > x2 + margin:
            fails.append(f"X max = {rep.x_max:.3f} mm — beyond {x2} + {margin} mm tolerance")
        if rep.y_min < y1 - margin:
            fails.append(f"Y min = {rep.y_min:.3f} mm — beyond {y1} - {margin} mm tolerance")
        if rep.y_max > y2 + margin:
            fails.append(f"Y max = {rep.y_max:.3f} mm — beyond {y2} + {margin} mm tolerance")

    if high_feed is not None:
        too_fast = [f for f in rep.feedrates if f > high_feed]
        if too_fast:
            fails.append(f"feed rates above --high-feed {high_feed}: {sorted(too_fast)}")

    # Generic structural checks
    last = " ".join(rep.last_lines).upper()
    if "M30" not in last and "M2" not in last:
        fails.append("program does not end with M30 / M2 — missing program-end marker")
    if not any("M5" in l.upper() for l in rep.last_lines):
        fails.append("spindle never stops at end (no M5 in tail)")
    if not rep.tools:
        fails.append("no tool numbers found anywhere in the file")
    if not rep.tool_change_lines:
        fails.append("no M6 tool-change instruction found")

    return fails


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="path to the .cnc / .nc file")
    ap.add_argument("--max-depth", type=float, default=None,
                    help="fail if any Z is deeper than -<max-depth> mm")
    ap.add_argument("--min-z", type=float, default=None,
                    help="alternative: fail if any Z is below this (negative) value")
    ap.add_argument("--bounds", type=str, default=None,
                    help="X1,Y1,X2,Y2 — fail if motion excursion goes beyond by >5 mm")
    ap.add_argument("--high-feed", type=float, default=None,
                    help="fail if any F > this (mm/min)")
    ap.add_argument("--quiet", action="store_true", help="only print failures and final verdict")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.path):
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2

    rep = parse(args.path)

    bounds = None
    if args.bounds:
        try:
            parts = [float(x) for x in args.bounds.split(",")]
            if len(parts) != 4:
                raise ValueError
            bounds = tuple(parts)  # type: ignore
        except ValueError:
            print(f"--bounds must be X1,Y1,X2,Y2 floats, got {args.bounds}", file=sys.stderr)
            return 2

    fails = check(rep, args.max_depth, args.min_z, bounds, args.high_feed)

    if not args.quiet:
        print(humanize(rep))
        print()

    if fails:
        print("=== FAIL ===")
        for f in fails:
            print(f"  - {f}")
        return 1

    print("=== PASS ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
