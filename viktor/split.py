import numpy as np
import h5py
import sys
import dxchange
import os
#print("This is the name of the script: ", sys.argv[0]
#print("Number of arguments: ", len(sys.argv)
#print("The arguments are: " , str(sys.argv)

file_name = str(sys.argv[1])

for k in range(0,8):  
    file_name_o = os.path.splitext(file_name)[0]+"_"+str(k)+".h5"
    Ntheta, Nz, N = 1500, 900, 2016
    fh5 = h5py.File(file_name_o, "w")
    dset = fh5.create_dataset("exchange/data", (1500, 900, N), chunks = (500,1,N), dtype='float32')
    ddark = fh5.create_dataset("exchange/data_dark", (20, 900, N), chunks = (20,1,N), dtype='float32')
    dwhite = fh5.create_dataset("exchange/data_white", (20, 900, N), chunks = (20,1,N), dtype='float32')

    print(k)
    for j in range(0,900,10):
        print(j)
        prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(j*10, (j+1)*10+1))  
        dset[:,j*10:(j+1)*10+1,:] = prj[k*1500:(k+1)*1500,:,:]
        ddark[:,j*10:(j+1)*10+1,:] = dark
        dwhite[:,j*10:(j+1)*10+1,:] = flat
    fh5.close()
