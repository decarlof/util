

# PV declaration:
PV_samx = 'XF:05ID1-ES:X2B{Stg:XY-Ax:X}Mtr'
PV_samy = 'XF:05ID1-ES:X2B{Stg:XY-Ax:Y}Mtr.VAL'
PV_dwelltime = 'XF:05ID-ES:X2B{Cam:1}AcquireTime'
PV_prefix = 'XF:05ID-ES:X2B{Cam:1}TIF:FileName'			# 
PV_radio_index = 'XF:05ID-ES:X2B{Cam:1}TIF:FileNumber'	# next file index
PV_trigger = 'XF:05ID-ES:X2B{Cam:1}Acquire'
PV_save = 'XF:05ID-ES:X2B{Cam:1}TIF:WriteFile'
PV_image = 'XF:05ID-ES:X2B{Cam:1}ARR:ArrayData'


#	caput(PV_samx, df_pos[1], wait=True, timeout=500)					# move samx for the dark field acquisition
#	caput(PV_dwelltime, dwell_rad, wait=True)						# set the dwell time of the snapshot
#	caput(PV_trigger, 1, wait=True, timeout=500)									# trigger the snapshot
#	caput(PV_prefix, FileName, datatype=DBR_CHAR_STR, wait=True, timeout=500)	# create the file name for the next snapshot saving
#	caput(PV_save, 1, wait=True, timeout=500)									# save the dark field snapshot

import inspect

def ascan(stage_name, stage_pos):
#	PV_samx = 'XF:05ID1-ES:X2B{Stg:XY-Ax:X}Mtr'
#	PV_samy = 'XF:05ID1-ES:X2B{Stg:XY-Ax:Y}Mtr.VAL'
#	PV_focus = 'XF:05ID1-ES:X2B{Cam-Ax:Focus}Mtr.VAL'
	
#	caput(eval('PV_'))

#	frame = inspect.currentframe()
#	aa = ascan.func_code.co_varnames
	frame = inspect.currentframe()
	args,_, values = inspect.getframeinfo(frame)[1]
	for i in args:
		print "    %s = %s" % (i,values[i])	
		return [(i, values[i]) for i in args] 
	
	
