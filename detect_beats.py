import wfdb
import numpy as np
import scipy
import scipy.ndimage
import scipy.stats
import matplotlib.pyplot as plot 
from scipy  import signal as sci
from collections import namedtuple
import math

from numpy import median

def detect_beats(ecg_band,sample_rate, ransac_window_size=5.0):
    EcgInfo=namedtuple('p','q','r','s''t');
    w_c=sample_rate*2*math.pi
    w_l=(10*2*math.pi)/w_c #10Hz
    w_h=(30*2*math.pi)/w_c #30Hz
    b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
    ecg_band=sci.filtfilt(b, a, ecg_band)
    ecg_diffed=scipy.diff(ecg_band);
    
    w_l=(15*2*math.pi)/w_c #10Hz
    b,a =sci.butter(2, w_l, 'low', False, 'ba')
    
    


    return [100]