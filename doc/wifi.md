nrf7002dk_nrf5340_cpunet

https://www.raytac.com/tw/news/ins.php?index_id=139
Nordic AN7002Q-nRF5340開發板(AN7002Q-DB-5340)

nrf/samples/wifi/radio_test: 測試 Wi‑Fi 無線收發功能

nrf/samples/wifi/scan: 掃描 AP

nrf/samples/wifi/connectivity_assistant 或 station: 實作 STA/Client 模式，連上 Wi‑Fi 網絡 
Raytac 官方文檔強調必須為 AN7002Q 模組寫入 MAC 地址（使用 OTP），且建議先 flash radio_test 以燒入 MAC，才可切換到 scan 或 station 範例


nrf/samples/bluetooth/peripheral_uart: BLE 外圍設備

nrf/samples/wifi/sta
nrf/samples/wifi/station
Wi‑Fi Station：nrf/samples/wifi/station
連上 Wi‑Fi AP，取得 IP。
這是核心範例

UART-to-Ethernet Bridge (若要做類似 USB dongle 行為)
參考：
nrf/samples/net/wifi/echo_server（示範 socket server）
Zephyr samples/net/slip（用 UART 傳 TCP/IP）
如果要做 pppd，可參考 Zephyr ppp 示例。

AN7002Q-DB-5340 跑 Wi‑Fi + SLIP over UART，讓 NUC980 pppd 撥號，模擬網卡（像 USB 網卡一樣）
NUC980 上層 TCP/IP Stack 全部不需要改，直接用。


Wi‑Fi 連網	nrf/samples/wifi/station
TCP Echo Server	nrf/samples/net/wifi/echo_server
SLIP over UART	zephyr/samples/net/slip
PPP over UART	Zephyr 支援，但需要自己加 CONFIG_PPP，範例可參考 Zephyr 官方 samples/net/ppp

PPP UART Bridge	zephyrproject-rtos/zephyr ppp sample
SLIP UART Bridge	zephyrproject-rtos/zephyr slip sample
Wi‑Fi Gateway	Nordic Wi‑Fi samples

zephyr/samples/net/slip



C:\ncs\v3.0.2\zephyr\samples\bluetooth\hci_usb\build\hci_usb\zephyr



若是將 nRF5340 SoC 本身具備的 原生 USB 控制器 的 D+ 和 D- 接腳，連接到那個 USB-C 接頭上，就能燒錄hci-usb 使用? 還能進行燒錄或是除錯嗎


好的，這是一個非常實際的問題。讓我們來分析 `slattach` 和 `pppd` 的差異，以及如何在 Buildroot 中啟用它們來進行測試。

### **`slattach` vs. `pppd`：大小與功能比較**

| 特性 | `slattach` | `pppd` (Point-to-Point Protocol Daemon) |
| :--- | :--- | :--- |
| **大小** | **非常小** (通常幾十 KB) | **較大** (數百 KB) |
| **功能** | 極其簡單，只負責將序列埠綁定到一個網路介面 (如 `sl0`)。 | **功能強大**，是一個完整的守護程式。支援認證 (PAP, CHAP)、壓縮、IP 位址協商等。 |
| **依賴** | **幾乎沒有**，是 `net-tools` 的一部分。 | 可能有依賴，例如 `libpcap` 或加密函式庫 (取決於配置)。 |
| **用途** | 建立一個最基本的、無協議的序列埠 IP 連結。 | 建立一個標準的、功能完整的點對點網路連結。 |

**結論：`slattach` 遠比 `pppd` 更輕量級。** 對於您的記憶體受限的 NUC980 來說，`slattach` 是理想的起點。

---

### **如何在 Buildroot 中啟用 (How to Enable in Buildroot)**

您可以同時啟用兩者，以便在目標系統上進行比較測試。

首先，進入 Buildroot 的配置介面：
```bash
cd /home/joseph/project/nuc980/buildroot_2024
make menuconfig
```

#### **1. 啟用 `slattach` (包含在 `net-tools` 中)**

`slattach` 是 `net-tools` 套件的一部分，這是一個包含許多基礎網路工具（如 `ifconfig`, `route`）的集合。您很可能已經啟用了它。

*   **路徑**:
    ```
    Target packages --->
        Networking applications --->
            [*] net-tools
    ```
*   **確認選項**: 確保 `net-tools` 前面有 `[*]`。
*   **`.config` 變數**: `BR2_PACKAGE_NET_TOOLS=y`

#### **2. 啟用 `pppd`**

`pppd` 是一個獨立的套件。

*   **路徑**:
    ```
    Target packages --->
        Networking applications --->
            [*] pppd
    ```
*   **確認選項**: 找到 `pppd` 並按下 `Y` 使其前面出現 `[*]`。您可以進入其子選項，但通常保持預設即可，以避免增加不必要的依賴和大小。
*   **`.config` 變數**: `BR2_PACKAGE_PPPD=y`

---

### **3. 重建並部署 (Rebuild and Deploy)**

儲存您的 `menuconfig` 設定並退出，然後執行 `make` 來重建您的根檔案系統。
```bash
make
```
完成後，將更新後的 `rootfs.tar` 或 `output/target` 目錄部署到您的 NUC980。

---

### **如何在 NUC980 上測試**

假設您的 Wi-Fi 模組連接到了 ttyS1。

#### **測試 `slattach` (更輕量，推薦)**

1.  **綁定序列埠**:
    ```bash
    # -p slip: 指定使用 SLIP 協議
    # -s 115200: 設定鮑率
    # /dev/ttyS1: 您的序列埠裝置
    # &: 在背景執行
    slattach -p slip -s 115200 /dev/ttyS1 &
    ```

2.  **檢查網路介面**:
    ```bash
    ifconfig
    ```
    您應該會看到一個新的介面，通常叫做 `sl0`。

3.  **啟用介面並設定 IP**:
    ```bash
    # 啟用 sl0 介面
    ifconfig sl0 up

    # 為 sl0 設定一個 IP 位址 (這個 IP 應該與您 Wi-Fi 連上的網路同網段)
    ifconfig sl0 192.168.1.123 netmask 255.255.255.0

    # 新增預設路由
    route add default gw 192.168.1.1 sl0
    ```

4.  **測試連線**:
    ```bash
    ping 8.8.8.8
    ```

#### **測試 `pppd` (功能更強大)**

`pppd` 的使用更複雜，通常需要配置文件或較長的指令行參數。

1.  **啟動 pppd**:
    ```bash
    # /dev/ttyS1: 序列埠
    # 115200: 鮑率
    # noauth: 不進行認證 (對於直接連接的協處理器是必要的)
    # local: 不發送 LCP echo 封包
    # 192.168.1.123:192.168.1.1: 設定本地和遠端 IP (如果對端不支援協商)
    pppd /dev/ttyS1 115200 noauth local 192.168.1.123:192.168.1.1
    ```

2.  **檢查網路介面**:
    ```bash
    ifconfig
    ```
    您應該會看到一個新的介面，通常叫做 `ppp0`，並且 IP 位址已經被自動設定好。

3.  **測試連線**:
    ```bash
    ping 192.168.1.1 # Ping 路由
    ping 8.8.8.8
    ```

### **建議**

**從 `slattach` 開始測試。** 它最簡單、最輕量，完全符合您將 Wi-Fi 模組作為一個透明 IP 通道的需求。只有當您發現需要 PPP 提供的特定功能（例如，需要對端進行認證）時，才需要考慮使用更複雜的 `pppd`。


mknod /dev/ppp c 108 0


這個錯誤訊息非常棒，它清楚地告訴了我們問題的根源！您又向前邁進了一大步。

這個新的錯誤 `Couldn't open the /dev/ppp device: No such device or address` 和提示 `Please load the ppp_generic kernel module` 意味著：

1.  您成功地建立了 ppp 設備節點 (user-space part)。**這一步是正確的！**
2.  但是，當 `pppd` 程式嘗試透過這個節點與核心溝通時，Linux 核心回報「我不知道這個設備是什麼」，因為**核心內部缺少 PPP 的驅動程式** (kernel-space part)。

這與 NUC980 的性能或記憶體完全無關，這純粹是一個**核心配置**問題。

---

### **解決方案：在 Linux 核心中啟用 PPP 支援**

您需要在 Buildroot 中為您的 Linux 核心啟用 PPP 相關的模組。

#### **1. 進入 Linux 核心配置 (linux-menuconfig)**

```bash
cd /home/joseph/project/nuc980/buildroot_2024
make linux-menuconfig
```

#### **2. 找到並啟用 PPP 選項**

請依照以下路徑導航：

```
Device Drivers  --->
    [*] Network device support  --->
```

進入 `Network device support` 後，向下捲動，找到 PPP 相關的選項，並確保它們被啟用。

您需要啟用以下幾個關鍵選項：

```
<*> PPP (point-to-point protocol) support
<*>   PPP support for async serial ports
<*>   PPP Deflate compression
< >   PPP filtering
<*>   PPP BSD-Compress compression
< >   PPP MPPE compression (encryption)
<*>   PPP multilink support
< >   PPP over Ethernet
< >   PPP over L2TP
```

**最重要的選項是：**

*   **`<*> PPP (point-to-point protocol) support`**: 這是最核心的 PPP 驅動 (`ppp_generic.ko` 的來源)。
*   **`<*> PPP support for async serial ports`**: 這是讓 PPP 能夠在序列埠 (`/dev/ttyS*`) 上運行的關鍵。

**說明：**
*   請確保選項前面是 `<*>` (built-in) 或 `<M>` (module)。
*   **`<*>` (built-in)**: 將驅動程式直接編譯進 Linux 核心。這是**最推薦**的方式，因為您不需要在系統啟動後手動載入模組。
*   `<M>` (module)**: 將驅動程式編譯成一個獨立的 `.ko` 檔案。如果您選擇這個，您需要在執行 `pppd` 之前，先執行 `modprobe ppp_generic` 和 `modprobe ppp_async`。對於嵌入式系統，直接編譯進核心 `<*>` 更簡單、更可靠。

#### **3. 儲存並重建核心**

1.  完成設定後，儲存您的變更並退出 `linux-menuconfig`。
2.  執行 `make` 來重建您的專案。Buildroot 會偵測到核心配置的變更，並自動重新編譯 Linux 核心。
    ```bash
    make
    ```
3.  將新生成的核心映像檔 (`zImage` 或類似名稱) 和根檔案系統部署到您的 NUC980。

---

### **再次測試**

當您使用新的核心啟動 NUC980 後，再次執行您的指令：

```bash
# mknod /dev/ppp c 108 0  (如果您的 /dev 是臨時的，每次重啟都需要執行)
# /data/usr/sbin/pppd /dev/ttyS1 115200 noauth local 192.168.1.123:192.168.1.1
```

這次，`pppd` 應該不會再報「No such device」或「Please load the ppp_generic kernel module」的錯誤了。它會成功啟動，並開始嘗試透過 ttyS1 與對端設備進行 LCP (Link Control Protocol) 協商。

由於您的 Wi-Fi 模組還沒有燒錄對應的韌體，`pppd` 最終可能會因為超時而退出，但這已經證明了您的 NUC980 **系統環境已經完全準備好了**，可以支援 `pppd`。


Of course. Your thinking is spot on. This is an excellent and very common strategy for resource-constrained embedded systems.

**Yes, you can absolutely put `pppd`, its libraries, and the necessary kernel modules onto the JFFS2 NAND partition and load them dynamically to spare your initramfs space.**

This approach has several key advantages:
*   **Smaller Initramfs:** Your initial RAM footprint is minimized, leading to a faster boot time.
*   **Flexible Updates:** You can update the `pppd` application or kernel modules on the NAND partition without having to rebuild and reflash the entire initramfs.
*   **More Space:** You free up precious space in the initramfs for truly essential boot-time components.

Here is the complete step-by-step guide on how to achieve this.

---

### **Step 1: Configure Buildroot for Kernel Modules**

First, you must configure the Linux kernel to build PPP support as loadable modules (`.ko` files) instead of building them directly into the kernel.

1.  **Enter `linux-menuconfig`**:
    ```bash
    cd /home/joseph/project/nuc980/buildroot_2024
    make linux-menuconfig
    ```

2.  **Change PPP options to `<M>` for Module**:
    Navigate to `Device Drivers ---> [*] Network device support --->` and change the following options from `<*>` (built-in) to `<M>` (module) by pressing the `M` key:

    ```
    <M> PPP (point-to-point protocol) support
    <M>   PPP support for async serial ports
    <M>   PPP Deflate compression
    <M>   PPP BSD-Compress compression
    ```
    This tells the kernel to generate `ppp_generic.ko`, `ppp_async.ko`, etc., as separate files.

3.  **Save and Rebuild**:
    Save the configuration and run `make`. Buildroot will now create the `.ko` files in `output/target/lib/modules/<kernel-version>/...`

---

### **Step 2: Identify and Copy All Necessary Files to NAND**

You need to copy three types of files from your Buildroot `output/target` directory to your JFFS2 partition.

Let's assume your JFFS2 partition is mounted at `/data` on the NUC980.

1.  **The `pppd` Executable**:
    *   **Source**: `output/target/usr/sbin/pppd`
    *   **Destination on NUC980**: `/data/usr/sbin/pppd`

2.  **The Kernel Modules (`.ko` files)**:
    *   **Source Directory**: `output/target/lib/modules/<your-kernel-version>/kernel/drivers/net/ppp/`
    *   **Files to Copy**: `ppp_generic.ko`, `ppp_async.ko`, and `slhc.ko` (a dependency).
    *   **Destination on NUC980**: `/data/lib/modules/` (or any other directory you choose).

3.  **The Shared Libraries (`.so` files)**:
    `pppd` may depend on shared libraries. You must find and copy them too.
    *   **How to find dependencies**: On your build host, run the `ldd` command from your cross-compile toolchain:
        ```bash
        # Replace with your actual toolchain prefix
        arm-nuvoton-linux-gnueabi-ldd output/target/usr/sbin/pppd
        ```
    *   The output will list the required `.so` files (e.g., `libpcap.so.1`, `libcrypt.so.1`).
    *   **Source**: Find these files in `output/target/lib/` or `output/target/usr/lib/`.
    *   **Destination on NUC980**: `/data/usr/lib/`

---

### **Step 3: Create a Script on NUC980 to Load and Run `pppd`**

Now, on the NUC980, you'll need a script that runs after the `/data` partition is mounted. This script will perform all the setup steps dynamically.

Create a script, for example, `/etc/init.d/S91_start_ppp`:

````bash
#!/bin/sh

# This script runs after the JFFS2 partition is mounted on /data

# 1. Load the required kernel modules from the NAND partition
#    The order is important due to dependencies.
echo "Loading PPP kernel modules from NAND..."
insmod /data/lib/modules/slhc.ko
insmod /data/lib/modules/ppp_generic.ko
insmod /data/lib/modules/ppp_async.ko

# 2. Create the device node (if it doesn't exist)
if [ ! -c /dev/ppp ]; then
    echo "Creating /dev/ppp device node..."
    mknod /dev/ppp c 108 0
fi

# 3. Tell the dynamic linker where to find the shared libraries on NAND
export LD_LIBRARY_PATH=/data/usr/lib:$LD_LIBRARY_PATH

# 4. Run the pppd executable from the NAND partition
echo "Starting pppd from NAND..."
/data/usr/sbin/pppd /dev/ttyS1 115200 noauth local 192.168.1.123:192.168.1.1

echo "PPP setup complete."
````

Make this script executable: `chmod +x /etc/init.d/S91_start_ppp`.

### **Summary of the Dynamic Loading Workflow**

1.  NUC980 boots using the minimal initramfs.
2.  An init script mounts your JFFS2 NAND partition to `/data`.
3.  Your `S91_start_ppp` script runs.
4.  `insmod` loads the PPP kernel drivers from `/data/lib/modules/`.
5.  `mknod` creates the ppp interface.
6.  `LD_LIBRARY_PATH` is set so the system can find libraries in `/data/usr/lib`.
7.  The `pppd` executable is run directly from `/data/usr/sbin/`.

This is a robust and professional way to structure an embedded system with limited RAM, and it will work perfectly for your use case.

ppp_generic.ko, ppp_async.ko, and slhc.ko
/data/lib/modules/


joseph@joseph-Virtual-Machine:~/project/nuc980/buildroot_2024$ find output/ -name ppp_generic.ko
output/target/lib/modules/5.10.140/kernel/drivers/net/ppp/ppp_generic.ko
output/build/linux-custom/drivers/net/ppp/ppp_generic.ko
joseph@joseph-Virtual-Machine:~/project/nuc980/buildroot_2024$ find output/ -name ppp_async.ko
output/target/lib/modules/5.10.140/kernel/drivers/net/ppp/ppp_async.ko
output/build/linux-custom/drivers/net/ppp/ppp_async.ko
joseph@joseph-Virtual-Machine:~/project/nuc980/buildroot_2024$ find output/ -name slhc.ko
output/target/lib/modules/5.10.140/kernel/drivers/net/slip/slhc.ko
output/build/linux-custom/drivers/net/slip/slhc.ko

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/lib/modules/5.10.140/kernel/drivers/net/ppp/ppp_generic.ko /data/usr/lib/modules/

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/lib/modules/5.10.140/kernel/drivers/net/ppp/ppp_async.ko /data/usr/lib/modules/

scp -P 8084 joseph@52.197.102.250:/home/joseph/project/nuc980/buildroot_2024/output/target/lib/modules/5.10.140/kernel/drivers/net/slip/slhc.ko /data/usr/lib/modules/

insmod /data/usr/lib/slhc.ko
insmod /data/usr/lib/ppp_generic.ko
insmod /data/usr/lib/ppp_async.ko