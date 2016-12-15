import matplotlib.pyplot as plot 
import numpy as np
import scipy
from scipy  import signal as sci
import math


def FindEcgPeriods(ecg_band,sample_rate,ecg_window=1.0):
   
    rawecg=ecg_band
    ecg_window=ecg_window*sample_rate
    w_c=sample_rate*2*math.pi

    
   
    w_l=(20*2*math.pi)/w_c #10Hz
    w_h=(50*2*math.pi)/w_c #30Hz
    b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
    ecg_band=sci.filtfilt(b, a, ecg_band)
   
    
    w_l=(15*2*math.pi)/w_c #10Hz
    b,a =sci.butter(2, w_l, 'low', False, 'ba')

    ecg_diffed=scipy.diff(ecg_band)
    ecg_diffed=ecg_diffed/max(ecg_diffed)
    ecg_diffed = np.clip(ecg_diffed,0.5,1)
    
    
    #peaks= peakutils.indexes(ecg_diffed)
    peaks=FindTurningPoints(ecg_diffed)
    
    r_peaks=Find_peak_inRange(ecg_band, peaks)
    r_peaks_refined=[]
    prev=0
    for r in r_peaks:
        if((r-prev) < ecg_window*0.1):
            continue
            
        r_peaks_refined.append(r)    
        prev=r;
        
        
    r_peaks = r_peaks_refined

   
    
   
    
    
    ecgs=[]
  
    for i in range(len(r_peaks)-1):
        curr_distance=r_peaks[i+1]-r_peaks[i]
        if(curr_distance > ecg_window):
            curr_distance=ecg_window
       
        endpos=peaks[i]+curr_distance/2
        start_pos=peaks[i]-curr_distance/2
        
        
        
     
        if(endpos > len(rawecg)):
            endpos=len(rawecg)
            
        if(start_pos < 0):
            start_pos=0
            
       
        try:
            ecgs.append(EcgPeriod(rawecg[start_pos:endpos],sample_rate))
        except:
            print'Could not create ecg'

    return ecgs


def Find_peak_inRange(signal,peakrange,window=500):
    peaks=[]
 
    for i in peakrange:
        
        sliceend=i+window
        


        if(sliceend > (len(signal)-1)):
            sliceend=len(signal)-1
            
        if(sliceend-i < window/2):
            continue
       
        sliced = signal[i:sliceend]

        peaks.append(FindTurningPoints(sliced)[0]+i)
        
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
        self.__Original=ecg_single_rythm

        self.__findEcgData()
    
    def __findEcgData(self):
 
        w_c=self.SampleRate*2*math.pi
        w_l=(20*2*math.pi)/w_c #10Hz
        w_h=(50*2*math.pi)/w_c #30Hz
        b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
        ecg_band=sci.filtfilt(b, a, self.Signal)
        ecg_diffed=scipy.diff(ecg_band)
        ecg_diffed=ecg_diffed/max(ecg_diffed)
        ecg_diffed = np.clip(ecg_diffed,0.5,1)
        peaks=FindTurningPoints(ecg_diffed)
        self.R_Peak=Find_peak_inRange(ecg_band, peaks)[0]


        
        
    def ReMapEcgData(self,target_r_peak_position,targetDataPoints):
        offset=self.R_Peak-target_r_peak_position
        
             
        #print('length',len(sliced),'offset',offset)
        self.Signal= sci.resample(self.__Original, targetDataPoints)
       # print(len(self.Signal))
        
        self.__findEcgData()
        offset=self.R_Peak-target_r_peak_position
        self.R_Peak=target_r_peak_position
        self.Signal = np.roll(self.Signal,-offset)
          
       # plot.plot(self.Signal)
        #plot.scatter(self.R_Peak,self.Signal[self.R_Peak])
        #plot.show()
       # print(len(self.Signal))

        
        