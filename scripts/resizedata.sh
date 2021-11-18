#!/bin/bash

#Terminal colors
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
reset=`tput sgr0`

OUTPUT_DIR=./smaller
OUTPUT_SIZE=432x322
FILE_TYPE=.png

echo "${green}Resizing Images${reset}"
mkdir ${OUTPUT_DIR}
magick mogrify -resize ${OUTPUT_SIZE} -quality 100 -path ${OUTPUT_DIR} *${FILE_TYPE}
