"""
Magic Angle Helical Magnetic Field Visualization
Converted into a standalone Python script for repository use.

This script reproduces the helical magnetic-field geometry shown in the
uploaded HTML/JS visualization using matplotlib in 3D.

Parameters are chosen to match the uploaded visualization:
- cavity radius R = 2.5 mm
- axial field Bz = 1.5 mT
- azimuthal field Bphi = sqrt(2) * Bz
- magic angle ~ 54.7 degrees
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# -----------------------------
# Parameters
# -----------------------------
R = 0.0025  # cavity radius, meters (2.5 mm)
BZ = 1.5e-3  # axial magnetic field, Tesla
BPHI = math.sqrt(2.0) * BZ  # azimuthal magnetic field, Tesla
TITLE = "Helical Magnetic Field in Empty Cavity\nMagic Angle: 54.7°, Bφ/Bz = √2 ≈ 1.41"


def generate_helical_line(radius: float, phi0: float, n_points: int = 200) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate one helical field line inside the cavity."""
    z = np.linspace(-R, R, n_points)
    angle = phi0 + (BPHI / BZ) * (z / radius)
    x = radius * np.cos(angle)
    y = radius * np.sin(angle)
    return x, y, z


def generate_vector_field(grid_n_phi: int = 12, grid_n_z: int = 8, shell_radius_factor: float = 0.8) -> tuple[np.ndarray, ...]:
    """Generate a sparse vector field on a cylindrical shell inside the cavity."""
    radius = R * shell_radius_factor
    phis = np.linspace(0, 2 * np.pi, grid_n_phi, endpoint=False)
    zs = np.linspace(-radius, radius, grid_n_z)

    xs, ys, zzs, u, v, w = [], [], [], [], [], []

    for phi in phis:
        for z in zs:
            x = radius * np.cos(phi)
            y = radius * np.sin(phi)

            bx = -BPHI * y / radius
            by = BPHI * x / radius
            bz = BZ

            norm = math.sqrt(bx * bx + by * by + bz * bz)
            bx /= norm
            by /= norm
            bz /= norm

            xs.append(x)
            ys.append(y)
            zzs.append(z)
            u.append(bx)
            v.append(by)
            w.append(bz)

    return tuple(np.array(arr) for arr in (xs, ys, zzs, u, v, w))


def plot_cavity_boundary(ax: plt.Axes) -> None:
    """Plot a faint spherical cavity boundary."""
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 24)
    x = R * np.outer(np.cos(u), np.sin(v))
    y = R * np.outer(np.sin(u), np.sin(v))
    z = R * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x, y, z, rstride=3, cstride=3, linewidth=0.5, alpha=0.18)


def add_axes(ax: plt.Axes, length: float | None = None) -> None:
    """Draw coordinate axes."""
    if length is None:
        length = 2 * R

    ax.plot([0, length], [0, 0], [0, 0], linewidth=2)
    ax.plot([0, 0], [0, length], [0, 0], linewidth=2)
    ax.plot([0, 0], [0, 0], [0, length], linewidth=2)

    ax.text(length * 1.05, 0, 0, "X", fontsize=12, weight="bold")
    ax.text(0, length * 1.05, 0, "Y", fontsize=12, weight="bold")
    ax.text(0, 0, length * 1.05, "Z", fontsize=12, weight="bold")


def create_figure() -> tuple[plt.Figure, plt.Axes]:
    """Create the 3D figure."""
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title(TITLE, pad=18, fontsize=14, weight="bold")

    # Helical field lines
    radii = [R * 0.3, R * 0.6]
    phi0_values = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
    for radius in radii:
        for phi0 in phi0_values:
            x, y, z = generate_helical_line(radius, phi0)
            ax.plot(x, y, z, linewidth=2)

    # Vector field
    xs, ys, zzs, u, v, w = generate_vector_field()
    ax.quiver(xs, ys, zzs, u, v, w, length=R * 0.22, normalize=True)

    # Boundary and axes
    plot_cavity_boundary(ax)
    add_axes(ax)

    # Formatting
    lim = 1.1 * R
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)

    return fig, ax


def save_figure(output_path: str | Path = "magic_angle_helical_field_visualization.png") -> Path:
    """Render and save the figure."""
    output_path = Path(output_path)
    fig, _ = create_figure()
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


def main() -> None:
    output_path = save_figure()
    print(f"Saved visualization to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
