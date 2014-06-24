"""
Find heights oftemperature etc. on  pressure levels from models and save

Takes calculate pressure level heights from geopotential_interpolate_multiple.py
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

    #experiment_ids = ['djzny', 'djznq', 'djznw', 'djzns', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 experiment_ids = ['dkbhu']
 for experiment_id in experiment_ids:
  print "======================================"
  print 'Start of interpolate script for temp/specific humidity'
  print experiment_id
  sys.stdout.flush()
  start_time = time.clock()
  try:
      p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
      expmin1 = experiment_id[:-1]
      
      fname_heights = '/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp'% (expmin1, experiment_id)

      fname_temp = '/projects/cascade/pwille/moose_retrievals/%s/%s/4.pp' % (expmin1, experiment_id)
      fname_sp_hum= '/projects/cascade/pwille/moose_retrievals/%s/%s/10.pp' % (expmin1, experiment_id)
      path_tempfile='/projects/cascade/pwille/temp/' 
      load_name_i='/408_pressure_levels_interp_pressure_%s' % experiment_id

      save_name_temp='/temp_pressure_levels_interp_%s' % experiment_id
      save_name_sp_hum='/sp_hum_pressure_levels_interp_%s' % experiment_id

      temp_p_heights_file = path.join("%s%s" % (path_tempfile, save_name_temp))
      sp_hum_p_heights_file = path.join("%s%s" % (path_tempfile, save_name_sp_hum))

      p_heights_file = path.join("%s%s" % (path_tempfile, load_name_i))

      hl = iris.load_cube(fname_heights)

      temp_cube = iris.load_cube(fname_temp) 
      sp_hum_cube = iris.load_cube(fname_sp_hum) 

      no_of_times = temp_cube.coord('time').points.size
      lat_len = temp_cube.coord('grid_latitude').points.size
      lon_len = temp_cube.coord('grid_longitude').points.size

      shape_alltime = (no_of_times,lat_len,lon_len, len(p_levels))
      shape_1time = (lat_len,lon_len, len(p_levels))

      print shape_alltime
      
      te = np.empty((shape_1time), dtype=float)
      sh = np.empty((shape_1time), dtype=float)
      sys.stdout.flush()

      heights = hl.slices(['model_level_number', 'grid_latitude', 'grid_longitude']).next().data

      with h5py.File(p_heights_file, 'r') as i:
       p_hsf = i['interps']
       with h5py.File(temp_p_heights_file, 'w') as tf:
        temps = tf.create_dataset('t_on_p', dtype='float32', shape=shape_alltime)                 

        for t, time_cube in enumerate(temp_cube.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
                p_hs=p_hsf[t,:,:,:]
                tc = time_cube.data
  
                for f in range(lat_len):
                 for y in range(lon_len):
                
                     i_func_t = InterpolatedUnivariateSpline(heights[:,f,y], tc[:,f,y])
                    
                     te[f,y,:] = i_func_t(p_hs[f,y,:])       
                     
                temps[t,:,:,:] = te
       with h5py.File(sp_hum_p_heights_file, 'w') as s:
        sphums = s.create_dataset('sh_on_p', dtype='float32', shape=shape_alltime)
         
        for t, time_cube in enumerate(sp_hum_cube.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
                p_hs=p_hsf[t,:,:,:]
                sphc = time_cube.data
  
                for f in range(lat_len):
                 for y in range(lon_len):
                     
                     i_func_sh = InterpolatedUnivariateSpline(heights[:,f,y], sphc[:,f,y])
                     
                     sh[f,y,:] = i_func_sh(p_hs[f,y,:])
                                
                sphums[t,:,:,:] = sh
      
      end_time=time.clock()
      print(('%s time elapsed: {0}' % experiment_id).format(end_time - start_time))

      # End of try for experiment_id loop  
  except Exception,e:
      print e
      print sys.exc_traceback.tb_lineno 
      print 'Failed to run interpolate script for %s' % experiment_id
      sys.stdout.flush()
      #pass

if __name__ == '__main__':
    main()
