# BioEmu — HPCC Workflow (MSU)

## Goal
Use BioEmu to generate **protein ensembles** (multiple plausible conformations) for the course proteins, then convert the ensemble output into a PyMOL-friendly format for inspection and superposition.

## What we used as input
- Protein sequences (same 8 course proteins).
- HPCC scratch workspace for running and storing ensemble outputs.

## Where the work happened
- Connected to an HPCC **development node** via VS Code Remote-SSH for setup and job submission.
- Ensemble generation ran as **SLURM jobs** on compute resources (GPU/CPU depending on configuration).
- Files were stored in scratch so they remained available after disconnects.

## Main steps (conceptual)
1) **Connect and set up a workspace**
   - Created a scratch folder and organized the project into inputs / outputs / logs.

2) **Prepare sequence inputs**
   - Placed the 8 sequences into an input format expected by BioEmu (FASTA list or one file per protein).

3) **Run BioEmu with SLURM**
   - Submitted a SLURM job (often an array) so each protein could be processed independently.
   - Monitored job state until completion.

4) **Collect ensemble outputs**
   - BioEmu produces an ensemble/trajectory representation (often a trajectory file plus a topology structure).

5) **Convert ensemble into a PyMOL-friendly multi-model PDB**
   - Converted a fixed number of frames (e.g., 50) into a single multi-state PDB file (`ensemble_50.pdb`) so PyMOL could load and animate/superimpose the ensemble.

6) **Analyze in PyMOL**
   - Loaded ensemble PDBs in PyMOL.
   - Superimposed ensemble members and compared to experimental structures where available.

## Deliverables
- For each protein: a multi-model PDB ensemble file (e.g., `ensemble_50.pdb`).
- Optional PyMOL session (`.pse`) and a short written summary of observed variability.

# Created wtih the help of ChatGPT 5

## Notes
- This repo stores the workflow and conversion scripts; large raw trajectories can be excluded from version control if needed.
