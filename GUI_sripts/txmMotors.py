#from epics import caput
'''
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
#print 'txmMotors parent dir = ',parentdir
'''
###### Beam Stop
def Beam_Stop_In():
    caput('32idcTXM:xps:c1:m1.VAL', 0) # beam stop X

def Beam_Stop_Out():
    caput('32idcTXM:xps:c1:m1.VAL', 8) # beam stop X

###### Condenser
def Condenser_In():
    #import process_variables as pv
    #pv.condenser_x.put(0, wait=False)
    from epics import caput
    caput('32idcTXM:xps:c2:m8.VAL', 0) # condenser X
    del caput

def Condenser_Out():
    #import process_variables as pv
    #pv.condenser_x.put(10, wait=False)
    from epics import caput
    caput('32idcTXM:xps:c2:m8.VAL', 10) # condenser X
    del caput

#def Condenser_Auto():
#    ca.put(

###### Pinhole
def Pinhole_In():
    caput('32idcTXM:xps:c1:m3.VAL', 0) # Pinhole X

def Pinhole_Out():
    caput('32idcTXM:xps:c1:m3.VAL', 8) # Pinhole X

###### Zone plate
def Zone_Plate_In():
    caput('32idcTXM:mcs:c0:m2.VAL', 0) # Zone plate X

def Zone_Plate_Out():
    caput('32idcTXM:mcs:c0:m2.VAL', 14) # Zone plate X




