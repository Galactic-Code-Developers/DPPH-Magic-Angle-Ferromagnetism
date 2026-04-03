"""
Magic Angle Helical Magnetic Field Data Export
Creates CSV outputs for reuse in plotting, validation, and supplementary analysis.

Exports:
1. helical_field_lines.csv
   Columns:
   line_id, radius_m, phi0_rad, point_index, x_m, y_m, z_m

2. magnetic_field_vectors.csv
   Columns:
   point_id, x_m, y_m, z_m, bx_unit, by_unit, bz_unit, bx_t, by_t, bz_t,
   field_magnitude_t, cavity_radius_m, bz_base_t, bphi_base_t

The parameterization is matched to the uploaded Three.js visualization:
- cavity radius R = 2.5 mm
- axial field Bz = 1.5 mT
- azimuthal field Bphi = sqrt(2) * Bz
"""

from __future__ import annotations

import csv
import math
from pathlib import Path


R = 0.0025          # meters
BZ = 1.5e-3         # Tesla
BPHI = math.sqrt(2.0) * BZ


def generate_helical_field_lines(
    radii: list[float] | None = None,
    phi0_values: list[float] | None = None,
    n_points: int = 200,
):
    if radii is None:
        radii = [R * 0.3, R * 0.6]
    if phi0_values is None:
        phi0_values = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]

    rows = []
    line_id = 0

    for radius in radii:
        for phi0 in phi0_values:
            for i in range(n_points + 1):
                z = (i / n_points * 2.0 - 1.0) * R
                angle = phi0 + (BPHI / BZ) * (z / radius)
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)

                rows.append({
                    "line_id": line_id,
                    "radius_m": radius,
                    "phi0_rad": phi0,
                    "point_index": i,
                    "x_m": x,
                    "y_m": y,
                    "z_m": z,
                })
            line_id += 1

    return rows


def generate_vector_field(
    grid_n_phi: int = 12,
    grid_n_z: int = 8,
    shell_radius_factor: float = 0.8,
):
    radius = R * shell_radius_factor
    rows = []
    point_id = 0

    for i in range(grid_n_phi):
        phi = (i / grid_n_phi) * 2.0 * math.pi
        for j in range(grid_n_z):
            z = ((j / (grid_n_z - 1)) * 2.0 - 1.0) * radius
            x = radius * math.cos(phi)
            y = radius * math.sin(phi)

            # Field components on the cylindrical shell
            bx = -BPHI * y / radius
            by = BPHI * x / radius
            bz = BZ

            magnitude = math.sqrt(bx * bx + by * by + bz * bz)
            bx_unit = bx / magnitude
            by_unit = by / magnitude
            bz_unit = bz / magnitude

            rows.append({
                "point_id": point_id,
                "x_m": x,
                "y_m": y,
                "z_m": z,
                "bx_unit": bx_unit,
                "by_unit": by_unit,
                "bz_unit": bz_unit,
                "bx_t": bx,
                "by_t": by,
                "bz_t": bz,
                "field_magnitude_t": magnitude,
                "cavity_radius_m": R,
                "bz_base_t": BZ,
                "bphi_base_t": BPHI,
            })
            point_id += 1

    return rows


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    base_dir = Path.cwd()

    helical_lines = generate_helical_field_lines()
    vectors = generate_vector_field()

    lines_path = base_dir / "helical_field_lines.csv"
    vectors_path = base_dir / "magnetic_field_vectors.csv"

    write_csv(lines_path, helical_lines)
    write_csv(vectors_path, vectors)

    print(f"Saved: {lines_path.resolve()}")
    print(f"Saved: {vectors_path.resolve()}")


if __name__ == "__main__":
    main()
