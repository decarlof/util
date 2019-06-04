# -*- coding: utf-8 -*-
'''
Transmission X-ray Microscope process variables grouped by component

'''

pv = dict()

# Beam Monitor
pv['beam_monitor_x'] = '32idcTXM:nf:c0:m1.VAL'
pv['beam_monitor_x_set'] = '32idcTXM:nf:c0:m1.SET'
pv['beam_monitor_y'] = '32idcTXM:nf:c0:m2.VAL'
pv['beam_monitor_y_set'] = '32idcTXM:nf:c0:m2.SET'

# Filter
pv['filter_x'] = '32idcTXM:xps:c2:m1.VAL'

# Beam Stop
pv['beam_stop_x'] = '32idcTXM:xps:c1:m1.VAL'
pv['beam_stop_y'] = '32idcTXM:xps:c1:m2.VAL'

# Condenser
pv['condenser_x'] = '32idcTXM:xps:c0:m7.VAL'
pv['condenser_x_set'] = '32idcTXM:xps:c0:m7.SET'
pv['condenser_y'] = '32idcTXM:mxv:c1:m1.VAL'
pv['condenser_y_set'] = '32idcTXM:mxv:c1:m1.SET'
#pv['condenser_z'] = '32idcTXM:mxv:c0:m1.VAL'
#pv['condenser_z_set'] = '32idcTXM:mxv:c0:m1.SET'
pv['condenser_z'] = '32idcTXM:mxv:c1:m5.VAL'
pv['condenser_z_set'] = '32idcTXM:mxv:c1:m5.SET'
pv['condenser_yaw'] = '32idcTXM:xps:c0:m8.VAL'
pv['condenser_pitch'] = '32idcTXM:mxv:c1:m2.VAL'
pv['condenser_shaker_x'] = '32idcTXM:jena1:2:VAL'
pv['condenser_shaker_y'] = '32idcTXM:jena1:1:VAL'
pv['condenser_shaker_z'] = '32idcTXM:jena1:0:VAL'

# Pin Hole
pv['pin_hole_x'] = '32idcTXM:xps:c1:m3.VAL'
pv['pin_hole_x_set'] = '32idcTXM:xps:c1:m3.SET'
pv['pin_hole_y'] = '32idcTXM:xps:c1:m4.VAL'
pv['pin_hole_y_set'] = '32idcTXM:xps:c1:m4.SET'
pv['pin_hole_z'] = '32idcTXM:xps:c1:m5.VAL'
pv['pin_hole_z_set'] = '32idcTXM:xps:c1:m5.SET'

# Sample
pv['sample_top_x'] = '32idcTXM:mmc:c0:m1.VAL'
pv['sample_top_z'] = '32idcTXM:mmc:c0:m2.VAL'
pv['sample_rotary'] = '32idcTXM:hydra:c0:m1.VAL'
pv['sample_x'] = '32idcTXM:xps:c1:m8.VAL'
pv['sample_y'] = '32idcTXM:xps:c1:m7.VAL'

# Zone Plate
pv['zone_plate_x'] = '32idcTXM:xps:c0:m4.VAL'
pv['zone_plate_y'] = '32idcTXM:xps:c0:m5.VAL'
pv['zone_plate_z'] = '32idcTXM:xps:c0:m6.VAL'

# Phase Ring
pv['phase_ring_x'] = '32idcTXM:xps:c0:m1.VAL'
pv['phase_ring_y'] = '32idcTXM:xps:c0:m2.VAL'
pv['phase_ring_z'] = '32idcTXM:xps:c0:m3.VAL'

# Bertrand Lens
pv['bertrand_lens_x'] = '32idcTXM:tau:c0:m2.VAL'
pv['bertrand_lens_y'] = '32idcTXM:tau:c0:m3.VAL'
pv['bertrand_lens_z'] = '32idcTXM:tau:c0:m1.VAL'

# CCD camera
pv['ccd_camera_objective'] = '32idcTXM:xps:c2:m2.VAL'
pv['ccd_camera_objective_set'] = '32idcTXM:xps:c2:m2.SET'
pv['ccd_camera_x'] = '32idcTXM:mxv:c1:m3.VAL'
pv['ccd_camera_x_set'] = '32idcTXM:mxv:c1:m3.SET'
pv['ccd_camera_y'] = '32idcTXM:mxv:c1:m4.VAL'
pv['ccd_camera_y_set'] = '32idcTXM:mxv:c1:m4.SET'
pv['ccd_camera_z'] = '32idcTXM:mxv:c0:m6.VAL'
pv['ccd_camera_z_set'] = '32idcTXM:mxv:c0:m6.SET'
# focus motor not working uder epics yet
# 'for test purposes I am using the pin_hole_x PV
pv['ccd_focus'] = '32idcTXM:xps:c1:m3.VAL'

if 1:
    pv['ccd_trigger'] = 'TXMNeo1:cam1:Acquire'
    pv['ccd_dwell_time'] = 'TXMNeo1:cam1:AcquireTime'
    pv['ccd_acquire_mode'] = 'TXMNeo1:cam1:ImageMode'
    pv['ccd_image'] = 'TXMNeo1:image1:ArrayData'
    #pv['ccd_image_rows'] = 'TXMNeo1:cam1:SizeY'
    #pv['ccd_image_columns'] = 'TXMNeo1:cam1:SizeX'
    pv['ccd_image_rows'] = 'TXMNeo1:cam1:ArraySizeY_RBV'
    pv['ccd_image_columns'] = 'TXMNeo1:cam1:ArraySizeX_RBV'
    pv['ccd_binning'] = 'TXMNeo1:cam1:A3Binning' # states from 0 to 4
    pv['ccd_EnableCallbacks'] = 'TXMNeo1:Proc1:EnableCallbacks' # (for background corrections) states: 0 or 1 
    pv['ccd_EnableFlatField'] = 'TXMNeo1:Proc1:EnableFlatField' # states: 0 or 1
    pv['ccd_SaveFlatField'] = 'TXMNeo1:Proc1:SaveFlatField'
    pv['ccd_Image_number'] = 'TXMNeo1:cam1:NumImages'

if 0:
    # CCD Manta
    pv['ccd_trigger'] = 'TXMMan1:cam1:Acquire'
    pv['ccd_dwell_time'] = 'TXMMan1:cam1:AcquireTime'
    pv['ccd_acquire_mode'] = 'TXMMan1:cam1:ImageMode'
    pv['ccd_image'] = 'TXMMan1:image1:ArrayData'
    pv['ccd_image_rows'] = 'TXMMan1:cam1:SizeY'
    pv['ccd_image_columns'] = 'TXMMan1:cam1:SizeX'

# DCM
pv['pzt_sec_crystal'] = '32idb:pzt1_arcsec.VAL'
pv['ion_chamber_DCM'] = '32idc01:scaler1.S2'
pv['ion_chamber_trigger'] = '32idc01:scaler1.CNT'
pv['ion_chamber_auto'] = '32idc01:scaler1.CONT'
pv['ion_chamber_dwelltime'] = '32idc01:scaler1.TP'
pv['ion_chamber_autodwelltime'] = '32idc01:scaler1.TP1'

# Temporary PV for the DBPM test:
pv['sample_x_bpm'] = '32idc02:m35.VAL'
pv['sample_y_bpm'] = '32idc02:m36.VAL'
pv['DBPM_x'] = '32idc02:m33.VAL'
pv['DBPM_y'] = '32idc02:m34.VAL'
pv['ion_chamber_bpm'] = '32idc01:scaler1.S3'
pv['jena_y'] = '32idcTXM:jena1:2:val'


