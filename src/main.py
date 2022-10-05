import pyaudio
import json
import numpy as np

RATE = 44100

BPM = 100
L1 = (60 / BPM * 4)
L2,L4,L8 = (L1/2,L1/4,L1/8)

C,D,E,F,G,A,B,C2 = (
        261.626, 293.665, 329.628, 
        349.228, 391.995, 440.000,
        493.883, 523.251)

def tone(freq, length, gain):
    slen = int(length * RATE)
    t = float(freq) * np.pi * 2 / RATE
    return np.sin(np.arange(slen) * t) * gain

def play_wave(stream, samples):
    stream.write(samples.astype(np.float32).tobytes())

def frequency(value):
    value += 64
    return 100 + value * 2

with open('2022_10_02_14_15_33.json', encoding='utf-8-sig') as f:
    raw_data = json.load(f)

data = []
for move in range(4, 65):
    value = raw_data[str(move)]['value']
    data.append(value)
print(data)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, frames_per_buffer=1024, output=True)

for datum in data:
    play_wave(stream, tone(frequency(datum), 0.1, 1.0))
    print(datum)

stream.close()