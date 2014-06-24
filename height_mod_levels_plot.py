"""
Plot model level heights vs. layer thickness to see which parts are linear
"""
import os,sys

import iris
import iris.coords as coords
import iris.unit as unit

#from tempfile import mkdtemp
import numpy as np
import os.path as path
import matplotlib.pyplot as plt

#import h5py

experiment_id = 'djzny'   
expmin1 = experiment_id[:-1]

fname_heights = '/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp'% (expmin1, experiment_id)

hl = iris.load_cube(fname_heights)
height = hl[0,:,0,0].data
#l_thick = np.empty_like(height)

l_thick = np.diff(height)

plt.plot(l_thick, height[:-1])

plt.show()
