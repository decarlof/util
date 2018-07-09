import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

# Number of data points
n = 10

# Dummy data
np.random.seed(19680801)
x = np.arange(0, n, 1)
y = np.arange(0, n, 1)
#y = np.random.rand(n) * 5.

# Dummy errors (above and below)
#x_size = np.random.rand(2, n) + 0.1
#y_size = np.random.rand(2, n) + 0.2
x_size = np.ones((2, n))
y_size = np.ones((2, n))
print(x_size)


def make_error_boxes(ax, xdata, ydata, x_sizeor, y_sizeor, facecolor='r',
                     edgecolor='None', alpha=0.5):

    # Create list for all the error patches
    errorboxes = []

    # Loop over data points; create box from errors at each point
    for x, y, xe, ye in zip(xdata, ydata, x_sizeor.T, y_sizeor.T):
        rect = Rectangle((x - xe[0], y - ye[0]), xe.sum(), ye.sum())
        errorboxes.append(rect)

    # Create patch collection with specified colour/alpha
    pc = PatchCollection(errorboxes, facecolor=facecolor, alpha=alpha,
                         edgecolor=edgecolor)

    # Add collection to axes
    ax.add_collection(pc)

    # Plot errorbars
    artists = ax.errorbar(xdata, ydata, x_size=x_sizeor, y_size=y_sizeor,
                          fmt='None', ecolor='k')

    return artists


# Create figure and axes
fig, ax = plt.subplots(1)

# Call function to create error boxes
_ = make_error_boxes(ax, x, y, x_size/2, y_size/2)

plt.show()

