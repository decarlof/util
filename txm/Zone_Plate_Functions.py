# Zone_Plate_Functions.py
#
# function related to zone plate calculations


def ZP_NA(landa, drn):
#   return the numerical aperture NA (semi-angle) of a zone plate (mrad)
#   script: ZP_NA(landa, drn)
#        landa: wavelength in nm
#        drn: outer most zone width (nm)
#   exple: NA = ZP_NA(0.155, 60)
    NA = 1000*landa/(2.0*drn)
    return NA

def ZP_DOF(landa, NA):
#   return the depth of focus (+/- DOF) of a zone plate (microns)
#   script: ZP_DOF(landa, NA)
#        landa: wavelength in nm
#        NA: numerical aperture NA (semi-angle) of a zone plate (mrad)
#   exple: DOF = ZP_DOF(0.155, 1.29)
    DOF = landa / (2*(NA/1000)^2) / 1000
    return DOF


def ZP_zone_number(ZP_diameter, drn):
#   return the number of zones of a zone plate
#   script: ZP_zone_number(ZP_diameter, drn)
#        ZP_diameter: zone plate diameter (microns)
#        drn: outer most zone width (nm)
    N = 1000 * ZP_diameter / (4*drn)
    return N

def ZP_focal_length(landa, ZP_diameter, drn):
#   Return the zone plate focal length (mm) at a given energy (keV)
#   script: ZP_focal_length(ZP_diameter, landa, drn)
#        landa: wavelength in nm
#        ZP_diameter: zone plate diameter (microns)
#        drn: outer most zone width (nm)
    f = ZP_diameter * drn / (1000*landa)
    return f

def ZP_work_dist(ZP_focal, ZP_CCD_dist):
#   Return the working distance of the zone plate (mm) for a given ZP focal length and ZP working distance
#   script: ZP_work_dist(ZP_focal, ZP_CCD_dist)
#        ZP_focal: mm
#        ZP_CCD_dist: mm
    ZP_WD = ZP_CCD_dist * ZP_focal / (ZP_CCD_dist - ZP_focal)
    return ZP_WD

def dZP_CCD_fct_M(ZP_focal, Mag):
#   Return the distance zone plate to CCD (mm) for a given focal and Magnification
#   script: dZP_CCD_fct_M(ZP_focal, Mag)
#        ZP_focal: mm
#        Mag: magnification
    dZP_CCD = Mag * ZP_focal + ZP_focal
    return dZP_CCD

def ZP_magnification(ZP_CCD_dist, ZP_WD):
#   Return the magnification operated by the objective lens zone plate
#   script: ZP_magnification(ZP_CCD_dist, ZP_WD)
#        ZP_CCD_dist: mm
#        ZP_WD: mm
    Mag = ZP_CCD_dist / ZP_WD
    return Mag



