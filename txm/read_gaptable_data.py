import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# col1: gap energy, col2: gap pos, col3: DCM energy scan, col4: DCM position, col5: intensity
data = np.load('gap_table_data.npy')
Display = 1
#-----------------------------------


nEn = np.size(data[0,0,:])
En_gap = data[0,0,:]

gap_table = np.zeros((nEn, 2)) # col1= gap_pos and col2= DCM energy at max intensity

# Find the maxima for each En_gap:
for iEn in range(0, nEn):
    vect_int = np.squeeze(data[:,4,iEn])
    index_max = np.where(vect_int==max(vect_int))
    gap_pos_opt = data[index_max, 1, iEn]
#    DCM_pos_opt = data[index_max, 3, iEn]
    DCM_en_pos_opt = data[index_max, 2, iEn]
    gap_table[iEn,:] = [gap_pos_opt, DCM_en_pos_opt]

def gap_en(En, table):
    f = interpolate.interp1d(table[:,1], table[:,0], kind='cubic')
    gap_pos_interp = f(En)
    return gap_pos_interp

if Display:
    # DCM scans display:
    cpt=-1
    plt.figure 
    plt.subplot(1,2,1)
    for iEn in range(0, nEn):
        cpt=cpt+1
        plt.hold(True), plt.plot(np.squeeze(data[:,2,iEn]), np.squeeze(data[:,4,iEn]), 'r-')
        plt.xlabel('En (keV)'), plt.ylabel('I0')
    plt.grid()

    # print the gap_table
    # Interpolate the rocking curve over 50 points
    f = interpolate.interp1d(gap_table[:,1], gap_table[:,0], kind='cubic')
    scan_val_interp = np.linspace(gap_table[0,1], gap_table[-1,1], 50)
    intensity_interp = f(scan_val_interp)

    plt.subplot(1,2,2)
    plt.plot(gap_table[:,1], gap_table[:,0], 'r*')
    plt.plot(scan_val_interp, intensity_interp, 'r-')
#    plt.xlabel('gap position'), plt.ylabel('DCM (theta)')
    plt.ylabel('gap position'), plt.xlabel('Energy (keV)')
    plt.grid()

    plt.show()


# Get the gap for a given energy:
#f2 = interpolate.interp1d(gap_table[:,1], gap_table[:,0], kind='cubic')



#fig, ax1 = plt.subplots()
#
#ax2 = ax1.twinx()
#ax1.plot(x, y1, 'g-')
#ax2.plot(x, y2, 'b-')
#
#ax1.set_xlabel('X data')
#ax1.set_ylabel('Y1 data', color='g')
#ax2.set_ylabel('Y2 data', color='b')


