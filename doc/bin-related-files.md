ldd ./rsync


tftp -g -r rsync 192.168.0.2
tftp -g -r python3.11 192.168.0.2
tftp -g -r libssl.so.3   192.168.0.2
tftp -g -r libpopt.so.0   192.168.0.2
tftp -g -r libcrypto.so.3   192.168.0.2
tftp -g -r ssh   192.168.0.2

./rsync -avz joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/user/ 

libpopt.so.0 => not found
libc.so.6 => /lib/libc.so.6 (0xb6f4c000)
/lib/ld-linux.so.3 => /lib/ld-linux.so.3 (0xb6f2c000)

find output -name libpopt.so.0
find output -name libcrypto.so.3
find output -name libssl.so.3

output/target/usr/lib/libpopt.so.0

mv libpopt.so.0 /usr/lib/
ldconfig
ldd ./rsync

find /lib /usr/lib -name libpopt.so.0

libcrypto.so.3

rsync -avz output/target/usr/ root@192.168.0.10:/data/usr/

rsync -avz /data/user joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/

 ./rsync -avz /data/user joseph@10.22.22.107:/home/joseph/project/nuc980/buildr
oot_2024/output/target/usr/
joseph@10.22.22.107's password: 
sending incremental file list

sent 56 bytes  received 17 bytes  20.86 bytes/sec
total size is 0  speedup is 0.00