"""
Load geopotential heights and orography cube to get lat/lon cross-section

22/05/14

"""

import os, sys

import pdb

import iris
import iris.analysis.cartography

#import h5py

import numpy as np

#c_section_lon=74.

c_lon_min=75.
c_lon_max=85.
gap=1.

c_section_lat=0

diagnostic=4
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'  ]
#experiment_ids = ['dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
#experiment_ids = ['dkbhu']
experiment_ids = ['dkjxq']




for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 diag = iris.load_cube('/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1,experiment_id, diagnostic))
 
 #diag = iris.load(f_diag)

 print diag

 cs = diag.coord_system('CoordSystem')
 print cs
 csur=cs.ellipsoid  

 lat = diag.coord('grid_latitude').points
 lon = diag.coord('grid_longitude').points

 lons, lats = np.meshgrid(lon, lat)  

 lons,lats = iris.analysis.cartography.unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

 lon=lons[0]
 lat=lats[:,0]

 for i, coord in enumerate (diag.coords()):
     if coord.standard_name=='grid_latitude':
         lat_dim_coord_diag = i
     if coord.standard_name=='grid_longitude':
         lon_dim_coord_diag = i

 diag.remove_coord('grid_latitude')
 diag.remove_coord('grid_longitude')
 diag.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=csur), lat_dim_coord_diag)
 diag.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=csur), lon_dim_coord_diag)

 for c_section_lon in np.arange(c_lon_min,c_lon_max, gap):

  if (c_section_lon != 0):
    print c_section_lon
 
    l=diag.coord('grid_longitude').nearest_neighbour_index(c_section_lon) 
    lon_slice = iris.analysis.interpolate.extract_nearest_neighbour(diag, [('grid_longitude', l)])
    #print lon_slice
    iris.save(lon_slice, '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' % (experiment_id, diagnostic, c_section_lon))
    
  if (c_section_lat != 0):
     print c_section_lat
    
     l=diag.coord('grid_latitude').nearest_neighbour_index(c_section_lat) 
     lat_slice = iris.analysis.interpolate.extract_nearest_neighbour(diag, [('grid_latitude', l)])
     iris.save(lat_slice, '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' % (experiment_id, diagnostic, c_section_lon))
   #print xc
   #print xc.shape
   #print oro.coord('grid_latitude').points
   #print oro.coord('grid_latitude').points.shape
