"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys
import datetime

import iris
import iris.unit as unit

diag = '3217'
cube_name='surface_upward_sensible_heat_flux'

#experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu', 'djznu' ]
experiment_ids = ['dkhgu']

#experiment_ids = ['dklwu', 'dklzq','dkbhu' ]

#experiment_ids = ['djzny']
for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1, experiment_id, diag)

 
 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 print experiment_id
 #h=iris.load(fu)
 #print h
 #del h
 fg = '/projects/cascade/pwille/moose_retrievals/djzn/djznw/%s.pp' % diag
 glob_load = iris.load_cube(fg, ('%s' % cube_name)  & time_constraint)
 
## Get time points from global LAM to use as time constraint when loading other runs
 time_list = glob_load.coord('time').points
 glob_tc = iris.Constraint(time=time_list)

 del glob_load
 del time_list

 cube = iris.load_cube(fu,('%s' % cube_name) & glob_tc)
 print cube
 
 sys.stdout.flush()

 try:
     os.remove('/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp' % (expmin1, experiment_id, diag))
 except OSError:
     print '/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp NOT REMOVED' % (expmin1, experiment_id, diag)
     pass 
  
 for t, time_cube in enumerate (cube.slices(['time', 'grid_latitude'])):
    #print time_cube
    u_mean.append = time_cube.collapsed('time', iris.analysis.MEAN)    
 iris.save((u_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/%s_mean.pp' % (expmin1, experiment_id, diag), append=True)

 del cube


