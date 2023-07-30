import pygame
import os
import time
from timeit import default_timer as time_time
import cv2
import mediapipe as mp
import math
checker=None


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []
 
        self.text = ""
    
        self.pfingers = None
        self.p2fingers = None
        
        
    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {"lmList":[]}
                
                ## lmList
                xList, yList = [], []

                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    myHand["lmList"].append([px, py, pz])
                    xList.append(px)
                    yList.append(py)
 
                myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    xmin, ymin = min(xList), min(yList)
                    cv2.putText(img, self.text, (xmin - 30, ymin - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                    self.text = ""
                    
        if draw:
            return allHands, img
        else:
            return allHands
        

    def fingersUp(self, myHand):
        global checker
        #self.check = -1
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            # Thumb
            if myHandType == "Left":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        hand = myHandType
        finger = None
        if fingers.count(0) == 1:
            finger = fingers.index(0)
        
        if hand and finger is not None:
            ftypes = {0:"Thumb", 1:"Index", 2:"Middle", 3:"Ring", 4:"Pinky"}
            ftype = ftypes[finger]
                        
            if hand == "Left":
                finger = 4 - finger
            else:
                finger += 5
                            
            #self.text = f"{finger} - {hand}-{ftype}"
            self.text = f"{key_names[finger]}"
            if self.p2fingers == self.pfingers and self.pfingers != fingers:
                self.check=finger
                checker=self.check
                #print(self.check)
                #print(check)
                #print(self.text)
            else:
                checker=None

        self.p2fingers = self.pfingers
        self.pfingers = fingers

##################################################
def air_keyboard():
    global key_names
    #check=0
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
    
    ##################]
    a,b=None,None
    running = True
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    #runner=True
    ###################
    while running:
        timer.tick((FPS))
        ###########################
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img)  
        for hand in hands:
            _fingers = detector.fingersUp(hand)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
       
        b=checker
        if checker is not None and a!=b:
            if previous is not None:
                pygame.draw.rect(screen,"black",previous,3)
            key_sounds[key_names[checker]].play()
            if activity:
                if(key_names[checker]!='NO'):
                    played_keys.append(key_names[checker])
                    time_positions.append(time_time())
            pygame.draw.rect(screen,"green",key_rects[checker],3)
            previous = key_rects[checker]
        a=b
        

        ####################################
        if key == ord('q'):
            running=False
            #runner=False
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN):
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

            elif (event.type == pygame.KEYDOWN):
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
                    song_name = input("Enter the name of the tune: ")
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
    cv2.destroyAllWindows()
#g4,a4,b4,c5,d5

