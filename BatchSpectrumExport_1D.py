# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:04:52 2020

@author: zheng
"""

import pandas
import numpy
import os
import os.path
numpy.set_printoptions(threshold=numpy.inf)
#import matplotlib.pyplot as plt

#%%
# define a function to get all the .pck file names (except extension) in a given path
# you can replace "pck" to any other extension to get the corresbonding name
def GetPCKName(dir):
    listName = []
    for fileName in os.listdir(dir):  
        if os.path.splitext(fileName)[1] == '.pck':
            fileName = os.path.splitext(fileName)[0]
            listName.append(fileName)
    return listName
#%%
# get all the .pck file names (except extention) in a given path
Allfiles = GetPCKName(r'C:\Users\zheng\Desktop\PhD_project\QD15009\QD15009_LD10\Attodry\QD4_FSS_tuning\Larger_BiasVolt')
# change current direction
os.chdir('C:\\Users\\zheng\\Desktop\\PhD_project\\QD15009\\QD15009_LD10\\Attodry\\QD4_FSS_tuning\\\Larger_BiasVolt')

FileNo = len(Allfiles)
#%%
for ExpFileNo in range(FileNo):
    # put the .pck file in the same document as this script and enter the name below
    df = pandas.read_pickle(Allfiles[ExpFileNo]+'.pck')['Andor_spectrum']
    
    # read the number of pixels
    v_x =  numpy.sort(numpy.array(list(set(numpy.array(df.index.tolist())[:,0]))))
    #nx = len(v_x)
    nx = 91
    
    # read the resolution of the CCD from the first spectrum file
    resolution = 1024
    
    # create variables for the data
    spectra = numpy.zeros((nx, resolution, 2))
    data = numpy.zeros((1, nx))
    # read spectra
    data_energies = numpy.array(df.index.tolist())[:,1]
    data_energies.shape = (nx, resolution)
    data_spectra = numpy.array(df.values.tolist())
    data_spectra.shape = (nx, resolution)
    spectra[:, :, 0] = 1239.841842144513 / data_energies
    spectra[:, :, 1] = data_spectra
    
    # remove the cosmic ray
    CosmicRay = 1*(data_spectra>350)
    CRPosition = numpy.where(CosmicRay==1)
    #try:
    #    data_spectra[CRPosition[0],CRPosition[1]] = data_spectra[CRPosition[0],CRPosition[1]-1]
    #except:
    #    print("Cosmic ray is on the edge pixels.")
    data_spectra[CRPosition[0],CRPosition[1]] = data_spectra[CRPosition[0],CRPosition[1]-1]
    
    # the background range should be chosen accordingly
    BackGround = numpy.mean(data_spectra[:,0:236])
    data_spectra = data_spectra-BackGround
    
    # export the files, both .asc and .txt are possible
    if ExpFileNo == 0:
        # export the spectrum data, x axis, y axis
        numpy.savetxt('spectra_'+Allfiles[ExpFileNo]+'.asc',(data_spectra))
        numpy.savetxt('energy.asc',(spectra[:, :, 0]))
        numpy.savetxt('angle.asc',(v_x))
    else:
        # export the rest spectrum data
        numpy.savetxt('spectra_'+Allfiles[ExpFileNo]+'.asc',(data_spectra))

