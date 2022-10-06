import pyaudio
import json
import numpy as np

rate = 44100

def tone(freq, length, gain):
    slen = int(length * rate)
    t = float(freq) * np.pi * 2.0 / rate
    return np.sin(np.arange(slen) * t) * gain

def tone_rich(freq, length, gain):
    return tone(freq, length, gain * 0.7) + tone(freq * 2, length, gain * 0.2) + tone(freq * 4, length, gain * 0.1)

def play_wave(stream, samples):
    stream.write(samples.astype(np.float32).tobytes())

def frequency(value):
    base_freq = 440.00
    return base_freq * 2.0 ** (value / 12)

with open('2022_10_02_14_15_33.json', encoding='utf-8-sig') as f:
    raw_data = json.load(f)

data = []
for move in range(4, 65):
    value = raw_data[str(move)]['value']
    data.append(value)
print(data)


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, frames_per_buffer=1024, output=True)

for datum in data:
    play_wave(stream, tone_rich(frequency(datum), 0.1, 1.0))
    print(datum, frequency(datum))

stream.close()