import os, sys
import datetime

import iris
import iris.unit as unit
import iris.analysis.cartography

import numpy as np

import iris.analysis.geometry
from shapely.geometry import Polygon

from iris.coord_categorisation import add_categorised_coord

import imp
imp.load_source('UnrotateUpdateCube', '/home/pwille/python_scripts/modules/unrotate_and_update_pole.py')

from UnrotateUpdateCube import *

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

#experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
experiment_ids = ['dkhgu']
#experiment_ids = ['djzns', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ]
#experiment_ids = [ 'dklwu', 'dklzq', 'dklyu', 'dkmbq', 'dkbhu', 'djznu', 'dkhgu', 'djzns' ]
#experiment_ids = ['djznu', 'dkhgu' ] # High Res
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq']
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkmbq', 'dklzq', 'dkjxq' ] # Params
# Load global LAM
dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

# Min and max lats lons from smallest model domain (dkbhu) - see spreadsheet

#latmin=-10
#latmax=5
#lonmin=64.115
#lonmax=80

polygon = Polygon(((73., 21.), (83., 16.), (87., 22.), (75., 27.)))
        
#lat_constraint=iris.Constraint(grid_latitude= lambda la: latmin <= la.point <= latmax)
#lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin <= lo.point <= lonmax)

fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg, ('%s' % cube_name_param)  & time_constraint)   

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)

del glob_load

for experiment_id in experiment_ids:

    expmin1 = experiment_id[:-1]

    fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)

    flsm = '%s%s/%s/30.pp' % (pp_file_path, expmin1, experiment_id)
 
    print experiment_id
    sys.stdout.flush()

    try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc)
        cubeconv= unrotate_pole_update_cube(cubeconv)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc)
        cubestrat= unrotate_pole_update_cube(cubestrat)
        print cubestrat
        #cube=cubeconv.extract(lat_constraint & lon_constraint) + cubestrat.extract(lat_constraint & lon_constraint)
        cube=cubeconv + cubestrat
        cube.rename('total_precipitation_rate')
    except iris.exceptions.ConstraintMismatchError:        
        cube = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc)
        cube= unrotate_pole_update_cube(cube)
        #cube = cube.extract(lat_constraint & lon_constraint)

    cube.coord('grid_longitude').guess_bounds()
    cube.coord('grid_latitude').guess_bounds()

# Mean at each grid point by hour of day and save    
                                                    
    add_categorised_coord(cube, 'hour', 'time',lambda coord, x: coord.units.num2date(x).hour)
    diurnal_mean_cube = cube.aggregated_by('hour', iris.analysis.MEAN)
 
    del cube

    #try:
    #    iris.save(diurnal_mean_cube, '%s%s/%s/%s_rainfall_hourly_mean.pp' % (pp_file_path, expmin1, experiment_id, diag))
    #except Exception, e:
    #    print e
    #    pass
        
# Load land/sea mask 

    #lsm = iris.load_cube(flsm, ('land_binary_mask' ) )
    #lsm = unrotate_pole_update_cube(lsm)
    #lsm=lsm.extract(lat_constraint & lon_constraint)
    #print lsm
   
    sys.stdout.flush()

# Calculate weights

    l=iris.analysis.geometry.geometry_area_weights(diurnal_mean_cube, polygon)

# For Sea and Land, mask area and calculate mean of each hour for sea/land and SAVE as numpy array
    #tdmc=  diurnal_mean_cube.collapsed(['grid_latitude', 'grid_longitude'], iris.analysis.MEAN) 
    #total_diurnal_mean_cube=[tdmc.data.data, diurnal_mean_cube.coord('hour').points+0.5]
    #print total_diurnal_mean_cube
    #np.save('%s%s/%s/%s_total_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), total_diurnal_mean_cube) 
    
    for s in ([1]):
     #nancube = np.where(lsm.data==s, diurnal_mean_cube.data, np.NaN)
     #maskedcube = np.ma.masked_array(nancube,np.isnan(nancube))
     #total_rainfall = np.mean(maskedcube.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])), axis=1)
     #total_rainfall = np.ma.average(maskedcube.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])), axis=1, weights=l.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])))
     maskedcube=diurnal_mean_cube.data # No need to mask in this case as using weighted averages
     total_rainfall = np.ma.average(maskedcube.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])), axis=1, weights=l.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])))

     trnp =[total_rainfall.data, diurnal_mean_cube.coord('hour').points+0.5]
     #if s == 0:
         # Areas of ocean
     #    print total_rainfall  
         #np.save('%s%s/%s/%s_sea_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s_monsoon_trough' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), trnp)
         #np.save('%s%s/%s/%s_sea_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s_MASKED_ARRAY' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), maskedcube)
     if s == 1:
          # Areas of land
         np.save('%s%s/%s/%s_land_rainfall_diurnal_np_domain_constrain_monsoon_trough' % (pp_file_path, expmin1, experiment_id, diag), trnp) 
         #np.save('%s%s/%s/%s_land_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s_MASKED_ARRAY' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), maskedcube)
    #del lsm

    #tdmc=  diurnal_mean_cube.collapsed(['grid_latitude', 'grid_longitude'], iris.analysis.MEAN) 
    #total_diurnal_mean_cube=tdmc
    #np.save('%s%s/%s/%s_total_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), tdmc.data.data) 
    #np.save('%s%s/%s/%s_total_rainfall_diurnal_np_domain_constrain_lat_%s-%s_lon-%s-%s_MASKED_ARRAY' % (pp_file_path, expmin1, experiment_id, diag, latmin, latmax, lonmin, lonmax), ma)





