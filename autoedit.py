#import statements
from moviepy.editor import *
import cv2
import os
import torch
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Takes in a VALORANT videofile and creates a new video containing just your kills from the file. Changing values may result in errors')
parser.add_argument('--input_file', type=str,  help='the video file you want modified')
parser.add_argument('--frame_freq', type=float, default= 1.5, help="how many frames per your fps the program checks, so if the input file runs at 60 fps and this value is one, every 60 frames will be checked for a kill. Increasing this number will result in great wait times whereas decreasing will have faster load times but less accurate kill detection")
parser.add_argument('--output_file', type=str, default= "output.mp4", help="the name of the file that you want your program written to, the file type will always be .mp4 no matter what you put, if you don't enter something then the output file will just be output.mp4 which will overwrite any other files named that")
parser.add_argument('--kill_con', type=float, default= 0.7, help="a value from 0-1 for how confident the program is that your frame contains a kill. Recommended to keep this at default")
parser.add_argument('--death_conf', type=float, default= 0.6, help="a value from 0-1 for how confident the program is that you are dead in a frame. Recommended to keep this at default")
parser.add_argument('--multikill', type=float, default=2.0, help="how close multiple kills must be to each other for them to be combined into one clip stored in seconds. Default is 2")
parser.add_argument('--killb', type=float, default=2.0, help= "the time in seconds shown before a kill. Default is 2")
parser.add_argument('--killa', type=float, default=2.0, help="the time in seconds shown after a kill. Default is 2")

args = parser.parse_args()
INPUT_FILE = args.input_file
assert INPUT_FILE != None , "please put an input file"
FREQ = args.frame_freq
OUTPUT = args.output_file
K = args.kill_con
D = args.death_conf
MIN = args.multikill
TB = args.killb
TA = args.killa

#using yolov5 weights, check if a frame contains a kill
def is_kill(frame) :
    i = 0
    resized = cv2.resize(frame, (416, 416))
    results = model(resized)
    trueResults = results.pandas().xyxy[0].to_numpy()
    if (trueResults.size > 3) :
        for x in range(0, len(trueResults)) :
            if trueResults[x][5] == 1 and trueResults[x][4] > K :
                i += 1
            if trueResults[x][5] == 0 and trueResults[x][4] > D :
                return False
    if (i > 0) :
        return True
    return False


#loading videos
cap = cv2.VideoCapture(INPUT_FILE)
video = VideoFileClip(INPUT_FILE)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/goat.pt')

#loading frame directory
if not os.path.exists('data'):
    os.makedirs('data')

#setup variables
currentframe = 0
kills = []
fps = round(cap.get(cv2.CAP_PROP_FPS))
#print(fps)

# go through video
while (cap.isOpened()):
    ret, frame = cap.read()

    if ret:
        # every x frame, check for a kill and if so add to a array
        if (currentframe % round((fps/FREQ)) == 0) :
            #cv2.imwrite('./data/frame' + str(currentframe) + '.jpg', frame)
            if (is_kill(frame)) :
                kills.append(currentframe)
        
        currentframe += 1
    else:
        break

cap.release()
cv2.destroyAllWindows()

# put kills array into proper format to make video
w = 1
min = kills[0]
while w < len(kills) :
    if kills[w] < (min + (MIN*round(fps))) :
        min = kills[w]
        kills.pop(w)
    else :
        kills.insert(w, min + (MIN*round(fps)))
        min = kills[w + 1]
        w += 2
        
# make video
#print(kills)
if round(kills[0] / fps) - TB <= 0 :
    clip1 = video.subclip(0, round(((kills[1] - fps * TA, 2) / fps)))
else :
    clip1 = video.subclip(round((kills[0] - fps * TB) / fps, 2), round(((kills[1] - fps * TA) / fps), 2))
kills.pop(0)
kills.pop(0)

if len(kills) > 0 :
    p = 0
    while p in range(0, len(kills) - 2) :
        newclip = video.subclip(round((kills[p] - fps * TB) / fps, 2), round((kills[p + 1] - fps * TA) / fps, 2))
        clip1 = concatenate_videoclips([clip1, newclip])
        p += 2

if round(kills[len(kills) - 1]) + fps * TA > currentframe :
    newclip = video.subclip(round((kills[len(kills) - 1] - fps * TB) / fps, 2), round(currentframe / fps, 2))
else :
    newclip = video.subclip(round((kills[len(kills) - 1] - fps * TB)/ fps, 2), round((kills[len(kills) - 1] + fps * TA) / fps, 2))
clip1 = concatenate_videoclips([clip1, newclip])
#write videofile
clip1.write_videofile(OUTPUT)
