#!/bin/bash

MOUNT_DRIVE="//192.168.0.108/Public/Media"
MOUNTPOINT="mountPoint/"

## Detect the user who launched the script
usr=$(env | grep SUDO_USER | cut -d= -f 2)

## Exit if the script was not launched by root or through sudo
if [ -z $usr ] && [ $USER = "root" ]
then
    echo "The script needs to run as root" && exit 1
fi

## Run the job that needs to be run as root
mount -t cifs $MOUNT_DRIVE $MOUNTPOINT
if [ $? -ne 0 ] then
	echo "Error mounting drive" && exit $?
done

## Run the job(s) that don't need root
sudo -u $usr ./filemover.sh

## Run unmount as root too
umount $MOUNTPOINT

