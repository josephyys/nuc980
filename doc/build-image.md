setenv bootargs root=/dev/mtdblock2 rootfstype=yaffs2 rw rootwait console=ttyS0,115200n8 mem=64M ${mtdparts}
saveenv

scp /home/joseph/project/nuc980/initramfs/output/images/ 

output/build/linux-custom/.config

git add -f    output/images/rootfs.ubi
git add -f    output/images/rootfs.ubifs
git add -f    output/images/rootfs.yaffs2
git add -f    output/images/uImage