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


def main():
    
 #experiment_ids = ['dkbhu', 'djzns', 'djznq', 'djzny', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
 experiment_ids = ['djznw']   
 for experiment_id in experiment_ids:
  try:
    
    expmin1 = experiment_id[:-1]
    #p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    #p_levels = [400]
   
    fname_p_temp = '/projects/cascade/pwille/moose_retrievals/%s/%s/4.pp' % (expmin1, experiment_id)

    load_path_h='/projects/cascade/pwille/python_output/%s' % (experiment_id)
    load_name_h='/408_pressure_levels_h_%s' % experiment_id

    save_path='/projects/cascade/pwille/python_output/%s' % (experiment_id)     
    save_name_pt='/4_pt_on_p_levels_%s' % experiment_id

    save_path_tempfile='/projects/cascade/pwille/temp/' 

    numpy_ar_file = path.join("%s%s" % (save_path_tempfile, save_name_pt))     
    pt = iris.load_cube(fname_p_temp)
    
# Load data positions ( rho level with higher pressure (lower height) than reference levels
    data_load = np.load("%s%s.npz" % (load_path_h, load_name_h), mmap_mode='r')
    data_p_load = data_load['dp']
    p_levels = data_load['p']
 # Set time range

    #dtmindt = datetime.datetime(2011,8,20,0,0,0)
    #dtmaxdt = datetime.datetime(2011,8,20,1,0,0)

    #dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
    #dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
       
    #time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)
#    single_time_constraint = iris.Constraint(time= lambda cell: cell <= )
# Load iris cubes for pressure at model levels, height_of_levels, surface pressure, orography     

# Get array shapes for initializing

    no_of_times = pt.coord('time').points.size
    lat_len = pt.coord('grid_latitude').points.size
    lon_len = pt.coord('grid_longitude').points.size
   
    shape_1time = (lat_len, lon_len)
    shape_alltime = (no_of_times,len(p_levels),lat_len,lon_len)
    
    print shape_alltime

    pot_temp_at_p_lev = np.memmap(numpy_ar_file, dtype='float32', mode='w+', shape=shape_alltime)

#Number of levels in model output

    number_of_levels = pt.coord('model_level_number').points.size
    
# Pre declare arrays

    p0 = np.zeros(shape_1time)
    p1 = np.zeros(shape_1time) 
    layer_p = np.zeros(shape_1time)
   
# Create  arrays of indices for picking later (sigh)
    x_coords, y_coords = np.indices((shape_1time))

# Select time slice
    for t, time_cube in enumerate(pt.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
        
#  Reverse pressure on model levels and surface pressure data  cubes because searchsorted needs an array with ascending values to work. /100 to convert to hPa at the same time

        time_cube_rev = time_cube[::-1,:,:].data/100        

# Loop through pressure levels
        for n, p_lev in enumerate(p_levels):
            
           
# Filter out data positions that are outside index range (pressure below ground surface)
            data_positions = data_p_full[t,n]
            dpmin1 = (data_p_full[t,n]-1).astype(int)

            #data_positions =np.where(time_cube_rev[dpmin1_temp, x_coords, y_coords]>p_lev, dpmin1_temp+1, dpmin1_temp+1)
            p0_filt_time = data_positions*(np.less(data_positions,number_of_levels))
           
            p0 = np.where(p0_filt_time!=0, time_cube_rev[p0_filt_time, x_coords, y_coords], 0)
            p1 =np.where(p0!=0.,time_cube_rev[dpmin1, x_coords, y_coords], 0)
               
            layer_p= np.where(p0!=0., ((np.log(p_lev) - np.log(p1)) / (np.log(p0) - np.log(p1))), 0)

            pot_temp_at_p_lev[t,n] = p0+layer_p
           
            #print layer_p.shape            
            #print p0.shape
            #print p1.shape
            #print h.shape 
                        
            print "Potential Temperature calc bit (part 2 of 2). Pressure level %s.  Time %s. Finished" % (p_lev, t)
    
    lat = pt.coord('grid_latitude').points
    lon = pt.coord('grid_longitude').points
    time = pt.coord('time').points
    try:
        np.savez_compressed("%s%s" % (save_path, save_name_pt), h=height, p=p_levels, lat=lat, lon=lon, time=time)
    except Exception,e:
        print e
        print 'NP failed'
        pass
    try:
        np.savez_compressed(("%s%s_p0etc" % (save_path, save_name_pt)), p0, p1, layer_p)
    except Exception,e:
        print e
        print 'NP 2 failed'
        pass
    else:
        del height
  except Exception,e:
   print e   
   print 'Failed to run dp script for %s' % experiment_id
   pass


if __name__ == '__main__':
    main()


   
