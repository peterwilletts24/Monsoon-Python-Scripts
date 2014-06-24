"""
Find heights of pressure levels from models and save

Run this first, then geopotential.py
"""
import os,sys

import iris
import iris.coords as coords
import iris.unit as unit

from tempfile import mkdtemp
import numpy as np
import os.path as path

import datetime

import time

import h5py


def main():
 #experiment_ids = ['djzny', 'dkbhu', 'djzns', 'djznq', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 #experiment_ids = ['dkbhu', 'djzns', 'djznq', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 experiment_ids = ['djzny', 'djznq', 'djznw', 'djzns', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
#experiment_ids = ['djzns', 'djznq']
 for experiment_id in experiment_ids:
  print experiment_id
  sys.stdout.flush()
  start_time = time.time()
  try:
    p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    #p_levels = [400]
    expmin1 = experiment_id[:-1]
   
    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/408.pp' % (expmin1, experiment_id)
    
    save_path_dp='/projects/cascade/pwille/python_output/%s' % (experiment_id)
    save_name_dp='/408_pressure_levels_dp_%s' % experiment_id
    save_path_tempfile='/projects/cascade/pwille/temp/' 
    #numpy_ar_file = path.join('/projects/cascade/pwille/temp/', '%sdp.dat' %experiment_id)
    numpy_ar_file = path.join("%s%s" % (save_path_tempfile, save_name_dp))
    
    

    #dtmindt = datetime.datetime(2011,8,20,0,0,0)
    #dtmaxdt = datetime.datetime(2011,8,20,1,0,0)

    #dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
   
    
    #time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)
    #p_at_rho = iris.load_cube(fname, time_constraint)
    p_at_rho = iris.load_cube(fname)

    no_of_times = p_at_rho.coord('time').points.size
    lat_len = p_at_rho.coord('grid_latitude').points.size
    lon_len = p_at_rho.coord('grid_longitude').points.size

    shape_alltime = (no_of_times,len(p_levels),lat_len,lon_len)
    print shape_alltime
    sys.stdout.flush()

    #data_positions = np.memmap(numpy_ar_file, dtype='int', mode='w+', shape=shape_alltime)
    f = h5py.File(numpy_ar_file, 'w')
    data_positions = f.create_dataset('d_p', dtype='int', shape=shape_alltime)
    for t, time_cube in enumerate(p_at_rho.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
        

#  Reverse time cube because searchsorted needs an array with ascending values to work. /100 to convtert to hPa at the same time

        time_cube_rev = time_cube[::-1,:,:].data/100
       
        #for n, p_lev in enumerate(p_levels):

        data_positions[t] = np.apply_along_axis(lambda a: a.searchsorted(p_levels), axis = 0, arr = time_cube_rev)
            #data_positions[t,n].flush()
    
#out = interp1d(p_at_rho[0,0,::-1,0,0].data/100, hl[0,::-1,0,0].data, kind='cubic'
    f.close()

    if not os.path.exists(save_path_dp): os.makedirs(save_path_dp)
    
    #try:
    #    np.savez_compressed("%s%s" % (save_path_dp, save_name_dp), dp=data_positions.astype(int), p=p_levels)
    #except Exception,e:
     #    print e
      #   print 'NP failed'
      #   sys.stdout.flush()
       #  pass
   # else:
      #del data_positions

    end_time=time.time()
    print(('%s time elapsed: {0}' % experiment_id).format(end_time - start_time))

# End of try for experiment_id loop  
  except Exception,e:
      print e
      print 'Failed to run dp script for %s' % experiment_id
      sys.stdout.flush()
      pass
 try:
        os.system('/home/pwille/python_scripts/geopotential/geopotential_multiple.py') 
 except Exception,e:
        print e 
        print 'Failed to run /home/pwille/python_scripts/geopotential/geopotential.py'
        sys.stdout.flush()
        pass
 
if __name__ == '__main__':
    main()
