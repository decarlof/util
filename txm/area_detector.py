import matplotlib.pyplot as plt
import Image
import numpy as np

from epics import caget, caput

def ccdtake(dwelltime=0.2, colormap="gray", limits = (None, None), ff = None, df = None, camera = None):
#
#   script: ccdtake(dwelltime, colormap, limits, ff)
#   By default dwell time = 0.2 s, colormap = jet and limits are min & max, no flat field correction


    if camera == None:
            PV_Prefix = 'TXMNeo1:'
    PV_dwelltime = PV_Prefix + 'cam1:AcquireTime'
    PV_trigger = PV_Prefix + 'cam1:Acquire'
    PV_image = PV_Prefix + 'image1:ArrayData'
    PV_nCol_CCD = PV_Prefix + 'cam1:SizeX'
    PV_nRow_CCD = PV_Prefix + 'cam1:SizeY'

    nCol = caget(PV_nCol_CCD)
    nRow = caget(PV_nRow_CCD)

    image_size = nRow * nCol

    caput(PV_dwelltime, dwelltime, wait=True, timeout=100)		# set exposure time
    caput(PV_trigger, 1, timeout=100, wait=True)		        # trigger the CCD

    Img_vect = caget(PV_image)
    Img_vect = Img_vect[0:image_size]
    Img = np.reshape(Img_vect,[nRow, nCol])

    # Flat field correction
    if df!=None:
        Img = np.subtract(Img, df)
        if ff !=None:
                ff = np.subtract(ff, df)
                
    if ff!=None:
        Img = -np.log(np.divide(Img, ff, dtype = float))
        

    plt.imshow(Img), plt.set_cmap(colormap), plt.colorbar()

    if limits!=(None, None): plt.clim(*limits)

    plt.show()

    return Img

def ccdsave():
	# PV declaration:
	PV_ThePath = 'TXMNeo1:cam1:TIF:FilePath'
	PV_prefix = 'TXMNeo1:cam1:TIF:FileName' 
	PV_radio_index = 'TXMNeo1:cam1:TIF:FileNumber'
	PV_save = 'TXMNeo1:cam1:TIF:WriteFile'

	caput(PV_save, 1, wait=True, timeout=500);
	ThePath = caget(PV_ThePath, datatype=DBR_CHAR_STR)
	Prefix = caget(PV_prefix, datatype=DBR_CHAR_STR)
	Index = caget(PV_radio_index)
	
	print  Prefix,'_',Index,'.tiff saved in folder:',ThePath


def image_sav(Img, FileName, Path=None):
#
#	script: image_sav(Img, FileName, Path=None):
	im=Image.fromarray(Img)
	if Path!=None:
		Current_Path = os.getcwd()
		os.chdir(Path)

	im.save(FileName)		
	
	if Path!=None:
		os.chdir(Current_Path)
