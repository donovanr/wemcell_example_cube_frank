#!/usr/bin/env bash


MAX_ITER=$(grep max_total_iterations ../west.cfg | awk -F ': ' '{print $2}')
STEP_SIZE=1
INITIAL_ITER=$STEP_SIZE

for ITER in $(seq $INITIAL_ITER $STEP_SIZE $MAX_ITER); do
	./ascii_plot.py --iter $ITER --file ../west.h5 2>/dev/null
	sleep 0.1
done
