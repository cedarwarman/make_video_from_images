#!/usr/bin/env python3

#########################################################
#  make_video_from_images
#
#  Copyright 2020
#
#  Cedar Warman
#
#  Department of Botany & Plant Pathology
#  Oregon State University
#  Corvallis, OR 97331
#
# This program is not free software; it can be used and modified
# for non-profit only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#########################################################

"""
Takes a folder full of images, outputs a video. Designed to take micro-manager
time lapse output in 12 bit tif format. Not sure how this will work with other
inputs, but might be a good place to start.

Usage:

make_video_from_images.py
    -i <input_image_dir>
    -o <output_image_dir>
    -t # Flag to include timestamp
    -z <interval_in_ms> # Only used if -t present, interval between images
    -s <buffer_in_s> # Only used if -t present, time from start to first frame
"""


import glob
import os
import shutil
import argparse
import ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Setting up arguments
parser = argparse.ArgumentParser(description='make_video_from_images')
parser.add_argument('-i', 
                    '--input_dir',
                    type=str,
                    help=('Path to input directory'))
parser.add_argument('-o',
                    '--output_dir',
                    type=str,
                    help=('Path to output directory'))
parser.add_argument('-t',
                    '--timestamp',
                    action='store_true',
                    help=('Flag to include timestamp on video'))
parser.add_argument('-z',
                    '--interval',
                    type=int,
                    default=500,
                    help=('Use with -t. Interval between images, in ms'))
parser.add_argument('-s',
                    '--start_time',
                    type=int,
                    help=('Use with -t. Time between plating and video start, in s'))
args = parser.parse_args()


### Import image
def import_img(file):
    img = Image.open(file)
    return img


### Getting the max pixel value from all the images, for 8-12 bit conversion
def get_max_px(input_dir):
    os.chdir(input_dir)
    
    # This will hold the max pixel value across all the images
    max_px = 0
    print("Getting max px.......")

    for file in glob.glob("*.tif"):
        image = import_img(file)
        image_max_px = np.amax(image)

        if image_max_px > max_px:
            max_px = image_max_px

    print("max_px = " + str(max_px) + "\n")

    return max_px


### Converting from 12 to 8 bit
def convert_img(img, max_px = 3300):
    # Grabbing the min and max for the conversion.
    array_min = np.amin(img)
    array_max = max_px
    
    # I'm doing the conversion the same way ImageJ does it, which is linearly
    # scaling from the min-max of the input image to 0-255. Most of the images
    # I've looked at have a max of only ~3000, so this works well. Because 16
    # bit images can go up to 65,536, it's only using the very dark pixels.
    # That's probably why they all look black when opening them on a regular
    # computer. Not sure how to fix this on the microscope, might be a quirk of
    # the camera.
    converted_img = ((img - array_min)
                        * (1 / (array_max - array_min))
                        * 255).astype('uint8')

    # PIL won't recognize it as an image, because in the previous step I
    # converted it to an array. Converting it back into a PIL image here.
    converted_img = Image.fromarray(converted_img)

    return converted_img


### Adds a timestamp
def add_time_stamp(img, current_time, original_script_path):
    # Setting up the image size
    image_width, image_height = img.size

    # Setting up the fonts
    fonts_path = os.path.join(os.path.dirname(os.path.dirname(original_script_path)), 'fonts')
    font = ImageFont.truetype(os.path.join(fonts_path, 'arial.ttf'), 70)

    # Converting ms to minutes and seconds and setting up the print string
    seconds = (current_time/1000)%60
    seconds = int(seconds)
    minutes = (current_time/(1000*60))%60
    minutes = int(minutes)
    print_string = str(minutes).zfill(2) + "m " + str(seconds).zfill(2) + "s"
    
    ImageDraw.Draw(img).text((image_width - 300, image_height - 100), 
        print_string, 
        font = font,
        stroke_width = 1,
        stroke_fill = (255),
        align="left")  

    return(img)


### Makes a video
def make_video(input_dir, output_dir):
    # Making the input and output paths
    in_path = os.path.join(input_dir, '*.tif')

    output_file_name = str(os.path.basename(output_dir)) + ".mp4"
    out_path = os.path.join(output_dir, output_file_name)
    print("out path for the video is: ")
    print(out_path)

    # Using the ffmpeg bindings:
    (
        ffmpeg
        .input(in_path, pattern_type='glob', framerate=30)
        .output(out_path, vcodec='libx264', pix_fmt='yuv420p')
        .run()
    )

### Here's the main
def main():
    # Setting up the temporary processing folder
    original_script_path = os.path.abspath(__file__)
    os.chdir(args.input_dir)
    temp_folder_name = "temp_video_frame_output"

    # Making a directory to do all the processing in. This setup is for
    # testing, it shouldn't exist, and if it does you definitely shouldn't
    # delete it, which is eventually what's going to happen. Fix for the final
    # version.
    if not os.path.exists(temp_folder_name):
        os.mkdir(temp_folder_name)

    # Sets up the starting time for the first frame
    if args.timestamp:
        time = args.start_time * 1000
        print("timestamp activated, starting time = " + 
            str(time) +
            " ms")
    else:
        time = 0

    # Goes through all the images to find the max pixel value. Used for scaling
    # in the 16 to 8 bit conversion.
    max_px = get_max_px(args.input_dir)
    
    # Processing each frame
    for file in sorted(glob.glob("*.tif")):
        print("Processing " + file)
        image = import_img(file)
        image = convert_img(image, max_px)

        # Adding the timestamp
        if args.timestamp:
            print("Adding timestamp\n")
            image = add_time_stamp(image, time, original_script_path)
            time = time + args.interval

        output_save_path = os.path.join(args.input_dir, temp_folder_name, file)
        image.save(output_save_path)

    # Making the video
    video_input_dir = os.path.join(args.input_dir, temp_folder_name)
    make_video(video_input_dir, args.output_dir)

    # Deleting the temporary directory
    shutil.rmtree(video_input_dir)


if __name__== "__main__":
  main()
