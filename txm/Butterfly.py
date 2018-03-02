


######################### INPUT ##########################
n_cond_zstep = 20
cond_z_start = 1
cond_z_end = 5.8

# param for knife-edge scan
knife_xend = -1.35  # sample x
knife_xstart = -1.15     # sample x
knife_xstep = 25
knife_acq_time = 0.7
disp = 0 # display each knife edge; will pause the scan!!!
##########################################################

# Record the current sample position:
curr_SpleX_pos = pv.sample_x.get()

# Define the vector containing Motor positions to be scanned:
vect_pos_z = np.linspace(cond_z_start, cond_z_end, n_cond_zstep)

# Define the intensity matrix where intensity values will be stored:
intensities = np.zeros((n_cond_zstep, knife_xstep))
# Define the FWHM vector:
FWHMs = vect_pos_z*0

# CCD mode switched to fixed
pv.ccd_acquire_mode.put(0, wait=True, timeout=100)

########### START THE 2D SCAN
print '*** Start the butterfly:'
# Move the Butterfly to the Z starting point
pv.condenser_z.put(vect_pos_z[0], wait=True)
pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug

plt.figure

for iLoop in range(0, n_cond_zstep):
    print '\n ####################################'
    print '::: Knife edge # %i/%i\n' % (iLoop+1, np.size(vect_pos_z))
    print '    Motor pos: ',vect_pos_z[iLoop]
    pv.condenser_z.put(vect_pos_z[iLoop], wait=True, timeout=100)

    # Call the knife edge function
    [vect_pos_x_int, intensity, FWHM] = knife_edge(sample_x, knife_xstart, knife_xend, knife_xstep, knife_acq_time, disp)
    intensities[iLoop,:] = intensity
    FWHMs[iLoop] = FWHM

#    if iLoop<n_cond_zstep-1:
#        plt.show((block=False))
#    else:
#    plt.show()

index_waist = np.where(FWHMs==np.min(FWHMs)) # find the index of the butterfly waist
print ' --> Focus @ condenser z posisiton = %.3f ' % vect_pos_z[index_waist]

# Display the map of the Butterfly:
plt.figure
plt.subplot(1,2,1)
plt.imshow(intensities, cmap='jet', extent = [knife_xstart, knife_xend, vect_pos_z[0], vect_pos_z[-1]], aspect="auto")
plt.xlabel('sample x position'), plt.ylabel('Condenser z pozition'), plt.colorbar()
plt.subplot(1,2,2), plt.plot(vect_pos_z, FWHMs, 'g-'), plt.grid(), plt.show()


