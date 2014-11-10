from iris.coord_systems import RotatedGeogCS, GeogCS
from iris.analysis.cartography import unrotate_pole
from iris.coords import DimCoord
from numpy import meshgrid

def unrotate_pole_update_cube(cube):
    lat = cube.coord('grid_latitude').points
    lon = cube.coord('grid_longitude').points
    
    cs = cube.coord_system('CoordSystem')

    if isinstance(cs, RotatedGeogCS):
        #print ' %s  - %s - Unrotate pole %s' % (diag, experiment_id, cs)
        lons, lats = meshgrid(lon, lat) 

        lons,lats = unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
       
        lon=lons[0]
        lat=lats[:,0]
                
        for i, coord in enumerate (cube.coords()):
            if coord.standard_name=='grid_latitude':
                lat_dim_coord_cube = i
            if coord.standard_name=='grid_longitude':
                lon_dim_coord_cube = i

    
        # IRIS unrotate_pole uses the default cartopy.crs.Geodetic, which is 
        # WGS84 by default 
        wgs84_cs = GeogCS(semi_major_axis= 6378137.,
                                         inverse_flattening=298.257223563)

    
     
        cube.remove_coord('grid_latitude')
        cube.remove_coord('grid_longitude')
        cube.add_dim_coord(DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=wgs84_cs), lat_dim_coord_cube)
        cube.add_dim_coord(DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=wgs84_cs), lon_dim_coord_cube)

        return cube
