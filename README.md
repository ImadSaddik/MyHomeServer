# Home server documentation

In this repository, I am documenting my home server setup and the projects running on it. The home server is a `Lenovo ThinkCentre M720Q Tiny Core`, which is a small form factor desktop computer.

It is running `Ubuntu Server 24.04 LTS`, and is used to self-host applications, game servers, and run daily/weekly tasks.

My goal with this documentation is to make it easier for myself to remember how to set up and maintain my home server, as well as to share my setup with others who may be interested in self-hosting.

![A banner showing a title and a description on the left. On the right, we have an illustration of the Lenovo ThinkCentre M720Q Tiny Core](./images/banner_introduction.png)

## Hardware specifications and cost

I bought this mini PC and upgraded the RAM so it can comfortably run multiple Docker containers and background jobs. Here is a breakdown of the hardware specifications and the total cost.

| Component | Description | Cost (DH) |
| :--- | :--- | :--- |
| **Base unit** | Lenovo ThinkCentre M720Q Tiny (Intel core i3-9100T, 256GB NVMe SSD, and 8GB DDR4) | 1350 |
| **RAM upgrade** | 32GB DDR4 (bought after trading in the original 8GB stick) | 850 |
| **Total cost** | | **2200** |

> [!NOTE]
> The total cost of 2200 DH is about $235 USD. I purchased the mini PC and upgraded the RAM on February 27, 2026, when the exchange rate was approximately 9.15 MAD for 1 USD.

## Ubuntu server installation

Go to [get ubuntu server](https://ubuntu.com/download/server) and download the latest version of Ubuntu Server. At the time of writing, the latest version is `Ubuntu Server 24.04 LTS`.

After that, create a bootable USB drive. If you are on Windows, you can use [Rufus](https://rufus.ie/). If you are on Ubuntu, you can use the built-in `Startup Disk Creator` application.

> [!TIP]
> Follow this [official guide](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview) to create a bootable USB drive on Ubuntu with the `Startup Disk Creator` application.
>
> And [this guide](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview) shows how to create a bootable USB drive on Windows with Rufus.

Once you have the bootable USB drive, insert it into your home server and boot from it. You may need to change the boot order in the BIOS settings to boot from the USB drive.

I am not going to go into the details of the installation process. Instead, I will link to this [video tutorial](https://www.youtube.com/watch?v=ceYeDX5WTms&t=375s) that shows how to install Ubuntu server.

Once the installation is complete and you log in for the first time, you can verify that the correct version of Ubuntu server is running by typing this command:

```bash
cat /etc/os-release
```

You should see an output containing `PRETTY_NAME="Ubuntu 24.04.4 LTS"`. This confirms that the installation was successful and you are on the right version.

## Testing the hardware

Before you configure the system or install any services, you need to test your hardware. A bad RAM stick or a failing SSD will cause system crashes that look like software bugs. Finding physical hardware problems early will save you a lot of time.

### Testing the memory

Use [memtester](https://pyropus.ca./software/memtester/) to stress test the system memory. 

First, install the tool:

```bash
sudo nala install memtester
```

Because this machine has 32GB of RAM, we will test 28GB. This leaves 4GB free so the operating system does not crash from running out of memory. The `1` at the end of the command tells the tool to run the test loop exactly one time.

```bash
sudo memtester 28G 1
```

This test will take a long time to finish. The tool will write patterns of data to the RAM and read them back to make sure the memory cells hold the correct information. If the memory is healthy, you will see `ok` next to each test. 

Here is what a successful test looks like:

```text
memtester version 4.6.0 (64-bit)
Copyright (C) 2001-2020 Charles Cazabon.
Licensed under the GNU General Public License version 2 (only).

pagesize is 4096
pagesizemask is 0xfffffffffffff000
want 28672MB (30064771072 bytes)
got  28672MB (30064771072 bytes), trying mlock ...locked.
Loop 1/1:
  Stuck Address       : ok         
  Random Value        : ok
  Compare XOR         : ok
  Compare SUB         : ok
  Compare MUL         : ok
  Compare DIV         : ok
  Compare OR          : ok
  Compare AND         : ok
  Sequential Increment: ok
  Solid Bits          : ok         
  Block Sequential    : ok         
  Checkerboard        : ok         
  Bit Spread          : ok         
  Bit Flip            : ok         
  Walking Ones        : ok         
  Walking Zeroes      : ok         
  8-bit Writes        : ok
  16-bit Writes       : ok

Done.
```

### Testing the storage drive

Next, you need to check the health of your NVMe SSD. Linux uses a system called [SMART](https://en.wikipedia.org/wiki/Self-Monitoring,_Analysis_and_Reporting_Technology) to read hardware error logs directly from the drive.

Install [smartmontools](https://github.com/smartmontools/smartmontools):

```bash
sudo nala install smartmontools
```

First, find the exact name of your drive by listing your storage devices:

```bash
lsblk
```

Look for your main drive. For this mini PC, it is called `nvme0n1`. Once you have the name, ask the drive to print its internal health report:

```bash
sudo smartctl -a /dev/nvme0n1
```

Scroll through the output and look for a section called `SMART/Health Information`. You want to check the `Media and Data Integrity Errors` line. If this number is `0`, your drive is in perfect physical condition.

Here is an example of a healthy drive report:

```text
=== START OF SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

SMART/Health Information (NVMe Log 0x02)
Critical Warning:                   0x00
Temperature:                        32 Celsius
Available Spare:                    100%
Available Spare Threshold:          5%
Percentage Used:                    63%
Data Units Read:                    71,699,614 [36.7 TB]
Data Units Written:                 116,882,379 [59.8 TB]
Host Read Commands:                 1,750,814,398
Host Write Commands:                4,269,382,501
Controller Busy Time:               6,608
Power Cycles:                       496
Power On Hours:                     19,212
Unsafe Shutdowns:                   66
Media and Data Integrity Errors:    0
Error Information Log Entries:      0
```

Do not just glance at the output. Here are the five most important lines you need to check to know if your drive is healthy:

* **SMART overall-health self-assessment test result:** This must say `PASSED`. If it says `FAILED`, your drive is dying and you should replace it immediately.
* **Critical Warning:** This should be `0x00`. Any other number means the drive controller has found a serious hardware problem.
* **Available Spare:** This should be at or near `100%`. SSDs have backup memory blocks they use when normal blocks break. If this number drops close to the `Available Spare Threshold`, the drive is running out of backup memory.
* **Percentage Used:** This shows how much of the expected lifespan of the drive you have used. In the example above, `63%` means the drive is getting older, but it is not broken.
* **Media and Data Integrity Errors:** This number must be exactly `0`. If it is higher than zero, it means the drive is actively corrupting your data.


### Testing the network speed

Your home server should be connected directly to your router with an ethernet cable. Wi-Fi is too slow and unstable for a server. Sometimes, a damaged cable or a bad switch port will cause the connection to drop from `1000 Mbps` (Gigabit) down to `100 Mbps` without giving you any error messages. You should test the actual physical speed of your local network.

We will use a tool called [iperf3](https://github.com/esnet/iperf). You need to install it on both your server and your main computer.

On your server, install the tool:

```bash
sudo nala install iperf3
```

> [!NOTE]
> During the installation, a screen will appear asking if you want to "Start Iperf3 as a daemon automatically". Select **No**. We only want to run this tool manually when we are actively testing the network.

Start `iperf3` in server mode so it listens for a connection:

```bash
iperf3 -s
```

Now, open a terminal on your main personal computer. Install `iperf3` on it as well. Run this command on your main computer to send traffic to the server. Replace `192.168.1.14` with your server's actual IP address:

```bash
iperf3 -c 192.168.1.14
```

The test will run for 10 seconds. Look at the `Bitrate` column in the final output. If your network and cables are healthy, you should see speeds close to `940 Mbits/sec`.

Here is what a healthy Gigabit connection looks like:

```text
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  1.10 GBytes   943 Mbits/sec    0              sender
[  5]   0.00-10.00  sec  1.09 GBytes   940 Mbits/sec                  receiver
```

> [!WARNING]
> If your bitrate is around `95 Mbits/sec` while using an ethernet cable, you likely have a damaged cable that has fallen back to "Fast Ethernet" speeds. You need to replace the cable.
> If your bitrate is jumping around between `50 Mbits/sec` and `100 Mbits/sec`, you are likely testing over Wi-Fi instead of a wired connection.

### Testing the processor and thermals

Mini PCs have very small cooling fans. If the thermal paste is old or dust is blocking the vents, the server might overheat and shut down when it is under heavy load. You should stress test the CPU and monitor the temperatures to ensure the cooling system works.

First, install the CPU stress testing tool:

```bash
sudo nala install stress-ng
```

Next, open two terminal windows connected to your server. 

In the first window, open your system monitor to watch the CPU temperatures:

```bash
btop
```

In the second window, start the CPU stress test. The Intel Core i3-9100T in this machine has 4 cores, so we will tell the tool to stress all 4 cores for exactly 3 minutes:

```bash
stress-ng --cpu 4 --timeout 3m
```

Watch the temperature graph in `btop`. It is normal for the CPU to get hot under a 100% synthetic load, but it should stay below 85 degrees Celsius. If it quickly hits 90 or 100 degrees, you need to open the mini PC, clean the fan, and replace the thermal paste.

Here is an example of a healthy CPU under full load, maxing out at around 70 degrees Celsius:

![CPU stress test temperature curve](./images/cpu_stress_test.png)

> [!NOTE]
> The test started at 08:03 AM.

## Core system configuration

After installing Ubuntu Server, there are a few core system configurations you should complete before hosting any services. These initial steps ensure your server is secure, stable, and ready to run applications smoothly.

### Updating the BIOS

Lenovo ThinkCentre Tiny machines running Linux often suffer from a low-level hardware bug related to processor power management ([Intel C-states](https://www.thomas-krenn.com/en/wiki/Processor_P-states_and_C-states)). The system can fail to wake up from deep sleep states, causing the server to freeze completely without leaving any crash logs.

> [!TIP]
> This issue is well-documented in the community. For example, [this Proxmox forum thread](https://forum.proxmox.com/threads/max-cstate-1-fixed-freezing-on-ve-8-x-but-version-9-upgrade-fresh-seems-to-bring-the-issue-back-2400ge.177004/) shows users with similar Lenovo Tiny hardware experiencing identical freezes. The final solution for them was the same thing we are doing here. They updated the BIOS to the latest version and the freezes stopped.

To permanently fix this and ensure server stability, you must update the motherboard BIOS to the latest version.

First, check your current BIOS version and its release date:

```bash
sudo dmidecode -t bios
```

The output will look like this:

```text
# dmidecode 3.5
Getting SMBIOS data from sysfs.
SMBIOS 3.2.1 present.

Handle 0x0000, DMI type 0, 26 bytes
BIOS Information
    Vendor: LENOVO
    Version: M1UKT77A
    Release Date: 04/10/2024
    Address: 0xF0000
    Runtime Size: 64 kB
    ROM Size: 12 MB
    Characteristics:
        ...
    BIOS Revision: 1.119
    Firmware Revision: 1.24
```

#### Downloading the latest BIOS version

In this example, the BIOS version is `M1UKT77A`, released on `04/10/2024`. Let's use the [Lenovo support website](https://pcsupport.lenovo.com/ma/en/) to find if there is a newer BIOS version available for the ThinkCentre M720Q Tiny.

Type `M720q` in the search bar and click on the first result that appears. This will take you to the support page for your specific model.

![Type "M720q" in the search bar and click on the first result](./images/lenovo_support_search.png)

Click on "Drivers & Software" in the options below the model name.

![Click on "Drivers & Software"](./images/lenovo_support_drivers.png)

Next, click on "Select Drivers" under the "Manual Update" section.

![Click on "Select Drivers"](./images/lenovo_support_select_drivers.png)

Finally, click on "BIOS/UEFI" to see the available BIOS updates for your machine.

![Click on "BIOS/UEFI"](./images/lenovo_support_bios.png)

Download the file with the name "BIOS Update (ISO Image Version)". Do not use the Windows `.exe` file or the USB Drive Package.

![Download the "BIOS Update (ISO Image Version)"](./images/lenovo_support_bios_download.png)

#### Creating a bootable USB

We need to put this `.iso` file onto a USB flash drive. Instead of burning a single image, we will use [Ventoy](https://www.ventoy.net/). Ventoy is a tool that formats your USB drive once, and then you can drag and drop as many `.iso` files onto it as you want.

Go to the [Ventoy releases page on GitHub](https://github.com/ventoy/Ventoy/releases) and download the latest version. Get the `.zip` file if you are on Windows or the `.tar.gz` file if you are on Linux.

![Download the latest version of Ventoy](./images/ventoy_download.png)

Extract the downloaded file and plug a spare USB flash drive into your computer.

> [!WARNING]
> The next step will completely format your USB drive. All data on it will be permanently erased. Make sure you select the correct drive.

Open the extracted Ventoy folder. If you are on Windows, double click `Ventoy2Disk.exe`. If you are on Linux, open a terminal in that folder and run `sudo ./VentoyGUI.x86_64`.

![Open the Ventoy application](./images/ventoy_open.png)

Select your USB drive from the device dropdown menu and click the install button. Confirm the warning message about data and wait for the installation to complete.

![Successfull Ventoy installation](./images/ventoy_install_success.png)

> [!NOTE]
> If your USB drive does not show up after installing Ventoy, unplug it and plug it back in. It should show up as a normal storage drive named `Ventoy`.

#### Copying the bios update to the usb

Once the Ventoy installation finishes, your USB drive will show up on your computer as a normal empty storage drive named `Ventoy`. 

Copy the Lenovo BIOS `.iso` file you downloaded earlier and paste it directly into this drive.
  
> [!WARNING]
> Do not extract the ISO file.

![Copy the BIOS ISO file to the Ventoy drive](./images/ventoy_copy_iso.png)

#### Flashing the bios on the server

Safely eject the USB drive from your main computer and plug it into your Lenovo mini PC.

Reboot your server. As it starts up, press the `F12` key repeatedly to open the Lenovo boot menu. 

Select your USB flash drive from the list. It will be called `USB HDD: USB, Partition 2`.

![Select Partition 2 from the boot menu](./images/boot_menu_ventoy.jpg)

Because the server has [Secure Boot](https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-secure-boot) enabled, it will not recognize Ventoy at first. You will see a blue error screen that says [Verification failed: (0x1A) Security Violation](https://askubuntu.com/questions/1456460/verification-failed-0x1a-security-violation-while-installing-ubuntu). This is normal. 

![Secure boot verification failed error](./images/secure_boot_error.jpg)

Press `Enter` on the OK button. This opens the [MOK](https://wiki.debian.org/SecureBoot#MOK_-_Machine_Owner_Key) management screen where we can tell the motherboard to trust Ventoy.

Select `Enroll key from disk`.

![Select Enroll key from disk](./images/mok_enroll_key.jpg)

Select the `VTOYEFI` directory.

![Select VTOYEFI](./images/mok_select_vtoyefi.jpg)

Select the `ENROLL_THIS_KEY_IN_MOKMANAGER.cer` file.

![Select the certificate file](./images/mok_select_cer.jpg)

Select `Continue`.

![Select Continue](./images/mok_continue.jpg)

Select `Yes` to confirm you want to enroll the key.

![Select Yes to enroll the key](./images/mok_confirm_yes.jpg)

Finally, select `Reboot`.

![Select Reboot](./images/mok_reboot.jpg)

As the server restarts, press the `F12` key repeatedly again to open the boot menu. Select `USB, Partition 2` just like you did the first time. 

Now Ventoy will load successfully. You will see the Lenovo BIOS `.iso` file on the screen. Select it and press `Enter`.

![Select the BIOS iso file in Ventoy](./images/ventoy_select_iso.jpg)

Select `Boot in normal mode`.

![Select Boot in normal mode](./images/ventoy_normal_mode.jpg)

You do not need to press anything here, just wait for the startup script to finish.

![Startup script running in the shell](./images/bios_startup_script.jpg)

Once the Lenovo Firmware Update Utility launches, it will ask if you want to update the Serial Number. Type `N` and press `Enter`.

![Prompt to update the serial number](./images/bios_update_serial.jpg)

Next, it will ask if you want to update the Machine Type and Model. Type `N` and press `Enter`.

![Prompt to update the machine type and model](./images/bios_update_machine_type.jpg)

After you press `Enter` for the second time, the [AMI Firmware Update Utility](https://www.ami.com/resources/ami-firmware-utility-afu-a-secure-update-utility-for-aptio-v-uefi-bios-firmware/) will automatically take over and start processing the firmware update immediately.

![Firmware update in progress](./images/bios_flashing_progress.jpg)

> [!WARNING]
> Do not unplug the power cord while it is flashing. The process will take a few minutes, reach 100%, and the machine will restart automatically a few times.

#### Verifying the update

Once the process is complete and your server boots back into Ubuntu, run the check command one more time to confirm the new version is applied:

```bash
sudo dmidecode -t bios
```
You should see the release date is now updated to a 2026 date, and the version matches the file you downloaded. Your hardware is now fully stable and the C-state freezing bug is resolved.

### Configuring the BIOS settings

After updating the firmware, you should configure the motherboard. Reboot the machine and press `F1` repeatedly during startup to enter the Lenovo BIOS Setup Utility.

#### Automatic power on

If your house loses power, you want the server to turn itself back on automatically when the electricity comes back. If you do not set this, the server will stay off until you manually push the physical power button.

Go to the **Power** tab and select **After Power Loss**. Change the value to **Power On**.

![Set After Power Loss to Power On](./images/bios_power_on.jpg)

#### Disabling secure boot

While Secure Boot is fine for a standard Windows desktop, it can cause headaches on a Linux server if you need to use certain third-party drivers or boot from custom USB tools. 

Go to the **Security** tab, select **Secure Boot**, and change it to **Disabled**.

![Disable Secure Boot](./images/bios_secure_boot.jpg)

#### Enabling deep sleep C-states

C-states allow the processor to use its maximum power-saving features. This lowers your electricity consumption and keeps the mini PC running cool. Because you updated the BIOS in the previous step, it is now completely safe to enable them without the server freezing.

Go to the **Advanced** tab and select **CPU Setup**.

![Open CPU Setup](./images/bios_cpu_setup.jpg)

Find **C State Support** and change it to the maximum option available, which is `C1C3C6C7C8C10`.

![Enable all C States](./images/bios_c_states.jpg)

#### Saving the changes

Press `F10` on your keyboard to open the save prompt. Select **Yes** to save your configuration and reset the server.

![Save configuration and reset](./images/bios_save_reset.jpg)

### Network configuration

Your server needs to have a static IP address so that you can reliably access it from other devices on your network. If you do not set a static IP address, your server's IP may change after a reboot, making it difficult to connect to your self-hosted services.

To set a static IP address, you can use the [Netplan](https://netplan.io/) utility. First, you need to find the name of your network interface and your current IP address by running the following command:

```bash
ip a
```

This command will list all the network interfaces on your server. Look for the one connected to your network. The output of the `ip a` command looks like this:


```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever

2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
    inet 192.168.1.14/24 brd 192.168.1.255 scope global eno1

...
```

In this example, the network interface is `eno1`, and it has the IP address `192.168.1.14`.

Once you identify your network interface, you can configure it. Open the default Netplan configuration file using the `nano` text editor:

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

Replace the contents of the file with the following configuration. Make sure to replace `eno1` with your interface name, `192.168.1.14/24` with your desired static IP, and `192.168.1.254` with your router's gateway IP. 

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      dhcp4: no
      addresses:
        - 192.168.1.14/24
      routes:
        - to: default
          via: 192.168.1.254
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

Save the file and exit the editor. Finally, apply the changes to your network by running this command:

```bash
sudo netplan apply
```

### SSH configuration

Now that your server has a static IP, you can connect to it remotely from your main computer. To make this connection secure, you will set up SSH keys and disable standard password authentication. 

First, generate a new SSH key pair on your local machine using the `Ed25519` algorithm.

> [!NOTE]
> In the commands below, replace `imad` with the username you created during the Ubuntu server installation process.

```bash
ssh-keygen -t ed25519 -C "imad@saddik-server" -f ~/.ssh/saddik_server
```

> [!NOTE]
> Change the `-C` value to a comment that helps you identify the key later.
>
> The `-f ~/.ssh/saddik_server` flag saves the generated key pair as `saddik_server` (private key) and `saddik_server.pub` (public key) in your `~/.ssh/` directory. Make sure to change this name to something that makes sense for your setup.

Next, copy the public key to your home server. You will be prompted to enter your server user's password one last time.

```bash
ssh-copy-id -i ~/.ssh/saddik_server.pub imad@192.168.1.14
```

To make connecting easier in the future, configure your local SSH client to use this specific key and remember the server's IP address. Open your local SSH configuration file.

```bash
nano ~/.ssh/config
```

Add the following block to the file:

```text
Host saddik-server
  HostName 192.168.1.14
  User imad
  IdentityFile ~/.ssh/saddik_server
  IdentitiesOnly yes
```

Save the file. You can now connect to your server by typing `ssh saddik-server` in your terminal. 

Once you verify that you can log in successfully using your new SSH key, it is time to secure the server by disabling password authentication. Log into the server and open the `cloud-init` SSH configuration file.

```bash
sudo nano /etc/ssh/sshd_config.d/50-cloud-init.conf
```

Set `PasswordAuthentication` to `no`.

```text
PasswordAuthentication no
```

Save the file and restart the SSH service to apply the changes.

```bash
sudo systemctl restart ssh
```

### Storage expansion

When you install Ubuntu Server, the installer uses [Logical Volume Management](https://ubuntu.com/server/docs/explanation/storage/about-lvm/) (LVM) by default. It often leaves a large portion of your drive unallocated instead of giving all the space to your main operating system partition. You want to make sure your server can actually use your entire SSD.

First, check your current disk usage to see how much space is currently allocated:

```bash
df -h
```

Your output will look something like this:

```text
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                              782M  1.5M  780M   1% /run
efivarfs                           320K   78K  238K  25% /sys/firmware/efi/efivars
/dev/mapper/ubuntu--vg-ubuntu--lv   98G  6.6G   87G   8% /
tmpfs                              3.9G     0  3.9G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
/dev/nvme0n1p2                     2.0G  103M  1.7G   6% /boot
/dev/nvme0n1p1                     1.1G  6.2M  1.1G   1% /boot/efi
tmpfs                              782M   12K  782M   1% /run/user/1000
```

Notice that the filesystem mounted on `/` (`/dev/mapper/ubuntu--vg-ubuntu--lv`) only has `98G` allocated, even though the machine has a 256GB NVMe SSD.

To fix this, run this command to expand the logical volume to use 100% of the free space available:

```bash
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

The output will confirm that the logical volume size has increased:

```text
Size of logical volume ubuntu-vg/ubuntu-lv changed from 100.00 GiB (25600 extents) to 235.42 GiB (60268 extents).
Logical volume ubuntu-vg/ubuntu-lv successfully resized.
```

Even though the volume is larger, the filesystem does not know about the new space yet. You need to resize it to match the volume:

```bash
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

You will see a confirmation like this:

```text
resize2fs 1.47.0 (5-Feb-2023)
Filesystem at /dev/ubuntu-vg/ubuntu-lv is mounted on /; on-line resizing required
old_desc_blocks = 13, new_desc_blocks = 30
The filesystem on /dev/ubuntu-vg/ubuntu-lv is now 61714432 (4k) blocks long.
```

Finally, run `df -h` one more time to confirm that your root partition (`/`) now has access to the full capacity of your SSD:

```text
Filesystem                         Size  Used Avail Use% Mounted on
tmpfs                              782M  1.5M  780M   1% /run
efivarfs                           320K   78K  238K  25% /sys/firmware/efi/efivars
/dev/mapper/ubuntu--vg-ubuntu--lv  232G  6.6G  215G   3% /
tmpfs                              3.9G     0  3.9G   0% /dev/shm
tmpfs                              5.0M     0  5.0M   0% /run/lock
/dev/nvme0n1p2                     2.0G  103M  1.7G   6% /boot
/dev/nvme0n1p1                     1.1G  6.2M  1.1G   1% /boot/efi
tmpfs                              782M   12K  782M   1% /run/user/1000
```

The root partition size is now `232G`, which confirms the expansion was successful.

### Timezone setup

Setting the correct timezone ensures that your server logs, database entries, and background cron jobs execute exactly when you expect them to. 

To set the server timezone to `Africa/Casablanca`, run this command:

```bash
sudo timedatectl set-timezone Africa/Casablanca
```

After setting the timezone, it is good practice to ensure your server automatically synchronizes its clock with [internet time servers](https://tf.nist.gov/tf-cgi/servers.cgi) (NTP). This prevents the server's internal clock from drifting over time.

Enable the time synchronization service:

```bash
sudo timedatectl set-ntp true
```

You can verify that both the timezone and the NTP service are correctly configured by running:

```bash
timedatectl
```

Your output will look like this:

```text
               Local time: Fri 2026-03-20 20:36:58 +00
           Universal time: Fri 2026-03-20 20:36:58 UTC
                 RTC time: Fri 2026-03-20 20:36:58
                Time zone: Africa/Casablanca (+00, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

Notice that the "Time zone" is correctly set to `Africa/Casablanca`, "System clock synchronized" is `yes`, and the "NTP service" is `active`.

### Headless graphics fix

Because this mini PC will run completely headless (without a monitor attached), a known issue with the Intel graphics driver can occur. The driver may get stuck in an endless loop looking for a display, which hogs the CPU and eventually freezes the server. 

To prevent this, you need to add the `nomodeset` parameter to the GRUB boot configuration. This tells the Linux kernel to use basic video drivers instead of the advanced Intel ones, bypassing the issue entirely.

> [!WARNING]
> Adding `nomodeset` completely disables your Intel GPU. This is fine for CPU-bound tasks. But if you plan to host a media server like [Plex](https://watch.plex.tv/) or [Jellyfin](https://jellyfin.org/) in the future and want to use hardware video transcoding ([Intel Quick Sync](https://www.intel.com/content/www/us/en/support/articles/000029338/graphics.html)), this setting will prevent it from working. You will need to remove `nomodeset` if you ever need GPU acceleration.

Open the GRUB configuration file in `nano`:

```bash
sudo nano /etc/default/grub
```

Find the line that starts with `GRUB_CMDLINE_LINUX_DEFAULT`. Add `nomodeset` inside the quotes, separated by a space. It should look like this:

```text
GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"
```

Save and exit the file. To apply these changes, update the GRUB bootloader and reboot the server:

```bash
sudo update-grub
sudo reboot
```

After the server reboots, your core system configuration is complete, and you can safely unplug the monitor and keyboard from the mini PC.

## Command line utilities

With the core system configured, the next step is to install the essential command line utilities. These tools make package management, version control, and general server maintenance much easier.

### nala

I use [nala](https://github.com/volitank/nala) as a replacement for the default `apt` package manager. There is nothing wrong with `apt`, but `nala` formats the terminal output beautifully, making it much easier to read what is being installed or upgraded.

Install `nala` using `apt`:

```bash
sudo apt install nala
```

From this point forward, we will use `nala` for all package installations.

### git

I use `git` to track changes to my server configuration scripts and to push this exact documentation to my GitHub account. 

First, install `git`:

```bash
sudo nala install git
```

After installing, configure your global identity:

```bash
git config --global user.name "Imad Saddik"
git config --global user.email "your.email@example.com"
```

To securely connect the server to GitHub without typing a password every time, generate a new SSH key specifically for GitHub:

```bash
ssh-keygen -t ed25519 -C "A good description for this key" -f ~/.ssh/github_ed25519
```

Because we gave the key a custom name (`github_ed25519`), we need to tell SSH to use it whenever it connects to GitHub. Open the SSH config file:

```bash
nano ~/.ssh/config
```

Add this configuration block to the file:

```text
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_ed25519
```

Save and exit the editor. Then, restrict the permissions on the config file so SSH accepts it:

```bash
chmod 600 ~/.ssh/config
```

Now, display your public key so you can copy it:

```bash
cat ~/.ssh/github_ed25519.pub
```

Copy the output from the terminal, and follow these steps to add it to your GitHub account:

<!-- TODO: add images here -->
1. Go to your GitHub account settings in your browser.
2. Click on **SSH and GPG keys** in the sidebar.
3. Click the **New SSH key** button.
4. Give it a descriptive title and paste your key into the "Key" field.
5. Click **Add SSH key**.

Finally, test the connection to make sure the server can talk to GitHub:

```bash
ssh -T git@github.com
```

You will see a warning about the authenticity of the host. Type `yes` and press `Enter`. If everything is set up correctly, you will see a success message looking like this:

```text
Hi ImadSaddik! You've successfully authenticated, but GitHub does not provide shell access.
```

### uv

I love [Anaconda](https://www.anaconda.com/), but I do not want it to consume a lot of storage on my mini PC. Because of this, I use [uv](https://docs.astral.sh/uv/) instead to manage Python projects and dependencies quickly and efficiently.

Install `uv` by running its official installation script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After the installation is complete, run this command to print `uv`'s version and confirm that it is installed correctly:

```bash
uv --version
```

### nvm

I use [Node Version Manager](https://github.com/nvm-sh/nvm) (`nvm`) to install and manage `Node.js` versions.

First, download and run the installation script:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
```

> [!NOTE]
> The curl command above installs `nvm` version `0.40.4`. You can check for the latest version on the [nvm GitHub releases page](https://github.com/nvm-sh/nvm/releases).

Your current terminal session does not know about NVM yet. Run this command to load it immediately:

```bash
source ~/.bashrc
```

Now, install the latest LTS (Long Term Support) version of Node.js:

```bash
nvm install --lts
```

### pnpm

I use [pnpm](https://github.com/pnpm/pnpm) instead of the default `npm` to install JavaScript packages. It is much faster and saves disk space by using a global store.

Since you just installed Node.js and `npm` via `nvm`, you can use `npm` to install `pnpm` globally:

```bash
npm install -g pnpm@latest-10
```

### starship

I use [starship](https://starship.rs/) as a cross-shell prompt to make the terminal look better and provide useful context like git branches and directory information. I have a dedicated repository for my custom configuration.

First, clone the configuration repository:

```bash
git clone https://github.com/ImadSaddik/MyStarshipConfig.git
```

Navigate into the folder and run the installation script. This script handles the starship binary installation and copies my `starship.toml` file to `~/.config/`:

```bash
cd MyStarshipConfig
chmod +x install.sh
./install.sh
```

To finalize the setup, open your `.bashrc` file:

```bash
nano ~/.bashrc
```

Append this line to the bottom of the file:

```bash
eval "$(atuin init bash --disable-up-arrow)"
```

Apply the changes to your current session:

```bash
source ~/.bashrc
```

### Atuin

I use Atuin to replace the default bash history with a SQLite database. It allows me to search my command history easily.

Instead of compiling from source, install the pre-built binary using the official script:

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
```

During the installation, the script will ask you a series of questions. Answer them like this to automatically import your existing history but keep the installation completely local and private:

- Would you like to import your existing shell history into Atuin? -> **y**
- Sign up for a sync account? -> **n**
- Enable Atuin AI? -> **n**
- Enable Atuin Daemon? -> **n**

To use the `atuin` command immediately in your current terminal, source its newly created environment file:

```bash
source ~/.atuin/bin/env
```

Atuin requires `bash-preexec` to hook into Bash properly. Download it to your home directory:

```bash
curl https://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh -o ~/.bash-preexec.sh
```

Next, create the configuration directory and set up your preferences. This configuration explicitly disables syncing to external servers to keep your data local:

```bash
mkdir -p ~/.config/atuin
cat <<EOF > ~/.config/atuin/config.toml
# DISABLE SYNC: Prevents sending history to any server
auto_sync = false

# Check for updates online
update_check = true

# Store failed commands
store_failed = true

# Database path
db_path = "~/.local/share/atuin/history.db"
EOF
```

Now, configure your `.bashrc` file. Because you installed `Starship` earlier, you need to make sure the order of these tools is correct so they do not conflict. Open the file:

```bash
nano ~/.bashrc
```

Go to the very bottom of the file. Make sure your final lines look exactly like this, in this exact order:

```bash
[[ -f ~/.bash-preexec.sh ]] && source ~/.bash-preexec.sh
eval "$(starship init bash)"
eval "$(atuin init bash --disable-up-arrow)"
```

Save the file and apply the changes to your current session:

```bash
source ~/.bashrc
```

### tmux

I use [tmux](https://github.com/tmux/tmux) to manage multiple terminal sessions. I use a custom configuration for better shortcuts and mouse support.

First, install tmux using `nala`:

```bash
sudo nala install tmux
```

Clone the configuration repository:

```bash
git clone https://github.com/ImadSaddik/MyTmuxConfig.git
```

Navigate into the folder:

```bash
cd MyTmuxConfig
```

> [!NOTE]
> Because this server runs in a headless environment, you need to remove the clipboard integration (`wl-copy` or `xclip`) from the configuration before installing it. If you do not, the installation script will prompt you for a display server, and tmux will throw errors because there is no graphical interface.
>
> Open `tmux.conf` and delete section 10 at the bottom:
>
> ```text
> # 10. Copy text to clipboard
> set-window-option -g mode-keys vi
> # Copy to system clipboard when releasing mouse
> bind-key -T copy-mode-vi MouseDragEnd1Pane send-keys -X copy-pipe-and-cancel "wl-copy"
> ```
>
> Next, open `install.sh` and delete the interactive prompt at the bottom. The file should only contain this:
>
> ```bash
> #!/bin/bash
>
> CONFIG_FILE="tmux.conf"
> TARGET_FILE="$HOME/.tmux.conf"
> BACKUP_FILE="$HOME/.tmux.conf.backup"
>
> echo "Setting up your tmux configuration"
>
> if [ -f "$TARGET_FILE" ]; then
>     echo "Found existing tmux.conf. Backing it up to $BACKUP_FILE"
>     mv "$TARGET_FILE" "$BACKUP_FILE"
> fi
>
> echo "Copying new configuration"
> cp "$CONFIG_FILE" "$TARGET_FILE"
> ```

After updating the files, make the script executable and run it:

```bash
chmod +x install.sh
./install.sh
```

### btop

I use [btop](https://github.com/aristocratos/btop) to monitor server resources like CPU and RAM usage through a beautiful terminal interface.

```bash
sudo nala install btop
```

### tree

I use `tree` to see folder structures easily directly from the terminal.

```bash
sudo nala install tree
```

### nginx

I installed [nginx](https://github.com/nginx/nginx) to set up web servers and reverse proxies for my self-hosted applications.

```bash
sudo nala install nginx -y
```

### ffmpeg

I installed [ffmpeg](https://github.com/FFmpeg/FFmpeg) to process audio and video files.

```bash
sudo nala install ffmpeg
```

### aria2

I use [aria2](https://github.com/aria2/aria2) to make downloading music files with `yt-dlp` faster by opening multiple connections at once.

```bash
sudo nala install aria2
```

## Docker installation and configuration

Docker is the backbone of this home server. Instead of installing applications directly onto the operating system, which can cause dependency conflicts and make backups difficult, almost all of our self-hosted services will run in isolated Docker containers.

### Installing Docker

First, update your package list and install the basic tools required to fetch external repositories securely:

```bash
sudo nala update
sudo nala install ca-certificates curl -y
```

Next, set up the official GPG key so your system can verify and trust the files coming directly from Docker:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

With the security key in place, add the official Docker repository to your system sources. This command automatically detects your specific Ubuntu version and creates the source file:

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

Now, update your package list again so `nala` can read from the newly added Docker repository, and install the Docker packages (including Docker compose):

```bash
sudo nala update
sudo nala install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

### Post-installation steps

By default, running Docker commands requires `sudo` privileges. To avoid typing `sudo` every time you want to manage a container, you need to add your current user to the `docker` group.

Run this command to append your user to the group:

```bash
sudo usermod -aG docker $USER
```

To apply this new group membership to your current terminal session without logging out, run:

```bash
newgrp docker
```

You can verify that Docker is installed and you have the correct permissions by running a quick test:

```bash
docker ps
```

If it prints an empty table with headers like `CONTAINER ID`, `IMAGE`, and `COMMAND` without giving you a "permission denied" error, Docker is successfully set up and ready to use.

## Core Docker automation

### Watchtower

I use [Watchtower](https://github.com/containrrr/watchtower) to automate the process of updating Docker images. Watchtower monitors the running containers. When it detects that a new image is available on the registry, it pulls the new image, gracefully shuts down the existing container, and restarts it with the exact same options used during the initial deployment.

Installing this immediately after Docker ensures all subsequent containers are automatically kept up to date.

> [!NOTE]
> Before creating the container, we need to establish a directory structure. We will store all Docker configurations inside a central `~/docker_projects/` directory.
>
> Every application will get its own subfolder inside it. This convention keeps the host system clean and makes backing up your server configurations incredibly easy; you just copy the single `docker_projects` folder.

First, generate a secure API token. This token allows external services to read Watchtower's metrics. Run this command:

```bash
openssl rand -hex 16
```

> [!IMPORTANT]
> Copy the output of this command and save it in a secure password manager (like [Bitwarden](https://bitwarden.com/)). You will need this exact token later to connect Watchtower to the [Homepage](https://github.com/gethomepage/homepage) dashboard.

Next, create the central Docker directory, the specific Watchtower folder, and open the configuration file:

```bash
mkdir -p ~/docker_projects/watchtower
cd ~/docker_projects/watchtower
nano docker-compose.yml
```

Paste the following configuration into the file. Be sure to replace `my-secret-token` with the 16-character string you just generated:

```yaml
services:
  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    restart: unless-stopped
    ports:
      - "8081:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - TZ=Africa/Casablanca
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_SCHEDULE=0 0 21 * * *
      - WATCHTOWER_HTTP_API_METRICS=true
      - WATCHTOWER_HTTP_API_TOKEN=my-secret-token
      - DOCKER_API_VERSION=1.54
```

Configuration details:

- `docker.sock`: The container requires access to the Docker socket to interact with the Docker API and restart other containers.
- `WATCHTOWER_CLEANUP=true`: Deletes old, unused images after an update to save SSD storage space.
- `WATCHTOWER_SCHEDULE`: Uses cron syntax to check for updates every day at 9:00 PM (`0 0 21 * * *`). The `TZ` variable ensures it follows local Moroccan time (Change `TZ` to your local timezone if different).
- `DOCKER_API_VERSION=1.54`: Forces Watchtower to use a specific Docker API version. To find your current server API version if this ever needs updating, run this command: `docker version --format '{{.Server.APIVersion}}'`
- `ports`: Maps the internal port `8080` to `8081` on the host machine. This prevents a port conflict with the Minecraft dashboard, which will use `8080`.

To start the container, run:

```bash
docker compose up -d
```

## Dockerized services

This section covers the third-party applications running in isolated Docker containers. We store all of these configurations in the `~/docker_projects/` directory to keep the host system clean.

### Homepage

If you have multiple projects, you will find it hard to remember every port. [Homepage](https://github.com/gethomepage/homepage) solves this by giving you one dashboard that lists every project you are hosting. We will install the base dashboard first and add services to it one by one as we build the server.

Create the project directory and open the configuration file:

```bash
mkdir -p ~/docker_projects/homepage
cd ~/docker_projects/homepage
nano docker-compose.yml
```

Paste the following configuration:

```yaml
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    environment:
      HOMEPAGE_ALLOWED_HOSTS: YOUR_SERVER_IP:3000
      PUID: 1000
      PGID: 988
    ports:
      - "3000:3000"
    volumes:
      - ./config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped
```

Configuration details:

- `HOMEPAGE_ALLOWED_HOSTS`: Restricts access. You must replace `YOUR_SERVER_IP` with the actual IP address of your server. If you do not know your server IP, run the `ip a` command to find it.
- `PUID: 1000`: Runs the container as your primary user so you retain ownership of the created configuration files.
- `PGID: 988`: This maps the container to the `docker` group on the host. Homepage needs to read `/var/run/docker.sock` to monitor your containers and display their statuses. Passing this specific group ID allows it to read the socket securely without running as the root user. To find your system's exact docker group ID, run the `id` command in your terminal and look for the number next to `(docker)`.

Start the container in the background:

```bash
docker compose up -d
```

Docker will automatically create the `config/` directory and populate it with default files. Right now, the dashboard is mostly empty. You can view it by going to [http://YOUR_SERVER_IP:3000](http://YOUR_SERVER_IP:3000).

We will update the `config/services.yaml` file to populate this dashboard as we install the rest of the tools.

#### Initial dashboard configuration

With the dashboard running, we can start adding services to it. We will initialize the configuration with your public websites and the Watchtower container we set up earlier.

Open the services configuration file:

```bash
nano ~/docker_projects/homepage/config/services.yaml
```

Delete everything in the file and replace it with this foundational structure:

```yaml
- Self-hosted services:
  - Watchtower:
    href: http://YOUR_SERVER_IP:8081
    description: Automatic container updates
    icon: watchtower.png
    widget:
      type: watchtower
      url: http://YOUR_SERVER_IP:8081
      key: my-secret-token

- My websites:
  - imadsaddik.com:
    href: https://imadsaddik.com
    description: Personal website

  - myuniversehub.com:
    href: https://myuniversehub.com
    description: A better version of APOD.
```

> [!IMPORTANT]
> You need to make two manual changes to this file:
> 
> - Replace `YOUR_SERVER_IP` with your actual server IP address.
> - Replace `my-secret-token` with the secure 16-character key you generated during the Watchtower installation.

Save the file. Homepage updates automatically, so if you refresh your browser at [http://YOUR_SERVER_IP:3000](http://YOUR_SERVER_IP:3000), you will immediately see your websites and a live Watchtower widget showing your container update statistics.

<!-- TODO: add image here -->

Homepage is fully customizable. You can also modify `bookmarks.yaml`, `settings.yaml`, and `widgets.yaml` in the same `config/` directory. To learn more about how to customize it fully, read the [official configuration documentation](https://github.com/gethomepage/homepage/tree/main/docs/configs).
