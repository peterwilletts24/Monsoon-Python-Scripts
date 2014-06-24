"""

Load mean geopotential heights and plot in colour

"""
import os, sys
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
from mpl_toolkits.basemap import Basemap
import iris
import numpy as np
import imp
import h5py
import cartopy.crs as ccrs

from textwrap import wrap

model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/model_name_convert_title.py')


def main():
    def unrotate_pole(rotated_lons, rotated_lats, pole_lon, pole_lat):
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

# Set rotated pole longitude and latitude, not ideal but easier than trying to find how to get iris to tell me what it is.

    plot_levels = [925, 850, 700, 500] 
    #plot_levels = [500]

    experiment_id = 'djzny'

    p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]
    expmin1 = experiment_id[:-1]
  
    plot_type='mean'
    plot_diag='temp'
    fname_h = '/projects/cascade/pwille/temp/408_pressure_levels_interp_pressure_%s_%s' % (experiment_id, plot_type)
    fname_d = '/projects/cascade/pwille/temp/%s_pressure_levels_interp_%s_%s' % (plot_diag, experiment_id, plot_type)
    print fname_h
    print fname_d
#  Height data file
    with h5py.File(fname_h, 'r') as i:
        mh = i['%s' % plot_type]
        mean_heights = mh[. . .]
    print mean_heights.shape
    with h5py.File(fname_d, 'r') as i:
        mh = i['%s' % plot_type]
        mean_var = mh[. . .]
    print mean_var.shape
    
    #lon_low= 60
    #lon_high = 105
    #lat_low = -10
    #lat_high = 30

    f_oro =  '/projects/cascade/pwille/moose_retrievals/%s/%s/33.pp' % (expmin1, experiment_id)
    oro = iris.load_cube(f_oro)

    fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/30201_mean.pp' % (expmin1, experiment_id)
    #fv = '/projects/cascade/pwille/moose_retrievals/%s/%s/30202.pp' % (expmin1, experiment_id)
    
    u_wind,v_wind = iris.load(fu)
    print u_wind.shape
    lat_w = u_wind.coord('grid_latitude').points
    lon_w = u_wind.coord('grid_longitude').points
    p_levs = u_wind.coord('pressure').points

    lat = oro.coord('grid_latitude').points
    lon = oro.coord('grid_longitude').points

    lon_low= np.min(lon)
   
   # Wind may have different number of grid points so need to do this twice 

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
        lons_w,lats_w = unrotate_pole(lons_w,lats_w, cs_w.grid_north_pole_longitude, cs_w.grid_north_pole_latitude)
        
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
        lons,lats = unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        lon_corner_u,lat_corner_u = unrotate_pole(lon_corners, lat_corners, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
        #lon_highu,lat_highu = unrotate_pole(lon_high, lat_high, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

        lon=lons[0]
        lat=lats[:,0]

        print lon_corners
        print lat_corners
        print lon_corner_u
        print lat_corner_u
        print lon_corner_u[0,0]
        print lon_corner_u[0,1]
        print lat_corner_u[0,0]
        print lat_corner_u[1,0]

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

    else:
        lons, lats = np.meshgrid(lon, lat)
        lons_w, lats_w = np.meshgrid(lon_w, lat_w)

        lon_low= np.min(lons)
        lon_high = np.max(lons)
        lat_low = np.min(lats)
        lat_high = np.max(lats)


# 2 degree lats lon lists for wind regridding
    lat_wind_1deg = np.arange(lat_low,lat_high, 2)
    lon_wind_1deg = np.arange(lon_low,lon_high, 2)


    for p in plot_levels:

        #m_title = 'Height of %s-hPa level (m)' % (p)

# Set pressure height contour min/max
        if p == 925:
            clev_min = 680.
            clev_max = 810.
        elif p == 850:
            clev_min = 1435.
            clev_max = 1530.
        elif p == 700:
            clev_min = 3090.
            clev_max = 3155.
        elif p == 500:
            clev_min = 5800.
            clev_max = 5890.
        else:
            print 'Contour min/max not set for this pressure level'

# Set potential temperature min/max       
        if p == 925:
            clevpt_min = 295.
            clevpt_max = 310.
        elif p == 850:
            clevpt_min = 300.
            clevpt_max = 320.
        elif p == 700:
            clevpt_min = 310.
            clevpt_max = 325.
        elif p == 500:
            clevpt_min = 321.
            clevpt_max = 335.
        else:
            print 'Potential temperature min/max not set for this pressure level'


  # Set specific humidity min/max       
        if p == 925:
            clevsh_min = 0.012
            clevsh_max = 0.022
        elif p == 850:
            clevsh_min = 0.0035
            clevsh_max = 0.018
        elif p == 700:
            clevsh_min = 0.002
            clevsh_max = 0.012
        elif p == 500:
            clevsh_min = 0.002
            clevsh_max = 0.006
        else:
            print 'Specific humidity min/max not set for this pressure level'
       

        #clevs_col = np.arange(clev_min, clev_max)
        clevs_lin = np.linspace(clev_min, clev_max, num=20)

        s = np.searchsorted(p_levels[::-1], p)
        sc =  np.searchsorted(p_levs, p)
# Set plot contour lines for pressure levels

        plt_h = mean_heights[:,:,-(s+1)]
        plt_h[plt_h==0] = np.nan 


# Set plot colours for variable

        plt_v = mean_var[:,:,-(s+1)]
        plt_v[plt_v==0] = np.nan 
              
# Set u,v for winds, linear interpolate to approx. 1 degree grid
        u_interp = u_wind[sc,:,:]
        v_interp = v_wind[sc,:,:]
        #print u_interp.shape
        sample_points = [('grid_latitude', lat_wind_1deg), ('grid_longitude', lon_wind_1deg)]
        
        u = iris.analysis.interpolate.linear(u_interp, sample_points).data
        v = iris.analysis.interpolate.linear(v_interp, sample_points).data

        lons_w, lats_w = np.meshgrid(lon_wind_1deg, lat_wind_1deg)
        m =\
Basemap(llcrnrlon=lon_low,llcrnrlat=lat_low,urcrnrlon=lon_high,urcrnrlat=lat_high,projection='mill')

        x, y = m(lons, lats)
        x_w, y_w = m(lons_w, lats_w)

        print x_w.shape
        fig=plt.figure(figsize=(8,8))
        ax = fig.add_axes([0.05,0.05,0.9,0.85])

        m.drawcoastlines(color='gray')  
        m.drawcountries(color='gray')  
        m.drawcoastlines(linewidth=0.5)
        #m.fillcontinents(color='#CCFF99')
        m.drawparallels(np.arange(-80,81,10),labels=[1,1,0,0])
        m.drawmeridians(np.arange(0,360,10),labels=[0,0,0,1])
    
        cs_lin = m.contour(x,y, plt_h, clevs_lin,colors='k',linewidths=0.5)
       
        #wind = m.barbs(x_w,y_w, u, v, length=6)

        if plot_diag=='temp':
             cs_col = m.contourf(x,y, plt_v,  np.linspace(clevpt_min, clevpt_max), cmap=plt.cm.RdBu_r)
             cbar = m.colorbar(cs_col,location='bottom',pad="5%", format = '%d')  
             cbar.set_label('K')  
             plt.suptitle('Height, Potential Temperature and Wind Vectors at %s hPa'% (p), fontsize=10)  

        elif plot_diag=='sp_hum':
             cs_col = m.contourf(x,y, plt_v,  np.linspace(clevsh_min, clevsh_max), cmap=plt.cm.RdBu_r)
             cbar = m.colorbar(cs_col,location='bottom',pad="5%", format = '%.3f') 
             cbar.set_label('kg/kg')
             plt.suptitle('Height, Specific Humidity and Wind Vectors at %s hPa'% (p), fontsize=10) 

        wind = m.quiver(x_w,y_w, u, v, scale=400)
        qk = plt.quiverkey(wind, 0.1, 0.1, 5, '5 m/s', labelpos='W')
                
        plt.clabel(cs_lin, fontsize=10, fmt='%d', color='black')

        #plt.title('%s\n%s' % (m_title, model_name_convert_title.main(experiment_id)), fontsize=10)
        plt.title('\n'.join(wrap('%s' % (model_name_convert_title.main(experiment_id)), 80)), fontsize=10)

        #plt.show()  
        if not os.path.exists('/home/pwille/figures/%s/%s'  % (experiment_id, plot_diag)): os.makedirs('/home/pwille/figures/%s/%s' % (experiment_id, plot_diag))
        plt.savefig('/home/pwille/figures/%s/%s/geop_height_%shPa_%s_%s.tiff' % (experiment_id, plot_diag, p, experiment_id, plot_diag), format='tiff', transparent=True)




if __name__ == '__main__':
    main()
