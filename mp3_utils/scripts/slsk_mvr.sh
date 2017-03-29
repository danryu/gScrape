#!/bin/bash
for i in *.mp3
 do 
#  echo $i
  date=$(echo $i | grep -o '[0-9]\{4\}[.-][0-9]\{2\}[.-][0-9]\{2\}')
  #echo $date
  if [[ $date != "" ]]
    then
     
      echo ">>>>>>>YEEEEAHHHHH"   "$i" /hd/music/GILLES_SORT/Sorted/2008/GillesPeterson_WorldWide_${date}.mp3
  fi
 done
