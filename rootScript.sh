#!/bin/bash

export MOUNT_DRIVE="//192.168.0.108/Public/Media"
export MOUNTPOINT="../mountPoint/"

## Exit if the script was not launched by root or through sudo
if [[ "$EUID" -ne 0 ]]
then
    echo "The script needs to run as root"
    exit 1
fi

returnMount=$(./mountDrive.sh)

if [[ $? -ne 0 ]]
then
	echo "Error mounting file"
	exit 2
fi

echo "Calling fileMover now"
python listarArchivos.py $MOUNTPOINT

./unmountDrive.sh

exit 0