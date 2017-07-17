#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:02:36 2017

@author: Sanky
"""

import pandas as pd

r_cols=['user_id','movie_id','rating']
ratings=pd.read_csv('./data/u.data',sep='\t',names=r_cols,usecols=range(3),encoding='ISO-8859-1')

m_cols=['movie_id','title']
movies=pd.read_csv('./data/u.item',sep='|',names=m_cols,usecols=range(2),encoding='ISO-8859-1')

ratings=pd.merge(movies,ratings)

userRatings=ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')

#corrMatrix=userRatings.corr()
corrMatrix=userRatings.corr(method='pearson',min_periods=100)
myRatings=userRatings.loc[0].dropna()

simCandidates=pd.Series()
for i in range(0,len(myRatings.index)):
    print('Adding sims for '+ myRatings.index[i]+'...')
    sims=corrMatrix[myRatings.index[i]].dropna()
    sims=sims.map(lambda x: x * myRatings[i])
    simCandidates=simCandidates.append(sims)
    
simCandidates =simCandidates.groupby(simCandidates.index).sum()

simCandidates.sort_values(inplace=True,ascending=False)
filteredSims=simCandidates.drop(myRatings.index)