import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as Image
from scipy import misc

from pyhdf import SD
from imreg import translation, similarity


def normalize(image, image_white):

    c = image / ((image_white.astype('float') + 1) / 65535)
    d = c * (c < 65535) + 65535 * np.ones(np.shape(c)) * (c > 65535)
    image = d.astype('uint16')

    return image


#def main():

# Read data
image_file_name_0 = '/local/data/2014_07/TXM_commissioning/test/rotation_axis_twicking/Pin_0deg.tif'
image_file_name_180 = '/local/data/2014_07/TXM_commissioning/test/rotation_axis_twicking/Pin_180deg.tif'
image_0 = misc.imread(image_file_name_0)
image_180 = misc.imread(image_file_name_180)
image_180 = np.fliplr(image_180)

image_0 = image_0[400:700, 300:1000]
image_180 = image_180[400:700, 300:1000]
image_0 = np.float32(image_0)
image_180 = np.float32(image_180)

print image_180.shape
print np.max(image_180)
print np.max(image_0)

im2, scale, angle, t = similarity(image_0, image_180)
im3, scale, angle, t = similarity(image_0, im2)

<<<<<<< HEAD
print "Scale: ", scale, "Angle: ", angle, "Transformation Matrix: ", t

rot_axis_shift_x = -t[0]/2.0
rot_axis_tilt = -t[1]/1.0

print "Rotation Axis Shift (x, y):", "(", rot_axis_shift_x, ",", rot_axis_tilt,")"
=======
#    image_0 = read_tiff(image_file_name_0)
#    image_180 = read_tiff(image_file_name_180)
    image_0 = misc.imread(image_file_name_0)
    image_180 = misc.imread(image_file_name_180)
    image_180 = np.fliplr(image_180)
    
    image_0 = image_0[400:700, 300:1000]
    image_180 = image_180[400:700, 300:1000]

    print image_180.shape

    im2, scale, angle, t = similarity(image_0, image_180)
    print "Scale: ", scale, "Angle: ", angle, "Transformation Matrix: ", t
>>>>>>> 9ff11a7060428c30873ae4c51f35a205690678d7

plt.subplot(2,2,1)
plt.imshow(image_0, cmap=plt.cm.hot)
plt.title('0^o image'), plt.colorbar()
plt.subplot(2,2,2)
plt.imshow(image_180, cmap=plt.cm.hot)
plt.title('180^o image flipped left - right'), plt.colorbar()
plt.subplot(2,2,3)
plt.imshow(im3, cmap=plt.cm.hot)
plt.title('Im2 shifted'), plt.colorbar()
plt.subplot(2,2,4)
plt.imshow(np.subtract(image_0, im3), cmap=plt.cm.hot)
plt.title('difference'), plt.colorbar()
plt.show()

    plt.subplot(2,2,1)
    plt.imshow(image_0, cmap=plt.cm.hot)
    plt.title('0^o image'), plt.colorbar()
    plt.subplot(2,2,2)
    plt.imshow(image_180, cmap=plt.cm.hot)
    plt.title('180^o image flipped left - right'), plt.colorbar()
    plt.subplot(2,2,3)
    plt.imshow(im2, cmap=plt.cm.hot)
    plt.title('Im2 shifted'), plt.colorbar()
    plt.show()


<<<<<<< HEAD
#if __name__ == "__main__":
#    main()
=======
if __name__ == "__main__":
    main()

>>>>>>> 9ff11a7060428c30873ae4c51f35a205690678d7
