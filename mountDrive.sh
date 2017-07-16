#!/bin/bash

## Run the job that needs to be run as root
echo "Mounting drive."
mount -t cifs $MOUNT_DRIVE $MOUNTPOINT
if [[ $? -ne 0 ]]
then
	echo "Mount failed. Result: $?"
	exit "$?"
fi
exit 0