import matplotlib.pyplot as plt
import numpy as np
import dxchange
from matplotlib.widgets import Slider, Button, RadioButtons

def update(val):
    fig.canvas.draw_idle()

# set the data path
spath = '/local/decarlo/conda/util/viz/'

# read proj and recon


fig, (ax1, ax2) = plt.subplots(1, 2)
plt.pause(.01)

im1 = im2 = None
cnt = 0



#f0 = 3
#plt.axis([0, 1, -10, 10])
axcolor = 'lightgoldenrodyellow'

#axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
#sino_freq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
#sino_freq.on_changed(update)

rec_ax = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
rec_amp = Slider(rec_ax, 'Rec Scale', 0.1, 300.0, valinit=150)
rec_amp.on_changed(update)


proj_ax = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
proj_amp = Slider(proj_ax, 'Proj Scale', 0.1, 4000.0, valinit=2000)
proj_amp.on_changed(update)



while True:
  cnt += 1
  if cnt % 5 == 0:
    proj = dxchange.read_tiff(spath + 'proj.tif')
    if im1 is None:
        im1 = ax1.imshow(proj, cmap='gray', vmin=0, vmax=4000)
    else:
        im1.set_data(proj)
        im1.set_clim(0, proj_amp.val)
    fig.canvas.draw_idle()
    plt.pause(0.01)

  recon = dxchange.read_tiff(spath + 'recon.tif')
  print(recon.shape, rec_amp.val, proj_amp.val)

  if im2 is None:
      im2 = ax2.imshow(recon, cmap='gray', vmin=0, vmax=300)
  else:
      im2.set_data(recon)
      im2.set_clim(0, rec_amp.val)
  fig.canvas.draw_idle()
  plt.pause(0.01)

