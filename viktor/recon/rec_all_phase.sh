#!/usr/bin/bash

for f in 1{86..98}
 do
  echo /local/data/2019-03/Nikitin/${f}_cell100bar_Sand10NaBr10.h5
  python rec_phase.py --axis 1231 --type full /local/data/2019-03/Nikitin/${f}_cell100bar_Sand10NaBr10.h5
done
