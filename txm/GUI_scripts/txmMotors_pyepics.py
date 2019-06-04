# include parent directory for imports
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import process_variables as pv
import time


#wait on a pv to be a value until max_timeout (default forever)
def wait_pv(pv, wait_val, max_timeout_sec=-1):
    print 'wait_pv(', pv.pvname, wait_val, max_timeout_sec, ')'
    #delay for pv to change
    time.sleep(.01)
    startTime = time.time()
    while(True):
        pv_val = pv.get()
        if (pv_val != wait_val):
            if max_timeout_sec > -1:
                curTime = time.time()
                diffTime = curTime - startTime
                if diffTime >= max_timeout_sec:
                    return False
            time.sleep(.01)
        else:
            return True
            
###### rotary stage

###### Beam Stop
def Beam_Stop_In():
    pv.beam_stop_y.put(0)

def Beam_Stop_Out():
#    pv.beam_stop_x.put(11) # 350 um BS
#    pv.beam_stop_x.put(17) # 500 um BS
    pv.beam_stop_y.put(5)

###### Condenser
def Condenser_In():
# Zeiss condenser:
    pv.condenser_x.put(0)
    pv.condenser_y.put(0)
## Sigray condenser:
#    pv.condenser_x.put(-10.024000)
#    pv.condenser_y.put(-0.546800)
## BSCcondenser:
#    pv.condenser_x.put(-4.76)
#    pv.condenser_y.put(4.19)

def Condenser_Out():
#	pass
#    pv.condenser_y.put(9)       # condenser X BSC 60 nm
#    pv.condenser_y.put(10.0)       # 1.7 mrad moncapillary
#    pv.condenser_y.put(9)       # Sigray condenser
    pv.condenser_y.put(10)       # High Energy BSC

###### Pinhole
def Pinhole_In():
#    pv.pin_hole_x.put(0)
    pv.pin_hole_y.put(0)

def Pinhole_Out():
    pv.pin_hole_y.put(5)

###### Zone plate
def Zone_Plate_In():
## 50 nm ZP:
#    pv.zone_plate_x.put(3.915300)
#    pv.zone_plate_y.put(-0.085000)
#    pv.zone_plate_x.put(4.060300) # 17 kev
#    pv.zone_plate_y.put(-0.085000) # 17keV
#    pv.zone_plate_x.put(4.080300) # 18 kev
#    pv.zone_plate_y.put(-0.085000) # 18keV
# 60 nm ZP:
#    pv.zone_plate_x.put(-7.5)
#    pv.zone_plate_y.put(0.055)
# 16 nm ZP:
#    pv.zone_plate_x.put(-3.684300)
    pv.zone_plate_y.put(0.0000)
# 40 nm ZP:
#    pv.zone_plate_x.put(0)
#    pv.zone_plate_y.put(0)

    pass

def Zone_Plate_Out():
## 50 nm ZP:
#    pv.zone_plate_x.put(0.0)
#    pv.zone_plate_y.put(5.0)
# 60 nm ZP:
#    pv.zone_plate_x.put(-7.5)
#    pv.zone_plate_y.put(5.0)
# 16 nm ZP:
#    pv.zone_plate_x.put(-3.684300)
    pv.zone_plate_y.put(4.415)
# 100 nm ZP:
#    pv.zone_plate_x.put(3.6)
#    pv.zone_plate_y.put(0.0)
## 40 nm ZP:
#    pv.zone_plate_x.put()
#    pv.zone_plate_y.put()

    pass

###### Zone plate 2
#def Zone_Plate_2_In():
#    pv.zone_plate_2_y.put(0)
#    pv.zone_plate_2_x.put(0)
#
#def Zone_Plate_2_Out():
#    pv.zone_plate_2_y.put(0)
#    pv.zone_plate_2_x.put(4.5)

###### diffuser:
def Diffuser_In():
#    pv.diffuser_x.put(-6.2)
    pv.diffuser_x.put(0) # nylon diffuser
#    pv.diffuser_x.put(10.5) # carbon diffuser

def Diffuser_Out():
    pv.diffuser_x.put(7)

###### filter:
# thion filter, pos = 3
#def Filter_In():
#    pv.filter_x.put(0)

#def Filter_Out():
#    pv.filter_x.put(-7)

###### CRL's:
def crl_out():
#    pv.crl_actuators.put('R1', wait=True, timeout=1)
#    pv.crl_actuators.put('R2', wait=True, timeout=1)
#    pv.crl_actuators.put('R3', wait=True, timeout=1)
#    pv.crl_actuators.put('R4', wait=True, timeout=1)
    pv.crl_actuators_0.put(0, wait=True, timeout=1)
    pv.crl_actuators_1.put(0, wait=True, timeout=1)
    pv.crl_actuators_2.put(0, wait=True, timeout=1)
    pv.crl_actuators_3.put(0, wait=True, timeout=1)
    pv.crl_actuators_4.put(0, wait=True, timeout=1)
    pv.crl_actuators_5.put(0, wait=True, timeout=1)
    pv.crl_actuators_6.put(0, wait=True, timeout=1)
    pv.crl_actuators_7.put(0, wait=True, timeout=1)


def crl_in():
#    pv.crl_actuators.put('I1', wait=True, timeout=1)
#    pv.crl_actuators.put('I2', wait=True, timeout=1)
#    pv.crl_actuators.put('I3', wait=True, timeout=1)
#    #pv.crl_actuators.put('I4', wait=True, timeout=1)

    pv.crl_actuators_0.put(1, wait=True, timeout=1)
    pv.crl_actuators_1.put(1, wait=True, timeout=1)
#    pv.crl_actuators_2.put(1, wait=True, timeout=1)
#    pv.crl_actuators_3.put(1, wait=True, timeout=1)
    pv.crl_actuators_4.put(1, wait=True, timeout=1)
#    pv.crl_actuators_5.put(1, wait=True, timeout=1)
#    pv.crl_actuators_6.put(1, wait=True, timeout=1)
#    pv.crl_actuators_7.put(1, wait=True, timeout=1)


def change_ccd_exposure_in():
    exposure = 1
    pv.ccd_trigger.put(0, wait=True)
    time.sleep(0.5)
    pv.ccd_frame_rate_enable.put(0, wait=True, timeout=1) # turn off
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=1)
    time.sleep(0.5)
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=1) # Do it twice to force the acqu period without going back to frame_rate_enable on
    #pv.ccd_acquire_period.put(exposure, wait=True, timeout=1)

    pv.ccd_acquire_mode.put(2, wait=True, timeout=1) 
    time.sleep(1)
    pv.ccd_trigger.put(1, wait=True, timeout=1)
    time.sleep(1.5)

def change_ccd_exposure_out():
    exposure = 0.005
    acquire_period = 0.2
    pv.ccd_trigger.put(0, wait=True)
    pv.ccd_frame_rate_enable.put(1, wait=True)
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=1)
    pv.ccd_acquire_period.put(acquire_period, wait=True, timeout=1)
    pv.ccd_acquire_mode.put(2, wait=True, timeout=1) 
    time.sleep(2)
    pv.ccd_trigger.put(1, wait=True, timeout=1)

def change_rot_speed():
    pv.sample_rotary_speed.put(20)
    

#############################
#############################
def All_In():
#    pv.BPM_vert_readback.put(-3.3) # @ 9 keV
#    pv.BPM_horiz_readback.put(1.8) # @ 9 keV

    if 1: # if 1: if CRL needed, if 0: if CRL not needed
#        pv.BPM_vert_readback.put(-4.0) # @ 7 keV
#        pv.BPM_horiz_readback.put(4.0) # @ 7 keV
#        pv.BPM_vert_readback.put(-2.0) # @ 7.3 keV
#        pv.BPM_horiz_readback.put(4.7) # @ 7.3 keV
        pv.BPM_vert_readback.put(0.0) # @ 8 keV
        pv.BPM_horiz_readback.put(4.7) # @ 8 keV
#        pv.BPM_vert_readback.put(-3.50) # @ 8.4 keV
#        pv.BPM_horiz_readback.put(3.0) # @ 8.4 keV
#        pv.BPM_vert_readback.put(0.0) # @ 9.0 keV
#        pv.BPM_horiz_readback.put(4.5) # @ 9.0 keV
#        pv.BPM_vert_readback.put(-3.0) # @ 9.1 keV
#        pv.BPM_horiz_readback.put(3.7) # @ 9.1 keV
#        pv.BPM_vert_readback.put(-3.5) # @ 9.7 keV CRL 0,1,4,5
#        pv.BPM_horiz_readback.put(3.0) # @ 9.7 keV
#        pv.BPM_vert_readback.put(-2.0) # @ 11.15 keV CRL 0,1,2,3,4,5
#        pv.BPM_horiz_readback.put(4.0) # @ 11.15 keV
#        pv.BPM_vert_readback.put(-1.5) # @ 16 keV
#        pv.BPM_horiz_readback.put(4.1) # @ 16 keV
#        pv.BPM_vert_readback.put(-4.5) # @ 17 keV
#        pv.BPM_horiz_readback.put(0.6) # @ 17 keV
#        pv.BPM_vert_readback.put(0.0) # @ 18 keV
#        pv.BPM_horiz_readback.put(4.0) # @ 18 keV
        crl_in()

    Beam_Stop_In()
    Condenser_In()
    Pinhole_In()
#    Zone_Plate_In()
    #Zone_Plate_2_In()
    Diffuser_In()
    change_rot_speed()
#    pv.fast_shutter.put(1, wait=True)
    pv.BPM_DCM_Vert_FBL.put(1, wait=True, timeout=1) # Turn ON DCM / BMP vertical feedback
    pv.BPM_DCM_Horiz_FBL.put(1, wait=True, timeout=1) # Turn ON DCM / BMP horizontal feedback

    # CCD management:
    if 1:
        change_ccd_exposure_in()
        pv.ccd_trigger_mode.put(0, wait=True, timeout=1)
        pv.ccd_frame_rate_enable.put(0)
    else:
        pv.ccd_dwell_time.put(1, wait=True, timeout=1)
        pv.ccd_acquire_period.put(1, wait=True, timeout=1)
        
    pv.ccd_FF_norm.put(0, wait=True, timeout=1)
    pv.ccd_Trans_port.put('PROC1')
    pv.ccd_OverLay_port.put('TRANS1')
    pv.ccd_Image1_port.put('OVER1')


def All_Out():
#    pv.BPM_vert_readback.put(1.0) # 7.3 keV
#    pv.BPM_horiz_readback.put(4.7) # 7.3 keV
    pv.BPM_vert_readback.put(1.0) # 8 keV
    pv.BPM_horiz_readback.put(5.5) # 8 keV
#    pv.BPM_vert_readback.put(-1.5) # 8.4 keV
#    pv.BPM_horiz_readback.put(4.5) # 8.4 keV
#    pv.BPM_vert_readback.put(0.5) # 9.0 keV
#    pv.BPM_horiz_readback.put(5.8) # 9.0 keV
#    pv.BPM_vert_readback.put(-1.2) # 9.1 keV
#    pv.BPM_horiz_readback.put(6.5) # 9.1 keV
#    pv.BPM_vert_readback.put(-2.5) # 9.7 keV
#    pv.BPM_horiz_readback.put(1.4) # 9.7 keV
#    pv.BPM_vert_readback.put(-2.0) # 11.150 keV
#    pv.BPM_horiz_readback.put(5.5) # 11.150 keV
#    pv.BPM_vert_readback.put(-3.0) # 16. keV
#    pv.BPM_horiz_readback.put(1.6) # 16 keV
#    pv.BPM_vert_readback.put(-2.5) # 18 keV
#    pv.BPM_horiz_readback.put(1.4) # 18 keV
    pv.ccd_trigger_mode.put(0, wait=True, timeout=1)
    pv.ccd_FF_norm.put(0, wait=True, timeout=1)
    wait_pv(pv.ccd_FF_norm, 0, max_timeout_sec=3)
#    pv.BPM_DCM_Vert_FBL.put(0, wait=True, timeout=1) # Turn OFF DCM / BMP vertical feedback
#    pv.BPM_DCM_Horiz_FBL.put(0, wait=True, timeout=1) # Turn OFF DCM / BMP vertical feedback
    Beam_Stop_Out()
    Condenser_Out()
    Pinhole_Out()
    crl_out()
    change_rot_speed()
#    Zone_Plate_Out()
    #Zone_Plate_2_Out()
    Diffuser_Out()
#    pv.fast_shutter.put(1, wait=True)
    pv.ccd_Recursive_Filter.put(0, wait=True, timeout=1)

    # CCD management:
    if 1:
        change_ccd_exposure_out()
        pv.ccd_trigger_mode.put(0, wait=True, timeout=1)
    else:
        pv.ccd_dwell_time.put(0.005, wait=True, timeout=1)
        pv.ccd_acquire_period.put(0.2, wait=True, timeout=1)

    pv.ccd_FF_norm.put(0, wait=True, timeout=1)
    pv.ccd_Trans_port.put('PROC1')
    pv.ccd_OverLay_port.put('PROC1')
    pv.ccd_Image1_port.put('OVER1')
    time.sleep(1)

#############################
#############################


if __name__ == '__main__':
    eval(sys.argv[1])

