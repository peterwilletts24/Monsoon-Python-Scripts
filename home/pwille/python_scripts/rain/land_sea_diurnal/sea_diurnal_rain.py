"""

Load npy xy, plot and save


"""

import os, sys

import matplotlib
import matplotlib.pyplot as plt

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

rc('font', family = 'serif', serif = 'cmr10')

import numpy as np

#model_name_convert_title = imp.load_source('util', '/home/pwille/python_scripts/modules/model_name_convert_title.py')
#unrotate = imp.load_source('util', '/home/pwille/python_scripts/modules/unrotate_pole.py')

pp_file = 'avg.5216'

top_dir='/projects/cascade/pwille/moose_retrievals'

def main():
 experiment_ids = ['djzny', 'djznq', 'djzns', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ] 

 plt.figure(figsize=(8,8))
 for experiment_id in experiment_ids:

  expmin1 = experiment_id[:-1]

  try:
      plotnp = np.load('%s/%s/%s/%s_sea_rainfall_diurnal_np.npy' % (top_dir, expmin1, experiment_id, pp_file))

      plt.plot(plotnp[1],plotnp[0])
  except:
      pass

 plt.show()

 if not os.path.exists('/home/pwille/figures/%s/%s' % (experiment_id, pp_file)): os.makedirs('/home/pwille/figures/%s/%s' % (experiment_id, pp_file))
  #plt.savefig('/home/pwille/figures/%s/%s/%s_%s.png' % (experiment_id, pp_file, experiment_id, pp_file), format='png', bbox_inches='tight')
  #plt.close()


if __name__ == '__main__':
   main()

   
       



