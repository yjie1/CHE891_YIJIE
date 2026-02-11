# BioEmu — HPCC 

## Goal
Run BioEmu on the MSU HPCC to generate **protein ensembles** (multiple plausible conformations) for the course proteins, then convert ensemble outputs into a **PyMOL-friendly** format for visualization, animation, and superposition.

## What we used as input
- **Protein sequences** (the same course protein set).
- A persistent HPCC workspace (scratch / research storage) to store ensemble outputs and conversion results.

## Where the work happened
- Connected to an HPCC **development node** (e.g., VS Code Remote-SSH / Open OnDemand terminal) for environment setup, preparing inputs, and submitting jobs.
- Ensemble generation ran as **SLURM jobs** on compute resources (GPU/CPU depending on the BioEmu configuration).
- All outputs were stored in a persistent filesystem (e.g., scratch) so they remained available after disconnects.

## Main steps (conceptual)
1) **Connect and set up a workspace**
   - Created a project folder on HPCC and organized a simple structure (e.g., `inputs/`, `outputs/`, `logs/`, `convert/`).

2) **Prepare sequence inputs**
   - Formatted the protein sequences in the input style expected by BioEmu (single FASTA file or one sequence per file, depending on the workflow).
   - Ensured each protein case had a stable ID for downstream file naming.

3) **Run BioEmu via SLURM**
   - Submitted SLURM jobs (often as an array) so each protein could be processed independently.
   - Monitored progress using queue tools (e.g., `squeue`) and checked log files until completion.

4) **Collect ensemble outputs**
   - BioEmu produced ensemble representations (commonly trajectories plus a reference structure/topology, depending on the run mode).
   - Organized outputs by protein ID for easier post-processing.

5) **Convert ensembles into a PyMOL-friendly multi-model PDB**
   - Extracted a fixed number of representative frames (e.g., 50) from the ensemble.
   - Combined them into a single **multi-model PDB** (e.g., `ensemble_50.pdb`) so PyMOL could load, animate, and superimpose conformations.

6) **Analyze ensembles in PyMOL**
   - Loaded multi-model ensemble PDBs in PyMOL for visualization.
   - Superimposed ensemble members to inspect conformational variability.
   - Optionally compared ensembles against experimental/reference structures when available.

## Deliverables
- For each protein: a multi-model PDB ensemble file (e.g., `ensemble_50.pdb`).
- Optional PyMOL session (`.pse`) and a short written summary of observed conformational variability.

# Created with the help of ChatGPT 5

## Notes
- This repository stores workflow documentation and conversion scripts.
- Large raw trajectories and intermediate files can be excluded from version control when necessary.
