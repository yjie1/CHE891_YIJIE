import pickle as pkl
import numpy as np
import scipy.sparse as ssp

# load protein ids
pids = pkl.load(open("data/pid_list.pkl", "rb"))
n_rows = len(pids)

# load interpro index mapping (defines number of columns)
inter_idx = pkl.load(open("data/inter_idx.pkl", "rb"))

if isinstance(inter_idx, dict):
    n_cols = max(inter_idx.values()) + 1
elif isinstance(inter_idx, (list, tuple)):
    n_cols = len(inter_idx)
else:
    raise ValueError(f"Unexpected inter_idx type: {type(inter_idx)}")

# empty (all-zero) sparse matrix
mat = ssp.csr_matrix((n_rows, n_cols), dtype=np.float32)

# write one interpro matrix per ontology (DPFunc uses these paths from YAML)
for ont in ["mf", "bp", "cc"]:
    out = f"data/{ont}_interpro.pkl"
    with open(out, "wb") as f:
        pkl.dump(mat, f)
    print("Wrote", out, "shape", mat.shape)
