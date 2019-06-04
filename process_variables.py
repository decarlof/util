# -*- coding: utf-8 -*-
"""
Transmission X-ray Microscope process variables grouped by component

"""

from epics import PV

# Beamline Status
current = PV('S:SRcurrentAI')
undulator_energy = PV('ID32ds:Energy.VAL')
undulator_gap = PV('ID32ds:Gap.VAL')
energy_dcm = PV('32ida:BraggEAO.VAL')
mirror_x  = PV('32idbMIR:m1.RBV')
mirror_y  = PV('32idbMIR:m2.RBV')

# Beam Monitor
beam_monitor_x = PV('32idcTXM:xps:c2:m1.VAL')
beam_monitor_x_set = PV('32idcTXM:xps:c2:m1.SET')
beam_monitor_y = PV('32idcTXM:nf:c0:m3.VAL')
beam_monitor_y_set = PV('32idcTXM:nf:c0:m3.SET')

# Filter
filter_x = PV('32idcTXM:xps:c2:m1.VAL')

# Diffuser
diffuser_x = PV('32idcTXM:xps:c1:m2.VAL')
diffuser_x_set = PV('32idcTXM:xps:c1:m2.SET')

# Beam Stop
beam_stop_x = PV('32idcTXM:mcs:c2:m1.VAL')
beam_stop_y = PV('32idcTXM:mcs:c3:m6.VAL')

# Condenser
condenser_x = PV('32idcTXM:mcs:c3:m1.VAL')
condenser_x_set = PV('32idcTXM:mcs:c3:m1.SET')
condenser_y = PV('32idcTXM:mcs:c3:m5.VAL')
condenser_y_set = PV('32idcTXM:mcs:c3:m5.SET')
condenser_z = PV('32idcTXM:mxv:c1:m5.VAL')
condenser_z_set = PV('32idcTXM:mxv:c1:m5.SET')
condenser_yaw = PV('32idcTXM:mcs:c3:m2.VAL')
condenser_pitch = PV('32idcTXM:mcs3:m4.VAL')
condenser_shaker_x = PV('32idcTXM:jena1:2:VAL')
condenser_shaker_y = PV('32idcTXM:jena1:1:VAL')
condenser_shaker_z = PV('32idcTXM:jena1:0:VAL')

# Pin Hole
pin_hole_x = PV('32idcTXM:xps:c1:m3.VAL')
pin_hole_x_set = PV('32idcTXM:xps:c1:m3.SET')
pin_hole_y = PV('32idcTXM:xps:c1:m5.VAL')
pin_hole_y_set = PV('32idcTXM:xps:c1:m5.SET')

# Sample
sample_top_x = PV('32idcTXM:mcs:c1:m2.VAL')
sample_top_z = PV('32idcTXM:mcs:c1:m1.VAL')
sample_rotary = PV('32idcTXM:hydra:c0:m1.VAL')
sample_rotary_home = PV('32idcTXM:hydra:c0:m1.HOMF')
sample_rotary_speed = PV('32idcTXM:hydra:c0:m1.VELO')
#sample_x = PV('32idcTXM:xps:c1:m8.VAL')
sample_y = PV('32idcTXM:mxv:c1:m1.VAL')

# Zone Plate
zone_plate_x = PV('32idcTXM:mcs:c2:m1.VAL')
zone_plate_y = PV('32idcTXM:mcs:c2:m2.VAL')
zone_plate_z = PV('32idcTXM:mcs:c2:m3.VAL')
# MST2 = vertical axis
Smaract_mode = PV('32idcTXM:mcsAsyn1.AOUT') # pv.Smaract_mode.put(':MST3,100,500,100')
zone_plate_2_x = PV('32idcTXM:mcs:c0:m3.VAL')
zone_plate_2_y = PV('32idcTXM:mcs:c0:m1.VAL')
zone_plate_2_z = PV('32idcTXM:mcs:c2:m3.VAL')

# Phase Ring
phase_ring_x = PV('32idc02:m33.VAL')
phase_ring_y = PV('32idc02:m34.VAL')
phase_ring_z = PV('32idc02:m35.VAL')

# Bertrand Lens
bertrand_lens_x = PV('32idcTXM:nf:c0:m4.VAL')
bertrand_lens_y = PV('32idcTXM:nf:c0:m5.VAL')
bertrand_lens_z = PV('32idcTXM:mxv:c1:m7.VAL')

# CCD camera
ccd_camera_objective = PV('32idcTXM:xps:c2:m2.VAL')
ccd_camera_objective_set = PV('32idcTXM:xps:c2:m2.SET')
ccd_camera_x = PV('32idcTXM:mxv:c1:m3.VAL')
ccd_camera_x_set = PV('32idcTXM:mxv:c1:m3.SET')
ccd_camera_y = PV('32idcTXM:mxv:c1:m4.VAL')
ccd_camera_y_set = PV('32idcTXM:mxv:c1:m4.SET')
ccd_camera_z = PV('32idcTXM:mxv:c0:m6.VAL')
ccd_camera_z_set = PV('32idcTXM:mxv:c0:m6.SET')
# focus motor not working uder epics yet
# for test purposes I am using the pin_hole_x PV
ccd_focus = PV('32idcTXM:xps:c1:m3.VAL')

if 1:
    # CCD Point Grey
    ccd_trigger = PV('32idcPG3:cam1:Acquire')
    ccd_acquire_period = PV('32idcPG3:cam1:AcquirePeriod')
    ccd_trigger_mode = PV('32idcPG3:cam1:TriggerMode')
    ccd_frame_rate_enable = PV('32idcPG3:cam1:FrameRateOnOff')
    ccd_detector_state = PV('32idcPG3:cam1:DetectorState_RBV')
    ccd_dwell_time = PV('32idcPG3:cam1:AcquireTime')
    ccd_acquire_mode = PV('32idcPG3:cam1:ImageMode')
    ccd_image = PV('32idcPG3:image1:ArrayData')
    ccd_image_rows = PV('32idcPG3:cam1:SizeY')        # checked
    ccd_image_columns = PV('32idcPG3:cam1:SizeX')     # checked
    ccd_FF_norm = PV('32idcPG3:Proc1:EnableFlatField')
    ccd_Recursive_Filter = PV('32idcPG3:Proc1:EnableFilter')
    ccd_Proc1_port = PV('32idcPG3:Proc1:NDArrayPort')
    ccd_Image1_port = PV('32idcPG3:Image1:NDArrayPort')
    ccd_OverLay_port = PV('32idcPG3:Over1:NDArrayPort')
    ccd_Trans_port = PV('32idcPG3:Trans1:NDArrayPort')

if 0:
    ccd_trigger = PV('TXMNeo1:cam1:Acquire')
    ccd_dwell_time = PV('TXMNeo1:cam1:AcquireTime')
    ccd_acquire_period = PV('TXMNeo1:cam1:AcquirePeriod')
    ccd_detector_state = PV('TXMNeo1:cam1:DetectorState_RBV')
    ccd_acquire_mode = PV('TXMNeo1:cam1:ImageMode')
    ccd_image = PV('TXMNeo1:image1:ArrayData')
    ccd_image_rows = PV('TXMNeo1:cam1:ArraySizeY_RBV')
    ccd_image_columns = PV('TXMNeo1:cam1:ArraySizeX_RBV')
    ccd_binning = PV('TXMNeo1:cam1:A3Binning') # states from 0 to 4
    ccd_EnableCallbacks = PV('TXMNeo1:Proc1:EnableCallbacks') # (for background corrections) states: 0 or 1 
    ccd_EnableFlatField = PV('TXMNeo1:Proc1:EnableFlatField') # states: 0 or 1
    ccd_SaveFlatField = PV('TXMNeo1:Proc1:SaveFlatField')
    ccd_Image_number = PV('TXMNeo1:cam1:NumImages')

if 0:
    # CCD Manta
    ccd_trigger = PV('TXMMan1:cam1:Acquire')
    ccd_detector_state = PV('TXMMan1:cam1:DetectorState_RBV')
    ccd_dwell_time = PV('TXMMan1:cam1:AcquireTime')
    ccd_acquire_mode = PV('TXMMan1:cam1:ImageMode')
    ccd_image = PV('TXMMan1:image1:ArrayData')
    ccd_image_rows = PV('TXMMan1:cam1:SizeY')
    ccd_image_columns = PV('TXMMan1:cam1:SizeX')

if 0:
    # CCD Procilica
    ccd_trigger = PV('TXMPro1:cam1:Acquire')
    ccd_detector_state = PV('TXMPro1:cam1:DetectorState_RBV')
    ccd_dwell_time = PV('TXMPro1:cam1:AcquireTime')
    ccd_acquire_mode = PV('TXMPro1:cam1:ImageMode')
    ccd_image = PV('TXMPro1:image1:ArrayData')
    ccd_image_rows = PV('TXMPro1:cam1:ArraySizeY_RBV')
    ccd_image_columns = PV('TXMPro1:cam1:ArraySizeX_RBV')

# DCM
pzt_sec_crystal = PV('32idb:pzt1_arcsec.VAL')
DCM_mvt_status = PV('32ida:KohzuModeBO.VAL')

# Feedback loops:
BPM_DCM_Vert_FBL = PV('32ida:fb3.FBON') # 0=off, 1=ON
BPM_DCM_Horiz_FBL = PV('32ida:fb4.FBON') # 0=off, 1=ON

# Shutters
open_shutter_B = PV('32idb:rshtrB:Open.PROC')
close_shutter_B = PV('32idb:rshtrB:Close.PROC')
fast_shutter = PV('32idcTXM:uniblitz:control')

# Ion Chamber
ion_chamber_DCM = PV('32idc01:scaler1_cts1.B') #  upstream
ion_chamber_down = PV('32idc01:scaler1_cts1.C') #  downstream
ion_chamber_trigger = PV('32idc01:scaler1.CNT')
ion_chamber_auto = PV('32idc01:scaler1.CONT')
ion_chamber_dwelltime = PV('32idc01:scaler1.TP')
ion_chamber_autodwelltime = PV('32idc01:scaler1.TP1')
diode = PV('32idc01:scaler1.S2')

# CRL:
#crl_actuators = PV('32idb:pfcu:sendCommand.VAL')
crl_actuators_0 = PV('32idbPLC:oY0')
crl_actuators_1 = PV('32idbPLC:oY1')
crl_actuators_2 = PV('32idbPLC:oY2')
crl_actuators_3 = PV('32idbPLC:oY3')
crl_actuators_4 = PV('32idbPLC:oY4')
crl_actuators_5 = PV('32idbPLC:oY5')
crl_actuators_6 = PV('32idbPLC:oY6')
crl_actuators_7 = PV('32idbPLC:oY7')

# Energy scans
gap_en = PV('32id:ID32us_energy')
#gap_en = PV('ID32us:Energy')
gap_motor_pos = PV('ID32us:Gap.VAL')
DCM_en = PV('32ida:BraggEAO.VAL')
Brag_motor_pos = PV('32ida:KohzuThetaRdbkAI')

# Temporary PV for the DBPM test:
BPM_vert_readback = PV('32ida:fb3.VAL')
BPM_horiz_readback = PV('32ida:fb4.VAL')
sample_x_bpm = PV('32idc02:m35.VAL')
sample_y_bpm = PV('32idc02:m36.VAL')
DBPM_x = PV('32idc02:m33.VAL')
DBPM_y = PV('32idc02:m34.VAL')
ion_chamber_bpm = PV('32idc01:scaler1.S3')
jena_y = PV('32idcTXM:jena1:2:val')




