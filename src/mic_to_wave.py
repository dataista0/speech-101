#!/usr/bin/env python
# coding: utf-8

import pyaudio
import numpy as np
import pandas as pd
import scipy.fft
import matplotlib.pyplot as plt

def get_closest_frequency(frequency, freq):
    idx = np.argmin(np.abs(frequency - freq))
    return frequency[idx]

# here we are creating sub plots


scale = pd.read_csv("../data/music_scale.csv")

def is_major(note):
    return '#' not in note and 'b' not in note

def is_chosen(note):
    return note in ['A2', 'A3']

xticks = scale[((scale['note'].apply(is_major)) \
                 & (scale['frequency'] < 2200) \
                 & (scale['frequency'] > 260)) | scale['note'].apply(is_chosen)]

#xticks.loc[xticks['note'].str.contains("3"), 'note'] = xticks['note'].str[:-1]




def get_xy(waveform):

    ft = scipy.fft.fft(waveform)
    magnitude = np.absolute(ft)
    frequency = np.linspace(0, RATE, len(magnitude)) 
    x = frequency[:4000]
    y = magnitude[:4000]# / 1e7
    return x, y

CHUNK = 1024*8
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
#RECORD_SECONDS = 10

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
plt.ion()

 
#waveforms = []
i = 0
while True:
    i+=1
    data = stream.read(CHUNK)
    waveform = np.frombuffer(data, dtype=np.int16)
    #waveforms.append(waveform)
    if i > 10:
        #x, y = get_xy(np.hstack(waveforms[-10:]))
        
        x1, y1 = get_xy(waveform)
        
        n = len(waveform)
        n_small = int(n/2)
        waveform = waveform[-n_small:]
        
        x2 = list(range(0, len(waveform)))
        y2 = waveform
        if i == 11:
            #plt.tight_layout()
            figure, (ax1, ax2) = plt.subplots(2, 1, figsize=(15,8))
            
            #figure, ax = plt.subplots()
            line1, = ax1.plot(x2, y2)
            
            line2, = ax2.plot(x1, y1)
            #plt.xlim([0, 2200])
            ax1.set_ylim([-10000, 10000])
            
            ax2.set_xlim([0, 2200])
            ax2.set_ylim([0, 14000000])
            ax2.set_xticks([row.frequency for _, row in xticks.iterrows()])
            ax2.set_xticklabels([row.note for _, row in xticks.iterrows()])
            for name, note in [("A2", 110), ("A3", 220), (330, 330), ("A4", 440), 
            (660, 660), ("A5", 880), (1100, 1100)]:
                ax2.axvline(x=get_closest_frequency(x1, note), alpha=0.2,
                    color='k', linestyle='--', label=name)

            
            #ax1.set_xlabel("Time")
            ax1.set_ylabel("Magnitude")
            ax1.set_title("Waveform")
            
            ax2.set_xlabel("Frequency [Hz]")
            ax2.set_ylabel("Magnitude")
            ax2.set_title("Frequency activations")

        line1.set_xdata(x2)
        line1.set_ydata(y2)
        
        line2.set_xdata(x1)
        line2.set_ydata(y1)

        figure.canvas.draw()
        figure.canvas.flush_events()
        
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()