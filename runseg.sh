#!/bin/bash

# This script propagates the MCell system for a short length of time tau,
# which is specified in the parameters.mdl file.  A progress coordinate is then
# computed and reported to WESTPA.

# Standard WEST ################################################################
# I think this is standard WEST stuff

set -x

WORKDIR=$WEST_CURRENT_SEG_DATA_REF
mkdir -pv $WORKDIR || exit 1
cd $WORKDIR

# MCell run ####################################################################

# load MCELL, MODEL_NAME, and OBSERVABLE1, defined in init.sh
. "$WEST_SIM_ROOT/bstates/variables.sh" || exit 1
wait

# Set up the run -- make links to all the files needed for the segment
ln -s ${WEST_SIM_ROOT}/istates/${MODEL_NAME} ${MODEL_NAME}
wait

# if we're continueing the trajectory, restart from the checpoint file of the parent traj

if [ $WEST_CURRENT_ITER -gt 1 ]; then
  CHKPT_FLAG="-checkpoint_infile $WEST_PARENT_DATA_REF/chkpt"
else
  CHKPT_FLAG=""
fi
wait

# run mcell
$MCELL $CHKPT_FLAG -seed $RANDOM $MODEL_NAME/Scene.main.mdl
wait

# Progress coordinate computation and extraction ###############################

# if not iteration 1, need to insert start state info from parent end state
# since we save aux coords, need to modify all dat files
if [ $WEST_CURRENT_ITER -gt 1 ]; then
  for DATFILE in react_data/*.dat; do # $DATFILE includes react_data/ in name
    PAR_END_STATE=$(tail -n1 $WEST_PARENT_DATA_REF/${DATFILE})
    sed -i "1i $PAR_END_STATE" ${DATFILE}
  done
fi

# report the progress coordinate to WESTPA
PCOORD1=$(awk '{print $2}' react_data/${OBSERVABLE1}.dat)
echo "$PCOORD1" > $WEST_PCOORD_RETURN

# report auxiliary coordinates to WESTPA
# grabs last line in each dat file, trims it to one column,
# and replaces line breaks with spaces
if [ -n "$WEST_COORD_RETURN" ] ; then
  COORD_MATRIX=$(paste react_data/*.dat | awk '{for(i=2;i<=NF;i+=2){printf "%s ", $i}; printf "\n"}')
  echo "$COORD_MATRIX" > $WEST_COORD_RETURN
fi

