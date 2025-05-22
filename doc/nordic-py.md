git clone https://github.com/NordicSemiconductor/pc-ble-driver-py.git
cd pc-ble-driver-py
pip3 install -r requirements.txt
python3 setup.py build
sudo python3 setup.py install

export CROSS_COMPILE=~/project/nuc980/initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-
export SYSROOT=~/project/nuc980/initramfs/output/host/arm-nuvoton-linux-gnueabi/sysroot
export CROSS_COMPILE=~/project/nuc980/initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-


# Building Nordic's pc-ble-driver-py for NUC980

Building Nordic's Python BLE driver for NUC980 requires cross-compilation. Here's a step-by-step guide:

## Prerequisites

First, ensure your Buildroot configuration includes these packages:

```bash
cd ~/project/nuc980/initramfs
make menuconfig
```

Select:
- `Target packages → Interpreter languages and scripting → python3`
- `Target packages → Development tools → boost`
- `Target packages → Libraries → Other → swig`

## Step 1: Build pc-ble-driver (C/C++ Library)

```bash
# Clone the C++ driver repo
cd ~/project/nuc980
git clone https://github.com/NordicSemiconductor/pc-ble-driver.git
cd pc-ble-driver

# Set up cross-compilation environment
export CROSS_COMPILE=~/project/nuc980/initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-
export SYSROOT=~/project/nuc980/initramfs/output/host/arm-nuvoton-linux-gnueabi/sysroot

# Create build directory
mkdir -p build && cd build

# Configure with CMake for cross-compilation
cmake -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-toolchain.cmake \
    -DCMAKE_INSTALL_PREFIX=$SYSROOT/usr \
    -DCONNECTIVITY_VERSION=4 \
    -DCOMPILE_CONNECTIVITY=1 ..

# Build and install to sysroot
make -j$(nproc)
make install
```

## Step 2: Create ARM Toolchain File

Create `~/project/nuc980/pc-ble-driver/cmake/arm-toolchain.cmake`:

```cmake
# ARM toolchain configuration for NUC980
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

# Set cross compiler paths
set(CMAKE_C_COMPILER ${CMAKE_CURRENT_LIST_DIR}/../../../initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-gcc)
set(CMAKE_CXX_COMPILER ${CMAKE_CURRENT_LIST_DIR}/../../../initramfs/output/host/bin/arm-nuvoton-linux-gnueabi-g++)

# Set sysroot path
set(CMAKE_SYSROOT ${CMAKE_CURRENT_LIST_DIR}/../../../initramfs/output/host/arm-nuvoton-linux-gnueabi/sysroot)

# Don't run test executables on host
set(CMAKE_CROSSCOMPILING TRUE)

# Search paths
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
```

## Step 3: Build Python Bindings

```bash
# Clone the Python bindings repo
cd ~/project/nuc980
git clone https://github.com/NordicSemiconductor/pc-ble-driver-py.git
cd pc-ble-driver-py

# Configure environment for cross-compiling Python extension
export PYTHONPATH=$SYSROOT/usr/lib/python3.9/site-packages
export PYTHON_INCLUDE_DIR=$SYSROOT/usr/include/python3.9
export PYTHON_LIBRARY=$SYSROOT/usr/lib/libpython3.9.so

# Build the Python package for ARM
python3 setup.py build_ext --inplace --swig-opts="-I$SYSROOT/usr/include" \
    --include-dirs="$SYSROOT/usr/include" \
    --library-dirs="$SYSROOT/usr/lib" \
    --rpath="$SYSROOT/usr/lib" \
    --plat-name=linux-armv7l
```

## Step 4: Create Wheel Package for NUC980

```bash
python3 setup.py bdist_wheel --plat-name linux-armv7l
```

## Step 5: Deploy to NUC980

```bash
# Copy the wheel to your NUC980 data partition
scp dist/pc_ble_driver_py-*.whl joseph@10.22.22.107:/data/

# On the NUC980, install the wheel
ssh joseph@10.22.22.107
cd /data
pip3 install pc_ble_driver_py-*.whl
```

## Step 6: Install Firmware

```bash
# On NUC980, create directory for connectivity firmware
mkdir -p /data/usr/lib/pc-ble-driver/hex/

# Copy firmware files
scp ~/project/nuc980/pc-ble-driver/build/hex/connectivity_*.hex joseph@10.22.22.107:/data/usr/lib/pc-ble-driver/hex/
```

## Troubleshooting

If you encounter issues:
1. Check all dependencies are properly installed
2. Verify USB permissions for the Nordic dongle
3. Make sure BLE kernel modules are loaded
4. Test with a simple example script first

The build process is complex - you may need to adjust paths based on your specific Buildroot configuration.

# Selecting Boost and SWIG Packages in Buildroot for Nordic pc-ble-driver-py

## Boost Requirements

Yes, you need boost-python specifically, but pc-ble-driver also needs other Boost components. Here's what to select:

```
Target packages → Libraries → boost
```

When you select boost, you'll see a submenu with many components. You should select:

- `[*] boost`
- `[*] boost-atomic` 
- `[*] boost-chrono`
- `[*] boost-date_time`
- `[*] boost-filesystem`
- `[*] boost-program_options`
- `[*] boost-python` (essential for Python bindings)
- `[*] boost-system`
- `[*] boost-thread`

The pc-ble-driver uses several Boost libraries for its C++ implementation, and the Python bindings specifically require boost-python.

## SWIG Requirements

Yes, you need the host-swig package, not the target swig package:

```
Host utilities → host-swig
```

SWIG is used during the build process on your host machine to generate the Python wrapper code for the C++ libraries, not on the target NUC980. That's why you need the host version.

Make sure you also have these Python-related packages:

```
Target packages → Interpreter languages and scripting → python3
Target packages → Interpreter languages and scripting → python3-setuptools
```

These selections will give you the minimum required packages to build the Nordic pc-ble-driver-py for your NUC980 platform.