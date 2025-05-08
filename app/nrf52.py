#!/usr/bin/env python3
# filepath: ble_controller.py
import serial
import time
import binascii

class NRF52Controller:
    def __init__(self, port="/dev/ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Give the connection time to establish
        
    def send_command(self, cmd):
        """Send command to nRF52 and get response"""
        self.ser.write((cmd + '\r\n').encode())
        time.sleep(0.5)
        response = b''
        while self.ser.in_waiting:
            response += self.ser.read(self.ser.in_waiting)
        return response.decode('utf-8', errors='ignore')
    
    def scan_devices(self):
        """Start scanning for BLE devices"""
        return self.send_command("ble_scan")
    
    def connect_device(self, address):
        """Connect to a BLE device by address"""
        return self.send_command(f"ble_connect {address}")
        
    def write_characteristic(self, handle, data):
        """Write data to a BLE characteristic"""
        hex_data = binascii.hexlify(data.encode()).decode()
        return self.send_command(f"ble_write {handle} {hex_data}")
    
    def read_characteristic(self, handle):
        """Read data from a BLE characteristic"""
        return self.send_command(f"ble_read {handle}")
    
    def disconnect(self):
        """Disconnect from BLE device"""
        return self.send_command("ble_disconnect")
        
    def close(self):
        """Close the serial connection"""
        if self.ser.is_open:
            self.ser.close()

if __name__ == "__main__":
    # Example usage
    nrf = NRF52Controller()
    
    # Scan for devices
    print("Scanning for devices...")
    print(nrf.scan_devices())
    
    # Example: connect to a device and exchange data
    # Replace with your device's MAC address
    device_addr = "XX:XX:XX:XX:XX:XX"
    print(f"Connecting to {device_addr}...")
    print(nrf.connect_device(device_addr))
    
    # Replace with your characteristic handle
    handle = "0x0025"
    print(f"Writing to characteristic {handle}")
    print(nrf.write_characteristic(handle, "Hello BLE"))
    
    print(f"Reading from characteristic {handle}")
    print(nrf.read_characteristic(handle))
    
    print("Disconnecting...")
    print(nrf.disconnect())
    
    nrf.close()