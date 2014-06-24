"""
Find heights of pressure levels from models and save

Run this first, then geopotential.py
"""
import os,sys

import iris
import iris.coords as coords
import iris.unit as unit

#from tempfile import mkdtemp
import numpy as np
import os.path as path

import datetime

import time

import h5py

#from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline




def main():
 experiment_ids = ['dklwu', 'dklzq']
 #experiment_ids = ['djzny', 'djznq', 'djznw', 'djzns', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 #experiment_ids = ['djzny']

 for experiment_id in experiment_ids:
  print "======================================"
  print 'Start of interpolate pressure script'
  print experiment_id
  sys.stdout.flush()
  start_time = time.clock()
  try:
    p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    #p_levels = [400]
    expmin1 = experiment_id[:-1]
   
    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/408.pp' % (expmin1, experiment_id)
    fname_heights = '/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp'% (expmin1, experiment_id)

    save_name_i='/408_pressure_levels_interp_pressure_%s' % experiment_id
    save_path_tempfile='/projects/cascade/pwille/temp/' 
   
    numpy_ar_file = path.join("%s%s" % (save_path_tempfile, save_name_i))
    
    #dtmindt = datetime.datetime(2011,8,20,0,0,0)
    #dtmaxdt = datetime.datetime(2011,8,20,1,0,0)
    #dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)
    #p_at_rho = iris.load_cube(fname, time_constraint)

    p_at_rho = iris.load_cube(fname)
    hl = iris.load_cube(fname_heights)

    no_of_times = p_at_rho.coord('time').points.size
    lat_len = p_at_rho.coord('grid_latitude').points.size
    lon_len = p_at_rho.coord('grid_longitude').points.size

    shape_alltime = (no_of_times,lat_len,lon_len, len(p_levels))
    shape_1time = (lat_len,lon_len, len(p_levels))

    print shape_alltime
   
    sys.stdout.flush()
    heights = hl.slices(['model_level_number', 'grid_latitude', 'grid_longitude']).next()[::-1].data
   
    pi = np.empty((shape_1time), dtype=float)

    with h5py.File(numpy_ar_file, 'w') as i:
     interps = i.create_dataset('interps', dtype='float32', shape=shape_alltime)

     #dt = h5py.special_dtype()
     
     #i_func = np.empty((no_of_times,lat_len,lon_len), dtype=object)
    

     for t, time_cube in enumerate(p_at_rho.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
      
       time_cube_rev = time_cube[::-1,:,:].data/100
       #start_time_int1d = time.clock()
       #for f in range(lat_len):
        # for y in range(lon_len):
        #   i_func[t,f,y] = interp1d(time_cube_rev[:,f,y], heights[:,f,y], kind="cubic", bounds_error=False, fill_value=0)
       #end_time_int1d = time.clock()
          #out = interp1d(time_cube_rev, heights, kind='cubic', bounds_error=False, fill_value=0, axis = 0)')
       

       #start_time_intus = time.clock()  
       for f in range(lat_len):
         for y in range(lon_len):
           i_func = InterpolatedUnivariateSpline(time_cube_rev[:,f,y], heights[:,f,y])
       #end_time_intus = time.clock()
       #print(('%s time elapsed: {0}' % experiment_id).format(end_time_int1d - start_time_int1d))
       #print(('%s time elapsed: {0}' % experiment_id).format(end_time_intus - start_time_intus))
           pi[f,y,:] = i_func(p_levels)

   
       interps[t,:,:,:] = pi
#sys.stdout.flush()
    #i.close() 
    if not os.path.exists(save_path_tempfile): os.makedirs(save_path_tempfile)
    
    #try:
    #    np.save("%s%s" % (save_path_dp, save_name_i), i_func)
    #except Exception,e:
     #    print e
     #    print 'NP failed'
      #   print sys.exc_traceback.tb_lineno
      #   sys.stdout.flush()
      #   pass
    #else:
     # del i_func2

    end_time=time.clock()
    print(('%s time elapsed: {0}' % experiment_id).format(end_time - start_time))

# End of try for experiment_id loop  
  except Exception,e:
      print e
      print sys.exc_traceback.tb_lineno 
      print 'Failed to run interpolate script for %s' % experiment_id
      sys.stdout.flush()
      #pass
 #try:
 #       os.system('/home/pwille/python_scripts/geopotential/geopotential_multiple.py') 
 #except Exception,e:
 #       print e 
 #       print 'Failed to run /home/pwille/python_scripts/geopotential/geopotential.py'
 #       sys.stdout.flush()
 #       pass
 
if __name__ == '__main__':
    main()
