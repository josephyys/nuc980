Use tools like nrfjprog or SEGGER J-Link to flash firmware that enables USB CDC-ACM.
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