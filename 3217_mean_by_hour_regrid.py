"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord
from iris.analysis.cartography import unrotate_pole

import numpy as np

diag = '3217'
cube_name='surface_upward_sensible_heat_flux'


pp_file_path='/projects/cascade/pwille/moose_retrievals/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

regrid_model='djznw'
regrid_model_min1=regrid_model[:-1]

def add_hour_of_day(cube, coord, name='hour'):
    add_categorised_coord(cube, name, coord,
          lambda coord, x: coord.units.num2date(x).hour)

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fr = '%s%s/%s/%s.pp' % (pp_file_path, regrid_model_min1, regrid_model, diag)
fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg, ('%s' % cube_name)  & time_constraint)

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
# Some models have radiation diagnostics that are 10s offset from others so checking int values of time 
glob_tc = iris.Constraint(time= lambda t: int(t.point) in time_list.astype(int))
#glob_tc = iris.Constraint(time=time_list)



regrid_cube = iris.load_cube(fr, ('%s' % cube_name)  & glob_tc)

del glob_load

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1, experiment_id, diag)

 print experiment_id
 sys.stdout.flush()

      
 cube = iris.load_cube(fu, ('%s' % cube_name)  & glob_tc)

 cs = cube.coord_system('CoordSystem')

 lons, lats = np.meshgrid(cube.coord('grid_longitude').points, cube.coord('grid_latitude').points)

 unrot_lons, unrot_lats = unrotate_pole(lons, 
                                        lats,
                                        cs.grid_north_pole_longitude,
                                        cs.grid_north_pole_latitude)
                                        
 
 latmin = unrot_lats.min()
 latmax = unrot_lats.max()
 lonmin = unrot_lons.min()
 lonmax = unrot_lons.max()

 lat_constraint=iris.Constraint(grid_latitude= lambda la: latmin <= la.point <= latmax)
 lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin <= lo.point <= lonmax)  

 print regrid_cube      

 regrid_cube = regrid_cube.extract(lat_constraint & lon_constraint)

 print regrid_cube

 cube = iris.analysis.interpolate.regrid(cube, regrid_cube, mode='bilinear')

 time_coords = cube.coord('time')
 add_hour_of_day(cube, time_coords)
 
 mean = cube.aggregated_by('hour', iris.analysis.MEAN)
 iris.save((mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean_by_hour_regrid.pp' % (expmin1, experiment_id, diag))


