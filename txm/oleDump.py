import olefile

fname = 'dino_LFOV-80kV-air-2s.txrm'
ole = olefile.OleFileIO(fname)

for entry in ole.listdir():
    print(entry)
