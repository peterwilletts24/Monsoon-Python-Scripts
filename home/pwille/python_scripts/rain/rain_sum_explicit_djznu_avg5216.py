"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit

#experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ]
#experiment_ids = ['dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ]
experiment_ids = ['djznu']
for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/4203.pp' % (expmin1, experiment_id)

 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 rain = iris.load_cube(fu, time_constraint)
 print rain
 
 # Rainfall output with Stuart scripts as hourly mean. time_interval is time_interval as fraction of hour
 time_interval = (rain.coord('time').points[1]-rain.coord('time').points[0])
 print time_interval
 #rain_pcp_flux = rain[3] 
 #for t, time_cube in enumerate (rain.slices(['time', 'grid_latitude', 'grid_longitude'])):
 iris.analysis.maths.multiply(rain,60*(60*time_interval),in_place=True)


 rain_total = rain.collapsed('time', iris.analysis.SUM)    

 save_range=np.arange
 iris.save((rain_total[0:1000,:]),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_total.pp' % (expmin1, experiment_id))
 iris.save((rain_total[1001:2000,:]),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_total.pp' % (expmin1, experiment_id), append=True)
 iris.save((rain_total[2001:-1,:]),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_total.pp' % (expmin1, experiment_id), append=True)
