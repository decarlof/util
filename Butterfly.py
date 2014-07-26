


######################### INPUT ##########################
n_cond_zstep = 10
cond_z_start = -2
cond_z_end = 2

# param for knife-edge scan
knife_xstart = -0.25  # sample x
knife_xend = 0.05     # sample x
knife_xstep = 11
knife_acq_time = 0.1
disp = 0 # display each knife edge; will pause the scan!!!
##########################################################


# Record the current sample position:
curr_SpleX_pos = pv.sample_x.get()

# Define the vector containing Motor positions to be scanned:
vect_pos_z = np.linspace(cond_z_start, cond_z_end, n_cond_zstep)

# Define the intensity matrix where intensity values will be stored:
intensities = np.zeros((n_cond_zstep, np.size(vect_pos_x)))
# Define the FWHM vector:
FWHMs = vect_pos_z*0

########### START THE 2D SCAN
print '*** Start the butterfly:'
# Move the Butterfly to the Z starting point
pv.condenser_z.put(vect_pos_z[0], wait=True)
pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug

plt.figure

for iLoop in range(0, n_cond_zstep):
    print '::: Knife edge # %i/%i' % (iLoop+1, np.size(vect_pos_z))
    print '    Motor pos: ',vect_pos_z[iLoop]
    pv.condenser_z.put(vect_pos_z[iLoop], wait=True, timeout=100)

    # Call the knife edge function
    [vect_pos_x_int, intensity, FWHM] = knife_edge(sample_x, knife_xstart, knife_xend, knife_xstep, knife_acq_time, disp)
    intensities[iLoop,:] = intensity
    FWHMs[iLoop] = FWHM

    plt.imshow(img, cmap='jet', extent = [knife_xstart, knife_xend, vect_pos_z[0], vect_pos_z[-1]], aspect="auto")
    plt.xlabel('sample x position'), plt.ylabel('Condenser z pozition'), plt.colorbar()
    if iLoop<n_cond_zstep-1:
        plt.show((block=False))
    else:
        plt.show()

index_waist = np.where(FWHMs==np.min(FWHMs)) # find the index of the butterfly waist
print ' --> Focus @ condenser z posisiton = %.3f ' % vect_pos_z[index_waist]

# Display the map of the Butterfly:
plt.figure
plt.imshow(img, cmap='jet', extent = [knife_xstart, knife_xend, vect_pos_z[0], vect_pos_z[-1]], aspect="auto")
plt.xlabel('sample x position'), plt.ylabel('Condenser z pozition'), plt.colorbar()
plt.show()
