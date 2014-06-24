"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit

experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ]
#experiment_ids = ['dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ]

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/272.pp' % (expmin1, experiment_id)

 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 rain = iris.load_cube(fu,time_constraint)

 for t, time_cube in enumerate (rain.slices(['time', 'grid_latitude', 'grid_longitude'])):
    print time_cube
    rain_total = time_cube.collapsed('time', iris.analysis.SUM)    
    iris.save((rain_total),'/projects/cascade/pwille/moose_retrievals/%s/%s/272_total.pp' % (expmin1, experiment_id), append=True)
 

