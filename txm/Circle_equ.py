
import numpy as np
import matplotlib.pyplot as plt

# circle equation
r = 20
phase_shift = np.pi/3
alpha = np.linspace(0, 2*np.pi, 360*10)
for i in alpha:
    x=r*np.cos(alpha)
    y=r*np.sin(alpha+phase_shift)

plt.figure
plt.plot(x, y, 'r-')
plt.axes().set_aspect('equal')
plt.grid()
plt.show()

