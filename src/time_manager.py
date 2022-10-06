from time import time, sleep
import subprocess
import sys
from othello_py import *

level = int(sys.argv[1])
use_book = int(sys.argv[2])
ai_player = int(sys.argv[3])
file = sys.argv[4]

#egaroucid = subprocess.Popen(('Egaroucid6_test.exe ' + str(level)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
egaroucid = subprocess.Popen(('Egaroucid6_test.exe ' + str(level) + ' ' + str(use_book)).split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)

sleep(3.0)

times = []
transcript = ''

o = othello()
while True:
    former_player = o.player
    if not o.check_legal():
        o.player = 1 - o.player
        if not o.check_legal():
            break
    o.print_info()
    if o.player == ai_player or ai_player == 2:
        grid_str = str(o.player) + '\n'
        for yy in range(hw):
            for xx in range(hw):
                if o.grid[yy][xx] == black:
                    grid_str += '0'
                elif o.grid[yy][xx] == white:
                    grid_str += '1'
                else:
                    grid_str += '.'
            grid_str += '\n'
        #print(grid_str)
        egaroucid.stdin.write(grid_str.encode('utf-8'))
        egaroucid.stdin.flush()
        s = time()
        _, coord = egaroucid.stdout.readline().decode().split()
        elapsed = time() - s
    else:
        s = time()
        coord = input('your turn: ')
        elapsed = time() - s
    y = int(coord[1]) - 1
    x = ord(coord[0]) - ord('a')
    times.append(elapsed)
    transcript += coord
    o.move(y, x)

egaroucid.kill()

with open(file, 'w') as f:
    for elem in times:
        f.write(str(elem) + '\n')
print(transcript)