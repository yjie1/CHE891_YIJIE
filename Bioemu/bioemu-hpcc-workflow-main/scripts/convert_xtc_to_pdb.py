#!/usr/bin/env python3
"""Convert BioEmu output (samples.xtc + topology.pdb) to a multi-model PDB for PyMOL.

Usage:
  python convert_xtc_to_pdb.py outputs/NAME/samples.xtc outputs/NAME/topology.pdb outputs/NAME/ensemble_50.pdb 50
"""
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)

    xtc_path = Path(sys.argv[1]).expanduser().resolve()
    top_path = Path(sys.argv[2]).expanduser().resolve()
    out_pdb  = Path(sys.argv[3]).expanduser().resolve()
    n = int(sys.argv[4]) if len(sys.argv) >= 5 else None

    try:
        import mdtraj as md
    except Exception as e:
        print("ERROR: mdtraj is not installed in this environment.")
        print("Fix:  pip install mdtraj")
        raise

    traj = md.load(str(xtc_path), top=str(top_path))
    if n is not None:
        traj = traj[:n]
    out_pdb.parent.mkdir(parents=True, exist_ok=True)
    traj.save_pdb(str(out_pdb))
    print(f"Wrote {out_pdb} with {traj.n_frames} models.")

if __name__ == "__main__":
    main()
