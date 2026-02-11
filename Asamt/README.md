# aSAMt / sam2 — HPCC Workflow (MSU)

## Goal
Generate structural ensembles using aSAMt (sam2), starting from predicted structures (Boltz-derived PDBs), and convert the results into a format viewable in PyMOL.

## What we used as input
- Starting structures as **PDB files** for each protein (converted from Boltz CIF outputs).
- HPCC scratch workspace to organize inputs/outputs.

## Where the work happened
- Setup and job submission were done on an HPCC **development node** via VS Code Remote-SSH.
- Ensemble generation ran as a **SLURM job/array** on compute resources.
- Files lived in scratch so runs continued even if the laptop disconnected.

## Main steps (conceptual)
1) **Connect and set up a workspace**
   - Created a scratch directory with a consistent folder layout.

2) **Prepare starting structures**
   - Ensured each protein had a clean PDB starting structure.
   - Filenames were kept consistent so scripts could map proteins to outputs.

3) **Run aSAMt with SLURM**
   - Submitted a SLURM job (often an array, one protein per task).
   - Monitored progress through the SLURM queue until all tasks completed.

4) **Collect outputs**
   - aSAMt produced a topology structure and an ensemble trajectory for each protein.

5) **Convert trajectory into a multi-model PDB**
   - Extracted a fixed number of frames (e.g., 50) into `ensemble_50.pdb` per protein.

6) **Analyze in PyMOL**
   - Loaded `ensemble_50.pdb` in PyMOL.
   - Superimposed ensemble states and aligned to experimental PDB structures where available.

## Deliverables
- For each protein: `ensemble_50.pdb` (multi-model ensemble file).
- Optional PyMOL `.pse` session and short write-up comparing ensemble variability to experimental structure.

# Created with the help of ChatGPT 5
## Notes
- Repo stores workflow scripts and conversion utilities; large raw trajectories can be excluded from GitHub.
