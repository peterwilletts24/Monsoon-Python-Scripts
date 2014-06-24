"""
Load winds on pressure levels and calculate vorticity and divergence
"""
import os, sys
import datetime
import iris
import iris.unit as unit
diag = '30201'
cube_name_u='eastward_wind'
cube_name_v='northward_wind'
pp_file_path='/projects/cascade/pwille/moose_retrievals/'
#experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq'] # All minus large 3
experiment_ids = ['djznw']
for experiment_id in experiment_ids:
 expmin1 = experiment_id[:-1]
 #fu = '/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1, experiment_id, diag)
 try:
  print 'hello'
  
  
