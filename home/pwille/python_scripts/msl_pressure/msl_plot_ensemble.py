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

    j=1
    #pickle_name = 'pickle_daily_mean_*.p'
    pickle_name = 'pickle_model_mean_collapsed_*.p'
    flist = glob.glob ('/home/pwille/python_scripts/*/%s' % pickle_name)


    plt.figure(figsize=(30, 15))
    #plt.gcf().subplots_adjust(hspace=0.05, wspace=0.05, top=0.95, bottom=0.05, left=0.075, right=0.925)

    plt.gcf().subplots_adjust(top=0.5)

    plt.suptitle('Mean sea level pressure of model runs (average of entire model run)')
    for i in flist:

        fname = str(i)
        
        experiment_id = fname.split('/')[4]
        if not os.path.exists('/home/pwille/python_scripts/pngs/%s' % (experiment_id)): os.makedirs('/home/pwille/python_scripts/pngs/%s' % (experiment_id))
      
  #daily_mean = pickle.load( open( "/home/pwille/python_scripts/%s/pickle_daily_mean_%s.p" % (experiment_id, experiment_id), "rb" ) )
        model_mean = pickle.load( open( "%s" % (fname), "rb" ) )
        #print model_mean
       
        for sub_cube in model_mean.slices(['grid_latitude', 'grid_longitude']):
            
      #Get date in iso format for title, if needed
      
            #day=sub_cube_daily.coord('dayyear')
            #day_number = day.points[0]
            #day_number_ordinal=first_ordinal-1 + day_number
            #date_print = datetime.date.fromordinal(day_number_ordinal)
            #date_iso = str(date_print.isoformat())

            sub_cube.units = 'hPa'
            sub_cube /= 100


 # Load a Cynthia Brewer palette.
            brewer_cmap = mpl_cm.get_cmap('Spectral')   
        #contour = qplt.contour(sub_cube_daily, brewer_cmap.N, cmap=brewer_cmap)
           

            clevs = np.arange(996,1016)
            
            sub_cube.coord('grid_latitude').guess_bounds()
            sub_cube.coord('grid_longitude').guess_bounds()
            print j
            plt.subplot(2, 4, j, projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))
            #plt.subplot(4, 2, j, projection=ccrs.PlateCarree())
            j+=1

            contour = iplt.contour(sub_cube, clevs, colors='k',linewidths=0.5)
            #iplt.contourf(sub_cube, 16, cmap=brewer_cmap)
            #plt.title('Daily Mean Sea Level Pressure: %s model run. %s' % (experiment_id, date_iso), fontsize=12)
            plt.title('%s' % (experiment_id), fontsize=8)
            dx, dy = 10, 10
           
                      
            plt.clabel(contour, fmt='%d', inline=1, fontsize=8)
           
            plt.gca().coastlines(resolution='110m', color='gray') 
            plt.gca().stock_img()
            
            gl = plt.gca().gridlines(draw_labels=True,linewidth=1, color='gray', alpha=0.5, linestyle='--')
            gl.xlabels_top = False
            gl.ylabels_right = False
            #gl.xlines = False
            gl.xlocator = mticker.FixedLocator(range(60,105+dx,dx))
            gl.ylocator = mticker.FixedLocator(range(-10,30+dy,dx))
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': 8, 'color': 'gray'}
            #gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
            gl.ylabel_style = {'size': 8, 'color': 'gray'}
            #gl.xlabel_style = {'color': 'red', 'weight': 'bold'}
           
            #plt.savefig('/home/pwille/python_scripts/pngs/%s/msl_model_mean_%s.png' % (experiment_id, experiment_id))
#    plt.subplots_adjust(top=0.9, bottom=0.1, hspace=0.2)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, wspace=0.2, hspace=0.2)
#plt.show()
    plt.savefig('/home/pwille/python_scripts/pngs/msl_model_mean_ensemble.png')
    plt.close()          
           

            #print sub_cube
            #print fname
            #print experiment_id
if __name__ == '__main__':
    main()
