
if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/'
    h5ext = '.h5'
    
    dictionary = {
                  10: {"UTK3_WB_30mmGlass_200mm_2mic_001": 940.0},
                  11: {"UTK3_WB_30mmGlass_200mm_2mic_002": 957.0},
                  12: {"UTK3_WB_30mmGlass_200mm_2mic_003": 955.0},
                  13: {"UTK3_WB_30mmGlass_200mm_2mic_004": 955.0},
                  14: {"UTK2_25keV_300mm_001": 955.0},
                  15: {"UTK2_25keV_300mm_002": 955.0},
                  16: {"UTK2_25keV_300mm_003": 945.0},
                  17: {"UTK2_WB_Glass30mm_001": 955.0},
                  18: {"UTK2_WB_Glass30mm_002": 955.0},
                  19: {"UTK2_WB_Glass30mm_003": 955.0}}

    for key in sorted(dictionary):
        dict2 = dictionary[key]
        for h5name in dict2:
            fname = top + h5name + h5ext 
            rot_center = dict2[h5name]
            print(key, fname, rot_center)

