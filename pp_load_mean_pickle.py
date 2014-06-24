"""
Average mean sea level pressure by day, unrotate lat/lon and save
"""

import os, sys

import itertools

import numpy as np

import cPickle as pickle
#import matplotlib.animation as animation

import iris
import iris.coords as coords
import iris.coord_categorisation

from iris.analysis.interpolate import linear
import cartopy.crs as ccrs 

import h5py
        
#def checkpoleposition(cube):

 #rot_pole = temperature.coord('grid_latitude').coord_system.as_cartopy_crs()
# ll = ccrs.Geodetic()
 #lon, lat = 40, -42
# Transform the lon lat point into unrotated coordinates.
 #target_xy = ll.transform_point(rotated_lon, rotated_lat, rot_pole) 
 
 #extracted_cube = linear(temperature, [('grid_latitude', target_xy[1]), ('grid_longitude', target_xy[0]   

#experiment_ids = ['djzny', 'djznq', 'djznw']
experiment_ids = ['djzny']
data_to_mean = ['temp', 'sp_hum']
dset = ['t_on_p', 'sh_on_p']


for experiment_id in experiment_ids:
    expmin1 = experiment_id[:-1]
    
    for a, dm in enumerate(data_to_mean):
    #dataset = iris.load_cube(fname)
        fname = '/projects/cascade/pwille/temp/%s_pressure_levels_interp_%s' % (dm,experiment_id)
        ds = dset[a]
        with h5py.File(fname, 'r') as i:
            d = i['%s' % ds]
            print d
     #iris.coord_categorisation.add_day_of_year(p_at_msl, 'time', name='dayyear')
        #print fname
    #daily_mean = .aggregated_by(['dayyear'], iris.analysis.MEAN)
#daily_mean_rot = checkpoleposition(daily_mean)


#if not os.path.exists(experiment_id): os.makedirs(experiment_id)

#pickle.dump( daily_mean, open( "/home/pwille/python_scripts/%s/pickle_daily_mean_%s.p" % (experiment_id, experiment_id), "wb" ) )






