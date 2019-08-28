import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt


def sequence(nproj_total, nproj_per_rot, prime, continuous_angle=True):

    # seq = np.array((nproj_total * nproj_per_rot))
    seq = []
    # nproj_per_rot = int(nproj_per_rot)
    # print (len(seq))
    i = 0

    while len(seq) < nproj_total:

        b = i
        i += 1
        r = 0
        q = 1 / prime

        while (b != 0):
            a = np.mod(b, prime)
            r += (a * q)
            # print (b, r, a, q)
            q /= prime
            b = np.floor(b / prime)
        r *= (360.0 / nproj_per_rot)

        k = 0
        while (np.logical_and(len(seq) < nproj_total, k < nproj_per_rot)):
            seq.append(r + k * 360.0 / nproj_per_rot )
            k += 1

    if continuous_angle:
        j = 0
        for x in range(len(seq)):       
            if (x%nproj_per_rot == 0):
                for y in range(nproj_per_rot):
                    if (x+y) < len(seq):
                        seq[x+y] += j*360.0
                j += 1

    return seq

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("--nproj_total", nargs='?', type=int, default=100, help="total number of projections: 100 (default 100)")
    parser.add_argument("--nproj_per_rot", nargs='?', type=int, default=10, help="total number of projections per rotation: 10 (default 10)")
    parser.add_argument("--prime", nargs='?', type=int, default=10, help="prime: 2 (default 2). Ratio to position the first angle past 360")
    parser.add_argument("--continuous_angle",action="store_true", help="set to generate continuous angles past 360 deg")

    args = parser.parse_args()

    nproj_total = args.nproj_total
    nproj_per_rot = args.nproj_per_rot
    prime = args.prime
    continuous_angle = args.continuous_angle

    seq = sequence(nproj_total, nproj_per_rot, prime, continuous_angle)

    print(seq)
    plt.plot(seq)
    plt.grid('on')
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])

