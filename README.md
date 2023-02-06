# Valorant-auto-editor
Automatically takes in a valorant video or clip and edits it down to just a kills that were by the person recording.

Here's how it works:

1. Loads the video into opencv
2. Runs every FPS/(user given amount via argument)th frame through a custom trained yolov5 model with a manually labeled 10K image dataset
3. If the frame contains a kill and the player isn't spectating, that frame is added a list
4. The frames are sorted down into clips 
5. A video is processed using moviepy

# Important Info

I've tested it on a 40 minute video and it took about 15 mins to run, however the longer the video the longer it will take to run.

All necessary libraries are listed at the top imports.

It uses python.

Use -h to learn more about arguments

# Example of ending video
https://user-images.githubusercontent.com/40571030/162643614-1b6b5125-5b90-48f1-9d9f-18a049e3f5a9.mp4

