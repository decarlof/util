# in_out_stages.py
#

def all_in():
    pv.zone_plate_x.put(0)
    pv.beam_stop_x.put(0)
    pv.condenser_x.put(0)
    pv.condenser_y.put(0)
    pv.pin_hole_x.put(0)
    pv.filter_x.put(14)
    #pv.diffuser_y.put(6)
    pv.diffuser_y.put(-6)

    # CCD parameter changes:
#    exposure = 0.5
#    pv.ccd_acquire_mode.put(0, wait=True, timeout=2) # CCD mode switched to fixed
#    pv.ccd_dwell_time.put(exposure, wait=True, timeout=2)
#    pv.ccd_acquire_mode.put(2, wait=True, timeout=2) # CCD mode switched to continuous
    return

def all_out():
    pv.beam_stop_x.put(8)
    pv.condenser_x.put(10)
    pv.condenser_y.put(-4)
    pv.pin_hole_x.put(8)
    pv.zone_plate_x.put(14)
    pv.diffuser_y.put(0)
    pv.filter_x.put(6)

    # CCD parameter changes:
#    exposure = 0.01
#    acq_periode = 0.1
#    pv.ccd_acquire_mode.put(0, wait=True, timeout=2) # CCD mode switched to fixed
#    pv.ccd_dwell_time.put(exposure, wait=True, timeout=2)
#    pv.ccd_acquire_period.put(acq_periode, wait=True, timeout=2)
#    pv.ccd_acquire_mode.put(2, wait=True, timeout=100) # CCD mode switched to continuous

    return

