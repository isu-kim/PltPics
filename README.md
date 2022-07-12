

# PltPics
A simple script that draws picture into `matplotlib.pyplot` using bezier curves.

## Special Thanks To
kevinjycui for https://github.com/kevinjycui/DesmosBezierRenderer

## Installation
1. Git clone this repository
2. `pip install -r requirements.txt`
3. `sudo apt-get install ffmpeg`
4. `sudo apt update`
5. `sudo apt install git python3-dev python3-pip build-essential libagg-dev libpotrace-dev pkg-config`
6. `jupyter notebook` and run scripts

## Features
### Photo to Graph
This feature can be achieved by `DrawImage.ipynb`

*My profile image converted*

![New Project](https://user-images.githubusercontent.com/49092508/178396834-84758ad6-c4c0-4cba-b49a-e800c6bc23e8.png)


### Video to Graphs
This feature can be achieved by `ProcessVideo.ipynb`

*Noot Noot Meme converted*

https://user-images.githubusercontent.com/49092508/178396814-b96c4db0-2a02-4ac2-bd77-f50044d49a21.mp4

## How is this possible?
1. Extract frames of video by [ffmpeg](https://ffmpeg.org)
1. Convert image to vector images using [pypotrace](https://pypi.org/project/pypotrace/).
2. Represent those contours using Bezier curves.
3. Use `matplotlib.pyplot` to draw Bezier curves using some features.
4. Save those `pyplot`s into images. 
5. Use [ffmpeg](https://ffmpeg.org) to turn those images into video.
