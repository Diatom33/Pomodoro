from time import sleep
import os
import json
# import sys


# the preset formatting is somewhat weird, 
# will probably switch to pickles at some point
def fix_json_tags(inputfile: dict[str, list[str | float]]):
    """
    fixes the fact that cycle indices are ints, but
    in json they must be strings
    """
    outputfile: dict[int, list[str | float]] = {}
    for k, v in inputfile.items():
        outputfile[int(k)] = v
    return outputfile

use_preset = ''
while not use_preset in ['y', 'n']: 
    use_preset = input('use preset?(y/n)')
if use_preset=='y':
    print('\n'+'\n'.join(item[:-5] for item in os.listdir('presets'))+'\n')
    preset_name = input('choose a preset from the list:') + '.json'
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

beeping: str = ''
while not beeping in ['y','n']:
    beeping = input('beep at end of cycle?(y/n)')

if beeping=='y':
    # set up beeping
    from playsound import playsound
    beepsound='resources/beep-07a.wav'


popup: str = ''
while not popup in ['y','n']:
    popup = input('show popup at end of cycle?(y/n)')
if popup == 'y':
    from platform import system
    os_name=system()
    if os_name == 'Linux':
        from subprocess import Popen
        def popup_func(prev_cycle: str, next_cycle: str): # type: ignore
            Popen([
                'notify-send',
                '--app-name="Pomodoro"',
                '--action=okay',
                '--wait',
                '--urgency=critical',
                'End of ' + prev_cycle + ', beginning of ' + next_cycle + '.',

            ])
    if os_name=='Windows':
        import ctypes
        def popup_func(prev_cycle: str, next_cycle: str): # type: ignore
            ctypes.windll.user32.MessageBoxW( # type: ignore
                0, 
                'End of ' + prev_cycle + ', beginning of ' + next_cycle + '.',
                'Pomodoro', 
                0x00001000
                )
    if os_name=='Darwin':
        def popup_func(*_):
            print("sorry, popups are't supported on Mac yet. Bug me about this")

    

while True:
    for i in range(cycle_count): # type: ignore
        print('starting '  +cycles[i][0])  # type: ignore
        print('sleeping')
        sleep(60*cycles[i][1]) # type: ignore
        if beeping == 'y':
            playsound(beepsound, block=True) # type: ignore 
        if popup == 'y':
            popup_func(cycles[i][0], cycles[(i+1) % cycle_count][0]) # type: ignore
            