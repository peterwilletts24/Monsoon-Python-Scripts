import os, sys

import iris
import glob



def main():

   
    diagnostic = '16222.pp'
    flist = glob.glob ('/projects/cascade/pwille/moose_retrievals/*/*/%s' % diagnostic)

    for i in flist:
        experiment_id = fname.split('/')[6]
        fname = str(i)
        p_at_msl = iris.load_cube(fname)
        
        print 
        print p_at_msl

if __name__ == '__main__':
    main()
