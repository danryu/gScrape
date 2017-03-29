#!/bin/bash
#mkfifo outt.dat
sox "$1" outt.dat 
awk '$2 > 0.8 { print }' <  outt.dat > "$1.filepeaks.out"
rm outt.dat
