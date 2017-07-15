#!/bin/bash

DOWNLOADS_DIR="/Users/matias/Downloads"
FILMS_DIR="/Users/Downloads/Media/Films"
SERIES_DIR="/Users/matias/Downloads/Media/Series"
SERIES_REGEX=".[Ss][0-9][0-9][eE][0-9][0-9]"
DEBUG=true

find $SERIES_DIR ! -path $SERIES_DIR -type d | while read folder;
do
	name="${folder##*/}"
	name=${name// /.}
	if [ $DEBUG = true ]; then
		find $DOWNLOADS_DIR -type f -name "$name$SERIES_REGEX*" | xargs -I '{}' echo "mv {} $folder"
		find $DOWNLOADS_DIR -type d -name "$name$SERIES_REGEX*" | xargs -I '{}' echo "rm -rf {}"
	else
		find $DOWNLOADS_DIR -type f -name "$name$SERIES_REGEX*" | xargs -I '{}' mv {} "$folder"
		find $DOWNLOADS_DIR -type d -name "$name$SERIES_REGEX*" | xargs -I '{}' rm -rf {}
	fi 
done

films=$(find $DOWNLOADS_DIR -type f -exec file -N -i -- {} + | sed -n 's!: video/[^:]*$!!p')

for film in $films
do
	if [ $DEBUG = true ]; then
		echo "mv $film $FILMS_DIR"
	else
		mv $film $FILMS_DIR
	fi
done

if [ $DEBUG = true ]; then
	echo "To remove:"
	find $DOWNLOADS_DIR -type d -mindepth 1 
else
	find $DOWNLOADS_DIR -type d -mindepth 1 | xargs -I '{}' rm -rf {}
done