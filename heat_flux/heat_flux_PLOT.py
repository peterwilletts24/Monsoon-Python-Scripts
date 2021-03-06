"""

Loop through multiple pickle files of averaged etc data, plot and save


"""

import os, sys


import glob

# import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as mpl_cm
import numpy as np

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
from mpl_toolkits.basemap import cm

import imp
from textwrap import wrap

model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/model_name_convert_title.py')

def main():
 lon_low= 60
 lon_high = 105
 lat_low = -10
 lat_high = 30

 #experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ] 
 experiment_ids = ['djzny' ] 
 for experiment_id in experiment_ids:
 
  expmin1 = experiment_id[:-1]

  pfile = '/projects/cascade/pwille/moose_retrievals/%s/%s/3217_mean.pp' % (expmin1, experiment_id)
  #pc =  iris(pfile)
  pcube = iris.load_cube(pfile)
  print pcube
  #iris.analysis.maths.divide(pcube,20,in_place=True)
  if not os.path.exists('/home/pwille/python_scripts/pngs/%s' % (experiment_id)): os.makedirs('/home/pwille/python_scripts/pngs/%s' % (experiment_id))
    
  plt.figure(figsize=(8,8))
         
  pcube.coord('grid_latitude').guess_bounds()
  pcube.coord('grid_longitude').guess_bounds()
  
  cmap= cmap=plt.cm.RdBu_r
  
  ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))
  #contour = iplt.contourf(pcube, 16, colors='k',linewidths=1.)
  
  clevs = np.linspace(0, 100,256)

  cs = iplt.contourf(pcube, clevs, cmap=cmap)
  #plt.title('Daily Mean Sea Level Pressure: %s model run. %s' % (experiment_id, date_iso), fontsize=12)
  #plt.title('Total rainfall: %s.' % (experiment_id), fontsize=12)
  dx, dy = 10, 10
                     
  #plt.clabel(contour, fmt='%d')
  #ax.stock_img()
  ax.coastlines(resolution='110m', color='#262626') 
            
          
  gl = ax.gridlines(draw_labels=True,linewidth=1, color='#262626', alpha=0.5, linestyle='--')
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
  #plt.savefig('/home/pwille/python_scripts/pngs/%s/msl_model_mean_%s.png' % (experiment_id, experiment_id))
  cbar = plt.colorbar(cs, orientation='horizontal', pad=0.05, extend='both', format = '%d')
  cbar.set_label('W/m^2') 
  cbar.set_ticks(np.arange(0.,100.+20.,20.))
  ticks = (np.arange(0.,100.+20.,20.))
  cbar.set_ticklabels(['%d' % i for i in ticks])

  plt.title('\n'.join(wrap('%s' % (model_name_convert_title.main(experiment_id)), 80)), fontsize=10)
  
  plt.show()
  #plt.close()
if __name__ == '__main__':
    main()
