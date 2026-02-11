import glob
import os
import pickle
import numpy as np

PDB_GLOB = "data/PDB/PDB_folder/*.pdb"
OUT_EMB = "data/pdb_residue_esm_embeddings_part0.pkl"
OUT_MAP = "data/map_pid_esm_file.pkl"

def pdb_len(pdb_path: str) -> int:
    residues = set()
    with open(pdb_path, "r") as f:
        for ln in f:
            if ln.startswith("ATOM"):
                chain = ln[21].strip()
                resseq = ln[22:26].strip()
                icode = ln[26].strip()
                residues.add((chain, resseq, icode))
    return len(residues)

def main():
    pdbs = sorted(glob.glob(PDB_GLOB))
    if not pdbs:
        raise SystemExit(f"No PDBs found at {PDB_GLOB}")

    pids = [os.path.basename(p)[:-4] for p in pdbs]
    emb = {}

    for pdb, pid in zip(pdbs, pids):
        L = pdb_len(pdb)
        emb[pid] = np.zeros((L, 1280), dtype=np.float32)

    os.makedirs("data", exist_ok=True)
    with open(OUT_EMB, "wb") as f:
        pickle.dump(emb, f)

    with open(OUT_MAP, "wb") as f:
        pickle.dump({pid: 0 for pid in pids}, f)

    print("Wrote embeddings for", len(pids), "proteins")
    print("Example:", pids[0], emb[pids[0]].shape)

if __name__ == "__main__":
    main()
