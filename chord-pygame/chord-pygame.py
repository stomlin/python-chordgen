# Generates chords randomly from an array (List of Lists) and
# plays them in realtime
#
# Change 'timeStep' to vary spacing between chords (in seconds)
#
#

# --> Now uses pygame.midi instead of rtmidi


import time
import random
import pygame
import pygame.midi

pygame.init()

pygame.midi.init()

print pygame.midi.get_default_output_id()
print pygame.midi.get_device_info(0)

midi_Output = pygame.midi.Output(0)
midi_Output.set_instrument(0)


# Defining chordStruct, a list of chords.
#
# Each chord is itself a list, with each integer showing its distance
# from the root note in semitones.
#


chordStruct = [

[0, 4, 7],

[0, 3, 7],

[0, 4, 7, 9],

[0, 2, 5, 7],

[1, 4, 7, 11],

[2, 5, 7, 9],

[0, 2, 7, 9]

    ]

# playChord function:
#
# 'position' is ascending from C, so:
#
# 0 = C
# 1 = C#
# 2 = D   etc...
#
# 'key' refers to a 'chord_x...' array which stores different formations
# of chords eg. Maj = 0, 4, 7  ... Min = 0, 3, 7 etc.
#
# 'octave' is the octave in which the chord is played
# Middle C is at 5 octaves in. Octave integer is multiplied by 12 to
# define the root note of the chord.
#
# So calling playChord(4, 0, 5) would send MIDI message for E major in
# the 5th Octave


def playChord(position, key, octave):

    chord = chordStruct[key]

    root = (octave*12) + position

    i = 0

    chordSize = len(chord)

    while i < chordSize:

        note = chord[i]

        chordMIDI = [0x90, root + note, 112]

        #midi_Output.write_short(chordMIDI)  ## not sure why this isn't working?

        ## had to use .note_on instead...

        midi_Output.note_on(root + note, 112, 0)
        

        i += 1

# stopChord function. Uses while loop to scan through all notes
# and sets all of their velocities to zero

def stopChord():

    i = 0
    
    while i<120 :
        notes_off = (0x90, i, 0)

        #again here...

        #midi_Output.write_short(notes_off)

        # .note_off instead...

        midi_Output.note_off(i, None, 0)

        i += 1

# Shockingly ugly main loop
# Just cycles throgh all the chords in the sequence until the counter reaches 999

counter = 0
mainRoot = 0

timeStep = 1

while counter < 1000:

    print(counter)

    

    
    

    if random.randint(0,30)>15:

        rootStep = random.randint(-5,5)
        
        mainRoot = mainRoot + rootStep

        chordSelect = random.randint(0,len(chordStruct)-1)

        

        playChord(mainRoot,chordSelect,5)

        print(chordStruct[chordSelect])

        time.sleep(timeStep)
        
        if mainRoot > 25:
            mainRoot = 0
            
    else :
        rootStep = random.randint(-5,5)
        
        mainRoot = mainRoot + rootStep

        chordSelect = random.randint(0,len(chordStruct)-1)

        if mainRoot < 1 :
            mainRoot = 20
            
        playChord(mainRoot-2,chordSelect,5)

        print(chordStruct[chordSelect])
        
        time.sleep(timeStep)

   

    counter += 1

    stopChord()

