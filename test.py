import wfdb

import matplotlib.pyplot as plot 
from scipy  import signal as sci
import math
import detect_beats as detector
import random

import numpy as np
import os
from joblib import Parallel, delayed
import classify

sample_rate=1000;
w_c=sample_rate*2*math.pi

w_l=(30*2*math.pi)/w_c #1Hz
w_h=(600*2*math.pi)/w_c #800Hz

ecg_length=600
evidence_vec =10
percentage_used_for_training=0.8
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
        
        
        
        random.shuffle(ecgs)
        
        maximum = int(percentage_used_for_training*len(ecgs))

        for ecg in range(0,maximum):
            ecgs[ecg].ReMapEcgData(r_peak_after,ecg_length)
            #print("length", len(data))
            normalized=sci.filtfilt(b, a, ecgs[ecg].Signal)
            normalized=normalized/(max(normalized))
            tuple=current_id, normalized
            
            training_set.append(tuple)
            
        for ecg in range(maximum,len(ecgs)):
            ecgs[ecg].ReMapEcgData(r_peak_after,ecg_length)
            #print("length", len(data))
            normalized=sci.filtfilt(b, a, ecgs[ecg].Signal)
            normalized=normalized/(max(normalized))
            #test_set.append(normalized)
            
            tuple=current_id, normalized
            test_set.append(tuple)
            
        print('Identifier',current_id)
        print('Number of samples', len(ecgs))
        print('Learning samples',maximum)
        print('test samples',len(ecgs)-maximum)
        print('###############################################################')
    

        current_id+=1   

gammas=np.logspace(-3,1,20,base=10)*4
cs=np.logspace(-3,1,20,base=10)*4
print(gammas)
print(cs)
res_matrix=np.empty([len(gammas), len(cs)])
random.shuffle(test_set)
random.shuffle(training_set)
random
curr_run =0
# res=Parallel(n_jobs=-1, verbose=5)(delayed(classify.do_classification)([item[1] for item in training_set],[item[0] for item in training_set],[item[1] for item in test_set],[item[0] for item in test_set],gamma_val,c_val) for c_val in cs for gamma_val in gammas)
# 
# accuracy, gamma, c, cfms = zip(*res) 
#  
#  
# for i in range(0,len(accuracy)):
#     curr_gamma = gamma[i]
#     curr_c=c[i]
#     gamma_idx=np.argwhere(gammas == curr_gamma)
#     c_idx = np.argwhere(cs == curr_c)
#     res_matrix[gamma_idx[0][0],c_idx[0][0]]=accuracy[i]
#        
# plot.imshow(res_matrix, cmap='hot', interpolation='nearest')
# ax = plot.gca()
# ax.set_xlabel(gammas) 
# ax.set_ylabel(cs) 
# plot.colorbar()
# plot.show()

predicted, gamma, c, cm=classify.do_classification([item[1] for item in training_set],[item[0] for item in training_set],[item[1] for item in test_set],[item[0] for item in test_set],0.5,9)
print(predicted)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plot.imshow(cm, cmap=plot.cm.Blues, interpolation='nearest')
ax = plot.gca()
plot.colorbar()
plot.show()



    