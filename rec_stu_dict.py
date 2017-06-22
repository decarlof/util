#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Stu data sets.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Stu/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {1: {"0001": 1122.5}, 2: {"0002": 1122.5}, 3: {"0003": 1122.0}, 4: {"0004": 1122.0}, 5: {"0005": 1122.5}, 6: {"0006": 1122.5}, 7: {"0007": 1122.5}, 8: {"0008": 1122.5}, 9: {"0009": 1122.5}, 10: {"0010": 1122.5},  
    11: {"0011": 1122.5}, 12: {"0012": 1122.5}, 13: {"0013": 1122.5}, 14: {"0014": 1122.5}, 15: {"0015": 1122.5}, 16: {"0016": 1122.5}, 17: {"0017": 1122.5}, 18: {"0018": 1122.5}, 19: {"0019": 1122.5}, 20: {"0020": 1124.5}, 
    21: {"0021": 1122.5}, 22: {"0022": 1122.5}, 23: {"0023": 1122.5}, 24: {"0024": 1122.5}, 25: {"0025": 1122.5}, 26: {"0026": 1122.5}, 27: {"0027": 1122.5}, 28: {"0028": 1122.5}, 29: {"0029": 1122.5}, 30: {"0030": 1122.5}, 
    31: {"0031": 1122.5}, 32: {"0032": 1122.5}, 33: {"0033": 1122.5}, 34: {"0034": 1122.5}, 35: {"0035": 1122.5}, 36: {"0036": 1122.5}, 37: {"0037": 1122.5}, 38: {"0038": 1122.5}, 39: {"0039": 1122.5}, 40: {"0040": 1124.5}, 
    41: {"0041": 1122.5}, 42: {"0042": 1122.5}, 43: {"0043": 1122.5}, 44: {"0044": 1122.5}, 45: {"0045": 1122.5}, 46: {"0046": 1122.5}, 47: {"0047": 1122.5}, 48: {"0048": 1122.5}, 49: {"0049": 1122.5}, 50: {"0050": 1122.5}, 
    51: {"0051": 1122.5}, 52: {"0052": 1122.5}, 53: {"0053": 1122.5}, 54: {"0054": 1122.5}, 55: {"0055": 1122.5}, 56: {"0056": 1122.5}, 57: {"0057": 1122.5}, 58: {"0058": 1122.5}, 59: {"0059": 1122.5}, 60: {"0060": 1122.5}, 
    61: {"0061": 1122.5}, 62: {"0062": 1122.5}, 63: {"0063": 1122.5}, 64: {"0064": 1122.5}, 65: {"0065": 1122.5}, 66: {"0066": 1122.5}, 67: {"0067": 1122.5}, 68: {"0068": 1122.5}, 69: {"0069": 1122.5}, 70: {"0070": 1124.5}, 
    71: {"0071": 1122.5}, 72: {"0072": 1122.5}, 73: {"0073": 1122.5}, 74: {"0074": 1122.5}, 75: {"0075": 1122.5}, 76: {"0076": 1122.5}, 77: {"0077": 1122.5}, 78: {"0078": 1122.5}, 79: {"0079": 1122.5}, 80: {"0080": 1122.5}, 
    81: {"0081": 1122.5}, 82: {"0082": 1122.5}, 83: {"0083": 1122.5}, 84: {"0084": 1122.5}, 85: {"0085": 1122.5}, 86: {"0086": 1122.5}, 87: {"0087": 1122.5}, 88: {"0088": 1122.5}, 89: {"0089": 1122.5}, 90: {"0090": 1122.5}, 
    91: {"0091": 1122.5}, 92: {"0092": 1122.5}, 93: {"0093": 1122.5}, 94: {"0094": 1122.5}, 95: {"0095": 1122.5}, 96: {"0096": 1122.5}, 97: {"0097": 1122.5}, 98: {"0098": 1122.5}, 99: {"0099": 1122.5}, 100: {"0100": 1122.5},
    101: {"0101": 1129.0}, 102: {"0102": 1131.5}, 103: {"0103": 1130.0}, 104: {"0104": 1131.5}, 105: {"0105": 1129.0}, 106: {"0106": 1131.5}, 107: {"0107": 1129.0}, 108: {"0108": 1129.0}, 109: {"0109": 1132.5}, 110: {"0110": 1132.5}, 
    111: {"0111": 1131.5}, 112: {"0112": 1131.5}, 113: {"0113": 1131.5}, 114: {"0114": 1131.5}, 115: {"0115": 1131.5}, 116: {"0116": 1131.5}, 117: {"0117": 1131.5}, 118: {"0118": 1131.5}, 119: {"0119": 1131.5}, 120: {"0120": 1131.5},
    121: {"0121": 1280.0}, 122: {"0122": 1278.0}, 123: {"0123": 1280.0}, 124: {"0124": 1275.5}, 125: {"0125": 1280.0}, 126: {"0126": 1277.0}, 127: {"0127": 1277.0}, 128: {"0128": 1277.0}, 129: {"0129": 1277.0}, 130: {"0130": 1277.0}, 
        131: {"0131": 1276.5}, 132: {"0132": 1276.5}, 133: {"0133": 1276.5}, 134: {"0134": 1276.5}, 135: {"0135": 1276.5}, 136: {"0136": 1276.5}, 137: {"0137": 1276.5}, 138: {"0138": 1276.5}, 139: {"0139": 1276.5}, 140: {"0140": 1276.5}, 
        141: {"0141": 1276.5}, 142: {"0142": 1276.5}, 143: {"0143": 1276.5}, 144: {"0144": 1276.5}, 145: {"0145": 1276.5}, 146: {"0146": 1276.5}, 147: {"0147": 1276.5}, 148: {"0148": 1276.5}, 149: {"0149": 1276.5}, 150: {"0150": 1276.5}, 
        151: {"0151": 1280.0}, 152: {"0152": 1280.0}, 153: {"0153": 1280.0}, 154: {"0154": 1280.0}, 155: {"0155": 1280.0}, 156: {"0156": 1280.0}, 157: {"0157": 1280.0}, 158: {"0158": 1280.0}, 159: {"0159": 1280.0}, 160: {"0160": 1280.0}, 
        161: {"0161": 1282.0}, 162: {"0162": 1282.0}, 163: {"0163": 1282.0}, 164: {"0164": 1282.0}, 165: {"0165": 1282.0}, 166: {"0166": 1282.0}, 167: {"0167": 1282.0}, 168: {"0168": 1282.0}, 169: {"0169": 1282.0}, 170: {"0170": 1282.0}, 
        171: {"0171": 1280.0}, 172: {"0172": 1280.0}, 173: {"0173": 1280.0}, 174: {"0174": 1280.0}, 175: {"0175": 1280.0}, 176: {"0176": 1280.0}, 177: {"0177": 1280.0}, 178: {"0178": 1280.0}, 179: {"0179": 1280.0}, 180: {"0180": 1280.0}, 
        181: {"0181": 1281.0}, 182: {"0182": 1281.0}, 183: {"0183": 1281.0}, 184: {"0184": 1281.0}, 185: {"0185": 1281.0}, 186: {"0186": 1281.0}, 187: {"0187": 1281.0}, 188: {"0188": 1281.0}, 189: {"0189": 1281.0}, 190: {"0190": 1281.0}, 
        191: {"0191": 1278.5}, 192: {"0192": 1278.5}, 193: {"0193": 1278.5}, 194: {"0194": 1278.5}, 195: {"0195": 1278.5}, 196: {"0196": 1278.5}, 197: {"0197": 1278.5}, 198: {"0198": 1278.5}, 199: {"0199": 1278.5}, 200: {"0200": 1278.5},
        201: {"0201": 1280.0}, 202: {"0202": 1280.0}, 203: {"0203": 1280.0}, 204: {"0204": 1280.0}, 205: {"0205": 1280.0}, 206: {"0206": 1280.0}, 207: {"0207": 1280.0}, 208: {"0208": 1280.0}, 209: {"0209": 1280.0}, 210: {"0210": 1280.5}, 
        211: {"0211": 1280.0}, 212: {"0212": 1280.0}, 213: {"0213": 1280.0}, 214: {"0214": 1280.0}, 215: {"0215": 1280.0}, 216: {"0216": 1280.0}, 217: {"0217": 1280.0}, 218: {"0218": 1280.0}, 219: {"0219": 1280.0}, 220: {"0220": 1280.5}, 
        221: {"0221": 1285.5}, 222: {"0222": 1285.5}, 223: {"0223": 1285.5}, 224: {"0224": 1285.5}, 225: {"0225": 1285.5}, 226: {"0226": 1285.5}, 227: {"0227": 1285.5}, 228: {"0228": 1285.5}, 229: {"0229": 1285.5}, 230: {"0230": 1283.5}, 
        231: {"0231": 1277.0}, 232: {"0232": 1277.0}, 233: {"0233": 1277.0}, 234: {"0234": 1277.0}, 235: {"0235": 1277.0}, 236: {"0236": 1277.0}, 237: {"0237": 1277.0}, 238: {"0238": 1277.0}, 239: {"0239": 1277.0}, 240: {"0240": 1277.0}, 
        241: {"0241": 1278.5}, 242: {"0242": 1278.5}, 243: {"0243": 1278.5}, 244: {"0244": 1278.5}, 245: {"0245": 1278.5}, 246: {"0246": 1278.5}, 247: {"0247": 1278.5}, 248: {"0248": 1278.5}, 249: {"0249": 1278.5}, 250: {"0250": 1278.5}, 
        251: {"0251": 1282.5}, 252: {"0252": 1282.5}, 253: {"0253": 1282.5}, 254: {"0254": 1282.5}, 255: {"0255": 1282.5}, 256: {"0256": 1282.5}, 257: {"0257": 1282.5}, 258: {"0258": 1282.5}, 259: {"0259": 1282.5}, 260: {"0260": 1282.5}, 
        261: {"0261": 1278.0}, 262: {"0262": 1278.0}, 263: {"0263": 1278.0}, 264: {"0264": 1278.0}, 265: {"0265": 1278.0}, 266: {"0266": 1278.0}, 267: {"0267": 1278.0}, 268: {"0268": 1278.0}, 269: {"0269": 1278.0}, 270: {"0270": 1278.0}, 
        271: {"0271": 1278.5}, 272: {"0272": 1278.5}, 273: {"0273": 1278.5}, 274: {"0274": 1278.5}, 275: {"0275": 1278.5}, 276: {"0276": 1278.5}, 277: {"0277": 1278.5}, 278: {"0278": 1278.5}, 279: {"0279": 1278.5}, 280: {"0280": 1278.5}, 
        281: {"0281": 1273.5}, 282: {"0282": 1273.5}, 283: {"0283": 1273.5}, 284: {"0284": 1273.5}, 285: {"0285": 1273.5}, 286: {"0286": 1273.5}, 287: {"0287": 1273.5}, 288: {"0288": 1273.5}, 289: {"0289": 1273.5}, 290: {"0290": 1273.5}, 
        291: {"0291": 1280.0}, 292: {"0292": 1280.0}, 293: {"0293": 1280.0}, 294: {"0294": 1280.0}, 295: {"0295": 1280.0}, 296: {"0296": 1280.0}, 297: {"0297": 1280.0}, 298: {"0298": 1280.0}, 299: {"0299": 1280.0}, 300: {"0300": 1280.0},
        301: {"0301": 1280.0}, 302: {"0302": 1280.0}, 303: {"0303": 1280.0}, 304: {"0304": 1280.0}} 
    for key in dictionary:
        dict2 = dictionary[key]
        for key2 in dict2:
            prefix = 'exp_'
            index = key2
            fname = top + prefix + index + '/proj_' + index + '.hdf'
            rot_center = dict2[key2]
            print(fname, rot_center)

