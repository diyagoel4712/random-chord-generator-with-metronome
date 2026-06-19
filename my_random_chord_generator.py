# my random chord generator
import random
import numpy as np
import simpleaudio as sa
import os
from time import sleep 

# set bpm
bpm = 60

major_chords = ['A','B','C','D','E','F','G']
minor_chords = []
seventh_chords = []

chords = major_chords + minor_chords + seventh_chords

SAMPLE_RATE = 44100

def generate_click(freq=800,dur=0.03,volume=0.5,decay=35):
    """ 
    builds a click as a numpy array pulse code modulation

    IN: freq: frequency of click (Hz)
        dur: length of click (s)
        volume: volume between 0.0 and 1.0
        decay: how fast the envelope fades out
    """
    # get x-axis values defined by sample_rate
    n_samples = int(SAMPLE_RATE * dur)
    x_values = np.linspace(0,dur,n_samples, endpoint=False)
    
    # get corresponding y-axis values (sine wave): y =  2.pi.f.x 
    y_values = np.sin(2*np.pi*freq*x_values)

    # build filter envelope (e^-x)
    envelope = np.exp(-x_values*decay)

    # combine
    click = y_values*envelope*volume

    # convert to 16-bit pcm
    audio = (click*32767).astype(np.int16)

    return audio

for i in range(100):
    audio = generate_click()

    sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
    sleep(60/bpm)

    sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
    sleep(60/bpm)

    sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
    sleep(60/bpm)

    sa.play_buffer(audio, 1, 2, SAMPLE_RATE) 
    os.system('clear') 
    print(random.choice(chords))
    sleep(60/bpm)
    




