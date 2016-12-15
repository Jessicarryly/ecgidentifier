import wfdb

import matplotlib.pyplot as plot 
from scipy  import signal as sci
import math
import detect_beats as detector
import tensorflow as tf
import random
from sklearn import svm
import numpy as np
import os

sample_rate=1000;
w_c=sample_rate*2*math.pi

w_l=(30*2*math.pi)/w_c #1Hz
w_h=(600*2*math.pi)/w_c #800Hz

ecg_length=600
evidence_vec =10
seed =1
percentage_used_for_training=0.5
current_id =0
training_set = []
test_set = []


basepath='..//wfdb_data//physiobank//database//ptbdb//'
basepath=os.path.realpath(basepath)
with open(basepath+'//CONTROLS') as f:

    for file in f:
        file=file.strip('\n')
        if(file =='patient180/s0545_re'): #ignore this sample
            continue
        
        sig, fields = wfdb.rdsamp(basepath+'//'+file)
        
        print(file)
        
        nrow,ncol= sig.shape
        
        b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba')
        
        
        ecgs=detector.FindEcgPeriods(sig[:,0],sample_rate) 
        
        r_peak_after=300
        w_l=(30*2*math.pi)/w_c #1Hz
        w_h=(600*2*math.pi)/w_c #800Hz
        b,a =sci.butter(1, [w_l, w_h], 'bandpass', False, 'ba') #remove drift
        
        
        
        indices=random.sample(range(0,len(ecgs)),len(ecgs))
        maximum = int(percentage_used_for_training*len(ecgs))

        for ecg in range(0,maximum):
            ecgs[ecg].ReMapEcgData(r_peak_after,ecg_length)
            #print("length", len(data))
            normalized=sci.filtfilt(b, a, ecgs[ecg].Signal)
            tuple=current_id, normalized
            
            training_set.append(tuple)
            
        for ecg in range(maximum,len(ecgs)):
            ecgs[ecg].ReMapEcgData(r_peak_after,ecg_length)
            #print("length", len(data))
            normalized=sci.filtfilt(b, a, ecgs[ecg].Signal)
            
            #test_set.append(normalized)
            
            tuple=current_id, normalized
            test_set.append(tuple)
            
         

    
       
      
        seed+=1
        current_id+=1   

gammas=np.logspace(0.001,10,10,base=10)
accuracy = []
for gamma_val in gammas:
    print('current gamma',gamma_val)
    classifier = svm.SVC(kernel='poly',gamma=gamma_val)
    
     
      
    classifier.fit([item[1] for item in training_set],
                   [item[0] for item in training_set])
    
    predicted=classifier.predict([item[1] for item in test_set])
    print(predicted)
                                        
    accuracy.append(np.mean([item[0] for item in test_set] == predicted))

plot.plot(gammas,accuracy)
plot.show
