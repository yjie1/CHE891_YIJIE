import joblib
import numpy as np
import scipy.sparse as ssp
from pathlib import Path
from collections import defaultdict
from Bio import SeqIO
from tqdm.auto import tqdm, trange
import math
import pickle as pkl
import dgl
import torch
from ruamel.yaml import YAML
import click
import os


def read_pkl(file_path):
    with open(file_path, 'rb') as fr:
        return pkl.load(fr)


def save_pkl(file_path, val):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as fw:
        pkl.dump(val, fw)


def get_dis(point1, point2):
    dis_x = point1[0] - point2[0]
    dis_y = point1[1] - point2[1]
    dis_z = point1[2] - point2[2]
    return math.sqrt(dis_x * dis_x + dis_y * dis_y + dis_z * dis_z)


def get_amino_feature(amino):
    # Map 20 standard amino acids to 0..19
    if amino == 'ALA':
        return 0
    elif amino == 'CYS':
        return 1
    elif amino == 'ASP':
        return 2
    elif amino == 'GLU':
        return 3
    elif amino == 'PHE':
        return 4
    elif amino == 'GLY':
        return 5
    elif amino == 'HIS':
        return 6
    elif amino == 'ILE':
        return 7
    elif amino == 'LYS':
        return 8
    elif amino == 'LEU':
        return 9
    elif amino == 'MET':
        return 10
    elif amino == 'ASN':
        return 11
    elif amino == 'PRO':
        return 12
    elif amino == 'GLN':
        return 13
    elif amino == 'ARG':
        return 14
    elif amino == 'SER':
        return 15
    elif amino == 'THR':
        return 16
    elif amino == 'VAL':
        return 17
    elif amino == 'TRP':
        return 18
    elif amino == 'TYR':
        return 19
    else:
        # Unknown residue; fall back to ALA
        return 0


def _extract_pid_embedding(esm_obj, pid):
    """
    Supports multiple formats:
      1) dict: pid -> np.ndarray [L,1280]
      2) dict: pid -> list/tuple where element 31 is np.ndarray [L,1280]  (ESM layer 31)
      3) dict: pid -> dict with key 31 as np.ndarray [L,1280]
    """
    pid_data = esm_obj[pid] if isinstance(esm_obj, dict) and pid in esm_obj else esm_obj

    if isinstance(pid_data, (list, tuple)) and len(pid_data) > 31 and hasattr(pid_data[31], 'shape'):
        emb = pid_data[31]
    elif isinstance(pid_data, dict) and 31 in pid_data and hasattr(pid_data[31], 'shape'):
        emb = pid_data[31]
    else:
        emb = pid_data

    if torch.is_tensor(emb):
        emb = emb.detach().cpu().numpy()

    emb = np.asarray(emb)
    if emb.ndim != 2:
        raise ValueError(f"Embedding for pid={pid} must be 2D [L,D], got shape {emb.shape}")

    return emb.astype(np.float32, copy=False)


def get_whole_pdb_graph(pdb_points, pid_list, map_pid_esm_file, residue_features, thresholds, ont, tag):
    out_dir = './data/PDB/graph_feature'
    os.makedirs(out_dir, exist_ok=True)

    pdb_graphs = []
    p_cnt = 0
    file_idx = 0

    for pid in tqdm(pid_list):
        p_cnt += 1

        if pid not in pdb_points:
            raise KeyError(f"pid {pid} not found in pdb_points. Check data/pdb_points.pkl and data/pid_list.pkl.")

        points = pdb_points[pid]
        L = len(points)

        file_id = map_pid_esm_file[pid]
        esm_tp = read_pkl(residue_features.format(file_id))
        pid_emb = _extract_pid_embedding(esm_tp, pid)

        # pad/truncate to match points length
        if pid_emb.shape[0] < L:
            padded = np.zeros((L, pid_emb.shape[1]), dtype=np.float32)
            padded[:pid_emb.shape[0]] = pid_emb
            pid_emb = padded
        elif pid_emb.shape[0] > L:
            pid_emb = pid_emb[:L]

        if pid_emb.shape[1] != 1280:
            raise ValueError(f"Expected embedding dim 1280 for pid={pid}, got {pid_emb.shape[1]}")

        u_list = []
        v_list = []
        dis_list = []

        for uid, amino_1 in enumerate(points):
            for vid, amino_2 in enumerate(points):
                if uid == vid:
                    continue
                dist = get_dis(amino_1, amino_2)
                if dist <= thresholds:
                    u_list.append(uid)
                    v_list.append(vid)
                    dis_list.append(dist)

        u_list = torch.tensor(u_list, dtype=torch.int64)
        v_list = torch.tensor(v_list, dtype=torch.int64)
        dis_list = torch.tensor(dis_list, dtype=torch.float32)

        graph = dgl.graph((u_list, v_list), num_nodes=L)
        graph.edata['dis'] = dis_list

        graph.ndata['x'] = torch.zeros(L, 1280, dtype=torch.float32)
        graph.ndata['aa'] = torch.zeros(L, 20, dtype=torch.float32)

        for node_id in range(L):
            amino = points[node_id][3]
            amino_id = get_amino_feature(amino)

            graph.ndata['x'][node_id] = torch.from_numpy(pid_emb[node_id])

            one_hot = torch.zeros(20, dtype=torch.float32)
            one_hot[amino_id] = 1.0
            graph.ndata['aa'][node_id] = one_hot

        pdb_graphs.append(graph)

        if p_cnt % 5000 == 0:
            save_pkl(f'{out_dir}/{ont}_{tag}_whole_pdb_part{file_idx}.pkl', pdb_graphs)
            p_cnt = 0
            file_idx += 1
            pdb_graphs = []

    if len(pdb_graphs) > 0:
        save_pkl(f'{out_dir}/{ont}_{tag}_whole_pdb_part{file_idx}.pkl', pdb_graphs)


@click.command()
@click.option('-d', '--data-cnf', type=click.Choice(['bp', 'mf', 'cc']), default='mf')
@click.option('-t', '--thresholds', type=click.INT, default=12)
def main(data_cnf, thresholds):
    yaml = YAML(typ='safe')
    data_cnf = yaml.load(Path(f'./configure/{data_cnf}.yaml'))
    ont = data_cnf['name']

    residue_features = data_cnf['base']['residue_feature']
    pdb_points_file = data_cnf['base']['pdb_points']
    pid_list_file = data_cnf['test']['pid_list_file']

    map_pid_esm_file = read_pkl('./data/map_pid_esm_file.pkl')
    pdb_points = read_pkl(pdb_points_file)

    with open(pid_list_file, 'rb') as fr:
        used_pid_list = pkl.load(fr)

    print(f"Used Pid in Test: {len(used_pid_list)}")

    get_whole_pdb_graph(pdb_points, used_pid_list, map_pid_esm_file, residue_features, thresholds, ont, 'test')


if __name__ == '__main__':
    main()
