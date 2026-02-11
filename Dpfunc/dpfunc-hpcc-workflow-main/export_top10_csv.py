import os
import pickle
import numpy as np
import pandas as pd
import joblib

RESULTS_DIR = "results"
PREFIX = "DPFunc_model"          # your files are named results/DPFunc_model_*_final.pkl
TOPN = 10

def load_obj(pkl_path):
    with open(pkl_path, "rb") as f:
        return pickle.load(f)

def guess_pid_col(df):
    for c in ["pid", "protein", "prot", "name", "ID", "id"]:
        if c in df.columns:
            return c
    return df.columns[0]

def dict_cols(df, max_rows=20):
    cols = []
    for c in df.columns:
        for v in df[c].head(max_rows):
            if isinstance(v, dict):
                cols.append(c)
                break
    return cols

def list_cols(df, max_rows=20):
    cols = []
    for c in df.columns:
        for v in df[c].head(max_rows):
            if isinstance(v, (list, tuple, np.ndarray)):
                cols.append(c)
                break
    return cols

def go_named_cols(df):
    return [c for c in df.columns if isinstance(c, str) and "GO:" in c]

def export_from_dict_scores(pid, go_scores, rows, topn=TOPN):
    if not isinstance(go_scores, dict) or len(go_scores) == 0:
        return
    # sort by score desc
    items = sorted(go_scores.items(), key=lambda x: x[1], reverse=True)[:topn]
    for rank, (go, score) in enumerate(items, 1):
        rows.append({"protein": str(pid), "rank": rank, "GO": str(go), "score": float(score)})

def export_from_vector(pid, vec, classes, rows, topn=TOPN):
    arr = np.asarray(vec, dtype=float)
    n = min(len(arr), len(classes))
    arr = arr[:n]
    idx = np.argsort(arr)[::-1][:topn]
    for rank, i in enumerate(idx, 1):
        rows.append({"protein": str(pid), "rank": rank, "GO": str(classes[i]), "score": float(arr[i])})

def write_csv(rows, out_csv):
    if not rows:
        return False
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print("WROTE", out_csv, "rows:", len(df))
    return True

def handle_one(ont):
    pkl_path = os.path.join(RESULTS_DIR, f"{PREFIX}_{ont}_final.pkl")
    if not os.path.exists(pkl_path):
        print("MISSING", pkl_path)
        return

    obj = load_obj(pkl_path)

    # Load MLB classes in case we need to decode score vectors
    mlb_path = os.path.join("mlb", f"{ont}_go.mlb")
    classes = None
    if os.path.exists(mlb_path):
        try:
            mlb = joblib.load(mlb_path)
            classes = getattr(mlb, "classes_", None)
        except Exception:
            classes = None

    rows = []

    # Case 1: dict-of-dicts {pid: {GO: score}}
    if isinstance(obj, dict):
        for pid, go_scores in obj.items():
            export_from_dict_scores(pid, go_scores, rows)
        if write_csv(rows, os.path.join(RESULTS_DIR, f"{ont}_top10.csv")):
            return
        print("NO_ROWS_EXTRACTED", ont, "type:", type(obj))
        return

    # Case 2: DataFrame-like
    if hasattr(obj, "columns") and hasattr(obj, "head"):
        df = pd.DataFrame(obj)
        pid_col = guess_pid_col(df)

        # 2A: GO terms are columns (wide format): columns like "GO:000xxxx"
        go_cols = go_named_cols(df)
        if go_cols:
            sub = df[[pid_col] + go_cols].copy()
            # melt into rows
            m = sub.melt(id_vars=[pid_col], var_name="GO", value_name="score")
            m["score"] = pd.to_numeric(m["score"], errors="coerce")
            m = m.dropna(subset=["score"])
            m = m.sort_values([pid_col, "score"], ascending=[True, False]).groupby(pid_col).head(TOPN)
            out_csv = os.path.join(RESULTS_DIR, f"{ont}_top10.csv")
            m.rename(columns={pid_col: "protein"}, inplace=True)
            m["rank"] = m.groupby("protein").cumcount() + 1
            m[["protein", "rank", "GO", "score"]].to_csv(out_csv, index=False)
            print("WROTE", out_csv, "rows:", len(m))
            return

        # 2B: One column contains dict GO->score per row
        dcols = dict_cols(df)
        if dcols:
            score_col = dcols[0]
            for _, r in df.iterrows():
                pid = r[pid_col]
                export_from_dict_scores(pid, r[score_col], rows)
            if write_csv(rows, os.path.join(RESULTS_DIR, f"{ont}_top10.csv")):
                return

        # 2C: One column contains a vector of scores; decode with MLB
        lcols = list_cols(df)
        if lcols and classes is not None:
            vec_col = lcols[0]
            for _, r in df.iterrows():
                pid = r[pid_col]
                export_from_vector(pid, r[vec_col], classes, rows)
            if write_csv(rows, os.path.join(RESULTS_DIR, f"{ont}_top10.csv")):
                return

        print("NO_ROWS_EXTRACTED", ont, "type: DataFrame", "cols:", list(df.columns))
        return

    print("NO_ROWS_EXTRACTED", ont, "type:", type(obj))

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    for ont in ["mf", "bp", "cc"]:
        handle_one(ont)

if __name__ == "__main__":
    main()

