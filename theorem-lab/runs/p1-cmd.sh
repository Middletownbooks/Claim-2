#!/bin/sh
# Phase 1 reproduction attempt: reported scale (m<=48, r<=12, d<=112), real oracle.
exec python3 lab.py --oracle real --control C \
  --r-train 8 --r-valid 10 --r-test 12 \
  --d-train 92 --d-valid 102 --d-test 112 \
  --budget 200000 --out runs/p1-real-C
