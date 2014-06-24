"""
Load winds on pressure levels and calculate vorticity and divergence
"""
import os, sys
sys.path.append('/home/pwille/python_scripts/modules')

from update_pp_cube_coords import update_coords

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
experiment_ids = ['dkmbq', 'dklwu', 'dklzq', 'djzns']

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
        v_i = v[p,:]
  
   if pressure_dim_coord==1:
        v_i = v[:,p,:]
  
   if pressure_dim_coord==2:
        v_i = v[:,:,p,:]
     
   if pressure_dim_coord==3:
        v_i = v[:,:,:,p,:]

   if v_i.shape != pressure_cube.shape:
    #for ne, n in enumerate(pressure_cube.shape):
     #if n!=dvdlat_interp.shape[ne]
           pressure_cube.transpose([1,0,2,3])

   V = iris.analysis.calculus.curl(pressure_cube, v_i, k_cube=None, ignore=None)
   print V
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
          #V_up_data=V[2].data.astype(np.float32)
          #V_up=V[2].copy(V[2].data.astype(np.float32))
          #iris.util.describe_diff(V_up, V[2])
          #pdb.set_trace()
          #print V_up
          #del V
          #iris.save(V_up, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id), append=True)
          try:
           os.remove('%s%s/%s/vorticity_%s.pp' % (pp_file_path, expmin1, experiment_id, int(V[2].coord('pressure').points[0])))
          except OSError:
           print '%s%s/%s/vorticity_%s.pp does not exist' % (pp_file_path, expmin1, experiment_id, int(V[2].coord('pressure').points[0]))
           pass
          iris.save(V[2], '%s%s/%s/vorticity_%s.pp' % (pp_file_path, expmin1, experiment_id, int(V[2].coord('pressure').points[0])))
          #else:
          del V
          #       iris.save(V, '%s%s/%s/vorticity.pp' % (pp_file_path, expmin1, experiment_id))
          #print V_up
   except Exception, e:
          print '%s - Failed to save' % V[2]
          print e
          print sys.exc_traceback.tb_lineno 
          pass
