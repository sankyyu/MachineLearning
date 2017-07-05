#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 18:53:58 2017

@author: Sanky
"""

from math import log
import operator

def createDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels


def calcShannonEnt(dataSet):
    count={}
    for data in dataSet:
        label=data[-1]
        count[label]=count.get(label,0)+1
    shannonEnt=0.0
    for key in count:
        prob=count[key]/len(dataSet)
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    res=[]
    for data in dataSet:
        if data[axis]==value:
            newData=data[:axis]
            newData.extend(data[axis+1:])
            res.append(newData)
    return res

def chooseBestFeatureToSplit(dataSet):
    numOfFeatures=len(dataSet[0])-1
    baseEnt=calcShannonEnt(dataSet)
    bestInfoGain=0.0
    for i in range(numOfFeatures):
        featList=[example[0] for example in dataSet]
        featureSet=set(featList)
        infoGain=0.0
        newEnt=0.0
        
        for feature in featureSet:
            subds=splitDataSet(dataSet,i,feature)
            prob=len(subds)/float(len(dataSet))
            newEnt+=prob*calcShannonEnt(subds)
        infoGain=baseEnt-newEnt
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestLabel=i
    return bestLabel
        
def majorityCnt(aList):
    count={}
    for data in aList:
        count[data]=count.get(label,0)+1
    sortedCount=sort(count.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestLabel=labels[bestFeat]
    myTree={bestLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    featSet=set(featValues)
    for key in featSet:
        subLabels=labels[:]
        myTree[bestLabel][key]=createTree(splitDataSet(dataSet,bestFeat,key),subLabels)
    return myTree
    

def classify(inputTree,featLabels,testVec):
    featList=list(inputTree.keys())
    featStr=featList[0]
    subTree=inputTree[featStr]
    featNum=featLabels.index(featStr)
    feat=testVec[featNum]
    featValue=subTree[feat]
    if type(featValue)==dict:
        classLabel=classify(featValue,featLabels,testVec)
    else: classLabel=featValue
    return classLabel
        