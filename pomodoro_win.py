from time import sleep
import ctypes
import os
import json
from winsound import Beep

use_preset = ''
def fix_json_tags(file: dict):
    outputfile = {}
    for k in file.keys():
        outputfile[int(k)] = file[k]
    return outputfile

while not use_preset in ['y', 'n']: 
    use_preset = input('use preset?(y/n)')
    if use_preset=='y':
        print(os.listdir('presets'))
        preset_name = input('choose a preset from the list (without extension)') + '.json'
        json = json.load(open('presets/' + preset_name, 'r'))
        cycles = fix_json_tags(json)
        cycle_count = len(cycles)
    elif use_preset=='n':
        cycle_count = int(input('cycle count:'))
        cycles = {}
        for i in range(cycle_count):
            cycles[i]=[]
            cycles[i].append(input('cycle ' + str(i+1) + ' name:'))
            cycles[i].append(float(input('cycle ' + str(i+1) + '  duration (minutes):')))
        save_as_preset = ''
        while not save_as_preset in ['y', 'n']:
            save_as_preset = input('save as preset?(y/n)')
            if save_as_preset == 'y':
                preset_name = input('preset name?(without extension)')
                if os.path.exists('presets/' + preset_name+ '.json'):
                    dump_mode = 'w'
                else:
                    dump_mode = 'x'
                json.dump(cycles, open('presets/' + preset_name+ '.json', dump_mode))

beeping = ''
while not beeping in ['y','n']:
    beeping = input('beep at end of cycle?(y/n)')

while True:
    for i in range(cycle_count):
        print('starting '  +cycles[i][0])
        print('sleeping')
        sleep(60*cycles[i][1])
        if beeping == 'y':
            Beep(1000, 600)
        print('popup')
        ctypes.windll.user32.MessageBoxW(0, 'end of cycle ' + cycles[i][0] + ', beginning of cycle ' + cycles[(i+1) % cycle_count][0], "Pomodoro", 0x00001000)