#!/bin/bash
file=`basename "$1"`
echo $file
#ffmpeg -i "$1" -codec:a libmp3lame -qscale:a 2 "$2"
ffmpeg -i "$1" -codec:a libmp3lame -b:a 192k "${2}${file}.mp3"
