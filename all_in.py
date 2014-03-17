from epics import PV

beam_monitor_x = PV('32idcTXM:nf:c0:m1.VAL')
beam_monitor_y = PV('32idcTXM:nf:c0:m2.VAL')
beam_stop_y = PV('32idcTXM:xps:c1:m2.VAL')

condenser_y = PV('32idcTXM:mxv:c1:m1.VAL')
pin_hole_x = PV('32idcTXM:xps:c1:m3.VAL')
zone_plate_y = PV('32idcTXM:xps:c0:m5.VAL')

# IN
#beam_monitor_x.put(0, wait=True)
#beam_monitor_y.put(0, wait=True)

beam_stop_y.put(0)
condenser_y.put(0)
pin_hole_x.put(0)
zone_plate_y.put(0)
