"""
Find heights of pressure levels from models and save

Run this first, then geopotential.py
"""
import os,sys

import iris
import iris.coords as coords
import iris.unit as unit

import numpy as np

import datetime


def main():
    experiment_id = 'djzns'
    expmin1 = experiment_id[:-1]
    
    p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    #p_levels = [400]
   
   
    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/408.pp' % (expmin1, experiment_id)
    
    save_path_dp='/home/pwille/python_scripts/%s' % (experiment_id)
    save_name_dp='/407_pressure_levels_dp_%s' % experiment_id

    #dtmindt = datetime.datetime(2011,8,20,0,0,0)
    #dtmaxdt = datetime.datetime(2011,8,20,1,0,0)

    #dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
   
    
    #time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)
    #p_at_rho = iris.load_cube(fname, time_constraint)
    p_at_rho = iris.load_cube(fname)

    shape_alltime = p_at_rho[:,0:len(p_levels),:,:].shape

    print shape_alltime
    
    data_positions = np.zeros(shape_alltime)
    

    for t, time_cube in enumerate(p_at_rho.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
        

#  Reverse time cube because searchsorted needs an array with ascending values to work. /100 to convtert to hPa at the same time

        time_cube_rev = time_cube[::-1,:,:].data/100
       
        for n, p_lev in enumerate(p_levels):

            data_positions[t,n] = np.apply_along_axis(lambda a: a.searchsorted(p_lev), axis = 0, arr = time_cube_rev)

            
    if not os.path.exists(save_path_dp): os.makedirs(save_path_dp)
    
    try:
        np.savez("%s%s" % (save_path_dp, save_name_dp), dp=data_positions.astype(int), p=p_levels)
    except Exception:
         print 'NP failed'
         pass

    try:
        os.system('/home/pwille/python_scripts/geopotential.py') 
    except Exception:
         print 'Failed to run /home/pwille/python_scripts/geopotential.py'
         pass
if __name__ == '__main__':
    main()
