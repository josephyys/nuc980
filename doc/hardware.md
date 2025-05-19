https://www.nuvoton.com.cn/export/resource-files/en-us--NUC980_Linux_5.10_BSP_User_Manual_EN.pdf
# Connecting nRF52 DK to NUC980 via UART

To establish a UART connection between your nRF52 Development Kit and NUC980 board, follow these pin-to-pin wiring instructions:

## Basic UART Connections

| nRF52 DK Pin | NUC980 Pin | Function |
|--------------|------------|----------|
| P0.06 (TX) | PC11 (RX) | nRF52 transmits to NUC980 |
| P0.08 (RX) | PC10 (TX) | nRF52 receives from NUC980 |
| GND | GND | Common ground |
| VCC | - | No connection needed (each board uses its own power) |

## Notes on Pin Selection

1. **For NUC980**:
   - The example above uses UART4 (TX=PC10, RX=PC11)
   - You could also use UART5 or UART6 based on your configuration:
     - UART6: TX=PB2, RX=PB3

2. **For nRF52 DK**:
   - The default UART pins on nRF52 DK are P0.06 (TX) and P0.08 (RX)
   - These are usually labeled on the board or available on the edge connector

## Hardware Flow Control (Optional)

If you need hardware flow control:

| nRF52 DK Pin | NUC980 Pin | Function |
|--------------|------------|----------|
| P0.07 (CTS) | PC12 (RTS) | Clear To Send |
| P0.05 (RTS) | PC13 (CTS) | Request To Send |

## Connection Steps

1. Power off both devices before making any connections
2. Identify the pins on both boards (refer to their respective pinout diagrams)
3. Use jumper wires to connect:
   - nRF52 TX to NUC980 RX
   - nRF52 RX to NUC980 TX
   - nRF52 GND to NUC980 GND
4. If using flow control, connect the CTS and RTS lines
5. Power on the devices
6. Configure both devices to use the same baud rate (115200 as mentioned in your documentation)
7. Test the connection with a simple loopback test

## Configuration Verification

After connecting, verify the UART is working:

```bash
# On NUC980
ls /dev/ttyS*  # Check available serial ports
stty -F /dev/ttyS4 115200  # Set baud rate for UART4
echo "Hello from NUC980" > /dev/ttyS4  # Send test message
```

On the nRF52 side, you'll need to configure UART in your firmware and listen for incoming messages.


# UART Wire Color Conventions

In conventional UART connections, there isn't a universally standardized color code, but there are some common practices:

## Most Common Convention
- **TX (Transmit)**: **Red** wire
- **RX (Receive)**: **Black** or **Green** wire

## Important Notes
1. This isn't a strict standard - manufacturers can use different color schemes
2. This convention can cause confusion because power connections typically use:
   - Red for VCC/positive (+)
   - Black for GND/negative (-)

3. When working with pre-made UART cables or adapters:
   - TTL UART cables often use red for TX
   - USB-to-UART adapters frequently follow this convention

## Recommendation
Always verify connections by checking the pinout documentation for your specific devices rather than relying solely on wire colors. When in doubt, use a multimeter to confirm connectivity before powering on.

ncu98 tx(red) -->P0.08
rx(bladck) --> p0.06


dmesg | grep -i uart


# NUC980 UART Pin Configuration in Newer Linux Kernels

You've identified a key difference between Linux 4.4 and newer kernel versions for the NUC980. In newer kernels, pin selection has been moved from the kernel menuconfig to the **Device Tree**.

## How Pin Selection Works in Newer Kernels

1. **Device Tree Configuration**:
   - Pin selections are now defined in the Device Tree files (DTS)
   - This is the standard approach in modern Linux kernels
   - Menuconfig options are simplified to just enable/disable features

2. **How to Configure UART Pins**:
   You need to modify your device tree file (typically in `arch/arm/boot/dts/nuc980*.dts`):
   
   ```
   /* For UART5 with PG pins */
   &uart5 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_uart5_PG>;  /* Select the PG pin group */
   };
   ```

3. **Available Pin Groups**:
   From your previous dmesg output:
   ```
   nuc980-pinctrl apb:pinctrl@b0000000: parse function(5): uart5
   nuc980-pinctrl apb:pinctrl@b0000000: group(0): uart5-PG
   nuc980-pinctrl apb:pinctrl@b0000000: group(1): uart5-PG-1
   nuc980-pinctrl apb:pinctrl@b0000000: group(2): uart5-PD
   ```
   UART5 can use pin groups PG, PG-1, or PD.

## Steps to Configure UART for nRF52 Connection

1. **Find your device tree file**:
   ```bash
   find arch/arm/boot/dts -name "nuc980*.dts"
   ```

2. **Edit the device tree file**:
   ```bash
   cd /path/to/kernel/source
   nano arch/arm/boot/dts/nuc980_your_board.dts
   ```

3. **Add or modify UART configuration**:
   For UART4 with PC10/PC11 pins:
   ```
   &uart4 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_uart4_PC>;  /* PC10/PC11 pins */
   };
   ```

4. **Rebuild the device tree and kernel**:
   ```bash
   make dtbs
   make
   ```

5. **Flash the updated dtb file**:
   ```bash
   nand erase 0x180000 0x20000
   nand write 0x7fc0 0x180000 0x20000
   ```

## Wire Connection

Your connection looks correct:
```
ncu98 tx(red) -->P0.08
rx(bladck) --> p0.06
```

This follows the standard: TX of one device connects to RX of the other device.

Let me know if you need help locating or modifying your device tree file!


# Modifying the NUC980 Device Tree for UART Configuration

Since you're using the `nuc980-iot-v1.0.dtb` file, you should modify the corresponding source file:

```
./output/build/linux-custom/arch/arm/boot/dts/nuc980-iot-v1.0.dts
```

## Steps to Configure UART for nRF52 Connection

1. **Edit the device tree source file**:
   ```bash
   cd ~/project/nuc980/initramfs
   nano ./output/build/linux-custom/arch/arm/boot/dts/nuc980-iot-v1.0.dts
   ```

2. **Locate the UART section** (look for existing UART definitions)

3. **Add or modify the UART4 configuration** to enable PC10/PC11 pins:
   ```c
   &uart4 {
       status = "okay";
       pinctrl-names = "default";
       pinctrl-0 = <&pinctrl_uart4_PC>;  /* PC10/PC11 pins */
   };
   ```

4. **Save the file** (Ctrl+O, then Enter, then Ctrl+X in nano)

5. **Compile the device tree**:
   ```bash
   cd ~/project/nuc980/initramfs
   make dtbs
   ```

6. **Check that the new DTB was generated**:
   ```bash
   ls -la ./output/images/nuc980-iot-v1.0.dtb
   ```
   Verify that the timestamp is recent.

7. **Flash the updated DTB file**:
   ```bash
   # In U-Boot:
   tftpboot 0x7fc0 nuc980-iot-v1.0.dtb
   nand erase 0x180000 0x20000
   nand write 0x7fc0 0x180000 ${filesize}
   ```

## Notes on Device Tree Structure

- The nuc980-iot-v1.0.dts file might include the base nuc980.dtsi file
- The UART pin control definitions are likely in the dtsi file
- If you can't find `pinctrl_uart4_PC` in the files, look for similar pin definitions to understand the naming convention

After updating and flashing the DTB, enable UART4 in the kernel configuration:
```
Device Drivers -> Character devices -> Serial drivers -> NUC980 UART4 support
```

Then rebuild the kernel and flash it to your device.

ls -l ./output/build/linux-custom/arch/arm/boot/dts/nuc980-iot-v1.0.dts

dtc -I dtb -O dts -o /tmp/processed.dts ./output/build/linux-custom/arch/arm/boot/dts/nuc980-iot-v1.0.dtb
cat /tmp/processed.dts | grep -A 20 "uart4"

grep . /proc/tty/driver/serial

dtc -I dtb -O dts -o /tmp/processed.dts ./output/build/linux-custom/arch/arm/boot/dts/nuc980-iot-v1.0.dtb
grep -A2 pinctrl_uart /tmp/processed.dts