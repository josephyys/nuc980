0x200
0x80000
0x100000
0x120000

1 block 128K(0x20000)
1M 8block
20M 160M



0x80000 uboot
4/1 (block offset/block size)

0x100000 uboot-spl

0x180000 dtb
15/1

0x200000 image
16/160 20M
128/8=16M

NUC980 的 MTD (Memory Technology Device) 儲存架構
NUC980 除了 RAM (64MB) 之外，還使用了 NAND Flash 作為非揮發性儲存設備。從您的 /proc/mtd 輸出可以看到：

NAND Flash 分區說明
u-boot 分區 (mtd0)

大小：2MB
用途：存放 bootloader
kernel 分區 (mtd1)

大小：22MB
用途：存放 Linux 核心映像
user 分區 (mtd2)

大小：104MB
用途：存放使用者資料、檔案系統等
啟動流程
NUC980 上電後，從 NAND Flash 的 u-boot 分區讀取 bootloader
bootloader 將 kernel 分區的內容讀入 RAM (載入位址 0x7fc0)
kernel 啟動後，可以掛載 user 分區作為檔案系統使用



scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/images/uImage  D:\project\vic\5.10\ram\initramfs\uImage.uart6
scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/images/uImage  D:\project\vic\5.10\ram\initramfs\uImage.bluez
scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/images/uImage  D:\project\vic\5.10\ram\initramfs\uImage.dbus.250627.bin
scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/output/images/uImage  D:\project\vic\5.10\ram\initramfs\uImage.250821.bin
scp joseph@10.22.22.107:/home/joseph/project/nuc980/initramfs/env.txt  D:\project\vic\5.10\ram\initramfs\env20M.bin
