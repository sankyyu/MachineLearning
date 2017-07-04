#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 21:20:03 2017

@author: Sanky
"""

#import the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def file2matrix(filename):
    fr=open(filename)
    arrayOfLines=fr.readlines()
    numberofLines=len(arrayOfLines)
    returnMat=[]
    classLabelVector=[]
    index=0
    for line in arrayOfLines:
        line=line.strip()
        listFromLine=line.split('\t')
        listFromLine[0:3]=[float(i) for i in listFromLine[0:3]]
        returnMat.append(listFromLine[0:3])
        classLabelVector.append(listFromLine[-1])
        index+=1
    returnMat=np.array(returnMat)
        
    return returnMat,classLabelVector



#Importing the dataset
x,y=file2matrix('datingTestSet.txt')



#Encoding categoricl data
from sklearn.preprocessing import LabelEncoder
labelencoder_y=LabelEncoder()
y=labelencoder_y.fit_transform(y) 


#from sklearn.preprocessing import StandardScaler
#sc=StandardScaler()
#x=sc.fit_transform(x)
#from sklearn.preprocessing import scale
#x=scale(x,with_std=False)
#x=sc.fit_transform()

def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    m=dataSet.shape[0]
    normDataSet=np.zeros(m)
    normDataSet=dataSet-np.tile(minVals,m)
    normDataSet=normDataSet/np.tile(ranges,m)
    return normDataSet

for i in range(len(x[0,:])):
    x[:,i]=autoNorm(x[:,i])

#splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(x,y,test_size=0.2,random_state=0)



#Fitting K-NN to the Training set
def KNNclassify(inX,dataSet,labels,k):
    dataSize=dataSet.shape[0]
    diffMat=np.tile(inX,(dataSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistIndices=distances.argsort()
    classCount={}
    max=0
    print("=============")
    for i in range(k):
        index=np.where(sortedDistIndices==i)
        label=labels[index][0]
        print(label)
        
        classCount[label]=classCount.get(label,0)+1
        if(classCount[label]>max):
            max=classCount[label]
            maxLabel=label
    return maxLabel


res=[]
for inX in X_test:
    res.append(KNNclassify(inX,X_train,Y_train,3))

# Making the Confusion Matrix
#from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(Y_test, res)
#confusion_matrix()

acu=res-Y_test
accuracy=1-np.count_nonzero(acu)/200

print('////////////////////////////////////////')

#using sklearn method
from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
classifier.fit(X_train, Y_train)

Y_pred = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred)



        

    
    
    
    

