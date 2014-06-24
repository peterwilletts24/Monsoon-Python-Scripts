import os, sys
import datetime

import iris
import iris.unit as unit

import numpy as np

from iris.coord_categorisation import add_categorised_coord

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='precipitation_flux'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
#experiment_ids = ['djzns', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ]
#experiment_ids = [ 'dklwu', 'dklzq', 'dklyu', 'dkmbq', 'dkbhu', 'djznu', 'dkhgu', 'djzns' ]
#experiment_ids = ['djzns', 'dkbhu', 'djznu', 'dkhgu' ]
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq']

# Load global LAM
dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg, ('%s' % cube_name_param)  & time_constraint)   

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)

del glob_load




for experiment_id in experiment_ids:

    expmin1 = experiment_id[:-1]

    #fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)

    flsm = '%s%s/%s/30.pp' % (pp_file_path, expmin1, experiment_id)
    fdm = '%s%s/%s/%s_rainfall_hourly_mean.pp' % (pp_file_path, expmin1, experiment_id, diag)
    print experiment_id
    sys.stdout.flush()

# Load diurnal mean cube
    try:
         diurnal_mean_cube = iris.load_cube(fdm, ('%s' % cube_name_explicit)  & glob_tc)
    except iris.exceptions.ConstraintMismatchError:        
         diurnal_mean_cube = iris.load_cube(fdm, ('%s' % cube_name_param)  & glob_tc)
    
    add_categorised_coord(diurnal_mean_cube, 'hour', 'time',lambda coord, x: coord.units.num2date(x).hour)
 
        
# Load land/sea mask 

    lsm = iris.load_cube(flsm, ('land_binary_mask' ))

    print lsm
   
    sys.stdout.flush()

# For Sea and Land, mask area and calculate mean of each hour for sea/land and SAVE as numpy array

    for s in ([0,1]):
     ms = np.where(lsm.data==s, diurnal_mean_cube.data, np.NaN)
     nancube = np.where(lsm.data==s, diurnal_mean_cube.data, np.NaN)
     maskedcube = np.ma.masked_array(nancube,np.isnan(nancube))
     total_rainfall = np.mean(maskedcube.reshape(maskedcube.shape[0], (maskedcube.shape[1]*maskedcube.shape[2])), axis=1)
     trnp =[total_rainfall.data, diurnal_mean_cube.coord('hour').points+0.5]
     if s == 0:
         # Areas of ocean
         print total_rainfall
         np.save('%s%s/%s/%s_sea_rainfall_diurnal_np' % (pp_file_path, expmin1, experiment_id, diag), trnp)
         #iris.save(total_rainfall, '%s%s/%s/%s_seamask_diurnal_total.pp' % (pp_file_path, expmin1, experiment_id, diag))
     if s == 1:
          # Areas of land
         np.save('%s%s/%s/%s_land_rainfall_diurnal_np' % (pp_file_path, expmin1, experiment_id, diag), trnp)      
         #iris.save(total_rainfall, '%s%s/%s/%s_landmask_diurnal_total.pp' % (pp_file_path, expmin1, experiment_id, diag))

    del lsm





