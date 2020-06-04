# -*- coding: utf-8 -*-
"""
Created on Thu May 21 13:17:14 2020

This is a curve fitting program. You can snip a png file and it will pop out a 4th order RC network thermal model values. 

@author: Joshua Quintero
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class ThermalCurveFit:
    
    
    def __init__(self):
        self.file_name = "t.png"
        self.ymin = .001
        self.ymax = 1000
        self.xmin = .001
        self.xmax = 1000
        self.clip = 1000
        
        #guess it
        self.g = [1,1,1,1]

        #bounds
        self.b = ((0,0,0,0),(np.inf,np.inf,np.inf,np.inf))
        
        self.pre = [0,0,0,0,0,0,0,0]
        
    def setFileName(self,file):
        self.file_name = file
    def setXAxis(self,_xmin,_xmax):
        self.xmin = _xmin
        self.xmax = _xmax
    def setYAxis(self,_ymin,_ymax):
        self.ymin = _ymin
        self.ymax = _ymax
    def setClip(self,_clip):
        self.clip = _clip
        
    def snipGraph(self):
        image = plt.imread(self.file_name)[:,:,:3]
        #plt.imshow(image) ####
        image -= image.mean(axis = 2).reshape(image.shape[0], image.shape[1], 1).repeat(3, axis = 2)

        im_maxnorm = image.max(axis=2)

        # Find y-position of remaining line
        ypos = np.ones((image.shape[1])) * np.nan
        for i in range(im_maxnorm.shape[1]):
            if im_maxnorm[:,i].max()<0.01:
                continue
            ypos[i] = np.argmax(im_maxnorm[:,i])
        # Pick only values that are set
        ys = 1-ypos[np.isfinite(ypos)]
        
        self.y_px_max = image.shape[0]
        #plt.imshow(image) #####
        return ys
    
    def collectData(self):
        ys = self.snipGraph()
        #print(ys)
        self.scale_per_y = (self.y_px_max)/np.log10(self.ymax/self.ymin)
        self.ydecades = np.log10(self.ymax/self.ymin)
        self.scale_per_x = (len(ys))/np.log10(self.xmax/self.xmin)
        self.n = len(ys)
        #curve fit the first 2 decades
        self.len_2_dec = int(np.log10(100)*self.scale_per_x)
        self.xtest_low = np.ones(self.len_2_dec)
        self.ytest_low = np.ones(self.len_2_dec)
        self.xtest = np.ones(len(ys))
        self.ytest = np.ones(len(ys))
        
        m_y = (np.log10(self.ymax) - np.log10(self.ymin))/self.y_px_max
        b_y =  np.log10(self.ymin)
        m_x = (np.log10(self.xmax) - np.log10(self.xmin))/len(ys)
        b_x =  np.log10(self.xmin)

        #fill up arrays with proper data information
        for i in range(self.n):
            self.xtest[i] = 10**(m_x*i+b_x)
            #self.xtest[i] = np.power(10,i/(self.scale_per_x))*self.xmin
            
            self.ytest[i] = 10**(m_y*(self.y_px_max+ys[i])+b_y)
            #self.ytest[i] = np.power(10,(self.y_px_max+ys[i])/(self.scale_per_y))*self.ymin
    
        for i in range(self.len_2_dec):
            self.xtest_low[i] = 10**(m_x*i+b_x)
            #self.xtest_low[i] = np.power(10,i/(self.scale_per_x))*self.xmin
            
            self.ytest_low[i] = 10**(m_y*(self.y_px_max+ys[i])+b_y)
            #self.ytest_low[i] = np.power(10,(self.y_px_max+ys[i])/(self.scale_per_y))*self.ymin
        
        self.original = self.ytest.copy()
        #clip
        self.ytest = np.clip(self.ytest, a_min = 0, a_max = self.clip)

        
    def model_low (self,t, r0,t0,r1,t1):
        return r0+r1  -r0*np.exp(-t/(t0))-r1*np.exp(-t/(t1))
    
    def model (self,t, r0,t0,r1,t1):
        return r0 + r1 + self.c_low[0] + self.c_low[2] -r0*np.exp(-t/(t0))-r1*np.exp(-t/(t1)) -self.c_low[0]*np.exp(-t/(self.c_low[1])) -self.c_low[2]*np.exp(-t/(self.c_low[3]))

        
    def full_model (self,t, cl,ch):
        return cl[0]+cl[2] + ch[0] + ch[2]  -cl[0]*np.exp(-t/(cl[1]))-cl[2]*np.exp(-t/(cl[3])) -ch[0]*np.exp(-t/(ch[1]))-ch[2]*np.exp(-t/(ch[3])) 
    
    def curveFit(self):
        self.collectData()
        self.c_low, self.cov_low, self.c, self.cov = np.empty(4)
        self.c_low, self.cov_low = curve_fit(self.model_low,self.xtest_low,self.ytest_low, self.g, bounds = self.b, method = 'trf')
        self.c, self.cov = curve_fit(self.model,self.xtest,self.ytest,self.g,bounds = self.b, method = 'trf')

    def runModel(self):
        self.mod = []
        self.mod = np.empty(self.n)
        for i in range (self.n):
            self.mod[i] = self.full_model(self.xtest[i], self.c_low,self.c)
            
    def graph(self):
        
        plt.loglog(self.xtest,self.original, basex=10,basey=10)
        plt.loglog(self.xtest,self.mod,'ro', basex=10,basey=10)
        
    def compute(self):
        self.curveFit()
        self.runModel()
        
        self.pre = [self.c_low[0],self.c_low[1]/self.c_low[0],self.c_low[2],self.c_low[3]/self.c_low[2],self.c[0],self.c[1]/self.c[0],self.c[2],self.c[3]/self.c[2]]
        print('.param r0 = ',self.c_low[0],'\n.param c0 = ',self.c_low[1]/self.c_low[0],
        '\n.param r1 = ',self.c_low[2], '\n.param c1 = ',self.c_low[3]/self.c_low[2],
        '\n.param r2 = ',self.c[0], '\n.param c2 = ',self.c[1]/self.c[0],
        '\n.param r3 = ',self.c[2], '\n.param c3 = ',self.c[3]/self.c[2])