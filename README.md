# make_movie_from_images
This repository makes a movie, with optional time stamp, from µManager time lapse image output.

---

## Contents
*make_movie_from_images.py*  
Use this script to make a movie from µManager time lapse output.

## Requirements
pillow  
ffmpeg-python  
numpy  

## Example installation and use on an HPC with Conda, rclone/Google Drive, and SLURM

Setting up an environment

````
conda create -n make_movie_from_images python=3.9 ffmpeg ffmpeg-python numpy pillow
````

<br> Downloading files from Google Drive with rclone

````
rclone copy gdrive_me:/Imaging_videos_hypoploids/2021_zip_files_not_processed . --drive-shared-with-me -v
````

<br> Unzipping the files

````
7za x '*.zip'
````
