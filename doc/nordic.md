 tools like nrfjprog or SEGGER J-Link to flash firmware that enables USB CDC-ACM.
Mass Storage Device (MSD): For flashing firmware.
CDC-ACM (Serial): For serial communication.


SYSROOT=/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot
# Create necessary directories on NUC980
ssh joseph@10.22.22.107 "mkdir -p /data/usr/lib /data/usr/include/pc-ble-driver"
(*) mkdir -p /data/usr/lib /data/usr/include/pc-ble-driver

# Copy libraries from your sysroot to NUC980
rsync -avz --progress ${SYSROOT}/usr/lib/libnrf-ble-driver* joseph@10.22.22.107:/data/usr/lib/
(*) rsync -avz --progress joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot/usr/lib/libnrf-ble-driver* /data/usr/lib/

# Copy header files
rsync -avz --progress ${SYSROOT}/usr/include/pc-ble-driver/ joseph@10.22.22.107:/data/usr/include/pc-ble-driver/
(*) rsync -avz --progress joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot/usr/include/pc-ble-driver/ /data/usr/include/pc-ble-driver/

<!-- # From your build machine to NUC980
rsync -avz --progress $SYSROOT/usr/include/pc-ble-driver/ joseph@10.22.22.107:/data/usr/include/pc-ble-driver/

# For libraries
rsync -avz --progress $SYSROOT/usr/lib/libnrf-ble-driver* joseph@10.22.22.107:/data/usr/lib/ -->


# Copy the wheel file
scp ~/project/nuc980/pc-ble-driver-py/dist/pc_ble_driver_py-*.whl joseph@10.22.22.107:/data/
(*) scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/dist/pc_ble_driver_py-*.whl /data/

# Install on NUC980
ssh joseph@10.22.22.107 "cd /data && pip3 install pc_ble_driver_py-*.whl"
(*) cd /data && pip3 install pc_ble_driver_py-*.whl

# On NUC980
export LD_LIBRARY_PATH=/data/usr/lib:$LD_LIBRARY_PATH



===> copy 
# Create necessary directories
mkdir -p output/target/usr/include/pc-ble-driver
mkdir -p output/target/usr/lib

# Copy Nordic headers and libraries
cp -r ~/project/nuc980/pc-ble-driver/include/* output/target/usr/include/pc-ble-driver/
cp ~/project/nuc980/pc-ble-driver/build/libnrf-ble-driver* output/target/usr/lib/


# Sync the modified usr directory to NUC980, using --delete to remove unneeded files
rsync -avz --progress --delete joseph@10.22.22.107:/joseph/project/nuc980/buildroot_2024/output/target/usr/ /data/usr/



# Remove existing Nordic BLE driver files
rm -rf ~/project/nuc980/buildroot_2024/output/target/usr/include/pc-ble-driver
rm -f ~/project/nuc980/buildroot_2024/output/target/usr/lib/libnrf-ble-driver*


# Make sure CROSS_COMPILE is correctly set
export CROSS_COMPILE=~/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-

# Verify the strip command exists
ls -la ${CROSS_COMPILE}strip

# Try the full path to strip
~/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-strip --strip-unneeded libnrf-ble-driver*.so*


cd ~/project/nuc980/pc-ble-driver-py

# Configure for minimal build
export PYTHONPATH=$SYSROOT/usr/lib/python3.9/site-packages
export PYTHON_INCLUDE_DIR=$SYSROOT/usr/include/python3.9
export PYTHON_LIBRARY=$SYSROOT/usr/lib/libpython3.9.so
export NRF_BLE_DRIVER_PATH=$SYSROOT/usr

# Build with size optimization
CFLAGS="-Os" CXXFLAGS="-Os" python3 setup.py build_ext --inplace \
    --include-dirs="$SYSROOT/usr/include" \
    --library-dirs="$SYSROOT/usr/lib" \
    --plat-name=linux-armv7l \
    --define-macros=NDEBUG=1

# Create a smaller wheel
python3 setup.py bdist_wheel --plat-name linux-armv7l

cd /data
pip3 install pc_ble_driver_py-*.whl --no-deps

# Install only minimal required Python dependencies
pip3 install enum34 wrapt

du -sh output/target/usr/lib/libnrf*
du -sh output/target/usr/include/pc-ble-driver


# Navigate to the Python bindings repository
cd ~/project/nuc980/pc-ble-driver-py

# Then run your setup commands
export PYTHONPATH=$SYSROOT/usr/lib/python3.9/site-packages
export PYTHON_INCLUDE_DIR=$SYSROOT/usr/include/python3.9
export PYTHON_LIBRARY=$SYSROOT/usr/lib/libpython3.9.so
export NRF_BLE_DRIVER_PATH=$SYSROOT/usr

# Build with size optimization
CFLAGS="-Os" CXXFLAGS="-Os" python3 setup.py build_ext --inplace \
    --include-dirs="$SYSROOT/usr/include" \
    --library-dirs="$SYSROOT/usr/lib" \
    --plat-name=linux-armv7l \
    --define-macros=NDEBUG=1

# Create a smaller wheel
python3 setup.py bdist_wheel --plat-name linux-armv7l


# Download the Nordic pre-built package
pip download pc-ble-driver-py

# Extract the wheel file
mkdir -p nordic_wheel
cd nordic_wheel
unzip ../pc_ble_driver_py-*.whl

# Copy the Python module files
cp -r pc_ble_driver_py $SYSROOT/usr/lib/python3.9/site-packages/

# Then copy to your NUC980
rsync -avz --progress $SYSROOT/usr/lib/python3.9/site-packages/pc_ble_driver_py joseph@10.22.22.107:/data/usr/lib/python3/site-packages/

# Copy to your sysroot's Python 3.11 site-packages
cp -r minimal_nordic_driver/pc_ble_driver_py $SYSROOT/usr/lib/python3.11/site-packages/

ls -la $SYSROOT/usr/lib/python3.11/site-packages/pc_ble_driver_py


### 
cp -r minimal_nordic_driver/pc_ble_driver_py ~/project/nuc980/buildroot_2024/output/target/usr/lib/python3/site-packages/
# Sync the entire usr directory to NUC980
rsync -avz --progress --delete ~/project/nuc980/buildroot_2024/output/target/usr/ joseph@10.22.22.107:/data/usr/



### test code
ssh joseph@10.22.22.107

# Create a test script
cat > /data/test_nordic_ble.py << 'EOF'
#!/usr/bin/env python3

import sys
import os

# Add path if needed
sys.path.append('/data/usr/lib/python3/site-packages')

# Print Python path for diagnosis
print("Python Path:", sys.path)

try:
    import pc_ble_driver_py
    from pc_ble_driver_py import BLEDriver, BLEAdvData, BLEEvtID
    from pc_ble_driver_py.observers import BLEDriverObserver, BLEAdapterObserver
    
    print("Successfully imported pc_ble_driver_py")
    print(f"Version: {pc_ble_driver_py.__version__}")
    
    # Try to detect Nordic USB dongle
    serial_port = '/dev/ttyACM0'  # Adjust if necessary
    
    print(f"Looking for Nordic dongle on {serial_port}")
    
    # Try to initialize the driver
    try:
        driver = BLEDriver(serial_port=serial_port, baud_rate=1000000)
        driver.open()
        print("Successfully opened BLE driver!")
        
        # Get adapter info
        version = driver.ble_version_get()
        print(f"Adapter version: {version}")
        
        # Close the driver properly
        driver.close()
        print("Driver closed successfully")
        
    except Exception as e:
        print(f"Error initializing driver: {str(e)}")
    
except ImportError as e:
    print(f"Failed to import pc_ble_driver_py: {str(e)}")
    
    # Check if library files exist
    if os.path.exists('/data/usr/lib/libnrf-ble-driver-sd_api_v6.so'):
        print("libnrf-ble-driver-sd_api_v6.so exists")
    else:
        print("libnrf-ble-driver-sd_api_v6.so missing!")
        
    # Check for Python module files
    if os.path.exists('/data/usr/lib/python3/site-packages/pc_ble_driver_py'):
        print("pc_ble_driver_py directory exists")
    else:
        print("pc_ble_driver_py directory missing!")
EOF

# Make the script executable
chmod +x /data/test_nordic_ble.py


## 
# On your development machine, check if the library exists
ls -la ~/project/nuc980/pc-ble-driver/build/libnrf-ble-driver-sd_api_v6.so*

# Copy the library to your target directory
cp ~/project/nuc980/pc-ble-driver/build/libnrf-ble-driver-sd_api_v6.so* ~/project/nuc980/buildroot_2024/output/target/usr/lib/

# Sync the library to NUC980
rsync -avz --progress ~/project/nuc980/buildroot_2024/output/target/usr/lib/libnrf-ble-driver-sd_api_v6.so* joseph@10.22.22.107:/data/usr/lib/



echo $SYSROOT
/home/joseph/project/nuc980/buildroot_2024/output/host/arm-nuvoton-linux-gnueabi/sysroot



# Copy the wheel to NUC980
scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper/dist/pc_ble_driver_py-*.whl /data/

# SSH to NUC980 and install
ssh joseph@10.22.22.107
cd /data
pip3 install pc_ble_driver_py-*.whl --no-deps


### simple_nordic_wrapper 
scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper/dist/pc_ble_driver_py-*.whl /data/

### binding
# Build the wheel
cd v6_wrapper
python3 setup.py bdist_wheel

# Copy to NUC980
scp dist/pc_ble_driver_py-*.whl joseph@10.22.22.107:/data/
# On NUC980
cd /data
python3 -m pip install pc_ble_driver_py-*.whl --no-deps
# Or extract manually
mkdir -p wheel_extract
cd wheel_extract
unzip ../pc_ble_driver_py-*.whl
cp -r pc_ble_driver_py /data/usr/lib/python3/site-packages/

# Test the wrapper
python3 test_nordic_ble.py


# Method 1: Check with pip list
pip3 list | grep pc_ble_driver_py

# Method 2: Try importing it in Python
python3 -c "import pc_ble_driver_py; print('Package installed')" 2>/dev/null || echo "Package not installed"

# Method 3: Check if the directory exists
ls -la /data/usr/lib/python3/site-packages/pc_ble_driver_py



### test
# python test_nordic_ble.py 
Python Path: ['/data', '/data/usr/lib/python3/site-packages', '/data', '/data/usr/lib/python311.zip', '/data/usr/lib/python3.11', '/data/usr/lib/python3.11/lib-dynload', '/data/usr/lib/python3.11/site-packages', '/data/usr/lib/python3/site-packages']
Successfully imported pc_ble_driver_py
Version: 0.15.0
Looking for Nordic dongle on /dev/ttyACM0
Opening connection to /dev/ttyACM0 at 1000000 baud
Successfully opened BLE driver!
Adapter version: {'company_id': 89, 'version_number': 6, 'subversion_number': 1}
Closing BLE connection
Driver closed successfully


###
cd /data
chmod +x ble_scanner.py
python ble_scanner.py
python3 ble_scanner.py /dev/ttyACM0 60

###
# python3 test_scan.py /dev/ttyACM0 60
1970-01-01 06:31:40,552 - INFO - Starting BLE scan on /dev/ttyACM0
Opening connection to /dev/ttyACM0 at 1000000 baud
1970-01-01 06:31:40,560 - INFO - Driver opened successfully
Initializing BLE adapter
Initializing physical layer
1970-01-01 06:31:40,568 - INFO - Starting scan with params: {'active': True, 'interval_ms': 60, 'window_ms': 40, 'timeout_s': 0}
Starting scan: active=True, interval=60ms, window=40ms, timeout=0s
Scanning... 0s left, 0 devices foundStopping scan
1970-01-01 06:32:40,619 - INFO - Scan stopped


=== SCAN RESULTS ===
No devices found!
Closing BLE connection
1970-01-01 06:32:40,627 - INFO - Driver closed

# In your test script
print(f"Firmware info: {driver.firmware_version_get()}")



# Getting Nordic Connectivity v6 Firmware

To get the v6 firmware for your Nordic dongle, you need to download it from Nordic's official resources. Here's how:

## Option 1: Nordic SDK Download

1. **Download nRF5 SDK**:
   - Go to the [Nordic nRF5 SDK](https://www.nordicsemi.com/Products/Development-software/nRF5-SDK/Download) page
   - Download the "nRF5 SDK for SoftDevice S140 v6.x.x" version
   - Look for connectivity firmware in this path after extracting:
     ```
     components/softdevice/s140/hex/s140_nrf52_6.x.x_softdevice.hex
     ```

2. **Download nRF Connect PC**:
   - Go to [nRF Connect for Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop/Download)
   - Install the app and its "Programmer" module
   - It includes connectivity firmware hex files

## Option 2: Pre-built Connectivity Firmware

1. **Direct Download**:
   - Visit [Nordic's GitHub repository](https://github.com/NordicSemiconductor/pc-ble-driver/tree/master/hex/sd_api_v6)
   - Download the appropriate hex file:
     - `connectivity_6.1.1_usb_with_s140_6.1.1.hex` (for nRF52840 dongles)
     - `connectivity_6.1.1_usb_with_s132_6.1.1.hex` (for nRF52832 dongles)

## Flashing the Firmware

1. **Using nRF Connect Programmer**:
   - Connect your dongle
   - Open nRF Connect → Add/Launch Programmer
   - Select your device
   - Click "Add file" and select the connectivity hex
   - Click "Write" to flash

2. **Using nrfjprog Command Line**:
   ```bash
   # Erase the chip first
   nrfjprog --eraseall
   
   # Program the connectivity firmware
   nrfjprog --program connectivity_6.1.1_usb_with_s140_6.1.1.hex --sectorerase
   
   # Reset the device
   nrfjprog --reset
   ```

Make sure you're using the firmware that matches the SoftDevice version (v6.x.x) to be compatible with the libraries you've built.

https://github.com/NordicSemiconductor/pc-ble-driver/tree/master/hex/sd_api_v6

https://www.nordicsemi.com/Products/Development-software/nRF5-SDK/Download

#### LD debug:
LD_DEBUG=libs,
unset LD_DEBUG


### nRF Connect for Desktop
Device setup completed
07:05:19.874	Connectivity firmware version: ble-connectivity 4.1.4+Mar-11-2021-08-36-04. SoftDevice API version: 5. Baud rate: 1000000.
07:05:19.877	Opening adapter connected to /dev/tty.usbmodemCFE5DED7946B2
07:05:20.856	Successfully opened /dev/tty.usbmodemCFE5DED7946B2. Baud rate: 1000000. Flow control: none. Parity: none.
07:05:20.861	Reset performed on adapter /dev/tty.usbmodemCFE5DED7946B2
07:05:21.977	Adapter connected to /dev/tty.usbmodemCFE5DED7946B2 opened
07:05:23.726	Scan started




cd ~/project/nuc980/pc-ble-driver-py
python make_simple_binding.py --sdk-version=5 --output=simple_nordic_wrapper_v5
cd simple_nordic_wrapper_v5
python setup.py bdist_wheel

# Nordic BLE Binding Successfully Created!

Great! The script ran successfully and created your simple binding for SDK version 5. Here's what to do next:

## Step 1: Build the Wheel Package

```bash
cd simple_nordic_wrapper_v5
python setup.py bdist_wheel
```

## Step 2: Install the Package (Development Machine)

```bash
pip install dist/simple_nordic_wrapper_v5-*.whl
```

## Step 3: Create a Test Script

Create a file called `test_scan.py`:

```python
#!/usr/bin/env python3
import sys
import time
from simple_nordic_wrapper_v5 import BLEDriver, BLEAdapterObserver

class ScanObserver(BLEAdapterObserver):
    def __init__(self):
        super(ScanObserver, self).__init__()
        self.devices = {}
        
    def on_gap_evt_adv_report(self, adapter, addr, rssi, adv_type, adv_data):
        addr_str = ':'.join([f"{addr.addr[i]:02X}" for i in range(5, -1, -1)])
        print(f"DEVICE: {addr_str}, RSSI: {rssi}, Name: {adv_data.name}")
        self.devices[addr_str] = (rssi, adv_data.name)

# Create driver with your dongle's serial port
driver = BLEDriver('/dev/ttyACM0', baud_rate=1000000)
driver.open()

# Initialize adapter
adapter = driver.adapter

# Create and register observer
observer = ScanObserver()
adapter.observer_register(observer)

# Query version
version = driver.ble_version_get()
print(f"Connected to device with firmware version: {version['version_number']}.{version['subversion_number']}")

# Initialize and scan
adapter.driver_init()
adapter.physical_layer_initialize()
adapter.gap_scan_start(active=True, interval_ms=30, window_ms=20, timeout_s=0)

# Run for 30 seconds
try:
    for i in range(30):
        time.sleep(1)
        print(f"Scanning... {i+1}/30s, {len(observer.devices)} devices found", end="\r")
except KeyboardInterrupt:
    print("\nScan interrupted")

# Clean up
adapter.gap_scan_stop()
driver.close()
print("\nComplete - devices found:", len(observer.devices))
```

## Step 4: Run the Test

```bash
chmod +x test_scan.py
./test_scan.py
```

## For Target Device Deployment

To deploy to your NUC980:

```bash
# Copy wheel to target device
scp dist/simple_nordic_wrapper_v5-*.whl joseph@10.22.22.107:/data/

# On the target device:
pip install /data/simple_nordic_wrapper_v5-*.whl
```

This simple binding will let you scan for BLE devices using the Nordic BLE dongle without building the full driver from source.


###
# On your NUC980 device
cd /data

# Create an extraction directory
mkdir -p wheel_extract
cd wheel_extract

# Unzip the wheel file
unzip ../simple_nordic_wrapper_v5-*.whl

# Find your Python site-packages directory
python3 -c "import site; print(site.getsitepackages()[0])"
# This will output something like /data/usr/lib/python3/site-packages

# Copy the package directory to site-packages
# Replace the path below with your actual site-packages path
cp -r simple_nordic_wrapper_v5 /data/usr/lib/python3/site-packages/

# If there's a .dist-info directory, copy that too
cp -r simple_nordic_wrapper_v5-*.dist-info /data/usr/lib/python3/site-packages/ 2>/dev/null || true

cd /data/usr/lib
ln -sf libnrf-ble-driver-sd_api_v6.so libnrf_ble_driver_sd_api_v5.so


# On your development system, check symbols in the cross-compiled library
/home/joseph/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-readelf -s /path/to/the/library/libnrf_ble_driver_sd_api_v6.so | grep sd_rpc

/home/joseph/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-readelf -s /path/to/the/library/libnrf_ble_driver_sd_api_v6.so | grep sd_rpc

### ASIO
 git clone --branch asio-1-12-branch --depth 1 https://github.com/chriskohlhoff/asio.git


### build the binding
/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5
 python create_simple_binding.py --sdk-version=5 --output=simple_nordic_wrapper_v5
cd simple_nordic_wrapper_v5
python setup.py bdist_wheel

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5/dist/simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl /data/


scp joseph@10.22.22.107:/home/joseph/project/nuc980/pc-ble-driver-py/simple_nordic_wrapper_v5/dist/simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl /data/
cd wheel_extract
unzip ../simple_nordic_wrapper_v5-0.1.0-py3-none-any.whl
cp -r simple_nordic_wrapper_v5 /data/usr/lib/python3/site-packages/


### check api

(nordic_env) joseph@joseph-Virtual-Machine:~/project/nuc980/pc-ble-driver/build_v5_arm_full$ /home/joseph/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-nm -D --defined-only ./libnrf-ble-driver-sd_api_v5.so | grep sd_rpc_adapter

/home/joseph/project/nuc980/buildroot_2024/output/host/bin/arm-nuvoton-linux-gnueabi-nm -D --defined-only ./libnrf-ble-driver-sd_api_v5.so | grep -i "event\|scan\|gap"
sd_ble_gattc_write 
