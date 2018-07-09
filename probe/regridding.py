import numpy as np
import scipy.interpolate

old_grid_data=np.random.rand(4,3)

#old grid dim
loni=np.array([109.94999695, 110.05000305, 110.15000153])
depi=np.array([3.04677272, 9.45404911, 16.36396599, 23.89871025])

#new grid dim
#lon=np.arange(110.,110.3,.1) #NB: 110.2 outside of convex hull of old so will produce nan
#depth=np.array([3.1,9,16,23])
lon=np.array([109.96, 110.06, 110.16])
depth=np.array([3.04, 9.45, 16.37, 23.90])

#create mesh
X, Y = np.meshgrid(loni, depi)
print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX", X)
XI, YI = np.meshgrid(lon,depth)

#interp
new_grid=scipy.interpolate.griddata((X.flatten(),Y.flatten()),old_grid_data.flatten() , (XI,YI),method='cubic')

print "this is original"
print old_grid_data.reshape(4,3)
print ""
print "this is interp' by cubic"
print new_grid

print
print "this is diff"
print new_grid-old_grid_data.reshape(4,3)