/Users/joseph/Downloads/nrfutil device program --firmware  /Users/joseph/Downloads/connectivity_dfu.zip --traits nordicDfu

-->
[00:00:00] ------   0% [2/2 CFE5DED7946B] Failed,
Error: One or more program tasks failed:
 * CFE5DED7946B:  (SdfuExtSdVersionFailure)


/Users/joseph/Downloads/nrfutil pkg generate --hw-version 52 --sd-req 0xB6 --application /Users/joseph/Downloads/connectivity_4.1.4_1m_with_s140_6.1.1.hex --application-version 1 /Users/joseph/Downloads/connectivity_dfu.zip



/Users/joseph/Downloads/nrfutil nrf5sdk-tools pkg generate --hw-version 52 --sd-req 0x00 --application /Users/joseph/Downloads/connectivity_4.1.4_1m_with_s140_6.1.1.hex --application-version 1 /Users/joseph/Downloads/connectivity_dfu_0x00.zip

/Users/joseph/Downloads/nrfutil device program --firmware /Users/joseph/Downloads/connectivity_dfu_0x00.zip --traits nordicDfu


--->
/Users/joseph/Downloads/pc-ble-driver-4.1.4-hex\ 2/hex/sd_api_v6/connectivity_4.1.4_usb_with_s140_6.1.1.hex 

/Users/joseph/Downloads/nrfutil nrf5sdk-tools pkg generate --hw-version 52 --sd-req 0xB6 --application /Users/joseph/Downloads/pc-ble-driver-4.1.4-hex\ 2/hex/sd_api_v6/connectivity_4.1.4_usb_with_s140_6.1.1.hex --application-version 1 /Users/joseph/Downloads/connectivity_dfu_0x00.zip

-- AE
/Users/joseph/Downloads/nrfutil nrf5sdk-tools pkg generate --hw-version 52 --sd-req 0xAE --application /Users/joseph/Downloads/pc-ble-driver-4.1.4-hex\ 2/hex/sd_api_v6/connectivity_4.1.4_usb_with_s140_6.1.1.hex --application-version 1 /Users/joseph/Downloads/connectivity_dfu_0xAE.zip

/Users/joseph/Downloads/nrfutil device program --firmware /Users/joseph/Downloads/connectivity_dfu_0xAE.zip --traits nordicDfu


[00:00:00] ------   0% [2/2 CFE5DED7946B] Failed,
Error: One or more program tasks failed:
 * CFE5DED7946B:  (SdfuExtSdVersionFailure)

-- 0xCB
/Users/joseph/Downloads/nrfutil nrf5sdk-tools pkg generate --hw-version 52 --sd-req 0xCB --application /Users/joseph/Downloads/pc-ble-driver-4.1.4-hex\ 2/hex/sd_api_v6/connectivity_4.1.4_usb_with_s140_6.1.1.hex --application-version 1 /Users/joseph/Downloads/connectivity_dfu_0xCB.zip

/Users/joseph/Downloads/nrfutil device program --firmware /Users/joseph/Downloads/connectivity_dfu_0xCB.zip --traits nordicDfu

-- 0x00  as [https://academy.nordicsemi.com/flash-instructions-for-nrf52840-dongle/]
/Users/joseph/Downloads/nrfutil pkg generate --hw-version 52 --sd-req=0x00  --application /Users/joseph/Downloads/pc-ble-driver-4.1.4-hex\ 2/hex/sd_api_v6/connectivity_4.1.4_usb_with_s140_6.1.1.hex  --application-version 1 /Users/joseph/Downloads/connectivity_dfu_0x00.zip

/Users/joseph/Downloads/nrfutil device program --firmware /Users/joseph/Downloads/connectivity_dfu_0x00.zip --traits nordicDfu

/Users/joseph/Downloads/nrfutil install nrf5sdk-tools


### use NCS--> nrf52840dongle
#### flash
https://academy.nordicsemi.com/flash-instructions-for-nrf52840-dongle/

/Users/joseph/Downloads/nrfutil pkg generate --hw-version 52 --sd-req=0x00  --application zephyr.hex --application-version 1 app.zip

/Users/joseph/Downloads/nrfutil device program --firmware app.zip --traits nordicDfu



