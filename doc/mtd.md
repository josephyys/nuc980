# Increase kernel partition to 20MB for safety
setenv mtdparts 'mtdparts=nand0:0x200000(u-boot),0x1400000(kernel),-(user)'

# Update load commands
setenv loadkernel 'nand read 0x7fc0 0x200000 0x1400000'

# Save environment
saveenv


To show the `mtdparts` environment variable in the buildroot prompt, you have several options:

## **1. Show All Environment Variables**

```bash
# Show all U-Boot environment variables
printenv

# Or shorter version
env
```

## **2. Show Specific mtdparts Variable**

```bash
# Show only mtdparts
printenv mtdparts

# Or check if it's set
echo $mtdparts
```

## **3. Check Current Kernel Command Line (Runtime)**

```bash
# See what mtdparts the running kernel received
cat /proc/cmdline

# Should show something like:
# root=/dev/ram0 console=ttyS0,115200n8 mem=64M mtdparts=nand0:0x200000(u-boot),0x1600000(kernel),-(user) rootwait rw
```

## **4. Check MTD Partition Layout (Runtime)**

```bash
# Show actual MTD partitions as seen by kernel
cat /proc/mtd

# Show detailed MTD info
cat /proc/partitions | grep mtd
```

## **5. In U-Boot Console (Before Boot)**

If you want to check in U-Boot itself:

```bash
# Stop at U-Boot prompt (press key during boot)
=> printenv mtdparts

# Should show:
# mtdparts=mtdparts=nand0:0x200000(u-boot),0x1600000(kernel),-(user)
```

## **6. Verify Environment Match**

```bash
# Compare U-Boot env vs kernel runtime
echo "=== U-Boot Environment ==="
printenv mtdparts

echo "=== Kernel Command Line ==="
cat /proc/cmdline | grep -o 'mtdparts=[^[:space:]]*'

echo "=== Actual MTD Layout ==="
cat /proc/mtd
```

## **Expected Output for Your Configuration:**

```bash
# printenv mtdparts should show:
mtdparts=mtdparts=nand0:0x200000(u-boot),0x1600000(kernel),-(user)

# cat /proc/cmdline should contain:
...mtdparts=nand0:0x200000(u-boot),0x1600000(kernel),-(user)...

# cat /proc/mtd should show:
dev:    size   erasesize  name
mtd0: 00200000 00020000 "u-boot"
mtd1: 01600000 00020000 "kernel"  
mtd2: 06800000 00020000 "user"
```

## **7. If mtdparts is Missing**

If `printenv mtdparts` shows nothing:

```bash
# Set it manually in U-Boot
=> setenv mtdparts 'mtdparts=nand0:0x200000(u-boot),0x1600000(kernel),-(user)'
=> saveenv
=> reset
```

The most reliable way in buildroot is:
```bash
cat /proc/cmdline | grep mtdparts
```

This shows exactly what the kernel received from U-Boot.




# cat /proc/mtd
dev:    size   erasesize  name
mtd0: 00200000 00020000 "u-boot"
mtd1: 01600000 00020000 "kernel"
mtd2: 06800000 00020000 "user"
# 
