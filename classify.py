from sklearn import svm
import numpy as np
import sklearn.metrics as metrics
from sklearn.metrics.classification import confusion_matrix

def do_classification(x_train,y_train,x_test,y_test, gamma_val, c_val):
    
    classifier = svm.SVC(kernel='rbf',gamma=gamma_val, C=c_val)
    classifier.fit(x_train,y_train)
    predicted=classifier.predict(x_test)
    accuracy=np.mean(y_test == predicted)   
    cfm=confusion_matrix(y_test,predicted)
    return accuracy, gamma_val, c_val, cfm