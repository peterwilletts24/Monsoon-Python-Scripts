"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

#experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']
experiment_ids = ['dkhgu', 'djznu', 'dkbhu']

def add_hour_of_day(cube, coord, name='hour'):
    add_categorised_coord(cube, name, coord,
          lambda coord, x: coord.units.num2date(x).hour)

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

 try:
     os.remove('/projects/cascade/pwille/moose_retrievals/%s/%s/rain_mean.pp' % (expmin1, experiment_id))
 except OSError,e:
     print '/projects/cascade/pwille/moose_retrievals/%s/%s/rain_mean.pp NOT REMOVED' % (expmin1, experiment_id)
     print e
     pass 

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/avg.5216.pp' % (expmin1, experiment_id)

 print experiment_id
 sys.stdout.flush()

 try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc)
        cube_f=cubeconv+cubestrat
        cube_f.rename('total_precipitation_rate')
 except iris.exceptions.ConstraintMismatchError:        
        cube_f = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc)
         
 time_coords = cube_f.coord('time')
 add_hour_of_day(cube_f, time_coords)

 interval = 250 
 l_2s_min_ind = range(0,cube_f.coord('grid_longitude').shape[0]-1,interval)
 l_2s_max_ind = range((interval-1),cube_f.coord('grid_longitude').shape[0],interval)

 long_2s_min = cube_f.coord('grid_longitude').points[l_2s_min_ind]
 long_2s_max = cube_f.coord('grid_longitude').points[l_2s_max_ind]

 for i,l in enumerate(long_2s_min): 
  #lon_in_2s = iris.Constraint(grid_longitude=[l,long_2s_max[i]])
  lon_in_2s = iris.Constraint(grid_longitude= lambda g:  l <= g.point <= long_2s_max[i])
  cube = cube_f.extract(glob_tc & lon_in_2s)
  print cube
  sys.stdout.flush()


# Rainfall output with Stuart scripts as hourly mean. time_interval is time_interval as fraction of hour
# t = rain.coord('time').points
# time_interval = (t.flatten()[1]-t.flatten()[0])

# iris.analysis.maths.multiply(rain,60*(60*time_interval),in_place=True)

 #rain_total = rain.collapsed('time', iris.analysis.SUM)    
  for t, time_cube in enumerate (cube.slices(['time', 'grid_latitude', 'grid_longitude'])):
    #print time_cube
     rain_mean = cube.aggregated_by('hour', iris.analysis.MEAN)
     #rain_mean = time_cube.collapsed('time', iris.analysis.MEAN)
     rain_mean.rename('mean_total_precipitation_rate')
     iris.save((rain_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_mean_by_hour.pp' % (expmin1, experiment_id), append=True)


