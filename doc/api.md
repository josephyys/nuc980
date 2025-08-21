Based on your [`simple_web_server.py`]simple_web_server.py ) running on NUC980 at IP `192.168.0.4:8080`, here are the API endpoints for testing scan and send commands:

## **1. Scan Devices API**

### **Basic Scan (10 seconds default):**
```bash
curl http://192.168.0.4:8080/api/scan_devices/10
```

### **Custom Scan Duration:**
```bash
# Scan for 20 seconds
curl http://192.168.0.4:8080/api/scan_devices/20

# Scan for 5 seconds (quick scan)
curl http://192.168.0.4:8080/api/scan_devices/5
```

### **Expected Response:**
```json
{
  "success": true,
  "scan_duration": 10,
  "devices_found": 2,
  "devices": [
    {
      "address": "E8:D8:95:5E:2B:8C",
      "name": "vao19l-a1",
      "rssi": -65,
      "path": "/org/bluez/hci0/dev_E8_D8_95_5E_2B_8C"
    },
    {
      "address": "AA:BB:CC:DD:EE:FF", 
      "name": "Other Device",
      "rssi": -78,
      "path": "/org/bluez/hci0/dev_AA_BB_CC_DD_EE_FF"
    }
  ]
}
```

## **2. Send Command API**

### **Send Command by Device Name:**
```bash
curl -X POST http://192.168.0.4:8080/api/send_command_api \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "vao19l-a1",
    "command": "R/EBCAECAwQFBg8P",
    "timeout": 30
  }'
```

### **Send Command by Device Address:**
```bash
curl -X POST http://192.168.0.4:8080/api/send_command_api \
  -H "Content-Type: application/json" \
  -d '{
    "device_addr": "E8:D8:95:5E:2B:8C",
    "command": "R/EBCAECAwQFBg8P",
    "timeout": 30
  }'
```

### **Expected Response:**
```json
{
  "success": true,
  "command_sent": "R/EBCAECAwQFBg8P",
  "device_name": "vao19l-a1",
  "device_addr": "E8:D8:95:5E:2B:8C",
  "response": {
    "data": "b'\\x47\\xf1\\x01\\x08\\x01\\x02\\x03\\x04\\x05\\x06\\x0f\\x0f'",
    "hex": "47 f1 01 08 01 02 03 04 05 06 0f 0f",
    "timestamp": "2025-06-12 14:30:45"
  },
  "response_time": 1.25
}
```

## **3. Other Useful APIs**

### **Check Bluetooth Status:**
```bash
curl http://192.168.0.4:8080/api/bluetooth_status
```

### **Get Latest Notification:**
```bash
curl http://192.168.0.4:8080/api/notification
```

### **Server Status:**
```bash
curl http://192.168.0.4:8080/api/status
```

### **Network Info:**
```bash
curl http://192.168.0.4:8080/api/network
```

### **GATT Connection Status:**
```bash
curl http://192.168.0.4:8080/api/gatt_status
```

## **4. Complete Test Sequence**

```bash
#!/bin/bash
# Complete API test script

NUC980_IP="192.168.0.4:8080"

echo "=== 1. Check server status ==="
curl -s http://${NUC980_IP}/api/status | jq .

echo -e "\n=== 2. Check Bluetooth status ==="
curl -s http://${NUC980_IP}/api/bluetooth_status | jq .

echo -e "\n=== 3. Scan for devices (10 seconds) ==="
curl -s http://${NUC980_IP}/api/scan_devices/10 | jq .

echo -e "\n=== 4. Send command to device ==="
curl -s -X POST http://${NUC980_IP}/api/send_command_api \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "vao19l-a1",
    "command": "R/EBCAECAwQFBg8P",
    "timeout": 30
  }' | jq .

echo -e "\n=== 5. Get latest notification ==="
curl -s http://${NUC980_IP}/api/notification | jq .
```

## **5. Python Test Script**

```python
#!/usr/bin/env python3
import requests
import json
import time

NUC980_BASE_URL = "http://192.168.0.4:8080"

def test_nuc980_apis():
    print("=== Testing NUC980 BLE APIs ===")
    
    # 1. Check status
    print("\n1. Server Status:")
    response = requests.get(f"{NUC980_BASE_URL}/api/status")
    print(json.dumps(response.json(), indent=2))
    
    # 2. Scan devices
    print("\n2. Scanning devices (10 seconds)...")
    response = requests.get(f"{NUC980_BASE_URL}/api/scan_devices/10")
    scan_result = response.json()
    print(json.dumps(scan_result, indent=2))
    
    # 3. Send command if devices found
    if scan_result.get('success') and scan_result.get('devices'):
        device = scan_result['devices'][0]  # Use first device
        print(f"\n3. Sending command to {device['name']} ({device['address']})...")
        
        command_data = {
            "device_name": device['name'],
            "command": "R/EBCAECAwQFBg8P",
            "timeout": 30
        }
        
        response = requests.post(
            f"{NUC980_BASE_URL}/api/send_command_api",
            headers={"Content-Type": "application/json"},
            json=command_data
        )
        print(json.dumps(response.json(), indent=2))
    else:
        print("\n3. No devices found for command test")
    
    # 4. Get notification
    print("\n4. Latest notification:")
    response = requests.get(f"{NUC980_BASE_URL}/api/notification")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_nuc980_apis()
```

## **6. Web Browser Test**

You can also test directly in a web browser:

**Open:** `http://192.168.0.4:8080`

The web interface provides:
- ✅ **API Testing section** with buttons for scan and send commands
- ✅ **Real-time notification display**
- ✅ **Interactive forms** for device configuration
- ✅ **Auto-refresh** for notifications every 2 seconds

## **Key APIs Summary:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/scan_devices/10` | GET | Scan for 10 seconds |
| `/api/send_command_api` | POST | Send BLE command |
| `/api/notification` | GET | Get latest response |
| `/api/bluetooth_status` | GET | Check BT adapter |
| `/api/status` | GET | Server health |

The device must be **configured first** via the web interface at `http://192.168.0.4:8080` before sending commands via API.


curl -X POST http://192.168.0.4:8080/api/configure_device \
  -H "Content-Type: application/json" \
  -d '{
    "device_addr": "E8:D8:95:5E:2B:8C",
    "service_uuid": "6e400001-b5a3-f393-e0a9-e50e24dcca9e",
    "command_uuid": "6e400002-b5a3-f393-e0a9-e50e24dcca9e",
    "response_uuid": "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
  }'

  curl -X POST http://192.168.0.4:8080/api/connect_device