"""

Load pp, plot and save


"""

import os, sys

#import matplotlib

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
#from matplotlib import rc
#from matplotlib.font_manager import FontProperties
#from matplotlib import rcParams

#rc('font', family = 'serif', serif = 'cmr10')
#rc('text', usetex=True)

#rcParams['text.usetex']=True
 #rcParams['text.latex.unicode']=True

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

model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/modules/model_name_convert_title.py')
unrotate = imp.load_source('util', '/home/pwille/python_scripts/modules/unrotate_pole.py')
pp_file = '3234_mean'

degs_crop_top = 1
degs_crop_bottom = 2.5
#
#
# cmap= cm.s3pcpn_l

#main_title='' # Automatically gets from cube below


def main():

 #experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ] 
 experiment_ids = ['djzny' ] 
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

 
  plt.figure(figsize=(8,8))
         
  cmap= cmap=plt.cm.RdBu_r
  
  ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_top_and_bottom,lat_high-degs_crop_top_and_bottom))
  
  clevs = np.linspace(0, 200,256)

  cont = iplt.contourf(pcube, clevs, cmap=cmap, extend='both')
 
  
                     
  #plt.clabel(cont, fmt='%d')
  #ax.stock_img()
  ax.coastlines(resolution='110m', color='#262626') 
                     
  gl = ax.gridlines(draw_labels=True,linewidth=1, color='#262626', alpha=0.5, linestyle='--')
  gl.xlabels_top = False
  gl.ylabels_right = True
            #gl.xlines = False
  dx, dy = 10, 10
  gl.xlocator = mticker.FixedLocator(range(int(lon_low),int(lon_high)+dx,dx))
  gl.ylocator = mticker.FixedLocator(range(int(lat_low),int(lat_high)+dy,dy))
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  
  gl.xlabel_style = {'size': 12, 'color':'#262626'}
  #gl.xlabel_style = {'color': '#262626', 'weight': 'bold'}
  gl.ylabel_style = {'size': 12, 'color':'#262626'}         
 
  cbar = plt.colorbar(cont, orientation='horizontal', pad=0.05, extend='both', format = '%d')
  #cbar.set_label('') 
  cbar.set_label(pcube.units)
  cbar.set_ticks(np.arange(-20.,200.+20.,20.))
  ticks = (np.arange(-20.,200.+20.,20.))
  cbar.set_ticklabels(['%d' % i for i in ticks])
  main_title=pcube.standard_name.title().replace('_',' ')
  model_info=re.sub('(.{75})', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
  model_info = re.sub(r'[(\']', ' ', model_info)
  model_info = re.sub(r'[\',)]', ' ', model_info)
  print model_info
  plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=12)
 
  plt.show()

  if not os.path.exists('/home/pwille/figures/%s/%s' % (experiment_id, plot_diag)): os.makedirs('/home/pwille/figures/%s/%s' % (experiment_id, plot_diag))
  #plt.savefig('/home/pwille/figures/%s/%s/%s%s_%s.png' % (experiment_id, plot_diag, pcube.standard_name.title(), experiment_id, plot_diag), format='png', bbox_inches='tight'))
  #plt.close()


if __name__ == '__main__':
   main()
