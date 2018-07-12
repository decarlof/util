import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


def update(val):
    amp = sino_amp.val
    freq = sino_freq.val
    l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    fig.canvas.draw_idle()

def reset(event):
    sino_freq.reset()
    sino_amp.reset()


def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()



fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
t = np.arange(0.0, 1.0, 0.001)
a0 = 5
f0 = 3

s = a0*np.sin(2*np.pi*f0*t)
l, = plt.plot(t, s, lw=5, color='red')

plt.axis([0, 1, -10, 10])

axcolor = 'lightgoldenrodyellow'

axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
sino_freq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
sino_freq.on_changed(update)

axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
sino_amp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)
sino_amp.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
reset_button.on_clicked(reset)

radioax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(radioax, ('red', 'blue', 'green'), active=0)
radio.on_clicked(colorfunc)

plt.show()

