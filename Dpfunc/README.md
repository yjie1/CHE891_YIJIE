# DPFunc — HPCC Workflow (MSU)

## Goal
Run DPFunc to generate **Gene Ontology (GO) predictions** for our course protein set, producing top-ranked GO terms for:
- Molecular Function (MF)
- Biological Process (BP)
- Cellular Component (CC)

## What we used as input (important)
DPFunc, in our workflow, used **both**:
1) **Protein structures (PDBs)** → converted into structure graphs (primary signal for prediction)
2) **Protein sequences (FASTA)** → used for consistent protein ID mapping and residue-level alignment/bookkeeping

Because our dataset was small (course-scale), we used a **lightweight / practical** DPFunc setup:
- Generated structure graphs from our PDBs on HPCC.
- Used pretrained DPFunc model weights for inference.
- Handled auxiliary features in a minimal way to keep the pipeline runnable for a small dataset while still producing valid GO outputs.

## Where the work happened
- Connected to an HPCC **development node** (e.g., via VS Code Remote-SSH / Open OnDemand terminal) for setup and testing.
- Stored inputs/outputs in a persistent filesystem (e.g., `/mnt/ufs18/...` or scratch), not in HOME, to avoid quota issues.
- For small datasets, graph preparation and prediction can be run on a dev node; for larger batches, submit jobs via `sbatch` on compute nodes.

## Main steps (conceptual)
1) **Organize inputs**
   - Placed predicted protein structures as **PDB files** into the DPFunc PDB input directory.
   - Prepared a **FASTA file** containing the corresponding sequences.
   - Ensured FASTA headers (protein IDs) match the PDB basenames so DPFunc can map proteins consistently.

2) **Create a protein ID list**
   - DPFunc expects a consistent list of protein IDs (“pids”).
   - Generated the pid list from PDB filenames (basenames without `.pdb`).

3) **Generate “PDB points”**
   - DPFunc’s structure pipeline requires residue coordinate points extracted from each PDB.
   - Generated a `pdb_points.pkl` file that stores residue-level coordinate information for each protein.

4) **Generate required mapping/feature placeholder files**
   - DPFunc graph construction expects residue feature inputs and mapping files that link features to each protein ID.
   - For our course-scale run, we created the required placeholder/compatibility files so graph building and prediction could proceed cleanly.

5) **Build structure graphs**
   - Using DPFunc graph scripts, converted each protein into a graph representation.
   - Built graphs for each ontology task (MF/BP/CC). These graphs are the main structural inputs used during prediction.

6) **Download and extract pretrained DPFunc weights**
   - Downloaded pretrained DPFunc weights (e.g., `save_models.tar.gz`) from the project’s provided link.
   - Extracted `.pt` model files into the expected `save_models/` directory so DPFunc can load them during inference.

7) **Run DPFunc prediction**
   - Ran DPFunc inference separately for MF, BP, and CC using pretrained models and the generated graph inputs.
   - Saved prediction outputs (e.g., `*_final.pkl` files) for downstream export.

8) **Export deliverable CSVs**
   - Converted prediction objects into CSV tables (top-ranked GO terms).
   - Exported top-10 GO terms per protein for each ontology.

## Deliverables (final)
These are the files intended for submission / Excel viewing:
- `results/mf_top10.csv`
- `results/bp_top10.csv`
- `results/cc_top10.csv`

Each CSV contains:
- `protein` (protein ID)
- `rank` (1–10)
- `GO` (GO ID)
- `score` (model score used to rank terms)

## Notes / Limitations
- This workflow is designed to be practical for a course-scale dataset on HPCC.
- Full DPFunc pipelines may incorporate richer residue embeddings and domain annotations; here we focus on producing **valid GO predictions** and **exportable deliverables** for the course proteins.
- For large datasets or many proteins, run graph generation and inference on compute nodes via `sbatch` to avoid dev-node time limits.

# Created with the help of ChatGPT 5
