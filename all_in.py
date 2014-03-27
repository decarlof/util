import process_variables as pv

pv.zone_plate_y.put(0)
pv.beam_stop_y.put(0)
pv.condenser_y.put(0)
pv.pin_hole_x.put(0)
print pv.pin_hole_x.get()
