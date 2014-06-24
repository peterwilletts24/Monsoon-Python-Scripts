"""
Average mean sea level pressure by day, unrotate lat/lon and save
"""

import os, sys

import itertools

import numpy as np

import h5py
        

#experiment_ids = ['djzny', 'djznq', 'djznw']
experiment_ids = ['dkjxq']
data_to_mean = ['temp', 'sp_hum']
dset = ['t_on_p', 'sh_on_p']


for experiment_id in experiment_ids:
    expmin1 = experiment_id[:-1]
 
# Calculate mean of variable like temperature and specific humidity
    #"""
    for a, dm in enumerate(data_to_mean):
    
        fname = '/projects/cascade/pwille/temp/%s_pressure_levels_interp_%s' % (dm,experiment_id)
        
        ds = dset[a]
        with h5py.File(fname, 'r') as i:
            #d = i['%s' % ds]
            #print d.shape

            with h5py.File('%s_mean' % fname, 'w') as i2:
             mean = i2.create_dataset('mean' ,i['%s' % ds][0].shape, dtype='float32')
             print mean.shape
             print i['%s' % ds][0,0,0,:].shape
             sys.stdout.flush()
             for p in  range(len(i['%s' % ds][0,0,0,:])):
                 print '%s - %s' % (ds,p)
                 npmean =  np.mean(i['%s' % ds][:,:,:,p], axis = 0)
                 mean[:,:,p]=npmean
                 sys.stdout.flush()                 
     #        """
#Calculate mean of heights

    fname = '/projects/cascade/pwille/temp/408_pressure_levels_interp_pressure_%s' % (experiment_id)

        
    with h5py.File(fname, 'r') as i:
                    #d = i['interps']
                    #print d
            with h5py.File('%s_mean' % fname, 'w') as i2:
                mean = i2.create_dataset('mean' ,i['interps'][0].shape, dtype='float32')
                print i['interps'][0,0,0,: ].shape
                sys.stdout.flush()
                for p in  range(len(i['interps'][0,0,0,:])):
                    print p
                    sys.stdout.flush()
                
                    npmean =  np.mean(i['interps'][:,:,:,p], axis = 0)
                    mean[:,:,p] =npmean                   
