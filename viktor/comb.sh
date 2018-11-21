#!/bin/bash
n = 0
for k in $(find /local/data/2018-11/Viktor/cell3_KI_*rec -name *108*); do   
   echo $k
   cp $k /local/data/2018-11/Viktor/comb/$n.tiff
   let n=n+1
done


