
import numpy as np
import scipy
import peakutils
import matplotlib.pyplot as plot 
from scipy  import signal as sci
import math


def FindEcgPeriods(ecg_band,sample_rate):
    
    w_c=sample_rate*2*math.pi
    w_l=(30*2*math.pi)/w_c #1Hz
    w_h=(600*2*math.pi)/w_c #800Hz
    b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba') #remove drift
    original_ecg=sci.filtfilt(b, a, ecg_band)
    
   
    w_l=(10*2*math.pi)/w_c #10Hz
    w_h=(20*2*math.pi)/w_c #30Hz
    b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
    ecg_band=sci.filtfilt(b, a, ecg_band)
   
    
    w_l=(15*2*math.pi)/w_c #10Hz
    b,a =sci.butter(2, w_l, 'low', False, 'ba')

    ecg_diffed=scipy.diff(ecg_band)
    ecg_diffed=ecg_diffed/max(ecg_diffed)
    ecg_diffed = np.clip(ecg_diffed,0.3,1)
    #peaks= peakutils.indexes(ecg_diffed)
    peaks=FindTurningPoints(ecg_diffed)
    r_peaks=Find_peak_inRange(ecg_band, peaks)

    
    ecgs=[]
  
    for i in range(len(r_peaks)-1):
        curr_distance=r_peaks[i+1]-r_peaks[i]
        endpos=peaks[i]+curr_distance/2
        start_pos=peaks[i]-curr_distance/2
        if(endpos > len(original_ecg)):
            endpos=len(original_ecg)

        ecgs.append(EcgPeriod(original_ecg[start_pos:endpos],sample_rate))


    return ecgs


def Find_peak_inRange(signal,peakrange):
    peaks=[]
    
    for i in range(0,len(peakrange)-1,2):
        sliced = signal[peakrange[i]:peakrange[i+1]]
        peaks.append(FindTurningPoints(sliced)[0]+peakrange[i])
    return peaks


def FindTurningPoints(signal):
    tps=[]
    for i in range(0,len(signal)-2):
        if((signal[i]-signal[i+1] < 0) and (signal[i+1]-signal[i+2] > 0)):
            tps.append(i+1)
        
    return tps


class EcgPeriod:
    
  
    
    def __init__(self,ecg_single_rythm,sample_rate):
        self.R_Peak = 0
        self.Q_Peak =0
        self.S_Peak =0
        self.T_Peak =0
        self.P_Peak =0
        self.P_Start =0
        self.P_End =0
        self.T_Start =0
        self.T_End =0
        self.SampleRate = sample_rate
        self.Signal=ecg_single_rythm
        self.__findEcgData()
    
    def __findEcgData(self):
        w_c=self.SampleRate*2*math.pi
        w_l=(10*2*math.pi)/w_c #10Hz
        w_h=(20*2*math.pi)/w_c #30Hz
        b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
        ecg_band=sci.filtfilt(b, a, self.Signal)
        ecg_diffed=scipy.diff(ecg_band)
        ecg_diffed=ecg_diffed/max(ecg_diffed)
        ecg_diffed = np.clip(ecg_diffed,0.3,1)
        
        peaks=FindTurningPoints(ecg_diffed)
        self.R_Peak=Find_peak_inRange(ecg_band, peaks)[0]
        
        
        
        
        
    def MapEcgData(self,targetDataPoints):
        self.R_Peak = 0
        
        
        