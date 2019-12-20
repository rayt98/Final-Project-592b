import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile 

from ipywidgets import interactive
import scipy

from IPython.display import Audio, display

file= scipy.io.wavfile.read("file_example_WAV_5MG.wav")
print(file)
fs = 44100 # define the sampling rate, f_s = 44.1 kHz

t_start = 0 # We start sampling at t = 0s
t_stop =  3 # We stop sampling at t = 1s

ns = (t_stop - t_start) * fs + 1

x = np.linspace(t_start, t_stop, ns)


f1 = 440 # frequency of y_1(t)
f2 = 220 # frequency of y_2(t)

y1 = np.sin(2*np.pi*f1*x)
y1= np.array([i*2**16 for i in y1]).astype(np.int16)
y2 = np.sin(2*np.pi*f2*x)
y1= np.array([i*2**16 for i in y2]).astype(np.int16)

y1_plus_y2 = y1+y2

scipy.io.wavfile.write("first_sample.wav",fs,y1)
k =scipy.io.wavfile.read("first_sample.wav")
print(k)
scipy.io.wavfile.write("second_sample.wav",fs,y2)
scipy.io.wavfile.write("third_sample.wav",fs,y1_plus_y2)


