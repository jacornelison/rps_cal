import u6
import os
import numpy as np
import time
import pandas as pd

def rps_home():
    #os.system("python /opt/pyAPT-master/home.py")
    print("rps_home")


def rps_goto(angle):
    #os.system("python /opt/pyAPT-master/goto.py {0}".format(float(angle)))
    print("rps_goto")

def save_csv(daq_data, filename):
    daq_data.to_csv(filename)

## Main Program

# Initialize csv file
filenameroot = "rps_cal_test"

# Initialize Labjack
dmmtype = "u6"
dmm = u6.U6()
dmm.getCalibrationData()

scans = 1 # Number of scans to do
res = 30 # Angle Resolution in degrees
angle_cap1 = -180
angle_cap2 = 180
rest = 2 # Time in seconds to rest at position
daq_data = pd.DataFrame(columns=["Angle","Lock-In Amp","Temp"])


# Scan strategy
# Home, Go from 1 to 2, Home, go from 2 to 1, Home

# Loop over angles
for scanind in np.arange(0,scans):

    rps_home()
    for loopind in [1,2]:
        ang_array = np.arange(angle_cap1,angle_cap2,res)

        if loopind == 2:
            ang_array = np.flip(ang_array)

        for angind in ang_array:
            rps_goto(angind)

            # Collect some data
            tstart = time.time()
            while (time.time()-tstart < rest):
                data_row = [angind,
                            dmm.getAIN(0,differential=True),
                            dmm.getAIN(2, differential=True)]

                daq_data = daq_data.append(pd.DataFrame([data_row],
                            columns=daq_data.keys().to_list()),
                            ignore_index=True)

        rps_home()

        filename = filenameroot + "_scan_{0}_loop_{1}.csv".format(scanind,loopind)
        print("saving to "+filename)
        save_csv(daq_data,filename)
