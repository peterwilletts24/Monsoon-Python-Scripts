"""

Loop through multiple pickle files of averaged etc data, plot and save


"""

import os, sys


import glob

# import itertools
import matplotlib

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

model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/model_name_convert_title.py')



def main():

 

 lon_low= 60
 lon_high = 105
 lat_low = -10
 lat_high = 35

 #experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ] 
 experiment_ids = ['djzny' ] 
 for experiment_id in experiment_ids:
 
  expmin1 = experiment_id[:-1]

  pfile = '/projects/cascade/pwille/moose_retrievals/%s/%s/3234_mean.pp' % (expmin1, experiment_id)
  #pc =  iris(pfile)
  pcube = iris.load_cube(pfile)
  print pcube
  #iris.analysis.maths.divide(pcube,20,in_place=True)
  if not os.path.exists('/home/pwille/python_scripts/pngs/%s' % (experiment_id)): os.makedirs('/home/pwille/python_scripts/pngs/%s' % (experiment_id))
    
  plt.figure(figsize=(8,8))
         
  #pcube.coord('grid_latitude').guess_bounds()
  #pcube.coord('grid_longitude').guess_bounds()
  
  cmap= cmap=plt.cm.RdBu_r
  
  ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))
  
  clevs = np.linspace(0, 200,256)

  cs = iplt.contourf(pcube, clevs, cmap=cmap)
 
  dx, dy = 10, 10
                     
  plt.clabel(contour, fmt='%d')
  ax.stock_img()
  ax.coastlines(resolution='110m', color='#262626') 
                     
  gl = ax.gridlines(draw_labels=True,linewidth=1, color='#262626', alpha=0.5, linestyle='--')
  gl.xlabels_top = False
  gl.ylabels_right = False
            #gl.xlines = False
  gl.xlocator = mticker.FixedLocator(range(60,105+dx,dx))
  gl.ylocator = mticker.FixedLocator(range(-10,40+dy,dy))
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  
  gl.xlabel_style = {'size': 15, '#262626': 'gray'}
  gl.xlabel_style = {'color': '#262626', 'weight': 'bold'}
           
  plt.stock_img()
  plt.savefig('/home/pwille/python_scripts/pngs/%s/msl_model_mean_%s.png' % (experiment_id, experiment_id))
  cbar = plt.colorbar(cs, orientation='horizontal', pad=0.05, extend='both', format = '%d')
  cbar.set_label('W/m2') 
  cbar.set_ticks(np.arange(-20.,200.+20.,20.))
  ticks = (np.arange(-20.,200.+20.,20.))
  cbar.set_ticklabels(['%d' % i for i in ticks])
  main_title='Surface Upward Latent Heat Flux'
  model_info=re.sub('{80}', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
  print model_info
  plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=12)
 
  plt.show()
  #plt.savefig('test%s%s.png' % (experiment_id, experiment_id))

  #plt.close()
if __name__ == '__main__':
    main()
