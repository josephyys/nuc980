setenv bootargs root=/dev/mtdblock2 rootfstype=yaffs2 rw rootwait console=ttyS0,115200n8 mem=64M ${mtdparts}
saveenv