"""
Find heights of pressure levels from models and save
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
    
    #p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    #p_levels = [400]
   
    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/408.pp' % (expmin1, experiment_id)
    fsp = '/projects/cascade/pwille/moose_retrievals/%s/%s/409.pp'% (expmin1, experiment_id)
    fname_heights = '/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp'% (expmin1, experiment_id)
    f_oro =  '/projects/cascade/pwille/moose_retrievals/%s/%s/33.pp'% (expmin1, experiment_id)
    
    save_path_dp='/home/pwille/python_scripts/%s' % (experiment_id)
    save_name_dp='/407_pressure_levels_dp_%s' % experiment_id

    save_path_h='/home/pwille/python_scripts/%s' % (experiment_id)
    save_name_h='/407_pressure_levels_h_%s' % experiment_id

# Load data positions ( rho level with higher pressure (lower height) than reference levels
    data_load = np.load("%s%s.npz" % (save_path_dp, save_name_dp))
    data_p_load = npzfile['dp']
    p_levels = npzfile['p']
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

    shape_1time = p_at_rho[0,0:len(p_levels),:,:].shape
    shape_alltime = p_at_rho[:,0:len(p_levels),:,:].shape

    print shape_alltime

#Number of levels in model output

    number_of_levels = p_at_rho[0,:,0,0].shape[0]

# Get data from pp cubes that do not vary with time 
    height_of_level = hl[0,::-1,:,:].data
    oro_data = oro[0].data
    
# Pre declare arrays

    p0 = np.zeros(shape_1time)
    p1 = np.zeros(shape_1time) 
    h0 = np.zeros(shape_1time)
    h1 = np.zeros(shape_1time)
    layer_p = np.zeros(shape_1time)
    height = np.zeros(shape_alltime)

    data_p_full = data_p_load.astype(int)
   
# Create  arrays of indices for picking later (sigh)
    x_coords, y_coords = np.indices((data_p_full[0,0].shape))

# Select time slice
    for t, time_cube in enumerate(p_at_rho.slices(['model_level_number', 'grid_latitude', 'grid_longitude'])):
        
#  Reverse pressure on model levels and surface pressure data  cubes because searchsorted needs an array with ascending values to work. /100 to convert to hPa at the same time

        time_cube_rev = time_cube[::-1,:,:].data/100
        surf_p_time = surf_p[t,:,:].data/100

# Loop through pressure levels
        for n, p_lev in enumerate(p_levels):
            
           
# Filter out data positions that are outside index range (pressure below ground surface)
            data_positions = data_p_full[t,n]
            dpmin1 = (data_p_full[t,n]-1).astype(int)

            #data_positions =np.where(time_cube_rev[dpmin1_temp, x_coords, y_coords]>p_lev, dpmin1_temp+1, dpmin1_temp+1)
            p0_filt_time = data_positions*(np.less(data_positions,number_of_levels))

            p0_surf_filt = np.logical_and((p0_filt_time) == number_of_levels, p_lev < surf_p_time)

            p0 = np.where(p0_filt_time!=0, time_cube_rev[p0_filt_time, x_coords, y_coords], 0)
            p0 = p0 + (surf_p_time * p0_surf_filt) 

            #p1 = time_cube_rev[data_positions-1]
            p1 =np.where(p0!=0.,time_cube_rev[dpmin1, x_coords, y_coords], 0)
               
            h1 =np.where(p0!=0.,height_of_level[dpmin1, x_coords, y_coords], 0)

            h0 = np.where(p0_filt_time!=0., height_of_level[p0_filt_time, x_coords, y_coords], 0)  
            h0 = h0 + (oro_data * p0_surf_filt)

            layer_p= np.where(p0!=0., ((np.log(p_lev) - np.log(p1)) / (np.log(p0) - np.log(p1))), 0)

            #print 'P1 %s P0 %s H1 %s H0 %s P DIFF %s' %(p1,p0,h1,h0,layer_p)
            
            #print layer_p.shape
            
            #print p0.shape
            #print p1.shape
            #print h.shape 
            
            height[t,n] =  np.where(p0!=0., (h0 + (h1 - h0)*(1-layer_p)),0)
            
            print "Height calc bit (part 2 of 2). Pressure level %s.  Time %s. Finished" % (p_lev, t)
    
    lat = oro.coord('grid_latitude').points
    lon = oro.coord('grid_longitude').points
    
    try:
        np.savez("%s%s" % (save_path_h, save_name_h), h=height, p=p_levels, lat=lat, lon=lon)
    except Exception:
        print 'NP failed'
        pass
    try:
        np.savez(("%s%s_p0etc" % (save_path_h, save_name_h)), p0, p1, h0, h1, layer_p)
    except Exception:
        print 'NP 2 failed'
        pass
if __name__ == '__main__':
    main()


   
