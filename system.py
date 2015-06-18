from __future__ import division, print_function; __metaclass__ = type
import os, sys, math, itertools
import numpy
import west
from west import WESTSystem
from westpa.binning import RecursiveBinMapper, RectilinearBinMapper
import logging
log = logging.getLogger(__name__)
log.debug('loading module %r' % __name__)


class System(WESTSystem):
    def initialize(self):
        self.pcoord_ndim = 1
        self.pcoord_len = 10+1
        self.pcoord_dtype = numpy.float32
        binbounds = [float('-inf')] + [1.0*i + 0.5 for i in xrange(0,1000,1)] + [float('inf')]
        self.bin_mapper = RectilinearBinMapper([binbounds])
        self.bin_target_counts = numpy.empty((self.bin_mapper.nbins,), numpy.int)
        self.bin_target_counts[...] = 8

def coord_loader(fieldname, coord_file, segment, single_point=False):
    coord_raw = numpy.loadtxt(coord_file, dtype=numpy.float32)

    npts = len(coord_raw)
    assert coord_raw.shape[1] % 1 == 0
    ngrps = coord_raw.shape[1] // 1

    coords = numpy.empty((ngrps, npts, 1), numpy.float32)
    for igroup in xrange(ngrps):
        for idim in xrange(1):
           coords[igroup,:,idim] = coord_raw[:,igroup*1+idim]

    segment.data[fieldname] = coords
    

