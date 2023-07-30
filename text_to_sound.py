import os
import pygame
import time
from timeit import default_timer as time_time
def t2s():
    key_sounds={}
    files = os.listdir("text_files/")
    print(*files,sep="\n")
    song_name = input("Enter the song name from your saved files above:: ")
    with open(f'text_files/{song_name}') as f:
        lines = f.readlines()
        key_names=lines[0]
        song_notes=lines[1]
        time_gaps=lines[2]

    pygame.init()
    pygame.mixer.set_num_channels(20)

    key_names=list(map(str,key_names.split()))
    song_notes=list(map(str,song_notes.split()))
    time_gaps=list(map(float,time_gaps.split()))
    time_gaps.insert(0,0)

    for key_name in key_names:
        sound_file = os.path.join("assets/notes", f"{key_name}.wav")
        key_sound = pygame.mixer.Sound(sound_file)
        key_sounds[key_name] = key_sound

    song_notes_index=0

    while song_notes_index<len(song_notes):
        time.sleep(time_gaps[song_notes_index])
        key_sounds[song_notes[song_notes_index]].play()
        song_notes_index+=1

    time.sleep(time_gaps[-1])
    key_sounds[song_notes[-1]].play()
    pygame.quit()

