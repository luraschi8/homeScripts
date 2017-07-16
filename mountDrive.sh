#!/bin/bash

## Run the job that needs to be run as root
mount -t cifs $MOUNT_DRIVE $MOUNTPOINT
if [ $? -ne 0 ]; then
	echo "Error mounting drive" && exit $?
done

exit 0