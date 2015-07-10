#!/bin/bash

source env.sh
ps aux | grep w_run | grep -v grep
pkill -9 -f w_run

SFX=.d$$
mv traj_segs{,$SFX}
mv seg_logs{,$SFX}
rm -Rf traj_segs$SFX seg_logs$SFX istates$SFX & disown %1
rm -f system.h5 wemd.h5 seg_logs.tar
mkdir seg_logs traj_segs istates


echo "running on node: $HOSTNAME" || exit 1
echo "shell is $SHELL" || exit 1

export WEST_SIM_ROOT="$PWD"

export PYTHONPATH=.

rm -rf seg_logs
rm -rf traj_segs
rm -f system.h5
mkdir seg_logs traj_segs
rm -f recycled_weight.txt
rm -f pcoord_check.txt


cd $WEST_SIM_ROOT
SIM_FILES=$(eval ls bstates)

cp -r bstates/* istates/
cp -r bstates/* $WEST_SIM_ROOT

BSTATE_ARGS="--bstate=well1,1,${MODEL_NAME}"
#$WEST_ROOT/bin/w_init $BSTATE_ARGS --work-manager=threads --n-workers=8 "$@"
$WEST_ROOT/bin/w_init $BSTATE_ARGS --serial "$@"

