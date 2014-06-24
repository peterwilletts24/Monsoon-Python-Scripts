"""

Load numpy array, slice, mean, convert geometrich height to geopotential, and  save at pressure levels

"""

import os,sys

import numpy as np

def main():

    plot_levels = [850] 
    p_levels = [1000, 950, 925, 850, 700, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10]

    fname = '/home/pwille/python_scripts/djznw/pickle_407_pressure_levels_h_djznw.npy'
    
    experiment_id = fname.split('/')[4]
    
    save_path_h='/home/pwille/python_scripts/%s' % (experiment_id)
    save_name_h='/entire_mean_407_geopotential_h_%s' % experiment_id
    
    heights = np.load(fname)

    mean_over_time = heights.mean(axis=0)

    rad_e_lat = 1/(

    np.save("%s%s" % (save_path_h, save_name_h), mean_over_time_gp)

if __name__ == '__main__':
    main()
