#Pull vhd file from windows share and write to local device

sudo add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) universe"
sudo apt-get update
sudo apt-get install qemu-system-x86 -y
sudo apt-get install samba -y
sudo apt-get install gddrescue -y

#mkdir "Local directory to mount share"
#sudo mount.cifs "\\Windows share"
#sudo modprobe nbd max_part=8
#sudo qemu-nbd -c /dev/nbd0 -f vhdx "Local directory path to vhdx file" -r

#sudo ddrescue -f -v /dev/nbd0 /dev/sda
