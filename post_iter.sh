#!/bin/bash

# this script runs at the very end of an iteration.  so after all the segments
# are propagated for iteration N, and all the pcoords are returned and calcs
# are done, then this script will run, and delete the checkpoint files from
# iteration N-1, since they will never be used again.  we need to keep the
# checkpoints from iteration N, since they are needed for the next iteration.
# We also remover the react_data folder since it's also pretty large.


# delete restart files after we don't need them anymore to save disk space

# the name of the files to delete
CHKPT="chkpt"
REACT_DATA="react_data"

if [ $WEST_CURRENT_ITER -gt 1 ]; then

  PREV_ITER_NUM=$((10#$WEST_CURRENT_ITER - 1)) # force base-10 evaluation if nums have leading zeros
  printf -v STR_PREV_ITER_NUM "%06d" $PREV_ITER_NUM # format the prev iteration number with leading zeros
  find ${WEST_SIM_ROOT}/traj_segs/${STR_PREV_ITER_NUM}/ -maxdepth 2 -name $CHKPT -delete
  
  # can remove react_data as well if it's too big
  # find ${WEST_SIM_ROOT}/traj_segs/${STR_PREV_ITER_NUM}/ -maxdepth 2 -name $REACT_DATA -exec rm -rf {} \;

fi

