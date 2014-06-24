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
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'] # All minus large 3
#experiment_ids = ['djznq', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'] # All minus large 3
experiment_ids = ['djzns']

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
#
# Divergence, using something entirely different
 
 #sample_points = [('latitude', dudlon_lats),
  #               ('longitude',  dudlon_lons)]
 try:
   os.remove('%s%s/%s/divergence.pp' % (pp_file_path, expmin1, experiment_id))
 except OSError:
   print '%s%s/%s/divergence.pp does not exist' % (pp_file_path, expmin1, experiment_id)

 # interval = 2 
 # l_2s_min_ind = range(0,u.coord('pressure').shape[0]-1,interval)
 # l_2s_max_ind = range((interval-1),u.coord('pressure').shape[0],interval)

 # 2s_min = cube_f.coord('pressure').points[l_2s_min_ind]
 # 2s_max = cube_f.coord('pressure').points[l_2s_max_ind]

 # for i,l in enumerate(2s_min): 

 for p, pressure_cube in enumerate(u.slices(['time', 'latitude', 'longitude'])):

  dudlon = iris.analysis.calculus.differentiate(pressure_cube, 'longitude')
  dudlon.units=None

  #del u

  if pressure_dim_coord==0:
                 v_slice = v[p,:]
  if pressure_dim_coord==1:
                 v_slice = v[:,p,:]
  if pressure_dim_coord==2:
                 v_slice = v[:,:,p,:]
  if pressure_dim_coord==3:
                 v_slice = v[:,:,:,p,:]

  cos_lats=iris.analysis.cartography.cosine_latitude_weights(v_slice)
  dvdlat = iris.analysis.calculus.differentiate(v_slice*cos_lats, 'latitude')

  #del v

       # Some models give time in 2 dimensions, some in 1.  As regrid function mixes up 2-dimensional time coords, and I can't find a way to swap them back yet, collapsing the time dimension is one way I know to work around these issues.that works

         # if pressure_dim_coord==0:
         #         dlon_i = dudlon[p,:]
         # if pressure_dim_coord==1:
         #         dudlon_i = dudlon[:,p,:]
         # if pressure_dim_coord==2:
         #         dudlon_i = dudlon[:,:,p,:]
         # if pressure_dim_coord==3:
         #         dudlon_i = dudlon[:,:,:,p,:]

  dudlon.units=None
  dvdlat_interp = iris.analysis.interpolate.regrid(pressure_cube, dudlon, mode='bilinear')

  if dudlon.shape != dvdlat_interp.shape:
           #for ne, n in enumerate(pressure_cube.shape):
            #if n!=dvdlat_interp.shape[ne]
                #pdb.set_trace()
          dvdlat_interp.transpose([1,0,2,3])

  dudlon.units=None
  dvdlat_interp.units=None
  second_term=iris.analysis.maths.add(dudlon, dvdlat_interp)

       # Get cosine of lats again, to match grid size

  cos_lats=iris.analysis.cartography.cosine_latitude_weights(dvdlat_interp)
  first_term=1/(r*cos_lats)    
  D =  iris.analysis.maths.multiply(second_term, first_term)            
  #print D
  D_data = D.data.astype(np.float32)

  D_save = D.copy(data=D_data)
  print D_save
  #print D_save.coord('pressure')
  #pdb.set_trace()
  del D
  del D_data
  iris.save(D_save, '%s%s/%s/divergence_%s.pp' % (pp_file_path, expmin1, experiment_id, D_save.coord('pressure').points[0]))
 
