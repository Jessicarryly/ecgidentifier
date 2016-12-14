import wfdb
import numpy as np
import scipy
import scipy.ndimage
import matplotlib.pyplot as plot 
from scipy  import signal as sci
import math
import detect_beats as detector
from numpy import median

sample_rate=1000;
w_c=sample_rate*2*math.pi

w_l=(30*2*math.pi)/w_c #1Hz
w_h=(600*2*math.pi)/w_c #800Hz


basepath='//home//markus//Documents//Python//wfdb_data//physiobank//database//ptbdb//'
sig, fields = wfdb.rdsamp(basepath+'patient001//s0010_re')



nrow,ncol= sig.shape

b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')


for col in range(0,ncol):   
    sig[:,col]=sci.detrend(sig[:,col])
    sig[:,col]=sci.filtfilt(b, a, sig[:,col])
   
pos=detector.detect_beats(sig[:,0],sample_rate) 

window_size=[]
   

for i in range(0,pos.size-1):
    window_size.append(pos[i+1]-pos[i])
    
si=median(window_size)
print window_size
for i in range(0,len(window_size)):
    plot.plot(sig[pos[i]-si/2:pos[i]+si/2,0])
plot.show()




