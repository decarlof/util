To perform a test/full reconstruction

    python rec.py /local/data/jason/proj_0070.hdf
    python rec.py --axis 1283.50 --type full /local/data/jason/proj_0070.hdf

To run as scan from the beamline control machine
1. open a terminal then

   cd ~/MCT/scanscripts
   
2. for a first full reconstruction:
   
    /APSshare/anaconda/x86_64/bin/python dimax_fly_scan.py

3. for a loop

    /APSshare/anaconda/x86_64/bin/python dimax_fly_loop_scan.py

To initialize the DIMAX from the beamline control machine
1. open a terminal then

   cd ~/MCT/scanscripts
   /APSshare/anaconda/x86_64/bin/python dimax_reset.py


To soft reset the DIMAX from the beamline control machine
1. open a terminal then

   cd ~
   remote_grayhound

in the dos terminal type:
 
   exit

then double click on the DIMAX NEW icon




