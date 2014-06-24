import os,sys

import iris

import matplotlib.pyplot as plt
import numpy as np

fname1 = '/projects/cascade/pwille/moose_retrievals/djzn/djznw/407.pp'
fname2 = '/projects/cascade/pwille/moose_retrievals/djzn/djznw/15102.pp'

#fname ='/home/pwille/python_scripts/djznw/pickle_407_pressure_levels_dp_djznw.p.npy'

heights = iris.load_cube(fname2)
p_at_rho = iris.load_cube(fname1)

rho_plot=np.zeros((2,70))
rho_plot[0,:] = p_at_rho[0,:,0,0].data
rho_plot[1,:] = heights[0,:,0,0].data

f1 = plt.figure()
f2 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot(rho_plot[0,:],rho_plot[1,:])
ax2 = f2.add_subplot(111)
ax2.plot(np.log(rho_plot[0,:]), (rho_plot[1,:]))

plt.show()



