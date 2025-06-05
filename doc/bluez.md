/usr/libexec/bluetooth/bluetoothd &

vi /etc/bluetooth/main.conf
[Policy]
AutoEnable=true

[General]
DiscoverableTimeout = 0
PairableTimeout = 0


To check if your NUC980 is BlueZ ready and set it up for BLE control, let's go through the essential checks:

## 🔧 **Check 1: BlueZ Installation and Version**

````bash
# SSH to your NUC980 (via your tunnel)
ssh -P 8084 joseph@52.197.102.250
# Then to NUC980

rm -rf output/build/bluez-utils*
make

# Check if BlueZ is installed
bluetoothctl --version
hciconfig --version

# Check BlueZ service status
systemctl status bluetooth
systemctl status bluetoothd

# List BlueZ tools available
which bluetoothctl
which hcitool
which hciconfig
which gatttool
````

ls /usr/bin/bluetoothctl
ls /usr/bin/hciconfig
ls /usr/bin/hcitool
ls /usr/bin/gatttool
ls /usr/libexec/bluetooth/bluetoothd

lsmod | grep bluetooth

hciconfig hci0 up
hciconfig -a

ls /sys/class/bluetooth/
ls /sys/class/hci/

## 🔧 **Check 2: Bluetooth Hardware Detection**

````bash
# Check if Bluetooth hardware is detected
lsusb | grep -i bluetooth
lsusb | grep -i nordic

# Check HCI interfaces
hciconfig -a

# Expected output for working setup:
# hci0:	Type: Primary  Bus: USB
# 	BD Address: XX:XX:XX:XX:XX:XX  ACL MTU: 251:10  SCO MTU: 48:10
# 	UP RUNNING 
````

## 🔧 **Check 3: Kernel Bluetooth Support**

````bash
# Check kernel modules
lsmod | grep bluetooth
lsmod | grep hci

# Check if USB HCI driver is loaded
dmesg | grep -i bluetooth
dmesg | grep -i hci
````

## 🔧 **Check 4: Test Basic Bluetooth Functionality**

````bash
# Start bluetoothctl interactive mode
bluetoothctl

# Inside bluetoothctl:
[bluetooth]# show
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on

# Look for your BLE device
# Expected: Device found with address and name
````

## 🔧 **Setup BlueZ if Missing**

If BlueZ is not installed on your NUC980:

````bash
# For buildroot-based NUC980
# Check available packages
opkg list | grep blue
opkg list | grep bluetooth

# Install BlueZ
opkg update
opkg install bluez5-utils
opkg install bluez5-utils-extra

# Or if using apt-based system:
apt update
apt install bluez bluez-tools
````

## 🔧 **Configure BlueZ for BLE**

````bash
# Edit BlueZ configuration
vi /etc/bluetooth/main.conf

# Key settings for BLE:
[General]
Class = 0x000100
DiscoverableTimeout = 0
PairableTimeout = 0
AutoConnectTimeout = 60
Name = NUC980-BLE
DeviceID = bluetooth:1d6b:0246:0532

[LE]
MinConnectionInterval=7
MaxConnectionInterval=9
ConnectionLatency=0
ConnectionSupervisionTimeout=720
Autoconnect=true

# Restart bluetooth service
systemctl restart bluetooth
````

## 🔧 **Test BLE Connection with Your Device**

````bash
# Test connecting to your vao19l-a1 device
bluetoothctl

[bluetooth]# scan on
# Wait for your device to appear
[bluetooth]# connect AA:BB:CC:DD:EE:FF  # Your device's MAC
[bluetooth]# info AA:BB:CC:DD:EE:FF
[bluetooth]# services AA:BB:CC:DD:EE:FF
````

## 🔧 **Compare with Your Working pc-ble-driver Setup**

````bash
# Your current working setup using pc-ble-driver:
cd /home/joseph/project/nuc980/ble-scanner
./ble_scanner /dev/ttyACM0 vao19l-a1 "R/EBCAECAwQFBg8P"

# BlueZ equivalent would be:
bluetoothctl
[bluetooth]# connect <device_mac>
[bluetooth]# select-attribute <service_uuid>
[bluetooth]# write <value>
````

## 🔧 **Expected BlueZ-Ready Output**

````bash
# Successful BlueZ setup shows:
$ bluetoothctl --version
bluetoothctl: 5.64

$ hciconfig
hci0:	Type: Primary  Bus: USB
	BD Address: 12:34:56:78:9A:BC  ACL MTU: 251:10  SCO MTU: 48:10
	UP RUNNING 
	RX bytes:1234 acl:0 sco:0 events:56 errors:0
	TX bytes:5678 acl:0 sco:0 commands:56 errors:0

$ systemctl status bluetooth
● bluetooth.service - Bluetooth service
   Active: active (running)
````

## 🔧 **BlueZ vs pc-ble-driver Comparison**

| Feature | pc-ble-driver (Current) | BlueZ |
|---------|-------------------------|-------|
| **Setup** | ✅ Working with dongle | Requires system Bluetooth |
| **Control** | Direct API calls | Shell commands |
| **Integration** | C/C++ application | System service |
| **Flexibility** | Full programmatic control | Interactive + scripting |

## **Next Steps**

1. **Run the checks above** to see if BlueZ is available
2. **If BlueZ is ready**, we can create scripts to replicate your BLE scanner functionality
3. **If not ready**, decide whether to install BlueZ or stick with your working pc-ble-driver setup

Your **current pc-ble-driver solution** is already working perfectly! BlueZ would be an alternative approach, but your existing setup with the **v4.1.4 static library** and **event 0x0039 notification handler** is production-ready.

**Which approach interests you more?** BlueZ system integration or perfecting your current pc-ble-driver scanner?



Yes, your BlueZ setup is **working perfectly**!

- `bluetoothctl` is running and scanning.
- You are discovering BLE devices (including names and manufacturer data).
- The output shows new devices being found and updated in real time.

---

## **What this means:**

- Your USB BLE dongle is functioning as an HCI device.
- BlueZ is properly installed and configured.
- Your environment variables and library paths are now correct.
- You can use `bluetoothctl` for pairing, connecting, and GATT operations.

---

## **Next Steps (if you want):**

- To connect to a device:
  ```
  [bluetooth]# connect <MAC_ADDRESS>
  ```
- To pair:
  ```
  [bluetooth]# pair <MAC_ADDRESS>
  ```
- To trust:
  ```
  [bluetooth]# trust <MAC_ADDRESS>
  ```
- To explore GATT services:
  ```
  [bluetooth]# menu-gatt
  [bluetooth]# list-attributes
  ```

Or, you can use Python (e.g., with `bleak`) for scripting BLE operations.

---

**Congratulations! Your NUC980 is now BlueZ ready and BLE scanning is working!**


The D-Bus errors indicate that **BlueZ daemon is not running** or there are D-Bus communication issues. The fact that you need to manually power on Bluetooth confirms this.

## **1. Fix BlueZ Daemon Startup**

### **Check if bluetoothd is running:**
```bash
ps | grep bluetoothd
```

### **Start bluetoothd manually:**
```bash
# Kill any existing bluetoothd
killall bluetoothd

# Start bluetoothd with debug output
/usr/libexec/bluetooth/bluetoothd -d -n
```

### **Or start as background service:**
```bash
/usr/libexec/bluetooth/bluetoothd &
```

## **2. Fix Bluetooth Auto-Power-On**

### **Method A: Configure BlueZ main.conf**
```bash
vi /etc/bluetooth/main.conf
```
Add/modify these settings:
```ini
[Policy]
AutoEnable=true

[General]
DiscoverableTimeout = 0
PairableTimeout = 0
```

### **Method B: Create init script to auto-power on**
```bash
# Create startup script
cat > /etc/init.d/S91bluetooth << 'EOF'
#!/bin/sh

case "$1" in
    start)
        echo "Starting Bluetooth..."
        /usr/libexec/bluetooth/bluetoothd &
        sleep 2
        echo "power on" | bluetoothctl
        ;;
    stop)
        echo "Stopping Bluetooth..."
        killall bluetoothd
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
EOF

chmod +x /etc/init.d/S91bluetooth
```

## **3. Fix D-Bus Issues**

### **Check if D-Bus is running:**
```bash
ps | grep dbus
```

### **Start D-Bus if not running:**
```bash
# Start dbus-daemon
/usr/bin/dbus-daemon --system &
```

### **Check D-Bus Bluetooth service:**
```bash
dbus-send --system --dest=org.freedesktop.DBus --type=method_call --print-reply /org/freedesktop/DBus org.freedesktop.DBus.ListNames | grep -i blue
```

## **4. Manual USB-to-Bluetooth Power Sequence**

Create a script to automatically power on Bluetooth when USB dongle is detected:

```bash
cat > /usr/bin/bluetooth-auto-power << 'EOF'
#!/bin/sh

# Wait for USB Bluetooth device
echo "Waiting for USB Bluetooth device..."
while [ ! -d /sys/class/bluetooth/hci0 ]; do
    sleep 1
done

echo "USB Bluetooth device detected, powering on..."
sleep 2

# Power on Bluetooth
echo "power on" | bluetoothctl
echo "agent on" | bluetoothctl

echo "Bluetooth ready!"
EOF

chmod +x /usr/bin/bluetooth-auto-power
```

## **5. Test the Complete Sequence**

```bash
# 1. Start D-Bus
/usr/bin/dbus-daemon --system &

# 2. Start BlueZ daemon
/usr/libexec/bluetooth/bluetoothd &

# 3. Wait a moment
sleep 2

# 4. Power on Bluetooth
echo "power on" | bluetoothctl

# 5. Test Python scanner
python3 /data/test_bluez_bleak.py
```

## **6. Add to System Startup**

Update your `/etc/init.d/S91bluetooth` or add to profile:

```bash
# Add to /etc/profile or create init script
if [ ! -f /var/run/bluetoothd.pid ]; then
    /usr/bin/dbus-daemon --system &
    /usr/libexec/bluetooth/bluetoothd &
    sleep 2
    echo "power on" | bluetoothctl > /dev/null 2>&1
fi
```

## **Summary**

The issues are:
1. **bluetoothd not auto-starting** → Need init script
2. **D-Bus communication errors** → Need D-Bus running first  
3. **Bluetooth not auto-powered** → Need "power on" command
4. **USB detection timing** → Need delay after USB insertion

After fixing these, your USB dongle should automatically power on when plugged in, and the Python Bleak scanner should work without D-Bus errors.



The issue is that you have **conflicting D-Bus services**. The error "Name already in use" means there's already a D-Bus service running, but the Python Bleak library can't communicate with it properly.

## **Fix D-Bus and BlueZ Integration**

### **1. Check what's running and clean up:**

```bash
# Check what's running
ps | grep bluetoothd
ps | grep dbus

# Kill all Bluetooth services
killall bluetoothd

# Check D-Bus service status
dbus-send --system --dest=org.freedesktop.DBus --type=method_call --print-reply /org/freedesktop/DBus org.freedesktop.DBus.ListNames
```

### **2. Restart services in correct order:**

```bash
# 1. D-Bus is already running (good)
# D-Bus daemon PID 685 is running

# 2. Start bluetoothd with proper D-Bus integration
/usr/libexec/bluetooth/bluetoothd &

# 3. Wait for service to register
sleep 3

# 4. Check if BlueZ is registered with D-Bus
dbus-send --system --dest=org.freedesktop.DBus --type=method_call --print-reply /org/freedesktop/DBus org.freedesktop.DBus.ListNames | grep -i blue
```

### **3. Test D-Bus Bluetooth service:**

```bash
# Test if BlueZ is accessible via D-Bus
dbus-send --system --print-reply --dest=org.bluez / org.freedesktop.DBus.Introspectable.Introspect
```

### **4. Alternative: Use lower-level access**

If D-Bus continues to have issues, you can bypass Bleak and use direct `bluetoothctl` commands:

```bash
# Create a shell script wrapper for BLE operations
cat > /data/ble_shell_scanner.sh << 'EOF'
#!/bin/bash

DEVICE_NAME="vao19l-a1"
SCAN_TIME=10

echo "=== BLE Scanner (bluetoothctl) ==="
echo "Target device: $DEVICE_NAME"

# Power on and start scanning
bluetoothctl << EOL
power on
agent on
scan on
EOL

echo "Scanning for $SCAN_TIME seconds..."
sleep $SCAN_TIME

# Stop scanning and show results
bluetoothctl << EOL
scan off
devices
quit
EOL

echo "Scan complete"
EOF

chmod +x /data/ble_shell_scanner.sh
```

### **5. Fix the Python Bleak D-Bus issue:**

The Python error suggests that Bleak is trying to use `dbus_fast` but having socket communication issues. Try:

```bash
# Check if there are permission issues
ls -la /var/run/dbus/
ls -la /var/lib/dbus/

# Make sure the current user can access D-Bus
id
groups
```

### **6. Alternative Python approach (without Bleak):**

Create a simpler Python script that uses subprocess to call `bluetoothctl`:

```python
#!/usr/bin/env python3
# filepath: /data/simple_ble_scanner.py

import subprocess
import time
import sys

def run_bluetoothctl_command(command):
    """Run a bluetoothctl command and return output"""
    try:
        process = subprocess.Popen(['bluetoothctl'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        stdout, stderr = process.communicate(command + '\nquit\n')
        return stdout, stderr
    except Exception as e:
        return None, str(e)

def scan_for_device(device_name, scan_time=10):
    """Scan for a specific device"""
    print(f"🔍 Scanning for device: {device_name}")
    
    # Start scanning
    stdout, stderr = run_bluetoothctl_command("power on\nagent on\nscan on")
    if stderr:
        print(f"Error starting scan: {stderr}")
        return False
    
    print(f"Scanning for {scan_time} seconds...")
    time.sleep(scan_time)
    
    # Get devices
    stdout, stderr = run_bluetoothctl_command("scan off\ndevices")
    if stdout:
        print("Found devices:")
        for line in stdout.split('\n'):
            if 'Device' in line:
                print(f"  {line}")
                if device_name.lower() in line.lower():
                    print(f"  ✅ Found target device!")
                    return True
    
    return False

if __name__ == "__main__":
    device_name = sys.argv[1] if len(sys.argv) > 1 else "vao19l-a1"
    scan_for_device(device_name)
```

### **7. Test the solutions:**

```bash
# Test 1: Shell script approach
/data/ble_shell_scanner.sh

# Test 2: Simple Python approach  
python3 /data/simple_ble_scanner.py vao19l-a1

# Test 3: Direct bluetoothctl
bluetoothctl
[bluetooth]# power on
[bluetooth]# scan on
# Wait for devices
[bluetooth]# devices
[bluetooth]# quit
```

## **Summary**

The D-Bus communication issue is preventing Bleak from working properly. The solutions above provide:

1. **Direct bluetoothctl approach** (most reliable)
2. **Shell script wrapper** (simple automation)
3. **Python subprocess approach** (programmatic without D-Bus complexity)

Try the shell script approach first - if `bluetoothctl` works manually, this should work too and bypass the D-Bus issues entirely.


The Python Bleak library is having **D-Bus communication issues** even though `bluetoothctl` works fine. This is because:

1. **`bluetoothctl` uses direct BlueZ D-Bus calls** (simpler, more robust)
2. **Bleak uses `dbus_fast` library** which has more complex socket handling and is failing

## **Solution: Use the Shell Script or Python Subprocess Approach**

Since `bluetoothctl` works perfectly, let's bypass the problematic Bleak D-Bus layer:

### **Option 1: Shell Script (Simplest)**

````bash
cat > /data/ble_shell_scanner.sh << 'EOF'
#!/bin/bash

DEVICE_NAME="vao19l-a1"
SCAN_TIME=10

echo "=== BLE Scanner (bluetoothctl) ==="
echo "Target device: $DEVICE_NAME"

# Power on and start scanning
echo "🔍 Starting discovery..."
bluetoothctl << EOL
power on
agent on
scan on
EOL

echo "Scanning for $SCAN_TIME seconds..."
sleep $SCAN_TIME

# Stop scanning and show results
echo "Stopping scan and showing devices..."
bluetoothctl << EOL
scan off
devices
quit
EOL

echo "Scan complete"
EOF

chmod +x /data/ble_shell_scanner.sh

# Test it
/data/ble_shell_scanner.sh
````

### **Option 2: Python Subprocess (Programmatic)**

````bash
cat > /data/simple_ble_scanner.py << 'EOF'
#!/usr/bin/env python3

import subprocess
import time
import sys
import re

def run_bluetoothctl_command(commands):
    """Run bluetoothctl commands and return output"""
    try:
        # Create the command string
        cmd_string = '\n'.join(commands) + '\nquit\n'
        
        process = subprocess.Popen(['bluetoothctl'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        stdout, stderr = process.communicate(cmd_string, timeout=30)
        return stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        return None, "Command timeout"
    except Exception as e:
        return None, str(e)

def scan_for_device(device_name, scan_time=10):
    """Scan for a specific device"""
    print(f"🔍 Scanning for device: {device_name}")
    
    # Start scanning
    print("Starting scan...")
    stdout, stderr = run_bluetoothctl_command(["power on", "agent on", "scan on"])
    if stderr and "Error" in stderr:
        print(f"Error starting scan: {stderr}")
        return False
    
    print(f"Scanning for {scan_time} seconds...")
    time.sleep(scan_time)
    
    # Get devices
    print("Getting device list...")
    stdout, stderr = run_bluetoothctl_command(["scan off", "devices"])
    
    if stdout:
        print("\n=== FOUND DEVICES ===")
        found_target = False
        device_info = {}
        
        for line in stdout.split('\n'):
            if 'Device' in line:
                # Parse device line: Device AA:BB:CC:DD:EE:FF DeviceName
                parts = line.split()
                if len(parts) >= 2:
                    mac = parts[1]
                    name = ' '.join(parts[2:]) if len(parts) > 2 else "Unknown"
                    device_info[mac] = name
                    print(f"  📱 {mac} - {name}")
                    
                    # Check if this is our target
                    if device_name.lower() in name.lower():
                        print(f"  ✅ FOUND TARGET DEVICE: {name}")
                        found_target = True
        
        print(f"\nTotal devices found: {len(device_info)}")
        return found_target, device_info
    else:
        print("No output from bluetoothctl")
        return False, {}

def connect_to_device(mac_address):
    """Attempt to connect to a device"""
    print(f"🔗 Attempting to connect to {mac_address}")
    
    stdout, stderr = run_bluetoothctl_command([
        f"connect {mac_address}"
    ])
    
    if stdout:
        if "Connection successful" in stdout:
            print("✅ Connected successfully!")
            return True
        else:
            print(f"❌ Connection failed: {stdout}")
            return False
    return False

def get_device_info(mac_address):
    """Get detailed info about a device"""
    print(f"ℹ️  Getting info for {mac_address}")
    
    stdout, stderr = run_bluetoothctl_command([
        f"info {mac_address}"
    ])
    
    if stdout:
        print("Device Info:")
        for line in stdout.split('\n'):
            if line.strip():
                print(f"  {line}")

def main():
    device_name = sys.argv[1] if len(sys.argv) > 1 else "vao19l-a1"
    
    print("=== BLE Scanner (Python + bluetoothctl) ===")
    print(f"Target device: {device_name}")
    
    # Scan for devices
    found, devices = scan_for_device(device_name)
    
    if found:
        print(f"\n🎉 Successfully found target device: {device_name}")
        
        # Find the MAC address of our target
        target_mac = None
        for mac, name in devices.items():
            if device_name.lower() in name.lower():
                target_mac = mac
                break
        
        if target_mac:
            print(f"Target MAC: {target_mac}")
            
            # Ask user what to do next
            while True:
                action = input("\nWhat to do? (i)nfo, (c)onnect, (q)uit: ").lower().strip()
                
                if action == 'q':
                    break
                elif action == 'i':
                    get_device_info(target_mac)
                elif action == 'c':
                    connect_to_device(target_mac)
                else:
                    print("Invalid option")
    else:
        print(f"❌ Device '{device_name}' not found")
        print("Available devices:")
        for mac, name in devices.items():
            print(f"  {mac} - {name}")

if __name__ == "__main__":
    main()
EOF

chmod +x /data/simple_ble_scanner.py

# Test it
python3 /data/simple_ble_scanner.py vao19l-a1
````

### **Option 3: Fix Bleak D-Bus (Advanced)**

If you really want to use Bleak, try installing a different D-Bus library:

````bash
# Check what D-Bus libraries are available
python3 -c "import dbus_fast; print('dbus_fast OK')"
python3 -c "import dbus; print('dbus OK')"

# If you have pip, try installing an alternative
pip3 install pydbus
````

## **Why This Happens**

| Component | Status | Notes |
|-----------|--------|-------|
| **D-Bus daemon** | ✅ Working | System service OK |
| **BlueZ daemon** | ✅ Working | Registered with D-Bus |
| **bluetoothctl** | ✅ Working | Direct D-Bus calls |
| **Bleak + dbus_fast** | ❌ Failing | Complex async socket handling |

The issue is that **Bleak's D-Bus library (`dbus_fast`) is more complex** and has socket buffering/timing issues that don't affect the simpler `bluetoothctl` approach.

## **Recommended Solution**

**Use the Python subprocess approach** (`simple_ble_scanner.py`) because:
1. ✅ **Reliable** - Uses the same working `bluetoothctl` backend
2. ✅ **Programmatic** - You can script it like Bleak
3. ✅ **Feature-complete** - Scan, connect, get info, etc.
4. ✅ **No D-Bus issues** - Bypasses the problematic `dbus_fast` library

This gives you the best of both worlds: Python programming with the reliability of `bluetoothctl`.