# Code: Helical Magnetic Field Visualization & Data Export

This directory contains Python scripts for reproducing the helical magnetic field geometry and exporting field data used in the study:

"Ferromagnetic Phase Transition of DPPH Induced by a Helical Magnetic Field"

---

## Overview

The scripts in this folder replace the original HTML/JavaScript visualization with reproducible Python-based implementations suitable for scientific workflows and archival repositories.

---

## Files

### 1. Visualization Script

magic_angle_helical_field_visualization.py

Generates a 3D visualization of the helical magnetic field inside the cavity.

Features:
- Helical field lines at the magic angle (~54.7°)
- Magnetic field vector representation
- Cavity boundary visualization
- Publication-ready figure output

Run:
    python magic_angle_helical_field_visualization.py

Output:
- magic_angle_helical_field_visualization.png

---

### 2. Data Export Script

magic_angle_helical_field_data_export.py

Exports numerical field data for analysis and reproducibility.

Outputs:
- helical_field_lines.csv
- magnetic_field_vectors.csv

Run:
    python magic_angle_helical_field_data_export.py

---

## Physical Parameters

The scripts use the same parameters as the experimental visualization:

- Cavity radius: R = 2.5 mm
- Axial field: Bz = 1.5 mT
- Azimuthal field: Bφ = √2 · Bz
- Magic angle: θ ≈ 54.74°

---

## Dependencies

Install required packages:

    pip install numpy matplotlib

---

## Purpose

These scripts provide:

- Reproducible visualization of the magnetic field geometry
- Exportable datasets for independent verification
- Supplementary computational support for the experimental results

---

## Notes

- These scripts replace the original browser-based (Three.js) visualization.
- All outputs are deterministic and suitable for inclusion in supplementary materials.
- No external APIs or internet access are required.

---

## Suggested Use

- Use the visualization script to regenerate figures for publications.
- Use the data export script for:
  - numerical validation
  - plotting in external tools (MATLAB, Python, Origin)
  - inclusion in supplementary datasets
