"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys

#import glob

#import itertools

#import numpy as np


#import cPickle as pickle


import iris
#import iris.coords as coords
#import iris.coord_categorisation

#from iris.analysis.interpolate import linear
#import cartopy.crs as ccrs 

experiment_ids = 'djznq'
expmin1 = experiment_id[:-1]

fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/30201.pp' % (expmin1, experiment_id)
u_wind,v_wind = iris.load(fu)

    
try:
        #iris.coord_categorisation.add_year(p_at_msl, 'time', name='year')
    u_mean = u_wind.collapsed('time', iris.analysis.MEAN)
    v_mean = v_wind.collapsed('time', iris.analysis.MEAN)

except Exception, e:
    print e
    pass
    
#if not os.path.exists(experiment_id): os.makedirs(experiment_id)

iris.save((u_mean,v_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/30201_mean.pp' % (expmin1, experiment_id))

   



