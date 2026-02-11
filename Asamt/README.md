# aSAMt / sam2 — HPCC MSU

## Goal
Run aSAMt (sam2) on the MSU HPCC to generate **structural ensembles** starting from predicted structures (Boltz-derived PDBs), then convert the ensemble outputs into **PyMOL-viewable** multi-model PDB files for visualization and superposition.

## What we used as input
- Starting structures as **PDB files** for each protein (typically converted from Boltz mmCIF outputs).
- A persistent HPCC workspace (scratch / research storage) to organize inputs, outputs, and logs.

## Where the work happened
- Environment setup, file preparation, and job submission were performed on an HPCC **development node** (e.g., VS Code Remote-SSH / Open OnDemand terminal).
- Ensemble generation ran as **SLURM jobs** (often an array: one protein per task) on compute resources.
- Files were stored on a persistent filesystem (e.g., scratch) so runs were not affected by local disconnects.

## Main steps (conceptual)
1) **Connect and set up a workspace**
   - Created a project directory on HPCC with a consistent folder layout (e.g., `inputs/`, `outputs/`, `logs/`, `convert/`).

2) **Prepare starting structures**
   - Ensured each protein had a clean, valid PDB starting structure.
   - Standardized filenames/IDs so scripts could consistently map proteins to outputs.

3) **Run aSAMt via SLURM**
   - Submitted a SLURM job (often an array) to process proteins independently.
   - Monitored progress using queue tools (e.g., `squeue`) and checked log files for completion/errors.

4) **Collect outputs**
   - aSAMt produced ensemble results per protein (commonly a reference/topology structure plus a trajectory/ensemble file, depending on configuration).

5) **Convert ensemble outputs into a multi-model PDB**
   - Selected a fixed number of frames (e.g., 50) from the trajectory.
   - Wrote a single **multi-model PDB** per protein (e.g., `ensemble_50.pdb`) for easy loading/animation in PyMOL.

6) **Analyze ensembles in PyMOL**
   - Loaded `ensemble_50.pdb` in PyMOL for visualization.
   - Superimposed ensemble members and optionally aligned them to experimental/reference structures when available.

## Deliverables
- For each protein: `ensemble_50.pdb` (multi-model ensemble file).
- Optional PyMOL `.pse` session and a short write-up summarizing ensemble variability and any comparison to experimental structures.

# Created with the help of ChatGPT 5

