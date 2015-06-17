#!/usr/bin/env bash


MAX_ITER=$(grep max_total_iterations ../west.cfg | awk -F ': ' '{print $2}')
INITIAL_ITER=1
STEP_SIZE=1

for ITER in $(seq $INITIAL_ITER $STEP_SIZE $MAX_ITER); do
	clear
	echo "Iteration $ITER"
	./make_plot.py -i $ITER -f ../west.h5 2>/dev/null
	sleep 0.25
done
