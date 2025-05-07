#!/usr/bin/env bash
set -e
source .venv/bin/activate
if ! lsof -i:7545 >/dev/null; then
  ganache-cli --deterministic --miner.blockTime 0 >/dev/null 2>&1 &
  sleep 3
fi
python blockchain/scripts/deploy_contract.py
processing/build.sh
mpirun -np 4 python mpi/master.py
