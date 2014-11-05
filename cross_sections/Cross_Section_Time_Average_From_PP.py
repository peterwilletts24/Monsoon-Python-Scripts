"""
Load geopotential heights and orography cube to get lat/lon cross-section

22/05/14

"""

import os, sys

import pdb

import iris
import iris.analysis.cartography

import iris.coord_categorisation

import numpy as np

#c_section_lon=74.

c_lon_min=75.
c_lon_max=85.
gap=1.

c_section_lat=0

diagnostic=4
experiment_ids = ['djznw', 'djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns'  ]
#experiment_ids = ['dklyu', 'dkmbq', 'dklwu', 'djzns'  ] #djznw and dklwu missing
#experiment_ids = ['dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
#experiment_ids = ['dkbhu']
#experiment_ids = ['djzny', 'djznq', 'djznw']

for experiment_id in experiment_ids:

 expmin1 = experiment_id[:-1]

 diag_load = iris.load('/projects/cascade/pwille/moose_retrievals/%s/%s/%s.pp' % (expmin1,experiment_id, diagnostic))
 
 #diag = iris.load(f_diag)

 for diag in diag_load:
  print diag

  cs = diag.coord_system('CoordSystem')
  print cs
  csur=cs.ellipsoid  

  lat = diag.coord('grid_latitude').points
  lon = diag.coord('grid_longitude').points

  lons, lats = np.meshgrid(lon, lat)  

  lons,lats = iris.analysis.cartography.unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

  lon=lons[0]
  lat=lats[:,0]

  for i, coord in enumerate (diag.coords()):
     if coord.standard_name=='grid_latitude':
         lat_dim_coord_diag = i
     if coord.standard_name=='grid_longitude':
         lon_dim_coord_diag = i

  diag.remove_coord('grid_latitude')
  diag.remove_coord('grid_longitude')
  diag.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=csur), lat_dim_coord_diag)
  diag.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=csur), lon_dim_coord_diag)

  for c_section_lon in np.arange(c_lon_min,c_lon_max+1, gap):

   if (c_section_lon != 0):
   
    print c_section_lon
    l=diag.coord('grid_longitude').nearest_neighbour_index(c_section_lon) 

    if lon_dim_coord_diag==0:
       xc=diag[l,:]  
    if lon_dim_coord_diag==1:
       xc=diag[:,l,:]
    if lon_dim_coord_diag==2:
       xc=diag[:,:,l,:]
    if lon_dim_coord_diag==3:
       xc=diag[:,:,:,l,:]
    if lon_dim_coord_diag==4:
       xc=diag[:,:,:,:,l,:]
    if lon_dim_coord_diag==5:
       xc=diag[:,:,:,:,:,l,:]
    #iris.save(xc, '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' % (experiment_id, diagnostic, str(c_section_lon).replace(".", "")))
   #THESE METHODS MIGHT WORK BUT TAKE A LONG TIME - I THINK BECAUSE THEY LOAD THE WHOLD CUBE IN TO INDEX
    #xc = iris.analysis.interpolate.extract_nearest_neighbour(diag, [('grid_longitude', c_section_lon)]).data
    #lon_slice = iris.analysis.interpolate.linear(diag, [('grid_longitude', l), ('grid_latitude', np.linspace(20, 30, 50))])
    #print lon_slice
    #pdb.set_trace
    #iris.save(lon_slice, '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' % (experiment_id, diagnostic, str(c_section_lon).replace(".", "")))
    #iris.save(iris.analysis.interpolate.extract_nearest_neighbour(diag, [('grid_longitude', c_section_lon)]), 
     #         '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' 
      #        % (experiment_id, diagnostic, str(c_section_lon).replace(".", "")))
   
    #xc=lon_slice.data
    #np.savez('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s' % (experiment_id, diagnostic, c_section_lon), xc=xc.data, coord=diag.coord('grid_latitude').points)

    #iris.coord_categorisation.add_day_of_month(xc, 'time', name='day_of_month')
    # pdb.set_trace()
    # iris.coord_categorisation.add_day_of_year(xc, 'time', name='day_of_month')
    # iris.coord_categorisation.add_month_number(xc, 'time', name='month_number') 

   
    #pdb.set_trace()

    try:
      iris.coord_categorisation.add_day_of_year(xc, 'time', name='day_of_year')
      #iris.coord_categorisation.add_day_of_month(xc, 'time', name='day_of_month') 
      #iris.coord_categorisation.add_month_number(xc, 'time', name='month_number') 
    except(AttributeError):
      iris.coord_categorisation.add_day_of_year(xc, 'forecast_reference_time', name='day_of_year')
      #iris.coord_categorisation.add_day_of_month(xc, 'forecast_reference_time', name='day_of_month')
      #iris.coord_categorisation.add_month_number(xc, 'forecast_reference_time', name='month_number')   
    
    #days_and_months_xc = xc.aggregated_by(['day_of_month', 'month_number'], iris.analysis.MEAN) 
    days_and_months_xc = xc.aggregated_by(['day_of_year'], iris.analysis.MEAN) 
    print days_and_months_xc
    #iris.save(days_and_months_xc, '/projects/cascade/pwille/Cross_Sections/%s_%s_%s_height_XC_Longitude_Daily_Mean_%s.pp' % (diag.name(), experiment_id, diagnostic, c_section_lon)) 
    np.savez('/projects/cascade/pwille/Cross_Sections/%s_%s_%s_height_XC_Longitude_Mean_%s' % (diag.name(), experiment_id, diagnostic, c_section_lon), days_and_months_xc=days_and_months_xc.data, coord=days_and_months_xc.coord('grid_latitude').points)
    
#     Whole Mean
#    np.savez('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_Mean_%s' % (experiment_id, diagnostic, c_section_lon), xc_mean=xc_mean.data.data, coord=diag.coord('grid_latitude').points)


 
#  if (c_section_lat != 0):
 #    print c_section_lat
    
  #   l=diag.coord('grid_latitude').nearest_neighbour_index(c_section_lat) 
   #  lat_slice = iris.analysis.interpolate.extract_nearest_neighbour(diag, [('grid_latitude', l)])
    # iris.save(lat_slice, '/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Longitude_%s.pp' % (experiment_id, diagnostic, c_section_lat))
    #np.savez('/projects/cascade/pwille/Cross_Sections/%s_%s_height_XC_Latitude_%s' % (experiment_id, diag, c_section_lon), xc=lat_slice.data, coord=lat_slice.coord('grid_longitude').points)
