import sys, glob
import mdtraj as md
from mdtraj.formats import PDBTrajectoryFile

def main():
    if len(sys.argv) != 3:
        print("Usage: convert_traj_to_pdb.py <outdir> <Nframes>", file=sys.stderr)
        sys.exit(2)

    outdir = sys.argv[1].rstrip("/")
    n = int(sys.argv[2])

    top = sorted(glob.glob(outdir + "/*.pdb"))
    if not top:
        raise FileNotFoundError(f"No .pdb topology found in {outdir}")
    top_path = top[0]

    traj = sorted(glob.glob(outdir + "/*.dcd")) + sorted(glob.glob(outdir + "/*.xtc"))
    if not traj:
        raise FileNotFoundError(f"No .dcd or .xtc trajectory found in {outdir}")
    traj_path = traj[0]

    t = md.load(traj_path, top=top_path)
    n = min(n, t.n_frames)

    out_pdb = outdir + f"/ensemble_{n}.pdb"
    with PDBTrajectoryFile(out_pdb, mode="w") as f:
        for i in range(n):
            f.write(t.xyz[i], t.topology, modelIndex=i+1)

    print(f"Wrote {n} models -> {out_pdb}")

if __name__ == "__main__":
    main()
