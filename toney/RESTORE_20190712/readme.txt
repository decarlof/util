To install it:

    clone this repository in a folder that is in the PATH of your bash for example (export PATH="/local/usr32idc/bin:$PATH") then

    git clone https://github.com/decarlof/bin_utils.git /local/usr32idc/bin

Dependency: pyinotify


How to use rec and find_center:

To try different position of the rotation axis starting at 1290 +/- 5 pixels:

    rec proj_0070.hdf --axis 1290 --srs 5 --type try 

To perform a full reconstruction

    rec proj_0070.hdf --axis 1283.50 --type full


To batch reconstruct multiple data sets please follow these steps:


1. automatic finding of the rotation axis center for all data sets

        find_center all_hdf/  (<= full path to the directory containing the datasets)
    for help:
        find_center -h

    this generates in the all/ directory a file:
        
            rotation_axis.json 

        containing all the automatically calculated centers
            {"0": {"proj_0000.hdf": 1287.25}, "1": {"proj_0001.hdf": 1297.75},
            {"2": {"proj_0002.hdf": 1287.25}, "3": {"proj_0003.hdf": 1297.75},
            {"4": {"proj_0004.hdf": 1287.25}, "5": {"proj_0005.hdf": 1297.75}}

2. perform a 1 slice reconstruction for all data sets with the automatically found center
        rec all_hdf/

3. load the full series of reconstructed slices with ImageJ/File/Import/Image Sequence/ and select the 
   all_hdf/slice_rec/ folder
        inspect the images and adjust the shift in neede directly editing the shift in the rotation_axis.json file
        once done delete the /slice_rec/ folder:
        rm -rf all_hdf/slice_rec/

4. adjust the center if needed => rerun the 1 slice rec with
    rec  

5. once all 1-slice rec look good run the full reconstruction for all data sets with:
    rec all_hdf/ --type full


How to use auto_rec:

auto_rec runs on the data analysis machine by monitoring a folder and executing for any newly transferred h5 file a try reconstruction (rec new_file.h5  --srs 30 --type try)


Start monitoring:

    auto_rec /local/data/

the program will start monitoring /local/data recursively and at each new h5 file send a message like:

    waiting for new file in /local/data/ to process
    executing script: rec --type try --srs 30 /local/data/2019-06/004_test.h5
    Reconstructing a single file
    (1500, 2048, 2448)
    Raw data:  /local/data/2019-06/004_test.h5
    Center:  1224.0
    Reconstructions:  /local/data/2019-06/try_rec/004_test/recon_


