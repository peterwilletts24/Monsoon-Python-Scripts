"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord

import pdb

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

def add_hour_of_day(cube, coord, name='hour'):
    add_categorised_coord(cube, name, coord,
          lambda coord, x: coord.units.num2date(x).hour)

#def add_day_of_year(cube, coord, name='day_of_year'):
#    add_categorised_coord(cube, name, coord,
#          lambda coord, x: coord.units.num2date(x).day_of_year)



pdb.set_trace()

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

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/avg.5216.pp' % (expmin1, experiment_id)

 print experiment_id
 sys.stdout.flush()

 try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc)
        cube=cubeconv+cubestrat
        cube.rename('total_precipitation_rate')
 except iris.exceptions.ConstraintMismatchError:        
        cube = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc)
         
 time_coords = cube.coord('time')
 #add_hour_of_day(cube, time_coords)
 iris.coord_categorisation.add_day_of_year(cube, time_coords, name='day_of_year')
 #hours=[dt.hour for dt in time_dt.astype(object)]
 

 # Rainfall output with Stuart scripts as hourly mean. time_interval is time_interval as fraction of hour
# t = rain.coord('time').points
# time_interval = (t.flatten()[1]-t.flatten()[0])

# iris.analysis.maths.multiply(rain,60*(60*time_interval),in_place=True)

 #rain_total = rain.collapsed('time', iris.analysis.SUM)    
 #for t, time_cube in enumerate (cube.slices(['time', 'grid_latitude', 'grid_longitude'])):
 rain_mean = cube.aggregated_by('day_of_year', iris.analysis.MEAN)
 iris.save((rain_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_mean_by_day.pp' % (expmin1, experiment_id))


