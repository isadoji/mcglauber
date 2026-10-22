#!/bin/bash
set -e
cd /home/isadoji/github/mcglauber
for i in 0 1 2 3 4 5 6 7 8 9; do
  PYTHONPATH=src python3 -m mcglauber.cli -c config/bi11_shards/shard_${i}.yaml > logs/shard_${i}.log 2>&1 &
done
wait
echo "ALL_SHARDS_DONE"
