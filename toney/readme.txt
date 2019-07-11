To try different position of the rotation axis starting at 1290 +/- 5 pixels:

    recon proj_0070.hdf --axis 1290 --srs 5 --type try 

To perform a full reconstruction

    recon proj_0070.hdf --axis 1283.50 --type full


To batch reconstruct multiple data sets please follow these steps:

1. move all hdf files in the same folder. For 2-BM data:
    cd  top directory folder where the ExpXXX folders are then
    mkdir all_hdf
    mv Exp0*/*.hdf all_hdf/

2. automatic finding of the rotation axis center for all data sets

        python find_center.py all_hdf/  (<= full path to the directory containing the datasets)
    for help:
        python find_center.py -h

    this generates in the all/ directory a file:
        
            rotation_axis.json 

        containing all the automatically calculated centers
            {"0": {"proj_0000.hdf": 1287.25}, "1": {"proj_0001.hdf": 1297.75},
            {"2": {"proj_0002.hdf": 1287.25}, "3": {"proj_0003.hdf": 1297.75},
            {"4": {"proj_0004.hdf": 1287.25}, "5": {"proj_0005.hdf": 1297.75}}

3. perform a 1 slice reconstruction for all data sets with the automatically found center
        recon all_hdf/

4. load the full series of reconstructed slices with ImageJ/File/Import/Image Sequence/ and select the 
   all_hdf/slice_rec/ folder
        inspect the images and adjust the shift in neede directly editing the shift in the rotation_axis.json file
        once done delete the /slice_rec/ folder:
        rm -rf all_hdf/slice_rec/

4. adjust the center if needed => rerun the 1 slice rec with
    recon  

5. once all 1-slice rec look good run the full reconstruction for all data sets with:
    recon all_hdf/ --type full

