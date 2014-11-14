from iris.coord_systems import RotatedGeogCS, GeogCS
from iris.analysis.cartography import unrotate_pole
from iris.coords import DimCoord

import h5py

experiment_ids = ['dklyu', 'dkmbq']

data_to_mean = ['temp', 'sp_hum']
dset = ['t_on_p', 'sh_on_p']

p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]

for experiment_id in experiment_ids:
    expmin1 = experiment_id[:-1]

    info_cube = iris.load('/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/30201.pp' % (expmin1, experiment_id))[0]

    for a, dm in enumerate(data_to_mean):
    
        fname = '/projects/cascade/pwille/%s/%s_pressure_levels_interp_%s' % (dm, dm,experiment_id)
        ds = dset[a]

        with h5py.File(fname, 'r') as f:

            save_as_cube=iris.cube.Cube(f['%s' % ds], standard_name=None, long_name=None, var_name=None, units=None, attributes=None, cell_methods=None, dim_coords_and_dims=None, aux_coords_and_dims=None, aux_factories=None)

for i, coord in enumerate (info_cube.coords()):
            if coord.standard_name=='grid_latitude':
                lat_dim_coord_cube = i
            if coord.standard_name=='grid_longitude':
                lon_dim_coord_cube = i

save_as_cube.add_dim_coord(DimCoord(points=p_levels, long_name='pressure', units='hPa'),-1)
save_as_cube.add_dim_coord((info_cube.coord('grid_latitude')),lat_dim_coord_cube)
save_as_cube.add_dim_coord((info_cube.coord('grid_longitude')),lon_dim_coord_cube)
save_as_cube.add_dim_coord((info_cube.coord('time')),0)


iris.save('/nfs/a90/eepdw/Data/EMBRACE/%s/%s/%s_%s_on_p_levs.pp' % (expmin1, experiment_id, experiment_id, dm)) 

    
