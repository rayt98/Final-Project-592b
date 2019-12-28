import numpy as np
import math
from scipy import signal

def cpp(audio,Fs,F0,N_periods,frame_shift):
    N_periods = N_periods#getting the period from the global settings
    sampleshift = Fs/1000*frame_shift
    
    CPP= np.zeros((len(F0),1))
    N_ms = int(Fs/1000) 
    
    for k in range(len(F0)):
        ks = int(k*sampleshift)
        
        if ks <= 0 or ks > len(audio):
            continue
        
        F0_curr = F0[k]
        
        if np.isnan(F0_curr)  or F0_curr == 0 : 
            continue
        
        N0_curr= Fs/F0_curr
        
        ystart= int(ks- N_periods/2*N0_curr)
        yend = int(ks+ N_periods/2*N0_curr)-1
        
        if(ystart <= 0):
            continue
        
        if(yend > len(audio)):
            continue

        
        yseg= audio[ystart:yend]
        yseg= yseg * np.hamming(len(yseg)) #Taking the hamming window
        YSEG= np.fft.fft(yseg) #Does the Fourier Transform
        yseg_c = np.fft.ifft(np.log(abs(YSEG))) #This line does the inverse fourier transform of the log of spectrum
        
        yseg_c = abs(yseg_c)
        
        yseg_c_db= 10*np.log10(yseg_c**2)
        
        yseg_c_db=yseg_c_db[1:math.floor(len(yseg)/2)]
        
        inx, _= signal.find_peaks(np.transpose(yseg_c_db[N_ms:]),wlen=2*N0_curr) # this a function for determining peaks and their indices
        
        
        pinx = np.argmin(abs(np.subtract(inx,N0_curr))) #Original code uses min to get the indices, not the min values
        
        if pinx != None:
            inx = inx[pinx]
            vals = yseg_c_db[inx+N_ms-1]
            p = np.polyfit(range(N_ms,len(yseg_c_db)),np.transpose(yseg_c_db[N_ms:]),1) #original code has ' meaning tranpose
            base_val= p[0]* (inx+N_ms-1)+p[1] # MATLAB indices start from 1, updated from original code
            CPP[k]= vals-base_val 
        
    return CPP

import pandas as pd
df = pd.read_csv("data1.csv") # These are parameters calculated by VoiceSauce for first_sample.wav 
saved_column = df["strF0"] #reads the F0 column
F0=list(saved_column) # Gets F0 using VoiceSauce

from scipy.io import wavfile
fs, data = wavfile.read("first_sample.wav")
cpps= cpp(data,fs,F0,5,1) #These are the default values of number of periods and frameshift on VoiceSauce
import sys
np.set_printoptions(threshold=sys.maxsize)
print(cpps) 
np.savetxt('cpps1.txt', cpps, delimiter=',')  #Writing the cpps values to a txt file


df = pd.read_csv("data2.csv") # These are parameters calculated by VoiceSauce for second_sample.wav 
saved_column = df["strF0"] #reads the F0 column
F0=list(saved_column) # Gets F0 using VoiceSauce

fs, data = wavfile.read("second_sample.wav")
cpps= cpp(data,fs,F0,5,1) #These are the default values of number of periods and frameshift on VoiceSauce
import sys
np.set_printoptions(threshold=sys.maxsize)
print(cpps) 
np.savetxt('cpps2.txt', cpps, delimiter=',')  #Writing the cpps values to a txt file

df = pd.read_csv("data3.csv") # These are parameters calculated by VoiceSauce for third_sample.wav 
saved_column = df["strF0"] #reads the F0 column
F0=list(saved_column) # Gets F0 using VoiceSauce

fs, data = wavfile.read("third_sample.wav")
cpps= cpp(data,fs,F0,5,1) #These are the default values of number of periods and frameshift on VoiceSauce
import sys
np.set_printoptions(threshold=sys.maxsize)
print(cpps) 
np.savetxt('cpps3.txt', cpps, delimiter=',')  #Writing the cpps values to a txt file
