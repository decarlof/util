## gap_table.py
#
# ------------- INPUT ----------------
#gap_st = 8; gap_end = 13; gap_stp = 6
gap_st = 7; gap_end = 8; gap_stp = 1
dcm_range = 0.5; dcm_stp = 50
sleeptime_crystal = 60 # (s) for crystal thermalization
#-------------------------------------

gap_vector = np.linspace(gap_st, gap_end, gap_stp)
#  Intensity array: col1=gap_en, col2=gap pos, col3=DCM_en, col4=bragg position, col5=intensity
intensity_scan = np.zeros((dcm_stp, 5, gap_stp))

cpt_gap = -1
for iGap in gap_vector:
    print '*** Gap energy: %04.4f' % iGap
    cpt_gap = cpt_gap+1
    # move the gap and the DCM to the suitable energy:
    pv.gap_en.put(iGap, wait=True)
    pv.DCM_en.put(iGap, wait=True)
    execfile('rocking_curve.py')

    DCM_vector = np.linspace(iGap-dcm_range/2, iGap+dcm_range/2, dcm_stp)
    cpt_DCM = -1
    intensity_scan[:,0,cpt_gap] = iGap
    intensity_scan[:,1,cpt_gap] = pv.gap_motor_pos.get()

    for iDCM in DCM_vector:
        cpt_DCM = cpt_DCM+1
        pv.DCM_en.put(iDCM, wait=True)            # Move DCM to the wished energy
        Bragg_pos = pv.Brag_motor_pos.get()
        pv.ion_chamber_trigger.put(1, wait=True)  # trigger the ion chamber
        sleep(2)
        intensity_scan[cpt_DCM,2,cpt_gap] = iDCM
        intensity_scan[cpt_DCM,3,cpt_gap] = Bragg_pos
        intensity_scan[cpt_DCM,4,cpt_gap] = pv.ion_chamber_DCM.get()

    plt.plot(np.squeeze(intensity_scan[:,2,cpt_gap]), np.squeeze(intensity_scan[:,4,cpt_gap]), 'r-'), plt.grid()
    plt.xlabel('En (keV)'), plt.ylabel('I0')
    plt.show()

    sleep(sleeptime_crystal) #  for crystal thermalization



np.save('gap_table_data_7keV.npy', intensity_scan)
for i in range(0,gap_stp):
    FileName = 'gap_table_data_7keV_%i.txt' % i
    np.savetxt(FileName, np.squeeze(intensity_scan[:,:,i]), fmt='%4.4f', delimiter='   ', header='col1=gap_en, col2=gap pos, col3=DCM_en, col4=bragg position, col5=intensity')
