#Get year from date - used as input to iris.coord_categorisation.add_categorised_coord(p_at_msl, 'year', 'time', year_from_time)

import numpy
import iris.coords

def year_from_time(coord, point):

        yearnp = coord.units.num2date(point).time
        
        #yearpoint=[]
        for index, x in numpy.ndenumerate(yearnp):

             yearpoint[index] = x.year

        #year = iris.coords.AuxCoord(yearpoint)
        return year
