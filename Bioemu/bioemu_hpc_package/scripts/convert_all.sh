#!/bin/bash
set -euo pipefail

# Run from the project root:
#   bash scripts/convert_all.sh 50
N=${1:-50}

module purge
module load Miniforge3
conda activate bioemu

pip -q show mdtraj >/dev/null 2>&1 || pip install -q mdtraj

for d in outputs/*/ ; do
  [ -d "$d" ] || continue
  if [ -f "${d}/samples.xtc" ] && [ -f "${d}/topology.pdb" ]; then
    name=$(basename "$d")
    python scripts/convert_xtc_to_pdb.py "${d}/samples.xtc" "${d}/topology.pdb" "${d}/ensemble_${N}.pdb" "${N}"
  fi
done
