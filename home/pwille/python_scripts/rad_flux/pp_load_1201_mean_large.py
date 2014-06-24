"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys
import datetime

import iris
import iris.unit as unit

diag = '1201'
cube_name='surface_net_downward_shortwave_flux'

experiment_ids = ['dkhgu', 'djznu', 'dkbhu']

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 try:
     os.remove('/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp' % (expmin1, experiment_id, diag))
 except OSError,e:
     print '/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp NOT REMOVED' % (expmin1, experiment_id, diag)
     print e
     pass 


 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1, experiment_id, diag)

 
 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 #print experiment_id
 #h=iris.load(fu)
 #print h
 fg = '/projects/cascade/pwille/moose_retrievals/djzn/djznw/%s.pp' % diag
 glob_load = iris.load_cube(fg, ('%s' % cube_name)  & time_constraint)
 
## Get time points from global LAM to use as time constraint when loading other runs
 time_list = glob_load.coord('time').points

 #glob_tc = iris.Constraint(time=time_list)
# Some models have radiation diagnostics that are 10s offset from others so checking int values of time 
 glob_tc = iris.Constraint(time= lambda t: int(t.point) in time_list.astype(int))
 del glob_load

 cube_f = iris.load_cube(fu,('%s' % cube_name) & glob_tc)
 print cube_f
 sys.stdout.flush()

 interval = 250 
 l_2s_min_ind = range(0,cube_f.coord('grid_longitude').shape[0]-1,interval)
 l_2s_max_ind = range((interval-1),cube_f.coord('grid_longitude').shape[0],interval)

 long_2s_min = cube_f.coord('grid_longitude').points[l_2s_min_ind]
 long_2s_max = cube_f.coord('grid_longitude').points[l_2s_max_ind]


 for i,l in enumerate(long_2s_min): 
  #lon_in_2s = iris.Constraint(grid_longitude=[l,long_2s_max[i]])
  lon_in_2s = iris.Constraint(grid_longitude= lambda g:  l <= g.point <= long_2s_max[i])
  cube = cube_f.extract(('%s' % cube_name) & glob_tc & lon_in_2s)
  print cube
  sys.stdout.flush()

  for t, time_cube in enumerate (cube.slices(['time', 'grid_latitude', 'grid_longitude'])):
    #print time_cube
     u_mean = time_cube.collapsed('time', iris.analysis.MEAN)    
 
     iris.save((u_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp' % (expmin1, experiment_id, diag), append=True)

  #del cube


