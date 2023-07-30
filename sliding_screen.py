import os
import pygame
import time as ttt

def moving_screen():
    files = os.listdir("text_files/")
    print(*files,sep="\n")
    song_name = input("Enter the song name from your saved files above:: ")
    with open(f'text_files/{song_name}') as f:
        lines = f.readlines()
        key_names=lines[0]
        dot_names=lines[1]
        time_gaps=lines[2]
    time_gaps=list(map(float,time_gaps.split()))
    dot_names = list(map(str,dot_names.split()))

    dot_times=[600]
    for t in time_gaps:
        dot_times.append(t*160)
    #print(dot_times)



    pygame.init()


    screen_width = 1350
    screen_height = 480
    fps=120
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Moving Dots")


    line_width = 2
    line_color = (255, 255, 255)
    vertical_line_x = screen_width // 4
    vertical_line_height = screen_height
    horizontal_line_y = screen_height // 2


    dot_size = 5
    dot_color = (0, 255, 0)
    dot_speed = 6
    dot_positions = []
    dot_distance = dot_times[1]
    x=100
    for i, time in enumerate(dot_times):
        x = x + time 
        dot_positions.append((x, horizontal_line_y, time, dot_names[i])) 


    clock = pygame.time.Clock()

    finished = False
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        for i, (x, y, time,name) in enumerate(dot_positions):
            x -= dot_speed
            name_x = x - dot_size
            name_y = y - dot_size
            dot_positions[i] = (x, y, time,name)

        screen.fill((0, 0, 0))
        pygame.draw.line(screen, line_color, (vertical_line_x, 0), (vertical_line_x, vertical_line_height), line_width)
        pygame.draw.line(screen, line_color, (0, horizontal_line_y), (screen_width, horizontal_line_y), line_width)
        for x, y, time , name in dot_positions:
            pygame.draw.circle(screen, dot_color, (x, y), dot_size)
            font = pygame.font.Font(None, 20)
            text = font.render(name, True, (255, 255, 255))
            screen.blit(text, (x-5-dot_size, y-20 - 2 * dot_size))
        pygame.display.update()
        if not finished:
            last_dot_x, _, _, _ = dot_positions[-1]
            if last_dot_x <= vertical_line_x:
                ttt.sleep(3)
                finished = True
        if finished:
            running= False
        clock.tick(fps)
    pygame.quit()
#moving_screen()
