import random
import numpy as np
import simpleaudio as sa
from time import sleep 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--tempo', type=int, default=120, help='Set tempo in bpm')
parser.add_argument('--chords', default=['all'], nargs='+',
                                 choices=['major','minor','seventh','all'])
args = parser.parse_args()

# set bpm
bpm = args.tempo 

if bpm <= 0:
    parser.error("--tempo must be a positive number")

print("Tempo: ", bpm)

major_chords = ['A','B','C','D','E','F','G']
minor_chords = [f"{i}m" for i in major_chords]
seventh_chords = [f"{i}7" for i in major_chords]

chord_map = {'major': major_chords, 'minor': minor_chords, 'seventh': seventh_chords}

if 'all' in args.chords:
    chords = major_chords + minor_chords + seventh_chords
else:
    chords = []
    for choice in args.chords:
        chords += chord_map[choice]

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

while True:
    try:
        # play 4 clicks per bar, print a new chord on the downbeat
        audio = generate_click()

        sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
        sleep(60/bpm)
        sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
        sleep(60/bpm)
        sa.play_buffer(audio, 1, 2, SAMPLE_RATE)  
        sleep(60/bpm)
        sa.play_buffer(audio, 1, 2, SAMPLE_RATE)

        print("\033[A                             \033[A")  # clear previous chord
        print(random.choice(chords)) # print new chord
        sleep(60/bpm)
    except KeyboardInterrupt:
        print("\nStopped")
        break
