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

CHUNK = 1024*5
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

 
waveforms = []
i = 0
while True:
    i+=1
    data = stream.read(CHUNK)
    waveform = np.frombuffer(data, dtype=np.int16)
    waveforms.append(waveform)
    if i > 10:
        #x, y = get_xy(np.hstack(waveforms[-10:]))
        x, y = get_xy(waveform)
        if i == 11:
            figure, ax = plt.subplots(figsize=(20, 5))
            line1, = ax.plot(x, y)
            plt.xlim([0, 2200])
            plt.ylim([0, 14000000])
            ax.set_xticks([row.frequency for _, row in xticks.iterrows()])
            ax.set_xticklabels([row.note for _, row in xticks.iterrows()])
            for name, note in [("A2", 110), ("A3", 220), (330, 330), ("A4", 440), 
            (660, 660), ("A5", 880), (1100, 1100)]:
                plt.axvline(x=get_closest_frequency(x, note), alpha=0.2,
                    color='k', linestyle='--', label=name)

            
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Magnitude")
            plt.title("Frequencies For Geeks", fontsize=20)

        line1.set_xdata(x)
        line1.set_ydata(y)

        figure.canvas.draw()
        figure.canvas.flush_events()
        
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()