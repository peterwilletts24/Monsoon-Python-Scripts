"""
Find heights of pressure levels from models and save
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
    
 #experiment_ids = ['dkbhu', 'djzns', 'djznq', 'djzny', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 experiment_ids = ['djzny']   
 
 for experiment_id in experiment_ids:
  try:
    start_time = time.time()
    expmin1 = experiment_id[:-1]
    p_levels = [1000., 950., 925., 850., 700., 500., 400., 300., 250., 200., 150., 100., 70., 50., 30., 20., 10.]
    #p_levels = [400]
   
    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/408.pp' % (expmin1, experiment_id)
    fsp = '/projects/cascade/pwille/moose_retrievals/%s/%s/409.pp'% (expmin1, experiment_id)
    fname_heights = '/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp'% (expmin1, experiment_id)
    f_oro =  '/projects/cascade/pwille/moose_retrievals/%s/%s/33.pp'% (expmin1, experiment_id)
    
    save_path_dp='/projects/cascade/pwille/python_output/%s' % (experiment_id)
    save_name_dp='/408_pressure_levels_dp_%s' % experiment_id

    save_path_h='/projects/cascade/pwille/python_output/%s' % (experiment_id)
    save_name_h='/408_pressure_levels_h_%s' % experiment_id

    save_path_tempfile='/projects/cascade/pwille/temp' 

    numpy_ar_file = path.join("%s%s" % (save_path_tempfile, save_name_h))
    
# Load data positions ( rho level with higher pressure (lower height) than reference levels
    #data_load = np.load("%s%s.npz" % (save_path_dp, save_name_dp), mmap_mode='r')
    #data_p_load = data_load['dp']
    #p_levels = data_load['p']

 # Set time range

    #dtmindt = datetime.datetime(2011,8,20,0,0,0)
    #dtmaxdt = datetime.datetime(2011,8,20,1,0,0)

    #dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
       
    #time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)
#    single_time_constraint = iris.Constraint(time= lambda cell: cell <= )
# Load iris cubes for pressure at model levels, height_of_levels, surface pressure, orography  

    #p_at_rho = iris.load_cube(fname, time_constraint)
    p_at_rho = iris.load_cube(fname)
    hl = iris.load_cube(fname_heights)
    #surf_p = iris.load_cube(fsp, time_constraint)
    surf_p = iris.load_cube(fsp)
    oro = iris.load_cube(f_oro)  

# Get array shapes for initializing

    no_of_times = p_at_rho.coord('time').points.size
    lat_len = p_at_rho.coord('grid_latitude').points.size
    lon_len = p_at_rho.coord('grid_longitude').points.size
   
    shape_1time = (lat_len, lon_len)
    shape_alltime = (no_of_times,len(p_levels),lat_len,lon_len)
    
    print shape_alltime
    sys.stdout.flush()
    #height = np.memmap(numpy_ar_file, dtype='float32', mode='w+', shape=shape_alltime)

# Load data position file from previous script
    f = h5py.File(("%s%s" % (save_path_tempfile, save_name_dp)), 'r')
    data_p_full = f['d_p']
    print data_p_full.shape

# Create heights file

    h = h5py.File(numpy_ar_file, 'w')
    height = h.create_dataset('he', dtype='float32', shape=shape_alltime)

    lats = h.create_dataset('lat', oro.coord('grid_latitude').points.shape, dtype='float32')
    lons = h.create_dataset('lon', oro.coord('grid_longitude').points.shape, dtype='float32')
    ti = h.create_dataset('time', oro.coord('time').points.shape, dtype='float32')

    lats = oro.coord('grid_latitude').points
    lons =  oro.coord('grid_longitude').points
    ti = oro.coord('time').points

#Number of levels in model output

    number_of_levels = p_at_rho.coord('model_level_number').points.size

# Get data from pp cubes that do not vary with time 
    height_of_level = hl[0,::-1,:,:].data
    oro_data = oro[0].data
    
# Pre declare arrays

    p0 = np.zeros(shape_1time)
    p1 = np.zeros(shape_1time) 
    h0 = np.zeros(shape_1time)
    h1 = np.zeros(shape_1time)
    layer_p = np.zeros(shape_1time)

    time_coord=0
    for coord in p_at_rho.coords():
      if coord.name()=='forecast_period':
        frt=0.
        fp = 0.
        time_coord=2
        print '%s has Forecast Period and Reference Time Coords' % experiment_id
        sys.stdout.flush()
   
# Create  arrays of indices for picking later (sigh)
    x_coords, y_coords = np.indices((shape_1time))

# Select time slice
    for t, time_cube in enumerate(p_at_rho.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
        #print t
#  Reverse pressure on model levels and surface pressure data  cubes because searchsorted needs an array with ascending values to work. /100 to convert to hPa at the same time

        time_cube_rev = time_cube[::-1,:,:].data/100
        
# 
        if time_coord==2:
          frt = time_cube.coord('forecast_reference_time').points[0]            
          fp = time_cube.coord('forecast_period').points[0]
          surf_p_time = surf_p.extract(iris.Constraint(forecast_reference_time=frt, forecast_period=fp)).data/100
        else:
          for coord in p_at_rho.coords():
            print coord.name
        #print time_cube_rev.shape
# Loop through pressure levels
        #for n, p_lev in enumerate(p_levels):
            
           
# Filter out data positions that are outside index range (pressure below ground surface)
            data_positions = data_p_full[t].astype(int)
            dpmin1 = (data_p_full[t]-1).astype(int)
            #print data_positions.shape
            #print surf_p_time.shape
            
            #data_positions =np.where(time_cube_rev[dpmin1_temp, x_coords, y_coords]>p_lev, dpmin1_temp+1, dpmin1_temp+1)
            p0_filt_time = data_positions*(np.less(data_positions,number_of_levels))
            #print p0_filt_time.shape
            p0_surf_filt = np.logical_and((p0_filt_time) == number_of_levels, p_lev < surf_p_time)
            #print p0_surf_filt.shape
            p0 = np.where(p0_filt_time>0, time_cube_rev[p0_filt_time, x_coords, y_coords], 0)
            p0 = p0 + (surf_p_time * p0_surf_filt) 

            #p1 = time_cube_rev[data_positions-1]
            p1 =np.where(p0>0.,time_cube_rev[dpmin1, x_coords, y_coords], 0)
               
            h1 =np.where(p0>0.,height_of_level[dpmin1, x_coords, y_coords], 0)

            h0 = np.where(p0_filt_time>0., height_of_level[p0_filt_time, x_coords, y_coords], 0)  
            h0 = h0 + (oro_data * p0_surf_filt)

            p0[p0<=0]=np.nan
            p1[p1<=0]=np.nan
            
            #layer_p= np.where(p0>0., ((np.log(p_lev) - np.log(p1)) / (np.log(p0) - np.log(p1))), 0)
            layer_p= np.where(np.isnan(p0), 0, ((np.log(1000) - np.log(p1)) / (np.log(p0) - np.log(p1))))
  




p_diff=np.diff(time_cube_rev, axis =0)

p_diff_dp = p_diff[p0_filt_time-1,x_coords,y_coords]
            #print 'P1 %s P0 %s H1 %s H0 %s P DIFF %s' %(p1,p0,h1,h0,layer_p)
            
            #print layer_p.shape            
            #print p0.shape
            #print p1.shape
            
            height[t,n] =  np.where(p0>0., (h0 + (h1 - h0)*(1-layer_p)),0)
           
            #print "Height calc bit (part 2 of 2). Pressure level %s.  Time %s. Finished" % (p_lev, t)
            sys.stdout.flush()
    
    

    
    f.close()
    h.close()
  
    end_time=time.time()
    print(('%s time elapsed: {0}' % experiment_id).format(end_time - start_time))

  except Exception,e:
   print e   
   print sys.exc_traceback.tb_lineno 
   print 'Failed to run dp script for %s' % experiment_id
   sys.stdout.flush()
   pass


if __name__ == '__main__':
    main()

 #   try:
 #       np.savez_compressed("%s%s" % (save_path_h, save_name_h), h=height, p=p_levels, lat=lat, lon=lon, time=time)
  #  except Exception,e:
  #      print e
   #     print 'NP failed'
    #    sys.stdout.flush()
  #      pass
  #  try:
  #      np.savez_compressed(("%s%s_p0etc" % (save_path_h, save_name_h)), p0, p1, h0, h1, layer_p)
  #  except Exception,e:
  #      print e
   #     print 'NP 2 failed'
   #     sys.stdout.flush()
   #     pass
  #  else:
  #      del height
   
