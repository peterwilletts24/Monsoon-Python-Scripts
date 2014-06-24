"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and pickle
"""

import os, sys
import datetime

import iris
import iris.unit as unit

print 'Make sure you delete old 30201_mean files first.  Or append save will go wrong'



#experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ]
experiment_ids = ['dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
#experiment_ids = ['djzns']
for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/30201.pp' % (expmin1, experiment_id)

 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 w = iris.load(fu,time_constraint)

 try:
     u_wind,v_wind=w
 except Exception,e:
    print e
    print w
    print 'pp file  may have more cubes than it should - loading Cube 0 as u component (east) and 1 as v component (west)'
    sys.stdout.flush()

    u_wind = w[0]
    #v_wind = w[1]
    pass

 for t, time_cube in enumerate (u_wind.slices(['time', 'grid_latitude', 'grid_longitude'])):
    print time_cube
    u_mean = time_cube.collapsed('time', iris.analysis.MEAN)    
    iris.save((u_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/30201_mean.pp' % (expmin1, experiment_id), append=True)

 del u_wind
 v_wind = w[1]
 del w

 for t, time_cube in enumerate (v_wind.slices(['time', 'grid_latitude', 'grid_longitude'])):
    print time_cube
    v_mean = time_cube.collapsed('time', iris.analysis.MEAN)    
    iris.save((v_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/30201_mean.pp' % (expmin1, experiment_id), append=True)


