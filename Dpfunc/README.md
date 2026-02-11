

# DPFunc — HPCC Workflow (MSU)

## Goal
Run DPFunc to generate **Gene Ontology (GO) predictions** for the 8 course proteins, producing top-ranked GO terms for:
- Molecular Function (MF)
- Biological Process (BP)
- Cellular Component (CC)

## What we used as input (important)
DPFunc, in our workflow, used **both**:
1) **Protein structures (PDBs)** → converted into structure graphs (this was the main “real” signal)
2) **Protein sequences (FASTA)** → used for residue-level features alignment and bookkeeping

Because this was a small class dataset, we ran a lightweight version of the DPFunc pipeline:
- We generated the structure graphs from our PDBs on HPCC.
- We used pretrained DPFunc weights.
- Some auxiliary features (InterPro / full ESM embeddings) were handled in a minimal way to allow the pipeline to run on our small dataset.

## Where the work happened
- Connected to an HPCC **development node** (VS Code Remote-SSH) for setup and file editing.
- All data lived in scratch (`/mnt/scratch/<netid>/...`) so it persisted across disconnects.
- DPFunc graph preparation and prediction were run on the dev node (small dataset), using the dpfunc conda environment.

## Main steps (conceptual)
1) **Organize inputs**
   - Placed the 8 predicted protein structures as **PDB files** in the DPFunc PDB input folder.
   - Placed the 8 sequences in a **FASTA file**, with headers matching the PDB filenames (so DPFunc could map proteins consistently).

2) **Create a protein ID list**
   - DPFunc relies on a consistent list of protein IDs (“pids”). We generated that pid list from the PDB basenames.

3) **Generate “PDB points”**
   - DPFunc’s structure pipeline requires residue coordinate points extracted from each PDB. We generated a `pdb_points.pkl` file describing residue coordinates.

4) **Generate residue feature placeholders + required mapping files**
   - DPFunc’s graph code expects residue feature files and a mapping file indicating which feature-part belongs to which protein. We created those required files so graph construction and prediction could proceed for our small dataset.

5) **Build structure graphs**
   - Using DPFunc’s graph scripts, we converted each protein into a graph representation (one set each for MF/BP/CC). These graphs are the structural inputs used at prediction time.

6) **Download and extract pretrained DPFunc weights**
   - Downloaded DPFunc pretrained weights (`save_models.tar.gz`) from the link provided by the project.
   - Extracted the `.pt` model files into the `save_models/` folder so DPFunc could load them.

7) **Run DPFunc prediction**
   - Ran DPFunc prediction for MF, BP, and CC using the pretrained models and our generated graph features.
   - The prediction outputs were saved as `*_final.pkl` files.

8) **Export deliverable CSVs**
   - Ran an export script to convert the final prediction objects into CSVs containing the top 10 GO terms per protein for each ontology.

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
- This workflow was designed to be practical for a class dataset on HPCC.
- Full DPFunc runs may incorporate richer residue embeddings and domain features; the pipeline here focuses on producing valid GO predictions and exportable deliverables for the 8 proteins.

# Created with the help of ChatGPT 5

  
   
