#!/bin/sh

#read -r -p "Are you sure you want to shutdown the server? [y/N] " response
#case $response in
#       [yY][eE][sS]|[yY])
#               continue
#               ;;
#       *)
#               echo "Cancelling..."
#               sleep 2
#               exit
#               ;;
#esac

echo "Beginning shutdown of VMs..."

#/bin/vmware-autostart.sh stop
# VMwares auto start/stop is dumb and won't shutdown all VMs
# It only shutdowns VMs that were set for auto start
#
# Instead, iterate through each VM and check if it is running
# Run guest shutdown if it is

for vm in $(vim-cmd vmsvc/getallvms | sed 's/[A-z].*//g')
do
        if vim-cmd vmsvc/power.getstate $vm | grep "Powered on" > /dev/null
        then
                vim-cmd vmsvc/power.shutdown $vm
        fi
done

# Wait a few seconds, then loop and check if any VMs are still waiting to shutdown
sleep 5
while vm-support -V | grep 'Running'
do
        echo "Waiting for VMs to shutdown..."
        sleep 10
done

echo "Done"
echo "Goodnight Server"
halt
sleep 5
exit
