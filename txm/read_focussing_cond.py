
# zp_focus(output_path, condenser_z, -6, 5.8, 100, 0.015, 1)

if 0:
    the_path = '/local/data/2014_07/TXM_commissioning/condenser_focussing/condenser_20nm/focus_no_phl/'
    Radix = 'ZP_focus_'
    n_steps = 150
    pos_start = -7
    pos_end = 6.1
    nRow = 964
    nCol = 1292

    Col_zoom_1 = 550
    Col_zoom_2 = 750

if 1:
    the_path = '/local/data/2014_07/TXM_commissioning/condenser_focussing/condenser_20nm/focus_no_phl_unscrew/'
    Radix = 'ZP_focus_'
    n_steps = 200
    pos_start = -7
    pos_end = 6.1
    nRow = 964
    nCol = 1292

    Col_zoom_1 = 550
    Col_zoom_2 = 750

if 0: # zp_focus(output_path, condenser_z, -7, 7, 200, 0.02, 1)
    the_path = '/local/data/2014_07/TXM_commissioning/condenser_focussing/condenser_60nm/focus_no_phl/'
    Radix = 'ZP_focus_'
    n_steps = 250
    pos_start = -9
    pos_end = 9
    nRow = 964
    nCol = 1292

    Col_zoom_1 = 550
    Col_zoom_2 = 750


###########----------------------------
scan_val = np.linspace(pos_start, pos_end, n_steps)
Mat3D = np.zeros((nRow, nCol, n_steps))

for iLoop in range(0, n_steps):
    FileName = the_path+'/ZP_focus_%04i.tif' % iLoop
    img_tmp = misc.imread(FileName)
    Mat3D[:,:,iLoop] = img_tmp

Mat2D = Mat3D[485, Col_zoom_1:Col_zoom_2, :]
Mat2D = Mat2D.T
#Mat2D = Mat3D[:, :, 0]

plt.imshow(Mat2D, cmap='jet', extent = [Col_zoom_1, Col_zoom_2, pos_start, pos_end], aspect="auto")
plt.xlabel('knife edge'), plt.ylabel('Condenser z pozition'), plt.colorbar(), plt.show()





