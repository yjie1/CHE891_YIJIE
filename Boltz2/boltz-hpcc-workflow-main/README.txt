
# Boltz — HPCC Workflow (MSU)

## Goal
Use Boltz on the MSU HPCC to generate predicted 3D protein structures for the 8 course proteins, then view (and optionally convert) the structures for downstream use in PyMOL.

## What we used as input
- Protein sequences (the 8 course protein sequences).
- A working directory on HPCC scratch for organizing inputs and outputs.

## Where the work happened
- We connected to an HPCC **development node** (through VS Code Remote-SSH). This was used for editing files, preparing inputs, and submitting jobs.
- The heavy computation ran as a **SLURM job** on HPCC compute resources.
- All files were kept in **/mnt/scratch/<netid>/** so they persisted beyond the session.

## Main steps (conceptual)
1) **Connect and set up a workspace**
   - Connected via VS Code Remote-SSH to an HPCC dev node.
   - Created a scratch folder for the project and a simple folder layout (inputs / outputs / logs).

2) **Prepare sequence inputs**
   - Took the 8 protein sequences and formatted them for Boltz (FASTA/YAML depending on configuration).
   - Each protein was treated as a separate input case.

3) **Run Boltz through SLURM**
   - Used an HPCC batch script (SLURM) so the real computation ran on compute hardware.
   - Monitored job status using the queue tools until the run completed.

4) **Collect predicted structures**
   - Boltz produced predicted structures (commonly in **mmCIF (.cif)** format) and placed them into the outputs folder.

5) **View and/or convert for PyMOL**
   - Opened the resulting structures in PyMOL for visualization and comparison.
   - If a downstream tool required PDB, the mmCIF outputs were converted to **.pdb** (either through PyMOL saving or a converter).

## Deliverables
- Predicted structure files for each protein (Boltz outputs, usually `.cif`, plus optional `.pdb` copies).
- Optional PyMOL session file (`.pse`) showing aligned/compared structures.

## Notes
- The repo is intended to store workflow documentation and scripts; large caches/weights are not committed.

# README created with the help of ChatGPT 5
