ssh -i "d:/joseph/keys/OraDB.pem"  ubuntu@52.197.102.250 -p 8082

# Add to /etc/init.d/S90mount_data
mkdir -p /data
mount -t yaffs2 /dev/mtdblock2 /data
export LD_LIBRARY_PATH=/data/usr/lib:$LD_LIBRARY_PATH
export PATH=/data/usr/bin:$PATH
export PYTHONPATH=/data/usr/lib/python3.11/site-packages:$PYTHONPATH
export GI_TYPELIB_PATH=/data/usr/lib/girepository-1.0:/usr/lib/girepository-1.0
cd /data



# scp gateway controller
scp -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/hotel-gateway-system/start_wifi.sh /data/controller/
scp -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/hotel-gateway-system/nuc980_gateway.zip /data/controller/


scp -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/importlib/ /data/usr/lib/python3.11/importlib/
cp -r /home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/importlib/  /home/joseph/project/nuc980/data_backup/data20250618/usr/lib/python3.11/importlib/

cp /home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/encodings/utf_8.pyc  /home/joseph/project/nuc980/data_backup/data20250618/usr/lib/python3.11/encodings/

scp -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/hotel-gateway-system/scripts/start_gateway_controller.py /data/controller/scripts/

# First create the directory
mkdir -p /data/controller

# Then try scp with more verbose output
scp -v -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/hotel-gateway-system/start_wifi.sh /data/controller/

rsync -avz --progress -e "ssh -p 8084" joseph@52.197.102.250:/home/joseph/project/nuc980/hotel-gateway-system/start_wifi.sh /data/controller/

scp joseph@10.22.22.218:/d/Users/joseph/Documents/hotel-gateway-system/start_wifi.sh /data/controller
scp -P 22 joseph@10.22.22.218:"/d/joseph/app/hotel-gateway-system/start_wifi.sh" /data/controller/
D:\joseph\app\hotel-gateway-system>

(venv) (base) joseph@j2022-macbook hotel-gateway-system % cat start_wifi.sh
python scripts/start_gateway_controller.py --config config/setup


scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/data_backup/data20250618/nrf_ble_wifi_start.sh /data/
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/data_backup/data20250618/wifi_switch.py /data/
 
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/screen /data/usr/sbin

## controller

scp -r -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/sta-ble/samples/wifi/shell/controller/ /data/
rsync -avz --progress joseph@52.197.102.250:/home/joseph/project/nuc980/sta-ble/samples/wifi/shell/controller/ /data/ 
### test hciuart
# 在您的主機上
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/lib/modules/5.10.140/kernel/drivers/bluetooth/hci_uart.ko /data/usr/lib/modules/

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/lib/modules/5.10.140/kernel/net/bluetooth/bluetooth.ko  /data/usr/lib/modules/

# 先載入 bluetooth 核心模組（如果尚未載入）
<!-- insmod /data/usr/lib/modules/bluetooth.ko -->

# 然後載入 hci_uart 模組
insmod /data/usr/lib/modules/hci_uart.ko

hciattach -s 115200 /dev/ttyS4 any 115200 noflow &

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/hciattach /data/usr/sbin

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/bin/hciconfig /data/usr/sbin

### test pppd
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/sbin/pppd  /data/usr/sbin

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libpcap.so.1 /data/usr/lib

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/build/linux-custom/drivers/net/ppp/ppp_generic.ko /data/usr/lib
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/build/linux-custom/drivers/net/slip/slhc.ko /data/usr/lib
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/build/linux-custom/drivers/net/ppp/ppp_async.ko /data/usr/lib

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/sbin/slattach /data/usr/bin
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/build/linux-custom/drivers/net/slip/slip.ko /data/usr/lib
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/build/linux-custom/drivers/net/slip/slhc.ko /data/usr/lib
output/build/linux-custom/drivers/net/slip/slhc.ko
output/build/linux-custom/drivers/net/slip/slip.ko
insmod /data/usr/lib/slhc.ko
insmod /data/usr/lib/slip.ko

echo "wifi_connect ssid=JJj pw=0928099869" > /dev/ttyS4

route del default
route add default gw 192.168.8.1 dev sl0
cd 


output/build/linux-custom/drivers/net/ppp/ppp_generic.ko

insmod /data/usr/lib/slhc.ko
insmod /data/usr/lib/ppp_generic.ko
insmod /data/usr/lib/ppp_async.ko


### backup /data/ not include usr
rsync -avz --progress --delete /data/ joseph@10.22.22.107:/home/joseph/project/nuc980/data_backup/data_no_usr/
rsync -avz --progress --delete /data/ joseph@10.22.22.107:/home/joseph/project/nuc980/data_backup/data20250618/

## test init.d
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/initramfs/output/target/etc/init.d/K90unmount_data  /etc/init.d/
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/initramfs/output/target/etc/init.d/S90mount_data  /etc/init.d/
## web server
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/gateway-py/simple_web_server.py  /data/p_dbus/
##
scp -P 8084 /data/p_dbus/w-cmd.py joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver-py/
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver-py/w-cmd.py  /data/p_dbus/w-cmd.py 

# Make sure these are set correctly
export LD_LIBRARY_PATH=/data/usr/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/data/usr/lib/python3/site-packages:$PYTHONPATH

export LD_LIBRARY_PATH=/data/user/usr/lib:$LD_LIBRARY_PATH 

### rsync
** copy to nuc980 **

####  restore
##### dbus
rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/data_backup/backup_nuc980_dbus/usr/ /data/usr/ 

rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/data_backup/backup_nuc980_dbus/ /data/


rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/data_backup/backup_nuc980_data_dongle/usr/ /data/usr/ 

<!-- rsync -avz --progress -e "ssh -p 8084" --delete  joseph@52.197.102.250:/home/joseph/project/nuc980/data_backup/backup_nuc980_dbus/ /data/ -->

rsync -avz --whole-file --progress -e "ssh -p 8084" --delete joseph@52.197.102.250:/home/joseph/project/nuc980/data_backup/backup_nuc980_dbus/ /data/

#### backup

** backup nuc980 **
rsync -avz --progress -e "ssh -p 8084" --delete /data/ joseph@52.197.102.250:/home/joseph/project/nuc980/data_backup/backup_nuc980_dbus/ 

rsync -avz --progress --delete /data/usr/ joseph@10.22.22.107:/home/joseph/project/nuc980/backup_nuc980_data/ 

rsync -avz --progress --delete /data/ joseph@10.22.22.107:/home/joseph/project/nuc980/backup_nuc980_data_dongle/ 
rsync -avz --progress --delete /data/ joseph@10.22.22.107:/home/joseph/project/nuc980/backup_nuc980_data_dongle/ 

rsync -avz --progress -e "ssh -p 8084" --delete /data/ joseph@52.197.102.250:/home/joseph/project/nuc980/backup_nuc980_data_dongle/ 

ls output/target/usr/libexec
rsync -avz --progress --delete joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/libexec/ /data/usr/libexec/

## ldd nm
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/bin/objdump /data/

scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot/usr/bin/ldd /data/
/home/joseph/project/nuc980/ble-scanner/ble_scanner
/home/joseph/project/nuc980/pc-ble-driver/build_v5_arm_full

 ### static v6->v5
<!--
/home/joseph/project/nuc980/pc-ble-driver/build_v6_static

(nordic_env) joseph@joseph-Virtual-Machine:~/project/nuc980/pc-ble-driver/build_v6_static$ /home/joseph/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-nm -D --defined-only ./libnrf-ble-driver-sd_api_v5.so | grep sd_rpc_data_link_layer_create_bt_three_wi -->

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver/build_v6_static/libnrf-ble-driver-sd_api_v5.so /data/usr/lib

###
/data/usr/lib/python3/site-packages/simple_nordic_wrapper_v5

### v6 nordic 
scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v6/dist/simple_nordic_wrapper_v6-0.1.0-py3-none-any.whl /data/
mkdir -p wheel_extract
cd wheel_extract
unzip ../simple_nordic_wrapper_v6-0.1.0-py3-none-any.whl
cp -r simple_nordic_wrapper_v6 /data/usr/lib/python3/site-packages/

cd /data/usr/lib
ln -sf libnrf-ble-driver-sd_api_v6.so libnrf_ble_driver_sd_api_v6.so

# Navigate to your library directory
cd /data/usr/lib
<!-- 
# Create symbolic link from v6 (with dash) to v5 (with underscore)
ln -sf libnrf-ble-driver-sd_api_v6.so  libnrf-ble-driver-sd_api_v5.so -->

ln -sf libnrf-ble-driver-sd_api_v5.so  libnrf-ble-driver-sd_api_v6.so
ln -sf libnrf-ble-driver-sd_api_v5.so  libnrf_ble_driver_sd_api_v6.so
ln -sf libnrf-ble-driver-sd_api_v5.so  libnrf_ble_driver_sd_api_v5.so

libnrf-ble-driver-sd_api_v5.so

<!-- wget https://github.com/NordicSemiconductor/pc-ble-driver/releases/download/v4.1.4/pc-ble-driver-4.1.4.tar.gz
tar xzf pc-ble-driver-4.1.4.tar.gz -->

### v5

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/ble-scanner/ble_scanner /data
scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/ble-scanner/ble_scanner.py /data

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver/build_v5_arm_full/libnrf-ble-driver-sd_api_v5.so* /data/usr/lib

scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver/build_v5_arm_full/libnrf-ble-driver-sd_api_v5.so /data/usr/lib

scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver/build_v5_arm/libnrf-ble-driver-sd_api_v5.so /data/usr/lib

(nordic_env) joseph@joseph-Virtual-Machine:~/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5$ python create_simple_binding.py --sdk-version=5 --output=simple_nordic_wrapper_v5
cd ..
 python setup.py bdist_wheel
 scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5/dist/simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl /data/
unzip ../simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl
cp -r simple_nordic_wrapper_v5 /data/usr/lib/python3/site-packages/

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5/dist/simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl /data/
cd wheel_extract
unzip ../simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl
cp -r simple_nordic_wrapper_v5 /data/usr/lib/python3/site-packages/


# Verify the link was created
ls -l libnrf_ble_driver_sd_api_v6.so

### v5 nordic (simulation only)
```bash
# Copy wheel to target device
scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5/dist/simple_nordic_wrapper_v5-*.whl /data/

# On the target device:
pip install /data/simple_nordic_wrapper_v5-*.whl
```

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