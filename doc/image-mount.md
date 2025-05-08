# Add to /etc/init.d/S90mount_data
mkdir -p /data
mount -t yaffs2 /dev/mtdblock2 /data
export LD_LIBRARY_PATH=/data/user/lib:$LD_LIBRARY_PATH 