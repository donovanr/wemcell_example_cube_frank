#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
    set -x
    env | sort
fi

cd istates

mkdir -p $(dirname $WEST_ISTATE_DATA_REF)

# Simply copy in the basis state
cp -v $WEST_BSTATE_DATA_REF $WEST_ISTATE_DATA_REF

echo "$WEST_BSTATE_DATA_REF $WEST_ISTATE_DATA_REF" > gen_istates_data_ref.txt


