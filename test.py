import wfdb
import numpy as np
import scipy
import scipy.ndimage
import matplotlib.pyplot as plot 
from scipy  import signal as sci
import math
import detect_beats as detector
from numpy import median
import biosppy.signals as ecgdetector

sample_rate=1000;
w_c=sample_rate*2*math.pi

w_l=(30*2*math.pi)/w_c #1Hz
w_h=(600*2*math.pi)/w_c #800Hz


basepath='//home//markus//Documents//Python//wfdb_data//physiobank//database//ptbdb//'
sig, fields = wfdb.rdsamp(basepath+'patient001//s0010_re')



nrow,ncol= sig.shape

b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')


ecgs=detector.FindEcgPeriods(sig[:,0],sample_rate) 

r_peak_after=200
for ecg in ecgs:
    offset=ecg.R_Peak-r_peak_after
    plot.plot(ecg.Signal[offset:])
   
    
plot.show()





