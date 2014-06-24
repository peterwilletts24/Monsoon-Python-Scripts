"""
Load multiple pp diagnostic files, aggregate by year, day etc, calcualte mean, sum etc and save
"""

import os, sys
import datetime

import iris
import iris.unit as unit

diag = 'avg.5216'
cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

regrid_model='dkjxq'
regrid_model_min1=regrid_model[:-1]
experiment_ids = ['djzny', 'djzns', 'dkmbq', 'dklyu', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All models minus global and 24kms (no need to regrid to itself)
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dkjxq', 'dkmbq', 'dklzq']

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
fr = '%s%s/%s/%s.pp' % (pp_file_path, regrid_model_min1, regrid_model, diag)

def unrotate_pole(rotated_lons, rotated_lats, pole_lon, pole_lat):
     import cartopy.crs as ccrs

     """
      Convert rotated-pole lons and lats to unrotated ones.

      Example::

      lons, lats = unrotate_pole(grid_lons, grid_lats, pole_lon, pole_lat)

      .. note:: Uses proj.4 to perform the conversion.

      """
     src_proj = ccrs.RotatedGeodetic(pole_longitude=pole_lon,
                                    pole_latitude=pole_lat)
     target_proj = ccrs.Geodetic()
     res = target_proj.transform_points(x=rotated_lons, y=rotated_lats,
                                       src_crs=src_proj)
     unrotated_lon = res[..., 0]
     unrotated_lat = res[..., 1]

     return unrotated_lon, unrotated_lat
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

glob_load = iris.load_cube(fg, ('%s' % cube_name_param)  & time_constraint)

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)

regrid_cube = iris.load_cube(fr, ('%s' % cube_name_param)  & glob_tc)
experiment_id=regrid_model
regrid_cube = unrotate_and_update_cube(regrid_cube)
del glob_load

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/avg.5216.pp' % (expmin1, experiment_id)

 print experiment_id
 sys.stdout.flush()

 try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc)
        cube=cubeconv+cubestrat
        cube.rename('total_precipitation_rate')
 except iris.exceptions.ConstraintMismatchError:        
        cube = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc)

 cube = unrotate_and_update_cube(cube)
 cube_r = iris.analysis.interpolate.regrid(cube, regrid_cube, mode='bilinear')
 
 del cube        


 # Rainfall output with Stuart scripts as hourly mean. time_interval is time_interval as fraction of hour
# t = rain.coord('time').points
# time_interval = (t.flatten()[1]-t.flatten()[0])

# iris.analysis.maths.multiply(rain,60*(60*time_interval),in_place=True)

 #rain_total = rain.collapsed('time', iris.analysis.SUM)    
 for t, time_cube in enumerate (cube_r.slices(['time', 'grid_latitude', 'grid_longitude'])):
     rain_mean = cube_r.collapsed('time', iris.analysis.MEAN) 
 iris.save((rain_mean),'/projects/cascade/pwille/moose_retrievals/%s/%s/rain_mean_regrid.pp' % (expmin1, experiment_id))


## if global model rotate to same cs
