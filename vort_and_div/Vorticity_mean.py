"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit

diag = 'vorticity'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

pressure_levels=['925', '850', '700', '500'] 

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fg = '%sdjzn/djznw/%s_925.pp' % (pp_file_path, diag)
glob_load = iris.load_cube(fg, time_constraint)

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)


del glob_load
for experiment_id in experiment_ids:
  for p in pressure_levels:
   try:
    expmin1 = experiment_id[:-1]

    fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s.pp' % (expmin1, experiment_id, diag, p )

    print experiment_id
    sys.stdout.flush()

    cube  = iris.load_cube(fu,glob_tc)
   
    for t, time_cube in enumerate (cube.slices(['time', 'latitude', 'longitude'])):
     mean = cube.collapsed('time', iris.analysis.MEAN) 
    iris.save((mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s_mean.pp' % (expmin1, experiment_id, diag, p))

   except Exception, e:
       print e
       pass
