"""

Load 409.pp, get times, and save in h5py

"""
import os, sys

import iris

import numpy as np

import h5py

experiment_ids = ['djznu', 'dkbhu', 'djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]

for experiment_id in experiment_ids:
 print experiment_id
 expmin1 = experiment_id[:-1]
 pp_file =  '/projects/cascade/pwille/moose_retrievals/%s/%s/409.pp' % (expmin1, experiment_id)     
 timestamps_file = '/projects/cascade/pwille/temp/%s_time_list' % (experiment_id)
 cube = iris.load_cube(pp_file)
 time_list = cube.coord('time').points
 with h5py.File(timestamps_file, 'w') as i:
     tstamps = i.create_dataset('tstamps', cube.coord('time').shape, dtype='float32')
     tstamps[. . .] =  cube.coord('time').points
     print '%s - Number of times: %s' % (experiment_id, tstamps.shape)
 

 

    
