

import os,sys


import iris
import iris.unit as unit
from iris.coord_categorisation import add_categorised_coord

import datetime

import numpy as np

import pdb

#experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All except 3 big
#  Needs to be run as script on monsoon or pp files need to be copied across to here

cube_name_explicit='stratiform_rainfall_rate'
cube_name_param='convective_rainfall_rate'

pp_file_path='/projects/cascade/pwille/moose_retrievals/'

bins=np.linspace(0,200, 200)

diag='avg.5216'
regrid_model='djznw'
regrid_model_min1=regrid_model[:-1]

dtmindt = datetime.datetime(2011,8,19,0,0,0)
dtmaxdt = datetime.datetime(2011,9,7,23,0,0)
dtmin = unit.date2num(dtmindt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
dtmax = unit.date2num(dtmaxdt, 'hours since 1970-01-01 00:00:00', unit.CALENDAR_STANDARD)
time_constraint = iris.Constraint(time= lambda t: dtmin <= t.point <= dtmax)

# Min and max lats lons from smallest model domain (dkbhu) - see spreadsheet

# Unrotated - can only be used (without unrotating first) for djznw  - global model

latmin=-6.79
latmax=33.04
lonmin=64.12
lonmax=101.87
        
lat_constraint=iris.Constraint(grid_latitude= lambda la: latmin <= la.point <= latmax)
lon_constraint=iris.Constraint(grid_longitude= lambda lo: lonmin <= lo.point <= lonmax)

fg = '%sdjzn/djznw/%s.pp' % (pp_file_path, diag)
fr = '%s%s/%s/%s.pp' % (pp_file_path, regrid_model_min1, regrid_model, diag)

glob_load = iris.load_cube(fg, ('%s' % cube_name_param)  & time_constraint)

## Get time points from global LAM to use as time constraint when loading other runs
time_list = glob_load.coord('time').points
glob_tc = iris.Constraint(time=time_list)

regrid_cube = iris.load_cube(fr, ('%s' % cube_name_param)  & glob_tc & lat_constraint & lon_constraint)

#Load land sea mask
flsm = '%s%s/%s/30.pp' % (pp_file_path, regrid_model_min1, regrid_model)

lsm = iris.load_cube(flsm, ('land_binary_mask' ) )
 #lsm = unrotate_pole_update_cube(lsm)
lsm=lsm.extract(lat_constraint & lon_constraint)
 #print lsm
for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 fu = '%s%s/%s/%s.pp' % (pp_file_path, expmin1, experiment_id, diag)


 print experiment_id
 sys.stdout.flush()

 try:
        #cube_names = ['%s' % cube_name_param, '%s' % cube_name_explicit]
        cubeconv  = iris.load_cube(fu,'%s' % cube_name_param & glob_tc)
        cubestrat  = iris.load_cube(fu,'%s' % cube_name_explicit & glob_tc)
        cube=cubeconv+cubestrat
        cube.rename('total_precipitation_rate')
 except iris.exceptions.ConstraintMismatchError:        
        cube = iris.load_cube(fu, ('%s' % cube_name_explicit)  & glob_tc)

 cube_r = iris.analysis.interpolate.regrid(cube, regrid_cube, mode='bilinear')
 mmperhour = iris.analysis.maths.multiply(cube_r,3600)
 

 pdf=[]
 pdf_map=[]

 bmin=0.

 #pdb.set_trace()

 for b in bins:

  
 
           #pdf_map = mmperhour.collapsed('time', iris.analysis.COUNT, function=lambda values: ((values <= b) & (values>=bmin)))
            #iris.save(pdf_map, "/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s_pdf_map.pp" % (expmin1, experiment_id, experiment_id, diag), append=True) # Doesnt work - dtype issue
            pdf_map.append(mmperhour.collapsed('time', iris.analysis.COUNT, function=lambda values: ((values <= b) & (values>=bmin))).data)
            pdf.append(float(mmperhour.collapsed(('time', 'grid_latitude', 'grid_longitude'), iris.analysis.COUNT, 
                                            function=lambda values: ((values <= b) & (values>=bmin))).data))
            if bmin==0.:
                bmin=0.0000000001
            else:
                bmin=b
 
 np.save("/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s_pdf" %(expmin1, experiment_id, experiment_id, diag), pdf)
 np.save("/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s_pdf_map" %(expmin1, experiment_id, experiment_id, diag), pdf_map)



# Do for land and sea

 for ls in ['land', 'sea']:

     if ls=='land':
         mask=1
     elif ls=='sea':
         mask=0

     pdf=[]

     #pdb.set_trace()
   
     bmin=0.

     for b in bins:
            
         whole_area_pdf = mmperhour.collapsed('time', iris.analysis.COUNT, function=lambda values: ((values <= b) & (values>=bmin))).data

         pdf.append(np.ma.sum(whole_area_pdf[lsm.data==mask]))
           
         if bmin==0.:
             bmin=0.0000000001
         else:
             bmin=b
 
     np.savez("/projects/cascade/pwille/moose_retrievals/%s/%s/%s_%s_pdf_%s" %(expmin1, experiment_id, experiment_id, diag, ls), pdf=pdf, bins=bins)
