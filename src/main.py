import json
import numpy as np
import math
import sys
import cv2
from scipy.io.wavfile import write
import subprocess

directory = sys.argv[1]

rate = 44100
frame_rate = 30.0

freqs = []
'''
base_freqs = [130.813, 155.563, 164.814, 174.614, 184.997, 195.998, 233.082, 246.942]

for i in range(8):
    for j in range(len(base_freqs)):
        freqs.append(base_freqs[j] * (2 ** i))
freqs.append(base_freqs[0] * (2 ** 8))
'''

base_freqs = [130.813, 146.832, 164.814, 195.998, 220.000]

for i in range(8):
    for j in range(len(base_freqs)):
        freqs.append(base_freqs[j] * (2 ** i))
freqs.append(base_freqs[0] * (2 ** 8))


freq_offset = -10


def tone(freq, length, gain):
    slen = int(length * rate)
    t = float(freq) * np.pi * 2.0 / rate
    gain_lst = []
    for i in range(slen):
        gain_lst.append(gain * (1.0 - math.exp(-10.0 * (slen - i - 1) / slen)))
    return np.sin(np.arange(slen) * t) * np.array(gain_lst)

def tone_rich(freq, length, gain):
    return (tone(freq, length, gain * 0.7) + tone(freq * 2, length, gain * 0.2) + tone(freq * 4, length, gain * 0.1)) * 32768.0

def play_wave(stream, samples):
    stream.write(samples.astype(np.int16).tobytes())

def frequency(value):
    return freqs[(value + 64) // 4 + freq_offset]
    #base_freq = 440.00
    #return base_freq * 2.0 ** (value // 2 / 12)

with open(directory + '/game.json', encoding='utf-8-sig') as f:
    raw_data = json.load(f)

with open(directory + '/time.txt') as f:
    times = [float(elem) for elem in f.read().splitlines()]
    times.append(-1)

fixed_time = 15.0
sum_time = sum(times)
mul = fixed_time / sum_time

data = []
for move in range(4, 65):
    try:
        value = raw_data[str(move)]['value']
        if times[move - 4] != -1:
            data.append([value, max(1.0 / frame_rate, times[move - 4] * mul)])
        else:
            data.append([value, 1.0])
    except:
        continue

while frequency(data[-1][0]) / base_freqs[0] - round(frequency(data[-1][0]) / base_freqs[0]) > 0.1:
    freq_offset -= 1
#freq_offset += 1
print(freq_offset, frequency(data[-1][0]))

audio_data = []
for d, t in data:
    audio_data.extend(tone_rich(frequency(d), t, 1.0).astype(np.int16))
    #play_wave(stream, tone_rich(frequency(d), t, 1.0))
    print(d, frequency(d), t)

write(directory + '/audio.wav', rate, np.array(audio_data))





writer = cv2.VideoWriter(directory + '/video.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), frame_rate, (1920, 1080))
idx = 0
for d, t in data:
    file = directory + '/' + str(idx) + '.jpg'
    print(file)
    img = cv2.imread(file)
    for i in range(round(t * frame_rate)):
        writer.write(img)
    idx += 1
writer.release()


cmd = 'ffmpeg -i ' + directory + '/video.mp4 -i ' + directory + '/audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 ' + directory + '/out.mp4' 
print(cmd)

subprocess.run(cmd)