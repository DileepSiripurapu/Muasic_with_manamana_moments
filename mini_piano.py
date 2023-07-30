import pygame
import os
import time
from timeit import default_timer as time_time
def piano():
    pygame.init()
    pygame.mixer.set_num_channels(20)
    timer = pygame.time.Clock()
    FPS = 60
    played_keys = []
    key_names = []
    time_positions=[]
    time_differences=[]
    activity= False

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    previous = None

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 250
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(('gray'))


    KEY_WIDTH = SCREEN_WIDTH // 10
    KEY_HEIGHT = SCREEN_HEIGHT
    KEYS_X = 0



    song_notes = []
    key_sounds={}

    finger_names = ["left pinky","left ring","left middle","left index","left thumb","right thumb"
                   , "right index","right middle","right ring","right pinky"]



    print("Enter 'NO' if you don't want any key to assign")
    for i in range(10):
        key_name = input(f"Enter name for key {finger_names[i]}: ")
        key_names.append(key_name)




    for key_name in key_names:
        sound_file = os.path.join("assets/notes", f"{key_name}.wav")
        key_sound = pygame.mixer.Sound(sound_file)
        key_sounds[key_name] = key_sound


    font = pygame.font.Font(None, 36)
    key_rects=[]
    for i, key_name in enumerate(key_names):
        key_rect = pygame.Rect(KEYS_X, 0, KEY_WIDTH, KEY_HEIGHT)
        pygame.draw.rect(screen, WHITE, key_rect)
        pygame.draw.rect(screen, BLACK, key_rect, 3,5)
        key_text = font.render(key_name, True, BLACK)
        text_rect = key_text.get_rect(center=key_rect.center)
        screen.blit(key_text, text_rect)
        key_rects.append(key_rect)
        KEYS_X += KEY_WIDTH
    pygame.display.flip()
    ################################
    running = True
    while running:
        timer.tick((FPS))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                for i, key_rect in enumerate(key_rects):   
                    if key_rect.collidepoint(mouse_pos):
                        if previous is not None:
                            pygame.draw.rect(screen,"black",previous,3)
                        pygame.draw.rect(screen, "green", key_rect, 3)
                        previous = key_rect
                        key_sounds[key_names[i]].play()
                        if activity:
                            if(key_names[i]!='NO'):
                                played_keys.append(key_names[i])
                                time_positions.append(time_time())

            elif event.type == pygame.KEYDOWN:
                if previous is not None:
                    pygame.draw.rect(screen,"black",previous,3)
                if(event.key == pygame.K_0):
                    key_sounds[key_names[9]].play()
                    if activity: 
                        if(key_names[9]!='NO'):
                            played_keys.append(key_names[9])
                            time_positions.append(time_time())
                    pygame.draw.rect(screen,"green",key_rects[9],3)
                    previous = key_rects[9]
                elif(event.key >=49 and event.key<=57):
                    key_sounds[key_names[abs(49-event.key)]].play()
                    if activity: 
                        if(key_names[abs(49-event.key)]!='NO'):
                            played_keys.append(key_names[abs(49-event.key)])
                            time_positions.append(time_time())
                    pygame.draw.rect(screen,"green",key_rects[abs(49-event.key)],3)
                    previous = key_rects[abs(49-event.key)]  
                if event.key==pygame.K_s:
                    time_position=[0]
                    song_name = input("Enter the name of the song: ")
                    file_path = os.path.join("text_files", song_name)
                    played_keys = []
                    activity = True 
                if event.key == pygame.K_e:
                    if len(played_keys)!=0:
                        with open(file_path, 'w') as f:
                            f.write(' '.join(key_names)+"\n")
                            f.write(' '.join(played_keys)+"\n") 
                            for i in range(len(time_positions)-1):
                                time_differences.append(str(abs(time_positions[i]-time_positions[i+1])))
                            f.write(' '.join(time_differences))
                        activity = False
                        played_keys=[]
                if event.key == pygame.K_q:
                    runner = False

        pygame.display.flip()

    pygame.quit()
#g4,a4,b4,c5,d5
