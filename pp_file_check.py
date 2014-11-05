"""
Loop through specified model runs for diagnostic, print info, and plot time/date points
"""

import os,sys

import iris
import iris.coords as coords
import iris.unit as unit

import matplotlib.pyplot as plt
import datetime
import numpy as np

import datetime

import imp

import cartopy.crs as ccrs
import iris.analysis.cartography
#unrotate = imp.load_source('util', '/home/pwille/python_scripts/modules/unrotate_pole.py')
def main():

 diag_to_check='4'
 experiment_ids = ['djznu', 'djznq', 'djzny', 'djznw', 'djzns', 'dkbhu', 'dkhgu','dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ]


 #experiment_ids = ['djzny', 'djznq' ]
 #experiment_ids = ['dkhgu']
 u = unit.Unit('hours since 1970-01-01 00:00:00', calendar=unit.CALENDAR_STANDARD)
 try:
  for offset, experiment_id in enumerate(experiment_ids):
    expmin1 = experiment_id[:-1]

    fname = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp'% (expmin1, experiment_id, diag_to_check)

    try:
        cube_list = iris.load(fname)
        print '%s - %s' % (fname, cube_list)
        #print cube_list
  
        cube=cube_list[0]
        time_list = cube.coord('time').points
        dates = u.num2date(time_list)
        #dates_num = matplotlib.dates.date2num(dates)
        #print dates_num
        cs = cube.coord_system('CoordSystem')
        print cs
        lon = cube.coord('grid_longitude').points
        lat = cube.coord('grid_latitude').points

        lonr,latr=np.meshgrid(lon,lat)
        lons, lats = iris.analysis.cartography.unrotate_pole(lonr, latr, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

        #print '%s - Lons min/max %s %s' %(experiment_id, min(lons[0]), max(lons[0]))
        #print '%s - Lats unrotated min/max %s %s' %(experiment_id, min(lats[:,0]), max(lats[:,0]))
        #print '%s - Lats rotated min/max %s %s' %(experiment_id, min(lat), max(lats))

        y = np.empty(dates.shape)
        y.fill(offset)
        #print y
        l = plt.plot(dates.flatten(), y.flatten(), label=experiment_id, linestyle='', marker='o', markersize=2)
      
        pos = [734377, (y.flatten()[0]-0.2)]
        plt.text(pos[0], pos[1], experiment_id, size=9, rotation=0, ha="center", va="center")
    except Exception, e:
        print '%s - Failed to load' % fname
        print e
        print sys.exc_traceback.tb_lineno 
        pass
 except Exception, e:
        print '%s' % fname
        print e
        pass
 plt.yticks([])
 plt.xticks(rotation=20)
 plt.ylim(-1,offset+1)
 plt.ylabel('Model')

#plt.tick_params(\
 #   axis='y',          # changes apply to the x-axis
 #   which='both',      # both major and minor ticks are affected
 #   right='off',      # ticks along the bottom edge are off
 #   left='off')         # ticks along the top edge are off
    #labelbottom='off') #plt.yaxis.set_visible(False)
 #plt.legend()
 plt.show()
        
if __name__ == '__main__':
    main()    


