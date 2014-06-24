def unrotate_and_update_cube(rot_cube):
    import iris
    import numpy as np

    latr = rot_cube.coord('grid_latitude').points
    lonr = rot_cube.coord('grid_longitude').points
    #p_levs = rot_cube.coord('pressure').points
    
    cs = rot_cube.coord_system('CoordSystem')

    if isinstance(cs, iris.coord_systems.RotatedGeogCS):

        print '%s Unrotate cube %s' % (experiment_id, cs)

        lons, lats = np.meshgrid(lonr, latr)
        lons ,lats = unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

        lon=lons[0]
        lat=lats[:,0]

        csur=cs.ellipsoid

        for i, coord in enumerate (rot_cube.coords()):
            if coord.standard_name=='grid_latitude':
                lat_dim_coord_uwind = i
            if coord.standard_name=='grid_longitude':
                lon_dim_coord_uwind = i

        rot_cube.remove_coord('grid_latitude')
        rot_cube.remove_coord('grid_longitude')
        rot_cube.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=csur),lat_dim_coord_uwind )
        rot_cube.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=csur), lon_dim_coord_uwind)

    return rot_cube

def unrotate_pole(rotated_lons, rotated_lats, pole_lon, pole_lat):
     """
      Convert rotated-pole lons and lats to unrotated ones.

      Example::

      lons, lats = unrotate_pole(grid_lons, grid_lats, pole_lon, pole_lat)

      .. note:: Uses proj.4 to perform the conversion.

      """
     import cartopy.crs as ccrs

     src_proj = ccrs.RotatedGeodetic(pole_longitude=pole_lon,
                                    pole_latitude=pole_lat)
     target_proj = ccrs.Geodetic()
     res = target_proj.transform_points(x=rotated_lons, y=rotated_lats,
                                       src_crs=src_proj)
     unrotated_lon = res[..., 0]
     unrotated_lat = res[..., 1]

     return unrotated_lon, unrotated_lat
