# from pc_ble_driver_py.ble_adapter import BLEAdapter
# from pc_ble_driver_py.ble_driver import BLEDriver

# driver = BLEDriver(serial_port='/dev/ttyACM0', baud_rate=115200)
# adapter = BLEAdapter(driver)
# adapter.open()
# # 扫描
# adapter.driver.ble_gap_scan_start()
# 连接、写入、订阅···
import serial

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

# 举例：发 AT+SCAN? 命令，然后等待 JSON
ser.write(b"AT+SCAN?\r\n")
line = ser.readline().decode()
# e.g. '{"evt":"ADV","addr":"AB:CD:EF:12:34:56","rssi":-60}'

# 发起连接
ser.write(b"AT+CONNECT=AB:CD:EF:12:34:56\r\n")
resp = ser.readline()
print("resp", resp)

# 写入命令特征 UUID-CMD
uuid_cmd="uuid_cmd"
cmd_payload="cmd_payload"

ser.write(b"AT+WRITE=" + uuid_cmd.encode() + b"," + cmd_payload.encode() + b"\r\n")
print("Sent:", b"AT+WRITE=" + uuid_cmd.encode() + b"," + cmd_payload.encode() + b"\r\n")
resp = ser.readline()
print("Received:", resp)



# 订阅通知特征 UUID-RSP
uuid_rsp="uuid_rsp"
ser.write(b"AT+SUB=" + uuid_rsp.encode() + b"\r\n")
resp = ser.readline()
print("resp", resp)
