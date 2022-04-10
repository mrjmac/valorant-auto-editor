# Valorant-auto-editor
Automatically takes in a valorant video or clip and edits it down to just a kills that were by the person recording.
This isn't being actively worked on, but if I do change something it's most like the ML model.
Here's how it works:
Loads the video into opencv
Runs every FPS/(user given amount via argument)th frame through a custom trained yolov5 model with a manually labeled 10K image dataset
If the frame contains a kill and the player isn't spectating, that frame is added a list
The frames are sorted down into clips 
A video is processed using moviepy


# Important Info
It uses python3 and was tested on ubuntu.
I've tested it on a 40 minute video and it took about 15 mins to run, however the longer the video the longer it will take to run.
This program is pretty CPU intensive as it uses a ML model to identify which kills are frames.
All necessary libraries are listed at the top imports.
Use -h to learn more about arguments
