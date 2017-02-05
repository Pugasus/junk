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
# Auto start/stop is dumb and won't shutdown VMs
# that were powered on manually

for vm in $(vim-cmd vmsvc/getallvms | sed 's/[A-z].*//g')
do
        if vim-cmd vmsvc/power.getstate $vm | grep "Powered on" > /dev/null
        then
                vim-cmd vmsvc/power.shutdown $vm
        fi
done


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
