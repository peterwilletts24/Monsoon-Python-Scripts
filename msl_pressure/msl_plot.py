"""

Loop through multiple pickle files of averaged etc data, plot and save


"""

import os, sys

import cPickle as pickle

import glob

# import itertools
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np
#from mpl_toolkits.basemap import Basemap
#import matplotlib.animation as animation

import iris
import iris.coords as coords
import iris.quickplot as qplt
import iris.plot as iplt
import iris.coord_categorisation

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import datetime

def main():

    lon_low= 60
    lon_high = 105
    lat_low = -10
    lat_high = 30


    first_of_year = datetime.date(2011, 01, 01)
    first_ordinal = first_of_year.toordinal()

    #pickle_name = 'pickle_daily_mean_*.p'
    pickle_name = 'pickle_model_mean_collapsed*.p'
    flist = glob.glob ('/home/pwille/python_scripts/*/%s' % pickle_name)


    for i in flist:

        fname = str(i)

        experiment_id = fname.split('/')[4]
        if not os.path.exists('/home/pwille/python_scripts/pngs/%s' % (experiment_id)): os.makedirs('/home/pwille/python_scripts/pngs/%s' % (experiment_id))
      
       #daily_mean = pickle.load( open( "/home/pwille/python_scripts/%s/pickle_daily_mean_%s.p" % (experiment_id, experiment_id), "rb" ) )
        model_mean = pickle.load( open( "%s" % (fname), "rb" ) ) 
        for sub_cube in model_mean.slices(['grid_latitude', 'grid_longitude']):
            
      #Get date in iso format for title, if needed
      
            #day=sub_cube_daily.coord('dayyear')
            #day_number = day.points[0]
            #day_number_ordinal=first_ordinal-1 + day_number
            #date_print = datetime.date.fromordinal(day_number_ordinal)
            #date_iso = str(date_print.isoformat())

            sub_cube.units = 'hPa'
            sub_cube /= 100

            #local_min, local_max = extrema(sub_cube, mode='wrap', window=50)
            


            # Load a colour palette.
            cmap = mpl_cm.get_cmap('gist_rainbow')   
        
            # Set contour levels
            #clevs = np.arange(1002.,1016.,10.)

           
            sub_cube.coord('grid_latitude').guess_bounds()
            sub_cube.coord('grid_longitude').guess_bounds()

            ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))
            contour = iplt.contour(sub_cube, 16, colors='k',linewidths=1.)
            #iplt.contourf(sub_cube, 16, cmap=cmap)
            #plt.title('Daily Mean Sea Level Pressure: %s model run. %s' % (experiment_id, date_iso), fontsize=12)
            plt.title('Model Mean Sea Level Pressure: %s model run.' % (experiment_id), fontsize=12)
            dx, dy = 10, 10
                     
            plt.clabel(contour, fmt='%d')
            ax.stock_img()
            ax.coastlines(resolution='110m', color='gray') 
            
          
            gl = ax.gridlines(draw_labels=True,linewidth=1, color='gray', alpha=0.5, linestyle='--')
            gl.xlabels_top = False
            gl.ylabels_right = False
            #gl.xlines = False
            gl.xlocator = mticker.FixedLocator(range(60,105+dx,dx))
            gl.ylocator = mticker.FixedLocator(range(-10,30+dy,dx))
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            #gl.xlabel_style = {'size': 15, 'color': 'gray'}
            #gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
            #plt.savefig('/home/pwille/python_scripts/pngs/%s/msl_daily_mean_%s_%s.png' % (experiment_id, experiment_id, date_iso))
            #plt.stock_img()
            plt.savefig('/home/pwille/python_scripts/pngs/%s/msl_model_mean_%s.png' % (experiment_id, experiment_id))
            #plt.show()
            plt.close()
if __name__ == '__main__':
    main()
