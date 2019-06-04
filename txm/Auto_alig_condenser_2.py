


ThePath = '/local/vdeandrade/test_images/'

FileName1 = 'Condenser_1X_Yneg0p001.tif'
FileName2 = 'Condenser_1X_Yneg0p002.tif'
FileName3 = 'Condenser_1X_Yneg0p003.tif'
FileName4 = 'Condenser_1X_Yneg0p004.tif'
FileName5 = 'Condenser_1X_Yneg0p005.tif'
FileName6 = 'Condenser_1X_Yneg0p006.tif'

Thresh = 120
Thresh = 110

img1 = plt.imread(ThePath+FileName1)
img2 = plt.imread(ThePath+FileName2)
img3 = plt.imread(ThePath+FileName3)
img4 = plt.imread(ThePath+FileName4)
img5 = plt.imread(ThePath+FileName5)
img6 = plt.imread(ThePath+FileName6)


med1_1 = np.median(img1[np.where(img1>1000)]

if 0:
    img1[np.where(img1<Thresh)]=0
    img2[np.where(img2<Thresh)]=0
    img3[np.where(img3<Thresh)]=0
    img4[np.where(img4<Thresh)]=0
    img5[np.where(img5<Thresh)]=0
    img6[np.where(img6<Thresh)]=0

    # Gravity center:
    center1 = ndimage.measurements.center_of_mass(img1)
    center2 = ndimage.measurements.center_of_mass(img2)
    center3 = ndimage.measurements.center_of_mass(img3)
    center4 = ndimage.measurements.center_of_mass(img4)
    center5 = ndimage.measurements.center_of_mass(img5)
    center6 = ndimage.measurements.center_of_mass(img6)

    print np.round(center1)
    print np.round(center2)
    print np.round(center3)
    print np.round(center4)
    print np.round(center5)
    print np.round(center6)

    plt.figure
    plt.subplot(2,3,1), plt.imshow(img1, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center1[1],center1[0], 'w+',markersize=10)
    plt.subplot(2,3,2), plt.imshow(img2, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center2[1],center2[0], 'w+',markersize=10)
    plt.subplot(2,3,3), plt.imshow(img3, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center3[1],center3[0], 'w+',markersize=10)
    plt.subplot(2,3,4), plt.imshow(img4, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center4[1],center4[0], 'w+',markersize=10)
    plt.subplot(2,3,5), plt.imshow(img5, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center5[1],center5[0], 'w+',markersize=10)
    plt.subplot(2,3,6), plt.imshow(img6, cmap='jet',vmin=95, vmax=175), plt.colorbar(), plt.plot(center6[1],center6[0], 'w+',markersize=10)
    #plt.subplot(1,2,2), plt.hist(, bins=60), plt.grid()
    #plt.subplot(1,2,2), stats.histogram(img, numbins=10)
    plt.show()


if 1:
    #tmp = filters.median_filter(tmp, size=(3,3))
    Mask1 = np.zeros((np.shape(img1)))
    Mask2 = np.zeros((np.shape(img1)))
    Mask3 = np.zeros((np.shape(img1)))
    Mask4 = np.zeros((np.shape(img1)))
    Mask5 = np.zeros((np.shape(img1)))
    Mask6 = np.zeros((np.shape(img1)))

    Mask1[np.where(img1 > Thresh)] = 1
    Mask2[np.where(img2 > Thresh)] = 1
    Mask3[np.where(img3 > Thresh)] = 1
    Mask4[np.where(img4 > Thresh)] = 1
    Mask5[np.where(img5 > Thresh)] = 1
    Mask6[np.where(img6 > Thresh)] = 1


    struct_erosion = np.ones((5,5))
    Mask1 = ndimage.morphology.binary_erosion(Mask1, structure=struct_erosion)
    Mask2 = ndimage.morphology.binary_erosion(Mask2, structure=struct_erosion)
    Mask3 = ndimage.morphology.binary_erosion(Mask3, structure=struct_erosion)
    Mask4 = ndimage.morphology.binary_erosion(Mask4, structure=struct_erosion)
    Mask5 = ndimage.morphology.binary_erosion(Mask5, structure=struct_erosion)
    Mask6 = ndimage.morphology.binary_erosion(Mask6, structure=struct_erosion)

    # Gravity center:
    center1 = ndimage.measurements.center_of_mass(Mask1)
    center2 = ndimage.measurements.center_of_mass(Mask2)
    center3 = ndimage.measurements.center_of_mass(Mask3)
    center4 = ndimage.measurements.center_of_mass(Mask4)
    center5 = ndimage.measurements.center_of_mass(Mask5)
    center6 = ndimage.measurements.center_of_mass(Mask6)

    print np.round(center1)
    print np.round(center2)
    print np.round(center3)
    print np.round(center4)
    print np.round(center5)
    print np.round(center6)

    plt.figure
    plt.subplot(2,3,1), plt.imshow(Mask1, cmap='gray'), plt.colorbar(), plt.plot(center1[1],center1[0], 'w+',markersize=10)
    plt.subplot(2,3,2), plt.imshow(Mask2, cmap='gray'), plt.colorbar(), plt.plot(center2[1],center2[0], 'w+',markersize=10)
    plt.subplot(2,3,3), plt.imshow(Mask3, cmap='gray'), plt.colorbar(), plt.plot(center3[1],center3[0], 'w+',markersize=10)
    plt.subplot(2,3,4), plt.imshow(Mask4, cmap='gray'), plt.colorbar(), plt.plot(center4[1],center4[0], 'w+',markersize=10)
    plt.subplot(2,3,5), plt.imshow(Mask5, cmap='gray'), plt.colorbar(), plt.plot(center5[1],center5[0], 'w+',markersize=10)
    plt.subplot(2,3,6), plt.imshow(Mask6, cmap='gray'), plt.colorbar(), plt.plot(center6[1],center6[0], 'w+',markersize=10)
    plt.show()


