#!/bin/bash
set +x 
for i in *asf.mp3; do
  echo $i;
  day=$(echo $i | cut -c 29-30);
  month=$(echo $i | cut -c 32-33);
  year=$(echo $i | cut -c 35-38);
  newfilename="GillesPeterson_WorldWide_${year}-${month}-${day}.a.mp3";
  echo $newfilename;
  mv "${i}" $newfilename; 
done
