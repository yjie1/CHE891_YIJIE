BioEmu on MSU HPCC – Starter Package
===================================

This folder contains:
- inputs/*.fasta            (your 8 course sequences)
- inputs/protein_list.txt   (used by the SLURM array)
- scripts/run_bioemu_array.sb
- scripts/convert_xtc_to_pdb.py  (makes a PyMOL-friendly multi-model PDB)
- scripts/convert_all.sh

High-level workflow:
1) Create & activate a conda env named "bioemu"
2) pip install bioemu
3) sbatch scripts/run_bioemu_array.sb
4) After jobs finish: bash scripts/convert_all.sh 50
5) Download outputs/*/ensemble_50.pdb to your laptop and open in PyMOL

See the ChatGPT instructions for the detailed step-by-step.
