"""

Load pp, plot and save


"""

import os, sys

import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

from mpl_toolkits.basemap import Basemap

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

#rcParams['text.usetex']=True
#rcParams['text.latex.unicode']=True
#rcParams['font.family']='serif'
#rcParams['font.serif']='cmr10'

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

import re

import iris.analysis.cartography

import math

save_path='/home/pwille/Figures'

model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/modules/model_name_convert_title.py')
unrotate = imp.load_source('util', '/home/pwille/python_scripts/modules/unrotate_pole.py')
pp_file = 'rain_mean_regrid'

degs_crop_top = 1.7
degs_crop_bottom = 2.5

min_contour = 0
max_contour = 2
tick_interval=0.2
#
# cmap= cm.s3pcpn_l

divisor=10  # for lat/lon rounding

def main():

 #experiment_ids = ['djzny', 'djzns', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ] 
 experiment_ids = ['djzny', 'djzns', 'djznu', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkhgu'] 
 #experiment_ids = ['djzns' ] 
 #experiment_ids = ['dkhgu','dkjxq']

 for experiment_id in experiment_ids:

  expmin1 = experiment_id[:-1]
  pfile = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1, experiment_id, pp_file)

     #pc =  iris(pfile)
  pcube = iris.load_cube(pfile)
  print pcube
     #print pc
 
 # Get min and max latitude/longitude and unrotate  to get min/max corners to crop plot automatically - otherwise end with blank bits on the edges 
  lats = pcube.coord('grid_latitude').points
  lons = pcube.coord('grid_longitude').points
  
  cs = pcube.coord_system('CoordSystem')
  if isinstance(cs, iris.coord_systems.RotatedGeogCS):

      print 'Rotated CS %s' % cs
     
      lon_low= np.min(lons)
      lon_high = np.max(lons)
      lat_low = np.min(lats)
      lat_high = np.max(lats)

      lon_corners, lat_corners = np.meshgrid((lon_low, lon_high), (lat_low, lat_high))
      
      lon_corner_u,lat_corner_u = unrotate.unrotate_pole(lon_corners, lat_corners, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
      lon_low = lon_corner_u[0,0]
      lon_high = lon_corner_u[0,1]
      lat_low = lat_corner_u[0,0]
      lat_high = lat_corner_u[1,0]

  else: 
      lon_low= np.min(lons)
      lon_high = np.max(lons)
      lat_low = np.min(lats)
      lat_high = np.max(lats)

  #lon_low= 62
  #lon_high = 102
  #lat_low = -7
  #lat_high = 33

  #lon_high_box = 101.866 
  #lon_low_box = 64.115
  #lat_high_box = 33.
  #lat_low_box =-6.79

  #lon_high = 101.866 
  #lon_low = 64.115
  #lat_high = 33.
  #lat_low =-6.79

  lon_low_tick=lon_low -(lon_low%divisor)
  lon_high_tick=math.ceil(lon_high/divisor)*divisor

  lat_low_tick=lat_low - (lat_low%divisor)
  lat_high_tick=math.ceil(lat_high/divisor)*divisor
 
  print lat_high_tick
  print lat_low_tick
  plt.figure(figsize=(8,8))
         
  cmap=cm.s3pcpn_l
    
  ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_bottom,lat_high-degs_crop_top))
  
  #ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))

  #ax = plt.axes(projection=ccrs.PlateCarree())

  clevs = np.linspace(min_contour, max_contour,256)

  pcubeplot=iris.analysis.maths.multiply(pcube,3600)

  cont = iplt.contourf(pcubeplot, clevs, cmap=cmap, extend='both')
                     
  #plt.clabel(cont, fmt='%d')
  #ax.stock_img()
  ax.coastlines(resolution='110m', color='#262626') 
                     
  gl = ax.gridlines(draw_labels=True,linewidth=0.5, color='#262626', alpha=0.5, linestyle='--')
  gl.xlabels_top = False
  gl.ylabels_right = False
            #gl.xlines = False
  dx, dy = 10, 10

  gl.xlocator = mticker.FixedLocator(range(int(lon_low_tick),int(lon_high_tick)+dx,dx))
  gl.ylocator = mticker.FixedLocator(range(int(lat_low_tick),int(lat_high_tick)+dy,dy))
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  
  gl.xlabel_style = {'size': 12, 'color':'#262626'}
  #gl.xlabel_style = {'color': '#262626', 'weight': 'bold'}
  gl.ylabel_style = {'size': 12, 'color':'#262626'}         

  cbar = plt.colorbar(cont, orientation='horizontal', pad=0.05, extend='both')
  cbar.set_label('mm/h', fontsize=14, color='#262626') 
  #cbar.set_label(pcube.units, fontsize=10, color='#262626')
  cbar.set_ticks(np.arange(min_contour, max_contour+tick_interval,tick_interval))
  ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))
  cbar.set_ticklabels(['%.1f' % i for i in ticks])
  cbar.ax.tick_params(labelsize=14, color='#262626')
  
  main_title='Mean Rainfall for EMBRACE Period (smoothed to 24km)'
  #main_title=pcube.standard_name.title().replace('_',' ')
  model_info=re.sub('(.{68} )', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
  #model_info = re.sub(r'[(\']', ' ', model_info)
  #model_info = re.sub(r'[\',)]', ' ', model_info)
  #print model_info

  if not os.path.exists('%s%s/%s' % (save_path, experiment_id, pp_file)): os.makedirs('%s%s/%s' % (save_path, experiment_id, pp_file))

  plt.savefig('%s%s/%s/%s_%s_notitle.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file), format='png', bbox_inches='tight')

  plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=16)
 
  #plt.show()
 
  plt.savefig('%s%s/%s/%s_%s.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file), format='png', bbox_inches='tight')
  
  plt.close()
 

if __name__ == '__main__':
   main()
