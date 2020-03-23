#!/usr/bin/env python3

#########################################################
#  make_movie_from_images
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
Takes a folder full of images, outputs a movie. Designed to take micro-manager
time lapse output in 12 bit tif format. Not sure how this will work with other
inputs, but might be a good place to start.

Usage:

make_movie_from_images.py
    -i <input_image_dir>
    -o <output_image_dir>
    -t # Flag to include timestamp
    -z <interval_in_ms> # Only used if -t present, interval between images
    -b <buffer_in_ms> # Only used if -t present, time from start to first frame
"""


import glob
import os
import argparse
import numpy as np
from PIL import Image


# Setting up arguments
parser = argparse.ArgumentParser(description='make_movie_from_images')
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
parser.add_argument('-b',
                    '--buffer',
                    type=int,
                    help=('Use with -t. Time between plating and video start, in ms'))
args = parser.parse_args()


### Import image
def import_img(file):
    img = Image.open(file)
    return img


### Converting from 12 to 8 bit
def convert_img(img):
    # Grabbing the min and max for the conversion.
    array_min = np.amin(img)
    # You might have to figure out a better conversion solution to fix the
    # flickering. Here's using a fixed interval, as opposed to below
    array_max = 3300
    #array_max = np.amax(img)
    
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
     

### Here's the main
def main():
    os.chdir(args.input_dir)
    temp_folder_name = "temp_movie_frame_output"
    os.mkdir(temp_folder_name)
    
    for file in glob.glob("*.tif"):
        print("Converting " + file)
        image = import_img(file)
        image = convert_img(image)
        output_save_path = os.path.join(args.input_dir, temp_folder_name, file)
        image.save(output_save_path)


if __name__== "__main__":
  main()
