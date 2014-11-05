"""
Load geopotential heights and orography cube to get lat/lon cross-section

22/05/14

"""

import os, sys

import pdb

import iris
import iris.analysis.cartography

import numpy as np

diagnostic=4

experiment_ids = ['djzny', 'djznq', 'djznw']

c_lon_min=75.
c_lon_max=85.
gap=1.

for c_section_lon in np.arange(c_lon_min,c_lon_max, gap):
 for experiment_id in experiment_ids:

  data=np.load('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.npz' % (experiment_id, diagnostic, c_section_lon))
  xc=data['xc']
  coords=data['coord']

  iris.coord_categorisation.add_day_of_month(xc, 'time', name='day_of_month')
  iris.coord_categorisation.add_month_number(xc, 'time', name='month_number') 

  days_and_months_xc = xc.aggregated_by(['day_of_month', 'month_number'], iris.analysis.MEAN) 

  print days_and_months_xc
  
