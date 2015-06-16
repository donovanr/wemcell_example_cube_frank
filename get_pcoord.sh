#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
    set -x
    env | sort
fi

# Get progress coordinate

. variables.sh

# extract the final values of the progress coordinate
#FINAL_C1=$(awk '{print $2}' ${OBSERVABLE}.dat)
FINAL_C1="0"

wait

# report the progress coordinate values to WEST
echo "$FINAL_C1" > $WEST_PCOORD_RETURN || exit 1
wait

if [ -n "$SEG_DEBUG" ] ; then
    head -v $WEST_PCOORD_RETURN
fi

