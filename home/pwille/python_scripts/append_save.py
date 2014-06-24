"""

Load pp which has same diagnostic split into smaller cubes ( append save for alrge datasets) and saves as one


"""

import os, sys

import iris

def main():

 pp_file = '1201_mean'

 pp_file_dir ='/projects/cascade/pwille/moose_retrievals/'
 experiment_ids = ['dkhgu', 'dkbhu', 'djznu'] 
 
 #experiment_ids = ['djznu' ] 
 for experiment_id in experiment_ids:
 
  expmin1 = experiment_id[:-1]
  pfile = '%s%s/%s/%s.pp' % (pp_file_dir, expmin1, experiment_id, pp_file)

  plist = iris.load(pfile)

  print plist

  pcube = plist.concatenate()

  print pcube

if __name__ == '__main__':
   main() 
