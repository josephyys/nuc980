# Add to /etc/init.d/S90mount_data
mkdir -p /data
mount -t yaffs2 /dev/mtdblock2 /data
export LD_LIBRARY_PATH=/data/usr/lib:$LD_LIBRARY_PATH
export PATH=/data/usr/bin:$PATH
cd /data

export LD_LIBRARY_PATH=/data/user/usr/lib:$LD_LIBRARY_PATH 

### rsync
rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/usr/

ls output/target/usr/libexec
rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/libexec/ /data/usr/libexec/

### cp dbus
# On your development machine
mkdir -p ~/project/nuc980/buildroot_2024/output/target/tmp/dbus-data-setup/usr/share/dbus-1/
cp -r ~/project/nuc980/buildroot_2024/output/target/usr/share/dbus-1/* ~/project/nuc980/buildroot_2024/output/target/tmp/dbus-data-setup/usr/share/dbus-1/
# From development machine to target
rsync -avz --progress /home/joseph/project/nuc980/buildroot_2024/output/target/tmp/dbus-data-setup/ joseph@10.22.22.107:/data/
/data/usr/bin/dbus-daemon --system --fork --config-file=/data/usr/share/dbus-1/system.conf

# Cross-compile for NUC980
cd ~/project/nuc980/tools
~/project/nuc980/initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-gcc -o uart_control uart_control.c -Wall -O2 -static

## scp
scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/target/usr/sbin/telnetd /usr/sbin/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/hexdump /usr/bin/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/minicom /usr/bin/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/tools/uart_control /usr/bin/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/rsync /usr/bin/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libpopt.so.0 /usr/lib/
rsync -avz --progress  joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/usr/

minicom -D /dev/ttyS5 -b 115200



/data/user/usr/bin/python /tmp/app.py

export LD_LIBRARY_PATH=/data/user/lib:$LD_LIBRARY_PATH 

## check size
df -h /data

### check bad blocks
nanddump -f /dev/null /dev/mtd2

# On the target device
dd if=/dev/mtdblock2 bs=4M | ssh joseph@192.168.1.101 "cat > /private/tftpboot/user_partition.img"
dd if=/dev/mtdblock2 bs=4M  iflag=skip_bad_blocks  | ssh joseph@192.168.1.101 "cat > /private/tftpboot/user_partition.img"
dd if=/dev/mtdblock2 bs=4M iflag=skip_bad_blocks of=/tmp/mtd2.img

# On macOS (host)
nc -l 9999 > user_partition.img

# If nanddump is available
nanddump -f - /dev/mtd2 | nc 192.168.1.101 9999

# On target
nanddump -f - -l 1048576 /dev/mtd2 | ssh joseph@192.168.1.101 "cat > /Volumes/MAC_DATA/project/nuc980/test_ssh.img"


# Repeat for next chunks, changing start offset (-s):
# nanddump -f - -s 10485760 -l 10485760 /dev/mtd2 | nc 192.168.1.101 9999

<!-- # On target device
dd if=/dev/mtdblock2 bs=4M | nc 192.168.1.101 9999

# Then on the target device
dd if=/dev/mtdblock2 bs=4M | nc 192.168.1.101 9999 -->

scp  joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/rsync /usr/bin
scp  joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libpopt.so.0  /usr/lib

rsync -avz --progress joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/usr/


rsync -avz --progress joseph@192.168.1.101:/private/tftpboot/output/target/usr/ /data/user/
rsync -avz --progress -e "ssh -p 8083" joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/user/

# Navigate to your Buildroot directory
cd /home/joseph/project/nuc980/buildroot_2024

# Create the tar archive
tar -cvf target_usr.tar output/target/usr/

# Optional: Compress the tar file to reduce size
gzip -9 target_usr.tar

scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/images/* .

## from other port
scp -P 8083  ubuntu@c:/home/joseph/project/nuc980/buildroot_2024/usr /data/usr

scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/target_usr.tar.gz .

# For .tar file
tar -xvf ~/Downloads/target_usr.tar -C ~/destination/folder

# For .tar.gz file
tar -xzvf ~/Downloads/target_usr.tar.gz -C ~/destination/folder


# For .tar file
tar -xvf ~/Downloads/target_usr.tar -C ~/destination/folder

# For .tar.gz file
tar -xzvf ~/Downloads/target_usr.tar.gz -C ~/destination/folder