# -*- coding: utf-8 -*-
"""
Transmission X-ray Microscope process variables grouped by component

"""
from epics import PV

# Beam Monitor
beam_monitor_x = PV('32idcTXM:nf:c0:m1.VAL')
beam_monitor_x_set = PV('32idcTXM:nf:c0:m1.SET')
beam_monitor_y = PV('32idcTXM:nf:c0:m2.VAL')
beam_monitor_y_set = PV('32idcTXM:nf:c0:m2.SET')

# Filter
filter_x = PV('32idcTXM:xps:c2:m1.VAL')

# Beam Stop
beam_stop_x = PV('32idcTXM:xps:c1:m1.VAL')
beam_stop_y = PV('32idcTXM:xps:c1:m2.VAL')

# Condenser
condenser_x = PV('32idcTXM:xps:c0:m7.VAL')
condenser_y = PV('32idcTXM:mxv:c1:m1.VAL')
condenser_z = PV('32idcTXM:mxv:c0:m1.VAL')
condenser_yaw = PV('32idcTXM:xps:c0:m8.VAL')
condenser_pitch = PV('32idcTXM:mxv:c1:m2.VAL')
condenser_shaker_x = PV('32idcTXM:jena1:2:VAL')
condenser_shaker_y = PV('32idcTXM:jena1:1:VAL')
condenser_shaker_z = PV('32idcTXM:jena1:0:VAL')

# Pin Hole
pin_hole_x = PV('32idcTXM:xps:c1:m3.VAL')
pin_hole_y = PV('32idcTXM:xps:c1:m4.VAL')
pin_hole_z = PV('32idcTXM:xps:c1:m5.VAL')

# Sample
sample_top_x = PV('32idcTXM:mmc:c0:m1.VAL')
sample_top_z = PV('32idcTXM:mmc:c0:m2.VAL')
sample_rotary = PV('32idcTXM:hydra:c0:m1.VAL')
sample_x = PV('32idcTXM:xps:c1:m8.VAL')
sample_y = PV('32idcTXM:xps:c1:m7.VAL')

# Zone Plate
zone_plate_x = PV('32idcTXM:xps:c0:m4.VAL')
zone_plate_y = PV('32idcTXM:xps:c0:m5.VAL')
zone_plate_z = PV('32idcTXM:xps:c0:m6.VAL')

# Phase Ring
phase_ring_x = PV('32idcTXM:xps:c0:m1.VAL')
phase_ring_y = PV('32idcTXM:xps:c0:m2.VAL')
phase_ring_z = PV('32idcTXM:xps:c0:m3.VAL')

# Bertrand Lens
bertrand_lens_x = PV('32idcTXM:tau:c0:m2.VAL')
bertrand_lens_y = PV('32idcTXM:tau:c0:m3.VAL')
bertrand_lens_z = PV('32idcTXM:tau:c0:m1.VAL')

# CCD camera
ccd_camera_objective = PV('32idcTXM:xps:c2:m2.VAL')
ccd_camera_objective_set = PV('32idcTXM:xps:c2:m2.SET')
ccd_camera_x = PV('32idcTXM:mxv:c1:m3.VAL')
ccd_camera_x_set = PV('32idcTXM:mxv:c1:m3.SET')
ccd_camera_y = PV('32idcTXM:mxv:c1:m4.VAL')
ccd_camera_y_set = PV('32idcTXM:mxv:c1:m4.SET')
ccd_camera_z = PV('32idcTXM:mxv:c0:m2.VAL')
ccd_camera_z_set = PV('32idcTXM:mxv:c0:m2.SET')
# focus motor not working uder epics yet
# for test purposes I am using the pin_hole_x PV
ccd_focus = PV('32idcTXM:xps:c1:m3.VAL')

ccd_trigger = PV('TXMNeo1:cam1:Acquire')
ccd_dwell_time = PV('TXMNeo1:cam1:AcquireTime')
ccd_acquire_mode = PV('TXMNeo1:cam1:ImageMode')
ccd_image = PV('TXMNeo1:image1:ArrayData')
ccd_image_rows = PV('TXMNeo1:cam1:SizeY')
ccd_image_columns = PV('TXMNeo1:cam1:SizeX')

# DCM
pzt_sec_crystal = PV('32idb:pzt1_arcsec.VAL')
ion_chamber_DCM = PV('32idc01:scaler1.S2')