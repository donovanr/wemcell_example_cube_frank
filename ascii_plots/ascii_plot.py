#!/usr/bin/env python

'''
This script reads in an hdf5 file from a westpa simulation and produces a 
plot of the probability distribution for a desired iteration using gnuplot.

Written by Rory Donovan
'''

# deal with arguements
import argparse

parser = argparse.ArgumentParser(description='This script for extracting pcoords and weights from a WESTPA hdf5 file for a desired iteration.')
parser.add_argument('-i','--iter', help='iteration number',required=True)
parser.add_argument('-f','--file', help='Input file name',required=True)
args = parser.parse_args()

# import necessary libraries
import h5py
import numpy
import os
import subprocess

# read input args to variables
f = h5py.File(args.file, "r")
basename = os.path.splitext(args.file)[0]
iternum = int(args.iter)

# construct paths to iter info in the h5 file
segindex_path = '/iterations/iter_' + '{0:08d}'.format(iternum) + '/seg_index'
pcoord_path = '/iterations/iter_' + '{0:08d}'.format(iternum) + '/pcoord'

# get the vector of final pcoords
final_pcoord = f[pcoord_path][:,-1]
final_pcoord = numpy.array(final_pcoord,dtype='float32')
final_pcoord = numpy.squeeze(numpy.asarray(final_pcoord))

# get the weights
segindex = f[segindex_path]
weights = [x[0] for x in segindex]
weights = numpy.array(weights,dtype='float32')

# make sure they have the same length
assert len(weights) == len(final_pcoord), "length mismatch"

# make a histogram of the pcoord and weights from the desired iteration
hist,bin_edges = numpy.histogram(final_pcoord,weights=weights,bins=[i for i in xrange(-1,int(max(final_pcoord))+1)])
int_bins = bin_edges[1:]

# pass the histogram to gnuplot's ascii plot engine
gnuplot = subprocess.Popen(['/usr/bin/gnuplot'], stdin=subprocess.PIPE)
gnuplot.stdin.write('set term dumb 79 25\n')

gnuplot.stdin.write('set logscale y \n')

# change plot ranges by hand for now
gnuplot.stdin.write('set xrange [0:50] \n')
gnuplot.stdin.write('set yrange [0.000001:1.0] \n')
gnuplot.stdin.write('set title "WE iteration {0}" \n'.format(iternum))
gnuplot.stdin.write('set ylabel "Probability" \n')
gnuplot.stdin.write('set xlabel "Bound receptors on bottom of cube" \n')

#gnuplot.stdin.write('plot "-" using 1:2 title "Weighted Ensemble pdf" with linespoints \n')
gnuplot.stdin.write('plot "-" using 1:2 title "Weighted Ensemble pdf" with points \n')

for i,j in zip(int_bins,hist):
    gnuplot.stdin.write('%f %f\n' % (i,j))

gnuplot.stdin.write('e\n')
gnuplot.stdin.flush()

