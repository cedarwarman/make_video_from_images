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

import argparse
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
