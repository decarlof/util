To perform a full reconstruction

    python tomopy_rec.py --axis 1281.5 --type full /local/data/2018-11/Sangid/test_0001.h5


Full options:

    python tomopy_rec.py -h

usage: tomopy_rec.py [-h] [--axis [AXIS]] [--type [TYPE]] [--nsino [NSINO]]
                     fname

positional arguments:
  fname            file name of a tmographic dataset: /data/sample.h5

optional arguments:
  -h, --help       show this help message and exit
  --axis [AXIS]    rotation axis location: 1024.0 (default 1/2 image
                   horizontal size)
  --type [TYPE]    reconstruction type: full (default slice)
  --nsino [NSINO]  location of the sinogram used by slice reconstruction (0
                   top, 1 bottom): 0.5 (default 0.5)


