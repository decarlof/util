#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Arun data sets.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np

def read_aps_2bm_custom(fname, sino):

    # Read APS 2-BM raw data in temporary array to fix an acquisition error. 
    # All data (proj,dark and white) are stored in the proj array while flat/dark/theta arrays are invalid
    tproj, tflat, tdark, ttheta = dxchange.read_aps_2bm(fname, sino=sino)

    # Extracting from the tproj array proj, flat, dark and theta
    ndark = 10
    nflat = 10
    last_projection = tproj.shape[0] - nflat - ndark
    proj = tproj[0:last_projection, :, :]
    flat = tproj[last_projection:last_projection+nflat, :, :]
    dark = tproj[last_projection+nflat:last_projection+nflat+ndark, :, :]
    theta_size = proj.shape[0]
    theta = np.linspace(0. , np.pi, theta_size)
    
    return proj, flat, dark, theta
    
if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Dinc/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {
    332: {"0332": 646.2}, 333: {"0333": 646.5}, 334: {"0334": 646.5}, 335: {"0335": 646.5}, 336: {"0336": 647.5}, 337: {"0337": 647.5}, 338: {"0338": 648.5}, 339: {"0339": 648.5}, 340: {"0340": 648.5}, 
    341: {"0341": 648.5}, 342: {"0342": 648.5}, 343: {"0343": 648.5}, 344: {"0344": 648.5}, 345: {"0345": 648.5}, 346: {"0346": 648.5}, 347: {"0347": 648.5}, 348: {"0348": 648.5}, 349: {"0349": 648.5}, 350: {"0350": 648.5}, 
    351: {"0351": 648.5}, 352: {"0352": 648.5}, 353: {"0353": 648.5}, 354: {"0354": 648.5}, 355: {"0355": 648.5}, 356: {"0356": 648.5}, 357: {"0357": 648.5}, 358: {"0358": 648.5}, 359: {"0359": 648.5}, 360: {"0360": 648.5}, 
    361: {"0361": 648.5}, 362: {"0362": 648.5}, 363: {"0363": 648.5}, 364: {"0364": 648.5}, 365: {"0365": 648.5}, 366: {"0366": 648.5}, 367: {"0367": 648.5}, 368: {"0368": 648.5}, 369: {"0369": 648.5}, 370: {"0370": 648.5}, 
    371: {"0371": 648.5}, 372: {"0372": 648.5}, 373: {"0373": 648.5}, 374: {"0374": 648.5}, 375: {"0375": 648.5}, 376: {"0376": 648.5}, 377: {"0377": 648.5}, 378: {"0378": 648.5}, 379: {"0379": 648.5}, 380: {"0380": 648.5}, 
    381: {"0381": 648.5}, 382: {"0382": 648.5}, 383: {"0383": 648.5}, 384: {"0384": 648.5}, 385: {"0385": 648.5}, 386: {"0386": 648.5}, 387: {"0387": 648.5}, 388: {"0388": 648.5}, 389: {"0389": 648.5}, 390: {"0390": 648.5}, 
    391: {"0391": 648.5}, 392: {"0392": 648.5}, 393: {"0393": 648.5}, 394: {"0394": 648.5}, 395: {"0395": 648.5}, 396: {"0396": 648.5}, 397: {"0397": 648.5}, 398: {"0398": 648.5}, 399: {"0399": 648.5}, 400: {"0400": 648.5},
    401: {"0401": 648.5}, 402: {"0402": 648.5}, 404: {"0404": 645.5}, 405: {"0405": 645.5}, 406: {"0406": 648.5}, 407: {"0407": 648.5}, 408: {"0408": 648.5}, 409: {"0409": 648.5}, 410: {"0410": 648.5}, 
    411: {"0411": 648.5}, 412: {"0412": 648.5}, 413: {"0413": 648.5}, 414: {"0414": 648.5}, 415: {"0415": 648.5}, 416: {"0416": 648.5}, 417: {"0417": 648.5}, 418: {"0418": 648.5}, 419: {"0419": 648.5}, 420: {"0420": 648.5}, 
    421: {"0421": 648.5}, 422: {"0422": 648.5}, 423: {"0423": 648.5}, 424: {"0424": 648.5}, 425: {"0425": 648.5}, 426: {"0426": 648.5}, 427: {"0427": 648.5}, 479: {"0479": 649.0}, 480: {"0480": 649.0}, 
    481: {"0481": 649.0}, 482: {"0482": 649.0}, 483: {"0483": 649.0}, 484: {"0484": 649.0}, 485: {"0485": 649.0}, 486: {"0486": 649.0}, 487: {"0487": 649.0}, 488: {"0488": 649.0}, 489: {"0489": 649.0}, 490: {"0490": 649.0}, 
    491: {"0491": 649.0}, 492: {"0492": 649.0}, 493: {"0493": 649.0}, 494: {"0494": 649.0}, 495: {"0495": 649.0}, 496: {"0496": 649.0}, 497: {"0497": 649.0}, 498: {"0498": 649.0}, 499: {"0499": 649.0}, 500: {"0500": 649.0},
    501: {"0501": 649.0}, 502: {"0502": 649.0}, 503: {"0503": 649.0}, 504: {"0504": 649.0}, 505: {"0505": 649.0}, 506: {"0506": 649.0}, 507: {"0507": 649.0}, 508: {"0508": 649.0}, 509: {"0509": 649.0}, 510: {"0510": 649.0}, 
    511: {"0511": 649.0}, 512: {"0512": 649.3}, 513: {"0513": 649.3}, 514: {"0514": 649.3}, 515: {"0515": 649.3}, 516: {"0516": 649.3}, 517: {"0517": 649.3}, 518: {"0518": 649.2}, 519: {"0519": 649.3}, 520: {"0520": 649.0},  
    521: {"0521": 648.8}, 522: {"0522": 648.8}, 523: {"0523": 648.8}, 524: {"0524": 648.8}, 525: {"0525": 648.8}, 526: {"0526": 648.8}, 527: {"0527": 648.8}, 528: {"0528": 648.8}, 529: {"0529": 648.8}, 530: {"0530": 648.8}, 
    531: {"0531": 648.8}, 532: {"0532": 648.8}, 533: {"0533": 648.8}, 534: {"0534": 648.8}, 535: {"0535": 648.8}, 536: {"0536": 648.8}, 537: {"0537": 648.8}, 538: {"0538": 648.8}, 539: {"0539": 648.8}, 540: {"0540": 648.5}, 
    541: {"0541": 648.5}, 542: {"0542": 648.5}, 543: {"0543": 648.5}, 544: {"0544": 648.5}, 545: {"0545": 648.5}, 546: {"0546": 648.5}, 547: {"0547": 648.5}, 548: {"0548": 648.5}, 549: {"0549": 648.5}, 550: {"0550": 648.5}, 
    551: {"0551": 648.5}, 552: {"0552": 648.5}, 553: {"0553": 648.5}, 554: {"0554": 648.5}, 555: {"0555": 648.5}, 556: {"0556": 648.5}, 557: {"0557": 648.5}, 558: {"0558": 648.5}, 559: {"0559": 648.5}, 560: {"0560": 648.5}, 
    561: {"0561": 648.5}, 562: {"0562": 648.5}, 563: {"0563": 648.5}, 564: {"0564": 648.5}, 565: {"0565": 648.5}, 566: {"0566": 648.5}, 567: {"0567": 648.5}, 568: {"0568": 648.5}, 569: {"0569": 648.5}, 570: {"0570": 648.5}, 
    571: {"0571": 648.5}, 572: {"0572": 648.5}, 573: {"0573": 648.5}, 574: {"0574": 648.5}, 575: {"0575": 648.5}, 576: {"0576": 648.5}, 577: {"0577": 648.5}, 578: {"0578": 648.5}, 579: {"0579": 648.5}, 580: {"0580": 648.5}, 
    581: {"0581": 648.5}, 582: {"0582": 648.5}, 583: {"0583": 648.5}, 584: {"0584": 648.5}, 585: {"0585": 648.5}, 586: {"0586": 648.5}, 587: {"0587": 648.5}, 588: {"0588": 648.5}, 589: {"0589": 648.5}, 590: {"0590": 648.5}, 
    591: {"0591": 648.5}, 592: {"0592": 648.5}, 593: {"0593": 648.5}, 594: {"0594": 648.5}, 595: {"0595": 648.5}, 596: {"0596": 648.5}, 597: {"0597": 643.5}, 598: {"0598": 644.5}, 599: {"0599": 644.5}, 600: {"0600": 644.5}, 
    601: {"0601": 644.5}    
    } 
        
    sample_detector_distance = 5       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 0.65e-4    # Detector pixel size in cm
    monochromator_energy = 27.0        # Energy of incident wave in keV
    alpha = 1e-02                      # Phase retrieval coeff.
    zinger_level = 1000                # Zinger level for projections
    zinger_level_w = 1000              # Zinger level for white
    
    for key in dictionary:
        dict2 = dictionary[key]
        for h5name in dict2:
            prefix = 'exp_'
            fname = top + prefix + h5name + '/proj_' + h5name + '.hdf'
            rot_center = dict2[h5name]
            print(fname, rot_center)

            # Select sinogram range to reconstruct.
            sino = None
            
            start = 1000
            end = 1001
            sino = (start, end)

            # Read APS 2-BM raw data.
            if (key > 6):            
                proj, flat, dark, theta = read_aps_2bm_custom(fname, sino=sino)
            else:
                proj, flat, dark, theta = dxchange.read_aps_2bm(fname, sino=sino)
            
            # zinger_removal
            proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
            flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

            # Flat-field correction of raw data.
            data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

            # remove stripes
            #data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)
            ##data = tomopy.prep.stripe.remove_stripe_ti(data,alpha=7)
            ##data = tomopy.prep.stripe.remove_stripe_sf(data,size=51)

            # phase retrieval
            ##data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

            # Find rotation center
            #rot_center = tomopy.find_center(data, theta, init=rot_center, ind=start, tol=0.5)
            print(h5name, rot_center)

            data = tomopy.minus_log(data)

            # Reconstruct object using Gridrec algorithm.
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

            # Mask each reconstructed slice with a circle.
            rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

            # Write data as stack of TIFs.
            ##fname = top +'full_rec/' + prefix + h5name + '/recon'
            fname = top +'slice_rec/' + prefix + h5name + '_recon'
            print("Rec: ", fname)
            dxchange.write_tiff_stack(rec, fname=fname)
