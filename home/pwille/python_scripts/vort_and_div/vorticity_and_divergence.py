"""
Load winds on pressure levels and calculate vorticity and divergence
"""
import os, sys
import datetime
import iris
#import iris.unit as unit
import iris.analysis.calculus
import iris.analysis.cartography

import numpy as np

import math

import pdb

diag = '30201'
cube_name_u='eastward_wind'
cube_name_v='northward_wind'
pp_file_path='/projects/cascade/pwille/moose_retrievals/'
experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'] # All minus large 3
#experiment_ids = ['djzny']

for experiment_id in experiment_ids:
 print experiment_id
 expmin1 = experiment_id[:-1]
 fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)
 try:
  u = iris.load_cube(fu,'%s' % cube_name_u)
  v  = iris.load_cube(fu,'%s' % cube_name_v)

 except Exception, e:
        print '%s - Failed to load' % fu
        print e
        print sys.exc_traceback.tb_lineno 
        pass

 r = 6371.22  #Average radius of earth, same as ERA Interim 

#  Unrotate and update cube lat/lon coords, also change name of coords from grid_... to ...
 
 
 def update_coords(cube):
  cs = cube.coord_system('CoordSystem')
  csur=cs.ellipsoid  

  lat=cube.coord('grid_latitude').points
  lon=cube.coord('grid_longitude').points
  lonr,latr=np.meshgrid(lon,lat)
  lons, lats = iris.analysis.cartography.unrotate_pole(lonr, latr, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

  lon=lons[0]
  lat=lats[:,0]

  for i, coord in enumerate (cube.coords()):
     if coord.standard_name=='grid_latitude':
         lat_dim_coord_oro = i
     if coord.standard_name=='grid_longitude':
         lon_dim_coord_oro = i
  cube.remove_coord('grid_latitude')
  cube.remove_coord('grid_longitude')
  cube.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='latitude', units='degrees', coord_system=csur), lat_dim_coord_oro)
  cube.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='longitude', units='degrees', coord_system=csur), lon_dim_coord_oro)
  #print cube

  return cube,lats

 u,lats= update_coords(u)
 v,lats= update_coords(v)
   
 for i, coord in enumerate (u.coords()):
     if coord.standard_name=='pressure' or coord.long_name=='pressure':
         pressure_dim_coord = i
     print coord.long_name
 print pressure_dim_coord
 #pdb.set_trace()
# Vorticity, using the handy iris calculus curl function
 try:
  os.remove('%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id))
 except OSError:
  print '%s%s/%s/vorticity.pp does not exist' % (pp_file_path, expmin1, experiment_id)
  pass

 for p, pressure_cube in enumerate(u.slices(['time', 'latitude', 'longitude'])):
   if pressure_dim_coord==0:
          V = iris.analysis.calculus.curl(pressure_cube, v[p,:], k_cube=None, ignore=None)
  
   if pressure_dim_coord==1:
          V = iris.analysis.calculus.curl(pressure_cube, v[:,p,:], k_cube=None, ignore=None)
  
   if pressure_dim_coord==2:
          V = iris.analysis.calculus.curl(pressure_cube, v[:,:,p,:], k_cube=None, ignore=None)
     
   if pressure_dim_coord==3:
          V = iris.analysis.calculus.curl(pressure_cube, v[:,:,:,p,:], k_cube=None, ignore=None)
   #print V
   #print v[:,p,:]
   #print v
   #print pressure_cube
   #print 
   #pdb.set_trace()
   try:
          #V_east=V[0]
          #V_east.rename('eastward_curl')
          #iris.save(V_east, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id), append=True)
  #del V_east
          #V_north=V[1]
  #del V
          #V_north.rename('northward_curl')
          #iris.save(V_north, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id), append=True) 
  #del V_north 
          #V_up=V[2]
          #print V_up
          #V_up.rename('upward_curl')
          #print V
          #print V[2]
          #if os.path.isfile('%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id)):
          #pdb.set_trace()
          V_up_data=V[2].data.astype(np.float32)
          V_up=V[2].copy(data=V_up_data)
          del V
          iris.save(V_up, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id), append=True)
          #else:
          #       iris.save(V, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id))
          #print V_up
   except Exception, e:
          print '%s - Failed to save' % V[2]
          print e
          print sys.exc_traceback.tb_lineno 
          pass


# Divergence, using something entirely different
 
 #sample_points = [('latitude', dudlon_lats),
  #               ('longitude',  dudlon_lons)]
 dudlon = iris.analysis.calculus.differentiate(u, 'longitude')
 dudlon.units=None

 del u

 cos_lats=iris.analysis.cartography.cosine_latitude_weights(v)
 dvdlat = iris.analysis.calculus.differentiate(v*cos_lats, 'latitude')
 cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat)

 un=dudlon.units
 #dvdlat.units='%s' % un

 del v

 try:
  os.remove('%s%s/%s/divergence.pp' % (pp_file_path, expmin1, experiment_id))
 except OSError:
  print '%s%s/%s/divergence.pp does not exist' % (pp_file_path, expmin1, experiment_id)

 for p, pressure_cube in enumerate(dvdlat.slices(['time', 'latitude', 'longitude'])):

   if pressure_dim_coord==0:
          dvdlat_interp = iris.analysis.interpolate.regrid(pressure_cube, dudlon[p,:], mode='bilinear')
          cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat_interp)
#          dvdlat_interp.units='%s' % un
          dvdlat_interp.units=None
          D =  (1/(r*cos_lats[p,:])*(dudlon[p,:]+ dvdlat_interp))
   if pressure_dim_coord==1:
          dvdlat_interp = iris.analysis.interpolate.regrid(pressure_cube, dudlon[:,p,:], mode='bilinear')
          cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat_interp)
          
  
#          dvdlat_interp.units='%s' % un
          dvdlat_interp.units=None
          pdb.set_trace()
          first_term=1/(r*cos_lats)
          second_term=dudlon[:,p,:] + dvdlat_interp
          D =  iris.analysis.maths.multiply(first_term*second_term)
   if pressure_dim_coord==2:
          dvdlat_interp = iris.analysis.interpolate.regrid(pressure_cube, dudlon[:,:,p,:], mode='bilinear')
          cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat_interp)
 
#          dvdlat_interp.units='%s' % un
          dvdlat_interp.units=None

          D =  (1/(r*cos_lats[:,:,p,:])*(dudlon[:,:,p,:] + dvdlat_interp))
   if pressure_dim_coord==3:
          dvdlat_interp = iris.analysis.interpolate.regrid(pressure_cube, dudlon[:,:,:,p,:], mode='bilinear')
          cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat_interp)
   
#          dvdlat_interp.units='%s' % un
          dvdlat_interp.units=None
          

          D =  (1/(r*cos_lats[:,:,:,p,:])*(dudlon[:,:,:,p,:] + dvdlat_interp))
         #print D
   iris.save(D, '%s%s/%s/divergence.pp' % (pp_file_path, expmin1, experiment_id), append=True)
 
