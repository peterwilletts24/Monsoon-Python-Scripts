import os, sys

import iris
import iris.analysis.cartography

import h5py

import numpy as np

import pdb

#Load specific humidity and wind

#/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/sp_hum_pressure_levels_interp_djzns_mean_masked/

experiment_ids = ['djznw', 'djznq', 'djzny', 'djzns', 'dkmbq', 'dklyu', 'dklwu', 'dklzq']

p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]

for experiment_id in experiment_ids:
    
   expmin1 = experiment_id[:-1]

   fname_h = '/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/sp_hum_pressure_levels_interp_%s_mean_masked' % (experiment_id)

   with h5py.File(fname_h, 'r') as i:
        
#  q = i['%s' % 'mean'][. . .]
    q = i['%s' % 'mean'][. . .]
   print q.shape

   f_oro =  '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/33.pp' % (expmin1, experiment_id)
   oro = iris.load_cube(f_oro)

   fu = '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/30201.pp' % (expmin1, experiment_id)
    
   u_wind,v_wind = iris.load(fu)
   print u_wind.shape
    
   lat_w = u_wind.coord('grid_latitude').points
   lon_w = u_wind.coord('grid_longitude').points
   p_levs = u_wind.coord('pressure').points

   lat = oro.coord('grid_latitude').points
   lon = oro.coord('grid_longitude').points

   cs_w = u_wind.coord_system('CoordSystem')
   cs = oro.coord_system('CoordSystem')

   if isinstance(cs_w, iris.coord_systems.RotatedGeogCS):
        print ' Wind - %s - Unrotate pole %s' % (experiment_id, cs_w)
        lons_w, lats_w = np.meshgrid(lon_w, lat_w)
        lons_w,lats_w = iris.analysis.cartography.unrotate_pole(lons_w,lats_w, cs_w.grid_north_pole_longitude, cs_w.grid_north_pole_latitude)
        
        lon_w=lons_w[0]
        lat_w=lats_w[:,0]

        csur_w=cs_w.ellipsoid

        for i, coord in enumerate (u_wind.coords()):
            if coord.standard_name=='grid_latitude':
                lat_dim_coord_uwind = i
            if coord.standard_name=='grid_longitude':
                lon_dim_coord_uwind = i
       
        u_wind.remove_coord('grid_latitude')
        u_wind.remove_coord('grid_longitude')
        u_wind.add_dim_coord(iris.coords.DimCoord(points=lat_w, standard_name='grid_latitude', units='degrees', coord_system=csur_w),lat_dim_coord_uwind )
        u_wind.add_dim_coord(iris.coords.DimCoord(points=lon_w, standard_name='grid_longitude', units='degrees', coord_system=csur_w), lon_dim_coord_uwind)

        v_wind.remove_coord('grid_latitude')
        v_wind.remove_coord('grid_longitude')
        v_wind.add_dim_coord(iris.coords.DimCoord(points=lat_w, standard_name='grid_latitude', units='degrees', coord_system=csur_w), lat_dim_coord_uwind)
        v_wind.add_dim_coord(iris.coords.DimCoord(points=lon_w, standard_name='grid_longitude', units='degrees', coord_system=csur_w),lon_dim_coord_uwind )
        
   if isinstance(cs, iris.coord_systems.RotatedGeogCS):
        print ' 33.pp  - %s - Unrotate pole %s' % (experiment_id, cs)
        lons, lats = np.meshgrid(lon, lat)      
        
        lon_low= np.min(lons)
        lon_high = np.max(lons)
        lat_low = np.min(lats)
        lat_high = np.max(lats)

        lon_corners, lat_corners = np.meshgrid((lon_low, lon_high), (lat_low, lat_high))
        lons,lats = iris.analysis.cartography.unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        lon_corner_u,lat_corner_u = iris.analysis.cartography.unrotate_pole(lon_corners, lat_corners, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        #lon_highu,lat_highu = iris.analysis.cartography.unrotate_pole(lon_high, lat_high, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

        lon=lons[0]
        lat=lats[:,0]

        lon_low = lon_corner_u[0,0]
        lon_high = lon_corner_u[0,1]
        lat_low = lat_corner_u[0,0]
        lat_high = lat_corner_u[1,0]

        csur=cs.ellipsoid     

        for i, coord in enumerate (oro.coords()):
            if coord.standard_name=='grid_latitude':
                lat_dim_coord_oro = i
            if coord.standard_name=='grid_longitude':
                lon_dim_coord_oro = i

        oro.remove_coord('grid_latitude')
        oro.remove_coord('grid_longitude')
        oro.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=csur), lat_dim_coord_oro)
        oro.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=csur), lon_dim_coord_oro)
        print oro
   else:
        lons, lats = np.meshgrid(lon, lat)
        lons_w, lats_w = np.meshgrid(lon_w, lat_w)

        lon_low= np.min(lons)
        lon_high = np.max(lons)
        lat_low = np.min(lats)
        lat_high = np.max(lats)

   print u_wind
   print u_wind.coord('pressure')

   qu_div = np.empty((u_wind.shape[1], u_wind.shape[2], u_wind.shape[0]))
   qv_div = np.empty((u_wind.shape[1], u_wind.shape[2], u_wind.shape[0]))
 
   fl_la_lo = (lats.flatten(),lons.flatten())

   p_lev_delta = np.diff( np.append(u_wind.coord('pressure').points, u_wind.coord('pressure').points[-1]))
   
   for pn, p in enumerate(u_wind.coord('pressure').points):
 
    s = np.searchsorted(p_levels[::-1], p)
    #sc =  np.searchsorted(p_levs, p)

    q_slice = q[:,:,-(s+1)]
    q_interp = scipy.interpolate.griddata(fl_la_lo, q_slice.flatten(), (lats_w, lons_w), method='linear')

    pdb.set_trace()
    qu_div[:,:,pn] = (u_wind.coord('pressure').points[pn]*q_interp)/9.81
    qv_div[:,:,pn] = (v_wind.coord('pressure').points[pn]*q_interp)/9.81

   Qu_div = np.sum(qu_div*p_lev_delta, axis=-1)
   Qv_div = np.sum(qv_div*p_lev_delta, axis=-1)
