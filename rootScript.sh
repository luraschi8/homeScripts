#!/bin/bash

export MOUNT_DRIVE="//192.168.0.108/Public/Media"
export MOUNTPOINT="../mountPoint/"

## Detect the user who launched the script
usr=$(env | grep SUDO_USER | cut -d= -f 2)

## Exit if the script was not launched by root or through sudo
if [ -z $usr ] && [ $USER = "root" ]
then
    echo "The script needs to run as root" && exit 1
fi

returnMount=$(./mountDrive.sh)
echo $returnMount

if [ $returnMount -ne 0 ]; then
	exit 2
fi

echo "Calling fileMover now \n"

./unmountDrive.sh

exit 0