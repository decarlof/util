
En = 8.0


pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
offset = 0.132
pv.gap_en.put(En + offset, wait=True) # miove the gap
pv.DCM_en.put(En, wait=True) # move the DCM
pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto

