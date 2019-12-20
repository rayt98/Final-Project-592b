import numpy as np
import math
from scipy import signal

def cpp(audio,Fs, F0,N_periods,sample_shift):
    N_periods = N_periods#getting the period from the global settings
    sampleshift = sample_shift
    
    CPP= np.zeros(len(F0),1)
    N_ms = int(Fs/1000) 
    
    for k in range(1,len(F0)):
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
        yseg= yseg * np.hamming(len(yseg))
        YSEG= np.fft.fft(yseg)
        yseg_c = np.fft.ifft(math.log(abs(YSEG)))
        
        yseg_c = abs(yseg_c)
        
        yseg_c_db= 10*math.log10(yseg_c**2)
        
        yseg_c_db=yseg_c_db[1:math.floor(len(yseg)/2)]
        inx, prop= signal.find_peaks(yseg_c_db[N_ms:],wlen=2*N0_curr)
        vals= prop["peak_heights"]
        
        pos,pinx= min(abs(inx-N0_curr))
        
        if pinx != None:
            inx= inx[pinx[1]]
            vals = yseg_c_db[inx+N_ms-1]
            p = np.polyfit(range(N_ms,yseg_c_db),yseg_c_db[N_ms:],1)
            base_val= p[1]* (inx+N_ms-1)+p(2)
            CPP[k]= vals-base_val 
        
    return CPP

