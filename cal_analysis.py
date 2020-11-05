import numpy as np
import matplotlib.pyplot as plt

files = ["data\\rps_cal_90GHz_scan_0_loop_1.csv",
         "data\\rps_cal_90GHz_scan_0_loop_2.csv"]
scanind = 0
loopind = 2


for loopind in np.arange(1,3):
    fname = "data\\rps_cal_90GHz_scan_{0}_loop_{1}.csv".format(scanind,loopind)

    d = np.genfromtxt(fname,delimiter=',',skip_header=1)
    ang = d[:,1]
    amp = d[:,2]/np.median(d[:,2])
    T = d[:,3]

    plt.figure(1)
    plt.plot(amp)

    plt.figure(2)
    plt.plot(ang,amp,'.')

    plt.figure(3)
    plt.plot(ang,T,'.')

plt.show()

