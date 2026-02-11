# Boltz — HPCC Workflow (MSU)

## Goal
Run Boltz on the MSU HPCC to generate predicted **3D protein structures** for our course proteins, then visualize the outputs in PyMOL (and convert formats when needed for downstream tools).

## What we used as input
- **Protein sequences** (the course protein sequences).
- A persistent working directory on HPCC (scratch / research storage) to organize inputs and outputs.

## Where the work happened
- Connected to an HPCC **development node** (e.g., VS Code Remote-SSH / Open OnDemand terminal) for file editing, setup, and job submission.
- The actual structure prediction ran as a **SLURM batch job** on HPCC compute resources (CPU/GPU depending on configuration).
- Inputs/outputs were stored on a persistent filesystem (e.g., scratch) so they remained available after disconnecting.

## Main steps (conceptual)
1) **Connect and create a workspace**
   - Logged into an HPCC dev node.
   - Created a project folder with a simple layout (e.g., `inputs/`, `yamls/`, `outputs/`, `logs/`).

2) **Prepare sequence inputs**
   - Formatted protein sequences in the input format required by Boltz (FASTA and/or YAML depending on the run mode).
   - Treated each protein as an independent prediction case to keep bookkeeping simple.

3) **Run Boltz via SLURM**
   - Used a SLURM job script so the compute-heavy steps ran on allocated compute nodes.
   - Monitored the run using queue tools (e.g., `squeue`) and checked log files for progress/errors.

4) **Collect predicted structures**
   - After completion, gathered Boltz prediction outputs from the designated output directory.
   - Outputs are commonly written as **mmCIF (.cif)** structure files (plus metadata depending on the configuration).

5) **Visualize and/or convert for PyMOL**
   - Opened predicted structures in PyMOL for visualization.
   - When required by downstream tools, converted mmCIF outputs to **PDB (.pdb)** (e.g., by loading in PyMOL and saving as PDB, or using a converter).

## Deliverables
- Predicted structure files for each protein (Boltz outputs, typically `.cif`, plus optional `.pdb` copies).
- Optional PyMOL session file (`.pse`) for visualization, alignment, and comparison.

## Notes
- This repository is intended to store **workflow documentation and scripts**.
- Large model caches, temporary files, and downloaded weights should be stored on HPCC storage (not committed to GitHub).

# README created with the help of ChatGPT 5
