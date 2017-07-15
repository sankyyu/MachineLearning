#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 13:54:58 2017

@author: Sanky
"""

import matplotlib.pyplot as plt
import numpy as np


x=np.linspace(-1,1,3)
y=2*x+1
plt.figure()
plt.plot(x,y)
plt.show()