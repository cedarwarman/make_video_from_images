# make_movie_from_images
This repository makes a movie, with optional time stamp, from µManager time lapse image output.

---

## Contents
*make_movie_from_images.py*  
Use this script to make a movie from µManager time lapse output.
<br>
````
    -i <input_image_dir>
    -o <output_image_dir>
    -t # Flag to include timestamp
    -z <interval_in_ms> # Only used if -t present, interval between images
    -s <buffer_in_s> # Only used if -t present, time from start to first frame
````

## Requirements
pillow  
ffmpeg-python  
numpy  

## Example installation and use on an HPC with Conda, rclone/Google Drive, and SLURM

**Setting up an environment**

````
conda create -n make_movie_from_images python=3.9 ffmpeg ffmpeg-python numpy pillow
````

<br> **Downloading files from Google Drive with rclone**

````
rclone copy gdrive_me:/Imaging_videos_hypoploids/2021_zip_files_not_processed . --drive-shared-with-me -v
````

<br> **Unzipping the files**

````
7za x '*.zip'
````

<br> **Running for a single folder of images**
<br> Note: not having a slash for the output directory is important, it makes the output video name with os.path.basename, which will return an empty string if there's a trailing slash.
````
python ~/scripts/make_movie_from_images/python/make_movie_from_images.py -i /xdisk/rpalaniv/cedar/images_to_movies/20210304/2_17_2021_5/Default/ -o /xdisk/rpalaniv/cedar/images_to_movies/20210304/2_17_2021_5 -t -z 500 -s 840
````
