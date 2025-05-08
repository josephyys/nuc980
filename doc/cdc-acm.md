# lsmod | grep cdc_acm
# modprobe cdc_acm
modprobe: module cdc_acm not found in modules.dep
# modprobe cdc_acm
modprobe: module cdc_acm not found in modules.dep
# lsmod | grep cdc_acm

lsmod | grep cdc_acm
modprobe cdc_acm
Device Drivers → USB support → USB Modem (CDC ACM) support
dmesg | tail -n 20
    cdc_acm 2-2:1.0: ttyACM0: USB ACM device
ls /dev/ttyACM*    