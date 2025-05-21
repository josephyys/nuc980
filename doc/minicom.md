
sudo minicom -s
Navigate to "Serial port setup" and configure the following:

Serial Device: Set to /dev/tty.usbmodemA020140903051.
Bps/Par/Bits: Set to 115200 8N1 (115200 baud, 8 data bits, no parity, 1 stop bit).
Hardware Flow Control: Disable (set to No).
Software Flow Control: Disable (set to No).
Save the configuration as the default or a named configuration.

Ctrl + A, then X


Navigate to "Serial port setup" and configure the following:

Serial Device: Set to /dev/tty.usbmodemA020140903051.
Bps/Par/Bits: Set to 115200 8N1 (115200 baud, 8 data bits, no parity, 1 stop bit).
Hardware Flow Control: Disable (set to No).
Software Flow Control: Disable (set to No).
Save the configuration as the default or a named configuration.

Ctrl + A, then X


ssh -vvv -i "C:\Users\joseph\Desktop\project\algo\batch\OraDB.pem" -R 8084:127.0.0.1:8080 -N -T ubuntu@52.197.102.250 -p 8082
