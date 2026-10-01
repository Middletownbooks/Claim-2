#!/bin/sh
# Stage ONLY certified shards.  A shard is certified by its sh_i.json, which
# sweep.py writes last; low_i.txt.partial is never staged.  Without this, a
# `git add -A` during a run commits a half-written survivor file -- which is
# exactly what happened in c493ad5.
set -e
cd "$(dirname "$0")"
for j in sweep_L5/sh_*.json; do
    [ -e "$j" ] || continue
    i=$(basename "$j" .json | sed 's/^sh_//')
    git add "$j"
    [ -e "sweep_L5/low_$i.txt" ] && git add "sweep_L5/low_$i.txt"
done
git status --short -- sweep_L5/ | grep -v '\.partial' || true
