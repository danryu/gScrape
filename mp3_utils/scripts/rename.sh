#!/bin/bash
set +x 
for i in *000.mp3; do
  echo $i;
  day=$(echo $i | cut -c 32-33);
  month=$(echo $i | cut -c 30-31);
  year=$(echo $i | cut -c 26-29);
  echo "GillesPeterson_WorldWide_${year}-${month}-${day}.mp3";
  mv "${i}"  "GillesPeterson_WorldWide_${year}-${month}-${day}.mp3";
done
