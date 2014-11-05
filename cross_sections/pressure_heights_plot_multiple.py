"""

Load geopotential heights/pt/sp hum and plot

22/05/14

"""

import os, sys
import numpy as np

import matplotlib

import iris

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm

from matplotlib import rc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

sys.path.append('/home/pwille/python_scripts/modules')
from update_pp_cube_coords import update_coords

rc('font', family = 'serif', serif = 'cmr10')
#rc('text', usetex=True)

#c_section_lon=74.
c_section_lat=0

c_lon_min=75.
c_lon_max=85.

gap=1.

diags=['4']
#experiment_ids = ['djznw', 'djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns', 'dkjxq'  ]
experiment_ids = ['djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns']
sp='Mean'
#p_levels = [1000., 950., 925., 850., 700., 500., 400., 300., 250., 200., 150., 100., 70., 50., 30., 20., 10.]
experiment_ids = ['djzny', 'djznq', 'djznw']

for c_section_lon in np.arange(c_lon_min,c_lon_max, gap):
 for experiment_id in experiment_ids:
    expmin1 = experiment_id[:-1]
    for diag in diags:
        if diag=='408':
            clevpt_min=600.
            clevpt_max=700.
        if diag=='4':
            clevpt_min=300.
            clevpt_max=310.
        if diag=='10':
            clevpt_min=0.
            clevpt_max=0.02

      
        if c_section_lon!=0:
            data=np.load('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s_%s.npz' % (experiment_id, diag, sp, c_section_lon))
            xc=data['xc_mean']
            coords=data['coord']

            h=iris.load_cube('/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp' % (expmin1, experiment_id)) 
            h,lats,lons= update_coords(h) 
            l=h.coord('longitude').nearest_neighbour_index(c_section_lon) 

        # for i, coord in enumerate (h.coords()):
        #     if coord.standard_name=='longitude':
        #         lon_dim_coord_diag = i

        # if lon_dim_coord_diag==0:
        #      heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[l,:]  
        # if lon_dim_coord_diag==1:
        #      heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[:,l,:]  
        # if lon_dim_coord_diag==2:
        #      heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[:,:,l,:]  
        # if lon_dim_coord_diag==3:
        #      heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[:,:,:,l,:]  
        # if lon_dim_coord_diag==4:
        #      heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[:,:,:,:,l,:]  
        # if lon_dim_coord_diag==5:
        heights = h.slices(['model_level_number', 'latitude', 'longitude']).next()[:,:,l]  
        print heights

        if c_section_lat!=0:
            data=np.load('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Latitude_%s_%s.npz' % (experiment_id, diag, sp, c_section_lat))
            xc=data['xc_mean']
            coords=data['coord']
            h=iris.load_cube('/projects/cascade/pwille/moose_retrievals/%s/%s/15101.pp' % (expmin1, experiment_id))
            heights = h.slices(['model_level_number', 'grid_longitude']).next().data

        print heights.shape
        print heights
        print coords.shape
       
        #X,Y = np.meshgrid(coords,heights,coord)

        X=np.array([heights.coord('latitude').points,] * len(heights.coord('model_level_number').points))
        Y=heights.data
       
        # print xc
        # print xc.shape
        # print X.shape
        # print Y.shape
        # print X
        # print Y
 
        #p print np.swapaxes(X,0,1)rint coords
        #print p_levels[::-1]

        # grid the data.
        #zi = griddata(x,y,z,xi,yi,interp='linear')
        fig=plt.figure(figsize=(8,10))
        ax = fig.add_axes([0.05,0.05,0.9,0.85])
     
        if diag=='408':
            plt.title('%s - Geopotential Height' % experiment_id)
            CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 256), cmap=plt.cm.jet)
            #CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(300, 500, 8), cmap=plt.cm.jet)
            cbar = plt.colorbar(CS,orientation='horizontal', format='${%d}$')
            cbar.set_label('${K}$')
        if diag=='4':
            plt.title('%s - Potential Temperature' % experiment_id)
            #CS = ax.contourf(np.swapaxes(X,0,1),np.swapaxes(Y,0,1),np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 256), cmap=plt.cm.jet)
            #CS = ax.contourf(xc)
            CS = ax.contourf(X,Y,xc, np.linspace(clevpt_min, clevpt_max, 256), cmap=plt.cm.jet, extend='both')
            #CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(300, 500, 8), cmap=plt.cm.jet)
            cbar = plt.colorbar(CS,orientation='horizontal', format='${%d}$', extend='both')
            cbar.set_label('${K}$')
        if diag=='10':
            plt.title('%s - Specific Humidity' % experiment_id)
            CS = ax.contourf(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 256), cmap=plt.cm.jet_r)
            cbar = plt.colorbar(CS,orientation='horizontal', format='${%.3f}$')
            cbar.set_label('${kg/kg}$')
        #CS = ax.contour(X,Y,np.swapaxes(xc,0,1), np.linspace(clevpt_min, clevpt_max, 10), colors='k')
        
        plt.ylim([950,100])
        plt.xlim([20, 30])

        
        plt.gca().invert_yaxis
        #plt.clabel(CS, fontsize=9, inline=1)

        ax.xaxis.set_major_formatter(FormatStrFormatter('${%d}$'))
        ax.yaxis.set_major_formatter(FormatStrFormatter('${%d}$'))
              
        #plt.show()
        if c_section_lon!=0:
             plt.xlabel('Latitude')
             plt.savefig('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s_20_to_30N.png' % (experiment_id, diag, c_section_lon), bbox_inches='tight')
        if c_section_lat!=0:
             plt.xlabel('Longitude')
             plt.savefig('/nfs/a90/eepdw/Figures/EMBRACE/Cross_Sections/%s_%s_height_XC_Latitude_%s_??.png' % (experiment_id, diag, c_section_lat), bbox_inches='tight')

        plt.close()
