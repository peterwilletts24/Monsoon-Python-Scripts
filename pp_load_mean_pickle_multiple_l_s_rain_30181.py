"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys

import glob

import itertools

import numpy as np


import cPickle as pickle


import iris
import iris.coords as coords
import iris.coord_categorisation

from iris.analysis.interpolate import linear
import cartopy.crs as ccrs 


diagnostic = '30181.pp'
flist = glob.glob ('/projects/cascade/pwille/moose_retrievals/*/*/%s' % diagnostic)


for i in flist:

    fname = str(i)
    l_s_r_rate, t_tot_incr = iris.load_cubes(fname, ['stratiform_rainfall_rate', 'tendency_of_air_temperature'])
    experiment_id = fname.split('/')[6]

    #iris.coord_categorisation.add_day_of_year(p_at_msl, 'forecast_reference_time', name='dayyear')
 # forecast_period messes up aggergation sometimes so remove. Probably need to comment out for time of day



   

     # http://nbviewer.ipython.org/github/SciTools/iris_example_code/blob/master/coord_categorisation.ipynb

    # Because some model outputs have time as a 2-D aux coord, as opposed to a 1-D dim coord, the standard iris categorisation by day,  year etc throws an error.  Add_categorised_coord allows categorisation of 2-dimensional arrays. 

    # Get year from time coord.  Function to use in add_categorised_coord below

    #def year_from_time(coord, point):
     #   yearnp = coord.units.num2date(point).time
        
     #   yearpoint=np.zeros(yearnp.shape)

     #   for index, x in np.ndenumerate(yearnp):

     #        yearpoint[index] = x.year

     #   year = iris.coords.AuxCoord(yearpoint)
      #  return year

    #iris.coord_categorisation.add_categorised_coord(p_at_msl, 'year', 'time', year_from_time)
    
    try:
        #iris.coord_categorisation.add_year(p_at_msl, 'time', name='year')
        model_mean = l_s_r_rate.collapsed('time', iris.analysis.MEAN)

    except:
        #print p_at_msl
        continue
    
    #iris.coord_categorisation.add_month(p_at_msl, 'forecast_reference_time', name='month')


    #daily_mean = p_at_msl.aggregated_by(['dayyear'], iris.analysis.MEAN)
    #model_mean = p_at_msl.aggregated_by(['year'], iris.analysis.MEAN)
    #month_mean = p_at_msl2.aggregated_by(['month'], iris.analysis.MEAN)
#daily_mean_rot = checkpoleposition(daily_mean)


    if not os.path.exists(experiment_id): os.makedirs(experiment_id)



# iris.save(daily_mean,'daily_mean_rot%s.pp' % experiment_id)

    pickle.dump( model_mean, open( "/home/pwille/python_scripts/%s/pickle_model_mean_collapsed_%s.p" % (experiment_id, experiment_id), "wb" ) )

    #pickle.dump( daily_mean, open( "/home/pwille/python_scripts/%s/pickle_daily_mean_%s.p" % (experiment_id, experiment_id), "wb" ) )
    #pickle.dump( month_mean, open( "/home/pwille/python_scripts/%s/pickle_month_mean_%s.p" % (experiment_id, experiment_id), "wb" ) )




