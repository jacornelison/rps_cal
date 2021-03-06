import u6
import os
import numpy as np
import time
import pandas as pd

def rps_home():
    os.system("python /opt/pyAPT-master/home.py")
#    print("rps_home")


def rps_goto(angle):
    os.system("python /opt/pyAPT-master/goto.py {0}".format(float(angle)))
#    print("rps_goto")

def save_csv(daq_data, filename):
    daq_data.to_csv(filename)

## Main Program

# Initialize csv file
filenameroot = "data/rps_cal_90GHz"

# Initialize Labjack
dmmtype = "u6"
dmm = u6.U6()
dmm.getCalibrationData()

scans = 10 # Number of scans to do
res = 30 # Angle Resolution in degrees
angle_cap1 = -180
angle_cap2 = 180
wait_time = 30 # Time to wait before measuring
rest = 60 # Time in seconds to rest at position
scanstart = 0


# Scan strategy
# Home, Go from 1 to 2, Home, go from 2 to 1, Home

# Loop over angles
for scanind in np.arange(0,scans):

    time.sleep(1)
    rps_home()
    time.sleep(1)
    for loopind in [1,2]:
        filename = filenameroot + "_scan_{0}_loop_{1}.csv".format(scanind + scanstart, loopind)
        while os.path.isfile(filename):
            scanstart += 1
            filename = filenameroot + "_scan_{0}_loop_{1}.csv".format(scanind + scanstart, loopind)

        print("Beginning " + filename)

        daq_data = pd.DataFrame(columns=["Angle", "Lock-In Amp", "Temp"])
        ang_array = np.arange(angle_cap1,angle_cap2+res,res)

        if loopind == 2:
            ang_array = np.flip(ang_array)

        for angind in ang_array:
            print(angind)
            rps_goto(angind)

            time.sleep(wait_time)
            # Collect some data
            tstart = time.time()
            while (time.time()-tstart < rest):
                data_row = [angind,
                            dmm.getAIN(0,differential=True),
                            dmm.getAIN(2, differential=True)]

                daq_data = daq_data.append(pd.DataFrame([data_row],
                            columns=daq_data.keys().to_list()),
                            ignore_index=True)

        time.sleep(1)
        rps_home()
        time.sleep(1)

        print("saving to "+filename)
        save_csv(daq_data,filename)
