import board as eeg_headset
import cv2
import time
import numpy as np
import random

sample_count = 60
gui_name = "data trainer"
dir_name = "data_set_forward_yaw_right_empty"
com_port = "/dev/ttyUSB0"

current_sample_count = [0,0,0,0,0,0,0,0,0]
#directions = ["forward","backward","up","down","yaw left", "yaw right", "left", "right", "empty"]
directions = ["forward", "yaw right", "empty"]

def generate_random():
    return random.randint(0,len(directions)-1)

def generate_random_list():
    dir_list = []

    for i in range(sample_count * len(directions)):
        print("i = ", i)

        random = generate_random()

        while dir_list.count(random) >= sample_count:
            random = generate_random()

        dir_list.append(random) 

    return dir_list

directions_list = generate_random_list()

def sample_data(direction):

    frame_count = 0
    recording = False
    cap = None
    sample = None
    start_time = 30

    if direction == "forward":
        cap = cv2.VideoCapture('media/drone_forward.mp4')
    elif direction == "backward":
        cap = cv2.VideoCapture('media/drone_back.mp4')

    elif direction == "up":
        cap = cv2.VideoCapture('media/drone_up.mp4')
    elif direction == "down":
        cap = cv2.VideoCapture('media/drone_down.mp4')

    elif direction == "yaw left":
        cap = cv2.VideoCapture('media/drone_turn_left.mp4')
    elif direction == "yaw right":
        cap = cv2.VideoCapture('media/drone_turn_right.mp4')

    elif direction == "left":
        cap = cv2.VideoCapture('media/drone_left.mp4')
    elif direction == "right":
        cap = cv2.VideoCapture('media/drone_right.mp4')

    elif direction == "empty":
        cap = cv2.VideoCapture('media/drone_hover.mp4')

    while(cap.isOpened()):
        ret, frame = cap.read()
        time.sleep(1/50)
        
        if frame_count == start_time:
            eeg_headset.start_data_stream()
            recording = True

        elif frame_count == start_time + 65:
            sample = eeg_headset.stop_data_stream()
            recording = False

        if ret:
            cv2.putText(frame, str(current_sample_count) + " samples complete from " + str(sample_count) + " samples", (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
            cv2.putText(frame, "Think about the drone moving: "  + str(direction), (50,500), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 

            if recording:
                cv2.putText(frame, "recording now!", (50,100), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 

            cv2.imshow(gui_name,frame)

        else:
            cap.release()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    eeg_headset.save_sample(sample,direction)

home_image = cv2.imread("media/home.png")
image_width, image_height, channels = home_image.shape
cv2.putText(home_image, "Welcome to the data trainer. Please press any key to continue", (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.imshow(gui_name, home_image)
cv2.waitKey(0) 

home_image = cv2.imread("media/home.png")
cv2.putText(home_image, "This program will help you to train our models to recoginize your brain pattern", (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.putText(home_image, "In order to do this correctly it is important that you are completely focussed on this task!", (50,100), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.putText(home_image, "During the traning this program will show you a animation of a drone", (50,150), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.putText(home_image, "Your task is to move this drone forward by thinking about commanding it to move forward", (50,200), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.putText(home_image, "You can do this by looking at the drone and commanding in your mind 'move forward' ", (50,250), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.putText(home_image, "if you are ready then lets begin by pressing any key!", (50,300), cv2.FONT_HERSHEY_SIMPLEX , 1, (0, 0, 255), 3, cv2.LINE_AA) 
cv2.imshow(gui_name, home_image)
cv2.waitKey(0) 

eeg_headset.connect_to_headset(com_port)
eeg_headset.create_directory(dir_name)

for i in directions_list:

    print("direction = " + str(directions[i]))
    current_sample_count[i] += 1
    sample_data(directions[i])
