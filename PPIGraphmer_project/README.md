# PPI-Graphomer on MSU HPCC 

This README is ready to paste into GitHub. It covers:
1) Install + conda environment
2) HPCC cache/temp setup (avoid HOME quota issues)
3) Run single PDB
4) Fix KeyError by simplifying Boltz PDB filenames
5) Batch run many PDBs + save CSV + logs
6) Troubleshooting

------------------------------------------------------------
1) Install & create conda environment
------------------------------------------------------------

On MSU HPCC:

    module purge
    module load Miniforge3

    # Create environment
    conda create -n ppi-graphomer python=3.9 -y
    conda activate ppi-graphomer

    # Upgrade pip
    pip install -U pip

    # Install common deps (adjust if you have requirements.txt)
    pip install torch torchvision torchaudio
    pip install transformers fair-esm
    pip install numpy scipy pandas

    # If your repo provides requirements.txt, prefer this:
    # pip install -r requirements.txt


------------------------------------------------------------
2) One-time cache/temp configuration (CRITICAL on HPCC)
------------------------------------------------------------

Reason:
- HOME quota is small (e.g., /mnt/ffs24/home/<user>).
- ESM / Torch / HF downloads and temp files can exceed quota.
Solution:
- Redirect caches and temporary files to a large, writable filesystem (recommended: /mnt/ufs18/...).

Create a helper script env_cache.sh (do this once):

    cd ~/ppi-graphomer

    cat > env_cache.sh <<'EOF'
    # ==============================
    # PPI-Graphomer cache/temp setup
    # ==============================

    # Big filesystem path (recommended on MSU HPCC)
    export BIG=/mnt/ufs18/rs/CHE_882_Spring2026_001

    # Root folder for all caches
    export CACHE_ROOT=$BIG/.cache_hpc
    mkdir -p $CACHE_ROOT/{huggingface,torch,xdg,tmp}

    # HuggingFace cache root (Transformers + hub downloads)
    export HF_HOME=$CACHE_ROOT/huggingface

    # XDG cache (some libs use this by default)
    export XDG_CACHE_HOME=$CACHE_ROOT/xdg

    # Torch hub cache (ESM model downloads use torch.hub)
    export TORCH_HOME=$CACHE_ROOT/torch
    export TORCH_HUB_DIR=$TORCH_HOME/hub

    # Temporary directory for downloads/unpacking
    export TMPDIR=$CACHE_ROOT/tmp
    export TMP=$TMPDIR
    export TEMP=$TMPDIR
    EOF

    ls -lh env_cache.sh


------------------------------------------------------------
3) Every new session: activate env + load cache settings
------------------------------------------------------------

Every time you log in / open a new terminal:

    cd ~/ppi-graphomer
    conda activate ppi-graphomer
    source env_cache.sh

Optional sanity check:

    echo "HF_HOME=$HF_HOME"
    echo "TORCH_HOME=$TORCH_HOME"
    echo "TMPDIR=$TMPDIR"


------------------------------------------------------------
4) Run inference for a single PDB
------------------------------------------------------------

Single PDB run:

    cd ~/ppi-graphomer
    conda activate ppi-graphomer
    source env_cache.sh

    python inference.py --pdb /path/to/your.pdb

Example:

    python inference.py --pdb /mnt/gs21/scratch/$USER/BoltZ_PDB_simple/KAF5559671.pdb


------------------------------------------------------------
5) Fix KeyError from complex Boltz PDB filenames (recommended)
------------------------------------------------------------

If your PDB filenames look like:
    01_...__01_..._model_0.pdb

`inference.py` may raise KeyError because it expects simpler naming.
Workaround: copy/rename to a simplified filename folder (short ID only).

Input folder (Boltz PDBs):
    /mnt/gs21/scratch/$USER/BoltZ_PDB

Output folder (simplified names):
    /mnt/gs21/scratch/$USER/BoltZ_PDB_simple

Create simplified copies:

    INP=/mnt/gs21/scratch/$USER/BoltZ_PDB
    OUT=/mnt/gs21/scratch/$USER/BoltZ_PDB_simple
    mkdir -p "$OUT"
    cd "$INP"

    for f in *.pdb; do
      base=$(basename "$f")
      # Rule:
      # 1) take the part after "__"
      # 2) remove everything from ".1_" onward
      # Example:
      # 01_KAF...__01_KAF5559671.1_26-374_model_0.pdb -> KAF5559671.pdb
      simple=$(echo "$base" | sed 's/^.*__//' | sed 's/\.1_.*//')
      cp "$f" "$OUT/${simple}.pdb"
    done

    ls -lh "$OUT" | head


------------------------------------------------------------
6) Batch run many PDBs + save CSV summary + per-PDB logs
------------------------------------------------------------

This batch script:
- Reads PDBs from PDBDIR
- Writes outputs (CSV + logs) to /mnt/ufs18/... (avoid HOME quota)

Run batch:

    cd ~/ppi-graphomer
    conda activate ppi-graphomer
    source env_cache.sh

    # Input folder (recommended: simplified folder)
    PDBDIR=/mnt/gs21/scratch/$USER/BoltZ_PDB_simple

    # Output folder on ufs18 (avoid HOME quota)
    OUTDIR=/mnt/ufs18/rs/CHE_882_Spring2026_001/ppi_graphomer_runs
    mkdir -p "$OUTDIR/logs"

    OUTCSV="$OUTDIR/results.csv"
    echo "pdb,output" > "$OUTCSV"

    # Prevent "*.pdb" from being treated as literal text if no matches
    shopt -s nullglob
    files=("$PDBDIR"/*.pdb)

    if [ ${#files[@]} -eq 0 ]; then
      echo "No PDB files found in $PDBDIR"
      exit 1
    fi

    for pdb in "${files[@]}"; do
      base=$(basename "$pdb")
      log="$OUTDIR/logs/${base}.log"
      echo "Running $base ..."

      python inference.py --pdb "$pdb" > "$log" 2>&1

      # Save last line of log as summary output (edit if you want to parse affinity precisely)
      res=$(tail -n 1 "$log")
      echo "$base,\"$res\"" >> "$OUTCSV"
    done

    echo "Done."
    echo "CSV results: $OUTCSV"
    echo "Logs folder: $OUTDIR/logs/"


------------------------------------------------------------
7) Where are the outputs?
------------------------------------------------------------

CSV:
    /mnt/ufs18/rs/CHE_882_Spring2026_001/ppi_graphomer_runs/results.csv

Logs:
    /mnt/ufs18/rs/CHE_882_Spring2026_001/ppi_graphomer_runs/logs/*.log

Quick view:

    head /mnt/ufs18/rs/CHE_882_Spring2026_001/ppi_graphomer_runs/results.csv
    ls -lh /mnt/ufs18/rs/CHE_882_Spring2026_001/ppi_graphomer_runs/logs | head


------------------------------------------------------------
8) Troubleshooting
------------------------------------------------------------

(A) HOME quota exceeded (Disk quota exceeded)

    quota -v | head -n 10
    rm -rf ~/.cache/torch ~/.cache/huggingface ~/.cache/pip
    conda clean -a -y

(B) No space left on device even though df shows space

- Ensure you ran:
    source env_cache.sh

(C) Batch loop says file not found with *.pdb

    ls -lh $PDBDIR/*.pdb | head


------------------------------------------------------------
9) Dev node warning
------------------------------------------------------------

Development nodes are limited (e.g., ~2 hours). For large batches, use sbatch on compute nodes.
