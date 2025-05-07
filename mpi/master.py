"""
Run with:
    mpirun -np 4 --hostfile mpi/hosts python mpi/master.py
"""
import subprocess, sys
from pathlib import Path
from mpi4py import MPI

ROOT = Path(__file__).resolve().parents[1]
ENH = ROOT / "processing/enhance"
IMGS = ROOT / "images"
OUTS = ROOT / "outputs"

sys.path.insert(0, str(ROOT))
from utils.hash_util import hash_file
from blockchain.scripts.record_hash import record_hash_to_chain

comm = MPI.COMM_WORLD
rank, size = comm.Get_rank(), comm.Get_size()

def enhance(inp: Path, out: Path):
    out.parent.mkdir(exist_ok=True, parents=True)
    subprocess.run([str(ENH), str(inp), str(out)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

if rank == 0:  # Master
    imgs = sorted(IMGS.glob("*.jpg"))
    if not imgs: raise SystemExit("No images in images/")
    buckets = [[] for _ in range(size-1)]
    for i, p in enumerate(imgs): buckets[i % (size-1)].append(p.name)
    for w in range(1, size): comm.send(buckets[w-1], dest=w)
    print("📤 Distributed", len(imgs), "images to", size-1, "workers")
else:          # Worker
    todo = comm.recv(source=0)
    for name in todo:
        src = IMGS / name
        dst = OUTS / f"enh_{name}"
        enhance(src, dst)
        record_hash_to_chain(hash_file(dst))
        print(f"🛠️  Worker {rank}: done {name}")

if rank == 0:
    print("🎉  MPI job finished.")
