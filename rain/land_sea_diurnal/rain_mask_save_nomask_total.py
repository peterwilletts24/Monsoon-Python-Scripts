import os, sys
import datetime

import iris
import iris.unit as unit

import numpy as np

from iris.coord_categorisation import add_categorised_coord

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
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

latmin=-6.79
latmax=33.038
lonmin=340
lonmax=379.98

lonmin=340
lonmax=379.98

lonmin_g=64.115
lonmax_g=101.866

lat_constraint=iris.Constraint(grid_latitude= lambda la: latmin <= la.point <= latmax)
#lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin <= lo.point <= lonmax)

fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg, ('%s' % cube_name_param)  & time_constraint)   

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)

del glob_load

for experiment_id in experiment_ids:

    if (experiment_id=='djznw'):
        lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin_g <= lo.point <= lonmax_g)
    else:
        lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin <= lo.point <= lonmax) 

    expmin1 = experiment_id[:-1]

    fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)

    flsm = '%s%s/%s/30.pp' % (pp_file_path, expmin1, experiment_id)
 
    print experiment_id
    sys.stdout.flush()

    try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc & lat_constraint & lon_constraint)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc & lat_constraint & lon_constraint)
        cube=cubeconv+cubestrat
        cube.rename('total_precipitation_rate')
    except iris.exceptions.ConstraintMismatchError:        
        cube = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc & lat_constraint & lon_constraint)
         
    #time_interval = (cube.coord('time').points[1]-cube.coord('time').points[0])

# Mean at each grid point by hour of day and save    
                                                      #helper = np.vectorize(lambda r : r.hour)
                                                          #hour = helper(h)  

    add_categorised_coord(cube, 'hour', 'time',lambda coord, x: coord.units.num2date(x).hour)
    diurnal_mean_cube = cube.aggregated_by('hour', iris.analysis.MEAN)
 
    del cube

    #try:
    #    iris.save(diurnal_mean_cube, '%s%s/%s/%s_rainfall_hourly_mean.pp' % (pp_file_path, expmin1, experiment_id, diag))
    #except Exception, e:
    #    print e
    #    pass
        
# Load land/sea mask 

   
# For Sea and Land, mask area and calculate mean of each hour for sea/land and SAVE as numpy array

    

    tdmc =  diurnal_mean_cube.collapsed(['grid_latitude', 'grid_longitude'], iris.analysis.MEAN) 
    total_diurnal_mean_cube = [tdmc.data, tdmc.coord('hour').points+0.5]
    np.save('%s%s/%s/%s_total_rainfall_diurnal_np_domain_constrain' % (pp_file_path, expmin1, experiment_id, diag), total_diurnal_mean_cube) 





