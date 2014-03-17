from area_detector import ccdtake

flat_field = ccdtake(dwelltime = 2)
dark_field = ccdtake(dwelltime = 2)
ccdtake(dwelltime = 2, limits = (0, 1), ff = flat_field)



