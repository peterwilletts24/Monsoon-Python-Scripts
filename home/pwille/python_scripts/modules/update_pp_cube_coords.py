# 
# Take iris cube, unrotate and update cube coords
#
import numpy as np
import iris
import iris.analysis.cartography

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

  return cube,lats,lons
