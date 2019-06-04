# moveE.py

def keV2landa(Energy):
#   return the wavelength in nm of a photon at a given energy (keV)
#   script: keV2landa(Energy)
#   exple: landa = keV2landa(7.2)
    landa = 1.240/Energy
    return landa

def moveE(Energy):
# Function changing the energy of the DCM and the GAP
#   script: moveE(Energy)
#        Energy: photon energy (keV)

    min_bound = 6
    max_bound = 15
    offset = 0.155
    if Energy > max_bound or Energy < min_bound:
        print '!! Requested energy out of bounds [%i - %i keV]' % (min_bound, max_bound)
    else:
#        En_Gap = pv.gap_en.get()
#        En_DCM = pv.DCM_en.get()
#        offset = En_Gap - En_DCM   # energy offset between the Gap and the DCM (0.132 in December 2014)
#        if offset > 0.5: offset = 0.09   # in case DCM and gap are not tuned for a single energy, the offset is forced

        pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
        print 'gap_en.put',Energy
        pv.gap_en.put(Energy, wait=True) # move the gap below offest for backlash
        print 'gap_en.put',Energy + offset
        pv.gap_en.put(Energy + offset, wait=True) # move the gap
        print 'gap_en.get():',pv.gap_en.get() # print value
        pv.DCM_en.put(Energy, wait=True) # move the DCM
        pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto

    return


def moveE_cstMag(new_Energy, drn, zp_diam, drn_BSC, BSC_diam):
# Function adapting the zone plate, the condenser and CCD location
# while changing the incident energy to maintain a constant Magnification
#   script: moveE_xanes(new_Energy, drn, zp_diam)
#        new_Energy: photon energy (keV)
#               drn: 
#           zp_diam:

    # Update the optic location:
    init_En_DCM = pv.DCM_en.get()
    init_En_Gap = pv.gap_en.get()
#    offset = En_Gap - En_DCM        # energy offset between the Gap and the DCM (0.132 in December 2014)
#    if offset > 0.5: offset = 0.1   # in case DCM and gap are not tuned for a single energy, the offset is forced
    offset = 0.159

    init_landa = keV2landa(init_En_DCM)
    new_landa = keV2landa(new_Energy)

    init_samp_ccd_dist = pv.ccd_camera_z.get() # get the distance CCD - sample
    init_ZP_focal = ZP_focal_length(init_landa, zp_diam, drn)
    init_ZP_CCD_dist = init_samp_ccd_dist - init_ZP_focal # approximation since excat distance ZP - CCD not accurate
    init_ZP_WD = ZP_work_dist(init_ZP_focal, init_ZP_CCD_dist)
    init_Mag = init_ZP_CCD_dist / init_ZP_WD

    new_ZP_focal = ZP_focal_length(new_landa, zp_diam, drn) # focal length for the new Energy
    delta_ZP_z = new_ZP_focal - init_ZP_focal
    new_ZP_WD = init_ZP_WD + delta_ZP_z
    new_ZP_CCD_dist = new_ZP_WD * init_Mag
    
    pv.zone_plate_z.put(delta_ZP_z, wait=True)      # move the ZP at the good location to 
    pv.ccd_camera_z.put(new_ZP_CCD_dist, wait=True) # change the CCD location to maintain a constant Magnification
    
    # apply the energy change:
    moveE(new_Energy)











    
