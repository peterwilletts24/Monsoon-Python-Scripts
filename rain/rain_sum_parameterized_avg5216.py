"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit

diag = 'avg.5216'
cube_name='precipitation_flux'

experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/avg.5216.pp' % (expmin1, experiment_id)

 dtmindt = datetime.datetime(2011,8,19,0,0,0)
 dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
 dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
 time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

 # Load global LAM
 fg = '/projects/cascade/pwille/moose_retrievals/djzn/djznw/%s.pp' % diag
 glob_load = iris.load_cube(fg, ('%s' % cube_name)  & time_constraint)

 ## Get time points from global LAM to use as time constraint when loading other runs
 time_list = glob_load.coord('time').points
 glob_tc = iris.Constraint(time=time_list)

 del glob_load
 del time_list

 rain = iris.load_cube(fu,('%s' % cube_name) & glob_tc)
 print rain

 # Rainfall output with Stuart scripts as hourly mean. time_interval is time_interval as fraction of hour
 t = rain.coord('time').points
 time_interval = (t.flatten()[1]-t.flatten()[0])

 iris.analysis.maths.multiply(rain,60*(60*time_interval),in_place=True)

 rain_total = rain.collapsed('time', iris.analysis.SUM)    
 iris.save((rain_total),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_total.pp' % (expmin1, experiment_id))


