#!/usr/bin/env python3
"""Render the supplied PGM and binary XYZI PCD without changing map geometry."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def read_pcd(path):
    with path.open("rb") as stream:
        header = {}
        while True:
            line = stream.readline()
            if not line:
                raise ValueError("PCD header has no DATA field")
            parts = line.decode("ascii").split()
            if parts and not parts[0].startswith("#"):
                header[parts[0]] = parts[1:]
            if parts[:1] == ["DATA"]:
                break
        if (header.get("FIELDS") != ["x", "y", "z", "intensity"] or
                header.get("SIZE") != ["4"] * 4 or
                header.get("TYPE") != ["F"] * 4 or
                header.get("COUNT") != ["1"] * 4 or
                header.get("DATA") != ["binary"]):
            raise ValueError("Expected binary PCD with float32 x/y/z/intensity")
        points = np.frombuffer(stream.read(), dtype="<f4").reshape(-1, 4)
        if len(points) != int(header["POINTS"][0]):
            raise ValueError("PCD point count does not match header")
    return points[np.isfinite(points[:, :3]).all(axis=1), :3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_dir", type=Path)
    parser.add_argument("--output", type=Path, default=Path("docs/media"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    with Image.open(args.map_dir / "map_2d.pgm") as image:
        image.convert("L").save(args.output / "map-2d.png")
        print("2D map pixels:", image.size)

    points = read_pcd(args.map_dir / "cloudGlobal.pcd")
    # Fixed sampling only affects the preview; the source cloud is not modified.
    preview = points[::max(1, (len(points) + 159999) // 160000)]
    limits = np.array([points.min(axis=0), points.max(axis=0)])
    fig = plt.figure(figsize=(12, 8), facecolor="#111827")
    ax = fig.add_subplot(111, projection="3d", facecolor="#111827")
    scatter = ax.scatter(*preview.T, c=preview[:, 2], cmap="turbo",
                         s=0.35, alpha=0.8, linewidths=0, rasterized=True)
    ax.set_box_aspect(np.maximum(limits[1] - limits[0], 1))
    ax.view_init(elev=48, azim=-65)
    for axis, label in zip([ax.xaxis, ax.yaxis, ax.zaxis], ["X (m)", "Y (m)", "Z (m)"]):
        axis.set_pane_color((0.07, 0.1, 0.16, 1))
        axis.label.set_color("white")
        axis.set_label_text(label)
    ax.tick_params(colors="white", labelsize=8)
    ax.set_title(f"cloudGlobal.pcd | {len(points):,} points", color="white", pad=12)
    bar = fig.colorbar(scatter, ax=ax, shrink=0.55, pad=0.03)
    bar.set_label("Height Z (m)", color="white")
    bar.ax.tick_params(colors="white")
    fig.savefig(args.output / "map-3d.png", dpi=160, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)
    print("3D bounds (m):", limits.tolist())


if __name__ == "__main__":
    main()
