'Converts model run names e.g djznu to sub title for plots'


def main(experiment_id): 
    djznu = ('1.5km', '4500 km', '10s', 'L118, 78km lid', 'Explicit 3D SMAG', 'djznu')
    dkbhu = ('2.2km', '4500 km', '10s', 'L118, 78km lid', 'Explicit 3D SMAG', 'dkbhu')
    djzns = ('4km', '4500 km', '10s', 'L118, 78km lid', 'Explicit 3D SMAG', 'djzns')
    djznq = ('24km',	'4500 km',	'600s',	'Global NWP set L70, 80 km lid', 	'1DBL + conv param', 'djznq')
    djzny = ('120km',	'4500 km',	'1200s',	'Global NWP set L70, 80 km lid', 	'1DBL + conv param', 'djzny')
    djznw = ('Driving Global', '4500 km', '1200s?', 'Global NWP set L70, 80 km lid', '1DBL + conv param', 'djznw')
						
    dkhgu = ('2.2km Large', 'Big', '', '', '', 'dkhgu')			
    dkjxq = ('24km','Big', '', '', '', 'dkjxq')
						
    dklyu = ('8km','Big' ,'10s', 'L118, 78km lid', 'Explicit 3D SMAG', 'dklyu')
    dkmbq = ('8km', 'Big', '300s?', '', '1DBL + conv param', 'dkmbq')
						
    dklwu = ('12km', '', '10s', 'L118, 78km lid', 'Explicit 3D SMAG', 'dklwu')
    dklzq = ('12km', '', '300s?', '1DBL + conv param', 'dklzq')

    experiment_ids = [djznu, dkbhu, djzns, djznq, djzny, djznw, dkhgu, dkjxq, dklyu, dkmbq, dklwu, dklzq ]


    for ex in experiment_ids:

        if (experiment_id==ex[-1]):
            title=ex
            mod_sub_title = '%s' % (title[0])

    return mod_sub_title,

if __name__ == '__main__':
    main()
