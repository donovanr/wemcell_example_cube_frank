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
thisiter = int(args.iter)

def get_pcoords_and_weights(iternum):

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
    
    return final_pcoord,weights


def make_hist(final_pcoord,weights):
    # make a histogram of the pcoord and weights from the desired iteration
    hist,bin_edges = numpy.histogram(final_pcoord,weights=weights,bins=[i for i in xrange(-1,int(max(final_pcoord))+1)])
    int_bins = bin_edges[1:]
    return hist,int_bins


def bf_limit(iternum,f):
    summary = f['/summary']

    # tally the number of segs in each iter to make a total
    numsegs = 0
    for i in xrange(iternum):
        numsegs += summary[i][0]

    return float(iternum)/numsegs


def gnuplot_size():
    gnuplot_rows, gnuplot_cols = os.popen('stty size', 'r').read().split()
    gnuplot_rows = int(gnuplot_rows) - 1
    gnuplot_cols = int(gnuplot_cols) - 1
    return gnuplot_rows, gnuplot_cols


def plot_iter(iternum):

    final_pcoord,weights = get_pcoords_and_weights(thisiter)
    hist,int_bins = make_hist(final_pcoord,weights)
    
    gp_rows, gp_cols = gnuplot_size()
    
    bf = bf_limit(iternum,f)
    bfpoints = [bf for i in int_bins]

    # pass the histogram to gnuplot's ascii plot engine
    gnuplot = subprocess.Popen(['gnuplot'], stdin=subprocess.PIPE)
    gnuplot.stdin.write('set term dumb {0} {1}\n'.format(gp_cols,gp_rows))
    
    gnuplot.stdin.write('set logscale y \n')
    
    # change plot ranges by hand for now
    xmax = 50
    gnuplot.stdin.write('set xrange [0:{0}] \n'.format(xmax))
    gnuplot.stdin.write('set yrange [0.000001:1.0] \n')
    gnuplot.stdin.write('set title "WE iteration {0}" \n'.format(iternum))
    gnuplot.stdin.write('set ylabel "Probability" \n')
    gnuplot.stdin.write('set xlabel "Bound receptors on bottom of cube" \n')
    
    gnuplot.stdin.write('set arrow from 0,{1} to {0},{1} nohead linestyle \n'.format(xmax,bf))
    gnuplot.stdin.write('set label " Brute-force limit " at {0},{1} \n'.format(xmax*0.75,bf))
    
    gnuplot.stdin.write('plot "-" using 1:2 title "Weighted Ensemble pdf" with points \n')

    for i,j in zip(int_bins,hist):
        gnuplot.stdin.write('%f %f\n' % (i,j))
    
    gnuplot.stdin.write('e\n')
    gnuplot.stdin.flush()

plot_iter(thisiter)

