]      Enable UART2 CTS wake-up function 
            NUC980 UART2 pin selection (Tx:PF11, Rx:PF12)  ---> 
   [*]    NUC980 UART3 support 
   [*]    NUC980 UART4 support 
   [*]      Enable UART4 CTS wake-up function 
            NUC980 UART4 pin selection (Tx:PC10, Rx:PC11)  ---> 
   [*]    NUC980 UART5 support 
   [*]    NUC980 UART6 support 
   [*]      Enable UART6 CTS wake-up function 
            NUC980 UART6 pin selection (Tx:PB2, Rx:PB3)  ---> 
   [*]    NUC980 UART7 support 
            NUC980 UART7 pin selection (Tx:PG4, Rx:PG5)  ---> 
   [*]    NUC980 UART8 support  
   [*]      Enable UART8 CTS wake-up function 
            NUC980 UART8 pin selection (Tx:PE10, Rx:PE11)  ---> 
   [*]    NUC980 UART9 suppor  
            NUC980 UART9 pin selection (Tx:PH2, Rx:PH3)  ---> 
   [*]    NUC980 UART10 support  
   [*]      Enable UART10 CTS wake-up functio


   To enable `ttyS4` and `ttyS5` in your Buildroot configuration, you need to configure the Linux kernel to include support for these serial ports. Here's how to do it:

---

### **Steps to Enable `ttyS4` and `ttyS5`**

1. **Open Kernel Configuration**:
   ```bash
   make linux-menuconfig
   ```

2. **Navigate to Serial Port Configuration**:
   - Go to:
     ```
     Device Drivers → Character devices → Serial drivers
     ```
   - Ensure the following options are enabled:
     ```
     [*] Serial drivers
     [*] 8250/16550 and compatible serial support
     [*]   Console on 8250/16550 and compatible serial port
     ```

3. **Enable Additional UART Ports**:
   - Look for an option like:
     ```
     Maximum number of 8250/16550 serial ports (CONFIG_SERIAL_8250_NR_UARTS)
     ```
   - Increase the value to at least `6` to ensure `ttyS4` and `ttyS5` are included.

4. **Enable Runtime Configuration for UARTs**:
   - Enable:
     ```
     [*] Support for sharing serial interrupts
     [*] Support for console on serial port
     ```

5. **Save and Exit**:
   - Press `ESC` multiple times and select "Save" when prompted.

6. **Rebuild the Kernel**:
   ```bash
   make
   ```

---

### **Verify `ttyS4` and `ttyS5`**

1. **Check `/dev` for Serial Ports**:
   After booting the updated kernel, check if `ttyS4` and `ttyS5` are available:
   ```bash
   ls /dev/ttyS*
   ```

2. **Test the Serial Ports**:
   Use a tool like `minicom` or `screen` to test the serial ports:
   ```bash
   minicom -D /dev/ttyS4 -b 115200
   ```

---

### **Optional: Add to Init Script**

If you want to configure or test the serial ports automatically at boot, you can add commands to your init script (e.g., `/etc/init.d/S90mount_data`):
```bash
stty -F /dev/ttyS4 115200
stty -F /dev/ttyS5 115200
```

---

### **Summary**
- Use `make linux-menuconfig` to enable `ttyS4` and `ttyS5` by increasing the number of UARTs.
- Rebuild the kernel and verify the devices in `/dev`.
- Optionally, configure the serial ports in your init script.

Let me know if you need further assistance!---

### **Summary**
- Use `make linux-menuconfig` to enable `ttyS4` and `ttyS5` by increasing the number of UARTs.
- Rebuild the kernel and verify the devices in `/dev`.
- Optionally, configure the serial ports in your init script.

Let me know if you need further assistance!


# UART Single Port Loopback Test Script

Here's a shell script to test UART loopback that accepts a port parameter:

```bash
#!/bin/sh

# Default values
PORT="/dev/ttyS4"
BAUD=115200
TIMEOUT=3

# Show usage
show_usage() {
    echo "Usage: $0 [port] [-b baud_rate] [-t timeout]"
    echo "  port       UART port to test (default: /dev/ttyS4)"
    echo "  -b rate    Set baud rate (default: 115200)"
    echo "  -t seconds Set timeout in seconds (default: 3)"
    echo "  -h         Show this help"
    echo ""
    echo "Example: $0 /dev/ttyS5 -b 9600 -t 5"
    exit 1
}

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -b) BAUD="$2"; shift 2 ;;
        -t) TIMEOUT="$2"; shift 2 ;;
        -h) show_usage ;;
        -*) echo "Unknown option: $1"; show_usage ;;
        *) PORT="$1"; shift ;;
    esac
done

# Check if port exists
if [ ! -e "$PORT" ]; then
    echo "Error: Port $PORT does not exist"
    exit 1
fi

echo "Testing UART loopback on $PORT at $BAUD baud (timeout: ${TIMEOUT}s)"

# Configure UART port
stty -F "$PORT" $BAUD raw -echo -crtscts

# Clear any pending data
cat < "$PORT" > /dev/null &
CLEAR_PID=$!
sleep 0.5
kill $CLEAR_PID 2>/dev/null
wait $CLEAR_PID 2>/dev/null

# Create temporary file for output
OUTPUT_FILE="/tmp/uart_test_output.$$"
touch "$OUTPUT_FILE"

# Start reading in background with timeout
cat "$PORT" > "$OUTPUT_FILE" &
CAT_PID=$!

# Brief pause to ensure reader is ready
sleep 1

# Send test message
TEST_MESSAGE="UART Loopback Test"
echo "$TEST_MESSAGE" > "$PORT"
echo "Sent: $TEST_MESSAGE"

# Wait for specified timeout
sleep "$TIMEOUT"

# Stop the reader process
kill $CAT_PID 2>/dev/null

# Check results
if [ -s "$OUTPUT_FILE" ]; then
    echo "Received:"
    cat "$OUTPUT_FILE"
    echo "Loopback test: SUCCESS"
    RESULT=0
else
    echo "No data received"
    echo "Loopback test: FAILED"
    RESULT=1
fi

# Clean up
rm -f "$OUTPUT_FILE"

exit $RESULT
```

## Usage Examples:

```bash
# Test default port (ttyS4)
./test_uart.sh

# Test specific port
./test_uart.sh /dev/ttyS5

# Test with custom baud rate
./test_uart.sh /dev/ttyS4 -b 9600

# Test with longer timeout
./test_uart.sh /dev/ttyS5 -t 5

# Show help
./test_uart.sh -h
```

Remember to make the script executable:
```bash
chmod +x test_uart.sh
```


mkdir -p ~/project/nuc980/initramfs/output/build/uart-loopback-test
cd ~/project/nuc980/initramfs/output/build/uart-loopback-test
cd ~/project/nuc980/initramfs/
make -C output/build/uart-loopback-test CROSS_COMPILE=output/host/bin/arm-buildroot-linux-uclibcgnueabi-
cd ~/project/nuc980/initramfs/
make -C output/build/uart-loopback-test CROSS_COMPILE=output/host/bin/arm-buildroot-linux-uclibcgnueabi-

ls output/host/bin/arm-nuvoton-linux-gcc 

cd ~/project/nuc980/initramfs/
make -C output/build/uart-loopback-test CROSS_COMPILE=$(pwd)/output/host/bin/arm-nuvoton-linux-gnueabi-

# Option 1: Copy to target directory for inclusion in filesystem image
cp output/build/uart-loopback-test/uart_loopback_test output/target/usr/bin/

sudo scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/initramfs/output/build/uart-loopback-test/uart_loopback_test .


busybox tftp -g -r uart_loopback_test 192.169.0.1


# busybox tftp -g -r uart_loopback_test -l hhh 192.169.0.1
tftp: server error: (2) Only absolute filenames allowed