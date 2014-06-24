"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys

import glob

import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np
from mpl_toolkits.basemap import Basemap

import cPickle as pickle


import iris
import iris.coords as coords
import iris.coord_categorisation

from iris.analysis.interpolate import linear
import cartopy.crs as ccrs 

diagnostic = '4203'
flist = glob.glob ('/projects/cascade/pwille/moose_retrievals/*/*/%s.pp' % diagnostic)


for i in flist:

    fname = str(i)
    full_cube = iris.load_cube(fname)

    experiment_id = fname.split('/')[6]

# forecast_period messes up aggergation sometimes so remove. Probably need to comment out for time of day

   
    #can only use one at a time, or load mutliple times with different names (I think)

#These will not work with cubes that have 'time' as a multi dimensional coord

    #iris.coord_categorisation.add_day_of_year(full_cube, 'forecast_reference_time', name='dayyear')
    #iris.coord_categorisation.add_year(full_cube, 'forecast_reference_time', name='year')
    #iris.coord_categorisation.add_month(full_cube, 'forecast_reference_time', name='month')

    #daily_mean = full_cube.aggregated_by(['dayyear'], iris.analysis.MEAN)
    #model_mean = full_cube.aggregated_by(['year'], iris.analysis.MEAN)
    #month_mean = full_cube.aggregated_by(['month'], iris.analysis.MEAN)


    #daily_total = full_cube.aggregated_by(['dayyear'], iris.analysis.SUM)
    #model_total = full_cube.aggregated_by(['year'], iris.analysis.SUM

# Collapsing MAY work, not checked yet

    try:
        
        instant_rain_mean = full_cube.collapsed('time', iris.analysis.MEAN)

    except:
        print full_cube
        continue

    

    if not os.path.exists(experiment_id): os.makedirs(experiment_id)


    pickle.dump(instant_rain_mean, open( "/home/pwille/python_scripts/%s/pickle_instant_rain_largescale_mean%s_%s.p" % (experiment_id, experiment_id, diagnostic), "wb" ) )

#    pickle.dump(daily_total, open( "/home/pwille/python_scripts/%s/pickle_daily_total_%s_%s.p" % (experiment_id, experiment_id, diagnostic), "wb" ) )




