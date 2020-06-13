# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 12:12:55 2020

@author: mankleh
"""
import numpy as np
import math as m
import matplotlib.pyplot as plt

def Bretscheider(Centroids):
    """Plots the Bretscheider wave distribution for all centroids"""
    name = "Bretscheider Distribution"
    fr = np.array(np.arange(0.01,1.75,0.01), dtype=float)
    Hs = np.array(Centroids[0], dtype=float)
    Ts = np.array(Centroids[1], dtype=float)

    Fs = 1/Ts
    S = np.zeros([len(Hs),len(fr)],dtype=float)
    
    for i, current_Fs in enumerate(Fs):
        for j, current_fr in enumerate(fr):
            a = 5/16
            S[i,j] = a * ((Fs[i]**4)/(fr[j]**5)) * (Hs[i]**2) * m.exp(-5*(((Fs[i]**4)/(fr[j]**5))))
        
    return(S, name)

def JONSWAP(Centroids):
    """Plots the Bretscheider wave distribution for all centroids"""
    fr = np.array(np.arange(0.01,2,0.01), dtype=float)
    Hs = np.array(Centroids[0], dtype=float)
    Ts = np.array(Centroids[1], dtype=float)

    Fs = 1/Ts
    S = np.zeros([3,len(fr)],dtype=float)
    a = 0 
    g  = 9.81
    gamma = 3.3
    for i, current_Fs in enumerate(Fs):
        for j, current_fr in enumerate(fr):
            
            if fr[j] <= Fs[i]:
                sigma = 0.07
                r  = - (fr[j] - Fs[i])**2 /(2*(sigma**2)*(Fs[i]**2))
                S[i,j] = (a*(g**2)/(fr[j]**5)) * m.exp(-(5/4)*((Fs[i]/fr[j]))) * gamma**r
            else:
                sigma = 0.09
                r  = - (fr[j] - Fs[i])**2 /(2*(sigma**2)*(Fs[i]**2))
                S[i,j] = (a*(g**2)/(fr[j]**5)) * m.exp(-(5/4)*((Fs[i]/fr[j]))) * gamma**r
        
    return(S)

def Dist_Vis(Centroids,S, name):
    fr = np.array(np.arange(0.01,1.75,0.01), dtype=float)
    Hs = np.array(Centroids[0], dtype=float)
    Ts = np.array(Centroids[1], dtype=float)
    
    l = ['']*len(Hs)
    
    for i in range(len(Hs)):
        l[i] = str(Hs[i])+' m, '+str( Ts[i])+' sec'

    plt.figure() 
    for i in range(len(S)):
        plt.plot(fr,S[i,:])
        
    plt.title(name)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Wave Spectral Density [rad/sec]')
    plt.legend(l)
    plt.show()

