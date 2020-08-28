import numpy as np
import matplotlib.pyplot as plt

files = ["data\\rps_cal_test_scan_0_loop_1.csv",
         "data\\rps_cal_test_scan_0_loop_2.csv"]
scanind = 0
loopind = 2

fname = "data\\rps_cal_test_scan_{0}_loop_{1}.csv".format(scanind,loopind)

d = np.genfromtxt(fname,delimiter=',',skip_header=1)
ang = d[:,1]
amp = d[:,2]
T = d[:,3]

plt.figure()
plt.plot(ang)

plt.figure()
plt.plot(ang,amp,'.')
plt.show()