from time import sleep
import os
import json

use_preset = ''
def fix_json_tags(inputfile: dict[str, list[str | float]]):
    outputfile: dict[int, list[str | float]] = {}
    for k, v in inputfile.items():
        outputfile[int(k)] = v
    return outputfile

while not use_preset in ['y', 'n']: 
    use_preset = input('use preset?(y/n)')
    if use_preset=='y':
        print('\n'.join(item[:-5] for item in os.listdir('presets')))
        preset_name = input('choose a preset from the list') + '.json'
        inputfile = json.load(open('presets/' + preset_name, 'r'))
        cycles = fix_json_tags(inputfile)
        cycle_count = len(cycles)
    elif use_preset=='n':
        cycle_count=''
        while not isinstance(cycle_count, int):
            cycle_count = int(input('cycle count:'))
        cycles: dict[int,list[str | float]] = {}
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
popup = ''
while not popup in ['y','n']:
    popup = input('show popup at end of cycle?(y/n)')

while True:
    for i in range(cycle_count): # type: ignore
        print('starting '  +cycles[i][0])  # type: ignore
        print('sleeping')
        sleep(60*cycles[i][1]) # type: ignore
        if beeping == 'y':
            pass
        print('popup')
        if popup == 'y':
            pass
            # Popen([
            #     'notify-send',
            #     '--app-name="Pomodoro"',
            #     '--action="OKAY"',
            #     '--wait',
            #     '--urgency=critical',
            #     'end of cycle ' + cycles[i][0] + ', beginning of cycle ' + cycles[(i+1) % cycle_count][0],

            # ])