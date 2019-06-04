import process_variables as pv

def all_out():

    # OUT 
    pv.beam_stop_y.put(5)
    pv.condenser_y.put(-16)
    pv.pin_hole_x.put(7)
    pv.zone_plate_x.put(-6)
    
    return
