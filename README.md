# Home server documentation

In this repository, I am documenting my home server setup and the projects running on it. The home server is a `Lenovo ThinkCentre M720Q Tiny Core`, which is a small form factor desktop computer.

It is running `Ubuntu Server 24.04 LTS`, and is used to self-host applications, game servers, and run daily/weekly tasks.

My goal with this documentation is to make it easier for myself to remember how to set up and maintain my home server, as well as to share my setup with others who may be interested in self-hosting.

![A banner showing a title and a description on the left. On the right, we have an illustration of the Lenovo ThinkCentre M720Q Tiny Core](./images/banner_introduction.png)

## Table of contents

- [Hardware specifications and cost](#hardware-specifications-and-cost)
- [Ubuntu server installation](#ubuntu-server-installation)
- [Testing the hardware](#testing-the-hardware)
  - [Testing the memory](#testing-the-memory)
  - [Testing the storage drive](#testing-the-storage-drive)
  - [Testing the network speed](#testing-the-network-speed)
  - [Testing the processor and thermals](#testing-the-processor-and-thermals)
- [Core system configuration](#core-system-configuration)
  - [Updating the BIOS](#updating-the-bios)
    - [Downloading the latest BIOS version](#downloading-the-latest-bios-version)
    - [Creating a bootable USB](#creating-a-bootable-usb)
    - [Copying the bios update to the usb](#copying-the-bios-update-to-the-usb)
    - [Flashing the bios on the server](#flashing-the-bios-on-the-server)
    - [Verifying the update](#verifying-the-update)
  - [Configuring the BIOS settings](#configuring-the-bios-settings)
    - [Automatic power on](#automatic-power-on)
    - [Disabling secure boot](#disabling-secure-boot)
    - [Enabling deep sleep C-states](#enabling-deep-sleep-c-states)
    - [Saving the changes](#saving-the-changes)
  - [Network configuration](#network-configuration)
  - [SSH configuration](#ssh-configuration)
  - [Storage expansion](#storage-expansion)
  - [Timezone setup](#timezone-setup)
  - [Headless graphics fix](#headless-graphics-fix)
  - [Software watchdog setup](#software-watchdog-setup)
    - [Loading the software module](#loading-the-software-module)
    - [Installing the watchdog daemon](#installing-the-watchdog-daemon)
    - [Configuring the service](#configuring-the-service)
    - [Starting the watchdog](#starting-the-watchdog)
    - [Testing the watchdog](#testing-the-watchdog)
- [Command line utilities](#command-line-utilities)
  - [nala](#nala)
  - [git](#git)
  - [uv](#uv)
  - [nvm](#nvm)
  - [pnpm](#pnpm)
  - [starship](#starship)
  - [Atuin](#atuin)
  - [tmux](#tmux)
  - [btop](#btop)
  - [tree](#tree)
  - [nginx](#nginx)
  - [ffmpeg](#ffmpeg)
  - [aria2](#aria2)
- [Docker installation and configuration](#docker-installation-and-configuration)
  - [Installing Docker](#installing-docker)
  - [Post-installation steps](#post-installation-steps)
- [Core Docker automation](#core-docker-automation)
  - [Watchtower](#watchtower)
- [Dockerized services](#dockerized-services)
  - [Homepage](#homepage)
    - [Initial dashboard configuration](#initial-dashboard-configuration)
  - [Netdata](#netdata)
  - [Planka](#planka)
  - [Uptime Kuma](#uptime-kuma)
  - [Healthchecks](#healthchecks)
  - [Code server](#code-server)
  - [Navidrome](#navidrome)
    - [Adding Navidrome to Homepage](#adding-navidrome-to-homepage)
- [Native services and automation](#native-services-and-automation)
  - [Music backup](#music-backup)
  - [Planka backup](#planka-backup)
  - [Minecraft server](#minecraft-server)
    - [Accepting the EULA](#accepting-the-eula)
    - [Start and stop scripts](#start-and-stop-scripts)
    - [Server mods](#server-mods)
    - [Automated backups](#automated-backups)
  - [Minecraft dashboard](#minecraft-dashboard)
    - [Systemd backend service](#systemd-backend-service)
    - [Building the Vue.js frontend](#building-the-vuejs-frontend)
    - [Nginx frontend and reverse proxy](#nginx-frontend-and-reverse-proxy)
  - [Automatic shutdown and boot](#automatic-shutdown-and-boot)
  - [Uninterruptible power supply setup](#uninterruptible-power-supply-setup)
    - [Hardware and network preparation](#hardware-and-network-preparation)
    - [Bypassing Ubuntu security](#bypassing-ubuntu-security)
    - [Configuring the NUT data server](#configuring-the-nut-data-server)
    - [Verifying the data server](#verifying-the-data-server)
    - [Configuring the automated shutdown monitor](#configuring-the-automated-shutdown-monitor)
    - [Dashboard integrations](#dashboard-integrations)
    - [Secondary monitor configuration (gaming laptop)](#secondary-monitor-configuration-gaming-laptop)
    - [Testing the setup](#testing-the-setup)

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

> [!NOTE]
> If you are navigating the BIOS menus and the screen suddenly stops responding to your keyboard, do not panic. The Lenovo BIOS interface can sometimes lag and freeze for a few seconds. Your keyboard is fine. Just press the key a few more times and the menu will catch up.

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

### Software watchdog setup

A hardware watchdog timer is a physical timer built directly into your motherboard. However, on the Lenovo ThinkCentre M720Q, Lenovo hides and locks this feature in the BIOS. Because the operating system cannot access the physical chip, you must use a software fallback called [softdog](https://tools.bitfolk.com/wiki/Softdog).

`softdog` is a timer that runs inside the Linux kernel itself. The watchdog software on your Ubuntu server constantly resets this timer. If your server freezes and stops responding, the software cannot reset the timer. When the timer hits zero, the kernel forcefully restarts the system.

While it cannot protect against a total low-level kernel deadlock, it is a great safety net for a headless server and will successfully recover the system from the vast majority of crashes.

#### Loading the software module

First, force the kernel to load the `softdog` module:

```bash
sudo modprobe softdog
```

Verify that the module is running:

```bash
lsmod | grep softdog
```

If you see `softdog` in the output, your simulated timer is ready.

```text
softdog                12288  0
```

To make sure this driver loads every time the server boots, add it to the system modules file. Open the file:

```bash
sudo nano /etc/modules
```

Add this text to the very bottom of the file:

```text
softdog
```

Save the file and exit the editor.

#### Installing the watchdog daemon

You need to install the software that will talk to the hardware timer. Run this command:

```bash
sudo nala install watchdog
```

#### Configuring the service

Next, you need to tell the software where the simulated timer is located. Open the configuration file:

```bash
sudo nano /etc/watchdog.conf
```
Scroll down and find the line that says `#watchdog-device = /dev/watchdog`. Remove the `#` at the beginning to uncomment it so it looks exactly like this:

```text
watchdog-device = /dev/watchdog
```
Save the file and exit the editor.

#### Starting the watchdog

Finally, enable the service to start automatically when the server boots and start it right now:

```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
```

Make sure that the service is running without any errors:

```bash
sudo systemctl status watchdog
```

You should see `active (running)` in the output.

```text
● watchdog.service - watchdog daemon
     Loaded: loaded (/usr/lib/systemd/system/watchdog.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-03-30 08:51:58 +01; 1min 21s ago
   Main PID: 118328 (watchdog)
      Tasks: 1 (limit: 38263)
     Memory: 512.0K (peak: 1.0M)
        CPU: 12ms
     CGroup: /system.slice/watchdog.service
             └─118328 /usr/sbin/watchdog
```

#### Testing the watchdog

To validate the configuration of your automated recovery system, you should test it once. 

The correct way to test the software watchdog is to abruptly kill the background daemon without giving it a chance to gracefully close its connection to the kernel. This simulates a frozen operating system. The kernel will wait for a signal that never arrives, and the system will forcefully reboot.

> [!TIP]
> This testing methodology is adapted from Paul S. Crawford's excellent guide on [Testing the Watchdog Daemon](https://www.crawford-space.co.uk/old_psc/watchdog/watchdog-testing.html). It includes important precautions to help prevent file system corruption during a forced reboot.

> [!WARNING]
> This will instantly crash your server. Your SSH session will freeze and disconnect. Save any open files before you run this command.

First, prepare the system for a sudden crash by forcing a file system check on the next boot and syncing all data from the RAM to the disk:

```bash
sudo touch /forcefsck
sudo sync
```

Next, forcefully kill the watchdog daemon:

```bash
sudo killall -STOP watchdog
```

After you run this, do not press any keys. Wait about 60 seconds. The timer will hit zero and restart your mini PC. You will be able to log back in via SSH shortly after.

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
eval "$(starship init bash)"
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
> Before creating the container, we need to establish a directory structure. We will store all Docker configurations inside a central `~/docker-projects/` directory.
>
> Every application will get its own subfolder inside it. This convention keeps the host system clean and makes backing up your server configurations incredibly easy; you just copy the single `docker-projects` folder.

First, generate a secure API token. This token allows external services to read Watchtower's metrics. Run this command:

```bash
openssl rand -hex 16
```

> [!IMPORTANT]
> Copy the output of this command and save it in a secure password manager (like [Bitwarden](https://bitwarden.com/)). You will need this exact token later to connect Watchtower to the [Homepage](https://github.com/gethomepage/homepage) dashboard.

Next, create the central Docker directory, the specific Watchtower folder, and open the configuration file:

```bash
mkdir -p ~/docker-projects/watchtower
cd ~/docker-projects/watchtower
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

This section covers the third-party applications running in isolated Docker containers. We store all of these configurations in the `~/docker-projects/` directory to keep the host system clean.

### Homepage

If you have multiple projects, you will find it hard to remember every port. [Homepage](https://github.com/gethomepage/homepage) solves this by giving you one dashboard that lists every project you are hosting. We will install the base dashboard first and add services to it one by one as we build the server.

Create the project directory and open the configuration file:

```bash
mkdir -p ~/docker-projects/homepage
cd ~/docker-projects/homepage
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
nano ~/docker-projects/homepage/config/services.yaml
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

### Netdata

I use Netdata to monitor the system health and performance of my server. It runs as a Docker container to keep the host system clean.

First, create the project directory and the configuration folder:

```bash
mkdir -p ~/docker-projects/netdata/config
cd ~/docker-projects/netdata
```

Create the `docker-compose.yml` file:

```bash
nano docker-compose.yml
```

Paste the following configuration. This setup gives Netdata read-only access to the host metrics and uses the host network directly:

```yaml
services:
  netdata:
    image: netdata/netdata:stable
    container_name: netdata
    pid: host
    network_mode: host
    restart: unless-stopped
    cap_add:
      - SYS_PTRACE
      - SYS_ADMIN
    security_opt:
      - apparmor:unconfined
    volumes:
      - ./config:/etc/netdata
      - netdatalib:/var/lib/netdata
      - netdatacache:/var/cache/netdata
      - /:/host/root:ro,rslave
      - /etc/passwd:/host/etc/passwd:ro
      - /etc/group:/host/etc/group:ro
      - /etc/localtime:/etc/localtime:ro
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /etc/os-release:/host/etc/os-release:ro
      - /var/log:/host/var/log:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro

volumes:
  netdatalib:
  netdatacache:
```

To start the container, run:

```bash
docker compose up -d
```

Because we are using `network_mode: host`, Netdata binds directly to the mini PC network. You can access the dashboard here: [http://192.168.1.14:19999](http://192.168.1.14:19999).

Let's add Netdata to Homepage. Open the `services.yaml` file:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under the `Self-hosted services` category:

```yaml
- Netdata:
  href: http://192.168.1.14:19999
  description: System health and performance monitoring
  icon: netdata.png
  widget:
    type: netdata
    url: http://192.168.1.14:19999
```

### Planka

To offload my brain and manage my backlog of ideas, bugs, and features privately, I use [Planka](https://github.com/plankanban/planka). It is a beautiful, open-source alternative to [Trello](https://trello.com/) that gives me a visual Kanban board without exposing my private scribbles to the cloud.

First, create the project directory and the configuration file:

```bash
mkdir -p ~/docker-projects/planka
cd ~/docker-projects/planka
nano docker-compose.yml
```

Paste the following Docker Compose configuration. Notice that the default port is changed from `3000` to `3002` to avoid conflicts with the Homepage dashboard, and the `BASE_URL` is updated to match the server's static IP:

```yaml
services:
  planka:
    image: ghcr.io/plankanban/planka:latest
    container_name: planka
    user: "1000:1000"
    restart: unless-stopped
    volumes:
      - data:/app/data
    ports:
      - "3002:1337"
    environment:
      - BASE_URL=http://192.168.1.14:3002
      - DATABASE_URL=postgresql://postgres@postgres/planka
      - SECRET_KEY=generate_a_random_secret_string_here
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    container_name: planka-postgres
    restart: unless-stopped
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=planka
      - POSTGRES_HOST_AUTH_METHOD=trust
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d planka"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  data:
  db-data:
```

> [!IMPORTANT]
> Change the `SECRET_KEY` variable to a secure random string before starting the container. You can generate a random 32-character string in your terminal by running `openssl rand -hex 32`.

To create and start the containers, run:

```bash
docker compose up -d
```

Starting with version 1.13, Planka no longer creates a default admin user automatically. You need to create one manually by running this script in the same directory:

```bash
docker compose run --rm planka npm run db:create-admin-user
```

Follow the prompts in your terminal to set your email, username, and password. Once finished, Planka is running on port `3002` and can be accessed from here: [http://192.168.1.14:3002](http://192.168.1.14:3002).

Let's add Planka to the Homepage dashboard so we can access our backlog easily. Open `services.yaml`:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under your `Self-hosted services` category:

```yaml
- Planka:
  href: http://192.168.1.14:3002
  description: Private kanban & backlog
  icon: planka.png
```

> [!NOTE]
> Planka does not have an official Homepage API widget yet, but this bookmark will link you directly to your board.

### Uptime Kuma

I have a few websites deployed to production, and I plan to add more in the future. To ensure they stay online and respond quickly, I use [Uptime Kuma](https://github.com/louislam/uptime-kuma). It is a beautiful, easy-to-use, self-hosted monitoring tool.

First, create the project directory and open the configuration file:

```bash
mkdir -p ~/docker-projects/uptime-kuma
cd ~/docker-projects/uptime-kuma
nano docker-compose.yml
```

Paste the following Docker Compose configuration:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:2
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - ./data:/app/data
```

> [!NOTE]
> Similar to Netdata, Uptime Kuma runs as root internally. Docker will automatically create the `data/` folder when the container starts, and it will be owned by `root`. 

To create and start the container, run:

```bash
docker compose up -d
```

You can now access the Uptime Kuma setup screen to create your admin account and configure your website monitors here: [http://192.168.1.14:3001](http://192.168.1.14:3001).

Let's add Uptime Kuma to the Homepage dashboard so you can see your website statuses at a glance. Open `services.yaml`:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under your `Self-hosted services` category:

```yaml
- Uptime Kuma:
    href: http://192.168.1.14:3001
    description: Website health monitoring
    icon: uptime-kuma.png
    widget:
      type: uptimekuma
      url: http://192.168.1.14:3001
      slug: home
```

### Healthchecks

I use [Healthchecks](https://github.com/healthchecks/healthchecks) to monitor my automated cron jobs and background scripts. It listens for HTTP requests (pings) from my scripts and alerts me if a job fails to run on time.

First, create the project directory and navigate into it:

```bash
mkdir -p ~/docker-projects/healthchecks/data
cd ~/docker-projects/healthchecks
```

Next, create the environment variables file:

```bash
nano .env
```

Paste the following configuration into the file. This tells Healthchecks how to configure its database and where it is being hosted:

```text
ALLOWED_HOSTS=192.168.1.14
APPRISE_ENABLED=False
DB=sqlite
DB_NAME=/data/hc.sqlite
DEBUG=False
DEFAULT_FROM_EMAIL=healthchecks@example.org
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
EMAIL_HOST=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_VERIFICATION=True
INTEGRATIONS_ALLOW_PRIVATE_IPS=False
LINENOTIFY_CLIENT_ID=
LINENOTIFY_CLIENT_SECRET=
MASTER_BADGE_LABEL=Mychecks
MATRIX_ACCESS_TOKEN=
MATRIX_HOMESERVER=
MATRIX_USER_ID=
MATTERMOST_ENABLED=True
MSTEAMS_ENABLED=True
OPSGENIE_ENABLED=True
PAGERTREE_ENABLED=True
PD_APP_ID=
PD_ENABLED=True
PING_BODY_LIMIT=10000
PING_EMAIL_DOMAIN=192.168.1.14
PING_ENDPOINT=http://192.168.1.14:6969/ping/
PROMETHEUS_ENABLED=True
PUSHBULLET_CLIENT_ID=
PUSHBULLET_CLIENT_SECRET=
PUSHOVER_API_TOKEN=
PUSHOVER_EMERGENCY_EXPIRATION=86400
PUSHOVER_EMERGENCY_RETRY_DELAY=300
PUSHOVER_SUBSCRIPTION_URL=
REGISTRATION_OPEN=True
REMOTE_USER_HEADER=
ROCKETCHAT_ENABLED=True
RP_ID=
S3_ACCESS_KEY=
S3_BUCKET=
S3_ENDPOINT=
S3_REGION=
S3_SECRET_KEY=
S3_TIMEOUT=60
S3_SECURE=True
SECRET_KEY=secret_key
SHELL_ENABLED=False
SIGNAL_CLI_SOCKET=
SITE_LOGO_URL=
SITE_NAME=Mychecks
SITE_ROOT=http://192.168.1.14:6969
SLACK_CLIENT_ID=
SLACK_CLIENT_SECRET=
SLACK_ENABLED=True
# SMTPD_PORT=
SPIKE_ENABLED=True
TELEGRAM_BOT_NAME=ExampleBot
TELEGRAM_TOKEN=
TRELLO_APP_KEY=
TWILIO_ACCOUNT=
TWILIO_AUTH=
TWILIO_FROM=
TWILIO_USE_WHATSAPP=False
USE_PAYMENTS=False
VICTOROPS_ENABLED=True
WEBHOOKS_ENABLED=True
WHATSAPP_DOWN_CONTENT_SID=
WHATSAPP_UP_CONTENT_SID=
ZULIP_ENABLED=True
```

> [!IMPORTANT]
> You must change the `SECRET_KEY=secret_key` line to a strong, random string before starting the container to ensure your session data is secure. You can generate one by running `openssl rand -hex 32` in your terminal.

Save and exit the `.env` file. Now, create your Docker Compose file:

```bash
nano docker-compose.yml
```

Paste the following configuration:

```yaml
services:
  web:
    image: healthchecks/healthchecks:latest
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "6969:8000"
    volumes:
      - ./data:/data
    command: uwsgi /opt/healthchecks/docker/uwsgi.ini
```

> [!IMPORTANT]
> Healthchecks runs as a non-root user internally. If the container does not have write access to the mapped `data/` directory, it cannot create the SQLite database, and the initial setup will fail. 

Before starting the container, adjust the permissions on the `data/` directory so the container can write to it:

```bash
chmod 777 data
```

Now, create and start the container:

```bash
docker compose up -d
```

Because Healthchecks is a Django application, you need to initialize the database by running its migrations. Execute this command to run the migration script inside the active container:

```bash
docker compose run --rm web /opt/healthchecks/manage.py migrate
```

Next, create an admin account so you can log into the dashboard. It will prompt you for an email and a password:

```bash
docker compose run --rm web /opt/healthchecks/manage.py createsuperuser
```

Once the superuser is created, you can access the Healthchecks dashboard here: [http://192.168.1.14:6969/](http://192.168.1.14:6969/).

Let's add Healthchecks to the Homepage dashboard. Open `services.yaml`:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under your `Self-hosted services` category:

```yaml
    - Healthchecks:
        href: http://192.168.1.14:6969
        description: Cron job monitoring
        icon: healthchecks.png
```

### Code server

I use [code-server](https://github.com/coder/code-server) to run VS Code directly in my browser. This allows me to do quick edits on my server files without needing to use the remote server extension in a local VS Code instance, which consumes a lot of storage.

First, create the project directory and the configuration folder:

```bash
mkdir -p ~/docker-projects/code-server/config
cd ~/docker-projects/code-server
nano docker-compose.yml
```

Paste the following Docker Compose configuration:

```yaml
services:
  code-server:
    image: ghcr.io/coder/code-server:latest
    container_name: code-server
    restart: unless-stopped
    ports:
      - "8443:8080"
    volumes:
      - ./config:/home/coder/.config
      - /home/imad:/home/coder/workspace
    environment:
      - PUID=1000
      - PGID=988
      - PASSWORD=strong_password
```

> [!NOTE]
> We map `/home/imad` to `/home/coder/workspace` inside the container. This means when you open code-server in your browser, your entire home directory (including all your scripts and docker-projects) will be instantly available to edit. 

> [!IMPORTANT]
> Make sure to replace `strong_password` with a strong password before starting the container. You will be prompted to enter this password every time you access the web interface.

To create and start the container, run:

```bash
docker compose up -d
```

You can now access your web-based code editor here: [http://192.168.1.14:8443](http://192.168.1.14:8443).

Let's add code-server to the Homepage dashboard. Open `services.yaml`:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under your `Self-hosted services` category:

```yaml
    - Code Server:
        href: http://192.168.1.14:8443
        description: VS Code in the browser
        icon: vscode.png
```

### Navidrome

To listen to the music I backup on my phone or laptop, I need a service that can stream audio over the network. I use [Navidrome](https://github.com/navidrome/navidrome) to achieve this.

First, create the project directory and the data folder:

```bash
mkdir -p ~/docker-projects/navidrome/data
cd ~/docker-projects/navidrome
nano docker-compose.yml
```

Paste the following Docker Compose configuration:

```yaml
services:
  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    user: "1000:988"
    ports:
      - "4533:4533"
    restart: unless-stopped
    environment:
      - ND_SCANSCHEDULE=1m
      - ND_LOGLEVEL=info
    volumes:
      - ./data:/data
      - /home/imad/Music/YouTubeMusic:/music:ro
```

> [!NOTE]
> The configuration forces the container to run as `1000:988` (your user and the docker group) so it can securely access the host system. We also mount the `/home/imad/Music/YouTubeMusic` directory as read-only (`:ro`), so Navidrome can stream the music but cannot accidentally delete your backup files.

To create and start the container, run:

```bash
docker compose up -d
```

You can now access Navidrome here: [http://192.168.1.14:4533](http://192.168.1.14:4533). Upon your first visit, you will be prompted to create an admin user and password.

#### Adding Navidrome to Homepage

Navidrome requires a little extra work to connect to the Homepage dashboard because it uses a secure API token instead of a raw password. 

First, generate your token by combining your Navidrome **password** and a random **salt** string (e.g., `abc123`). 

For example, if your password is `MySecretPassword`, your combined string is `MySecretPasswordabc123`. Run this command in your terminal to generate the MD5 hash, replacing the string with your own:

```bash
echo -n "MySecretPasswordabc123" | md5sum
```

Copy the generated hash. Now, open the `services.yaml` file:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add the following under your `Self-hosted services` category, pasting your newly generated hash into the `token` field:

```yaml
    - Navidrome:
        href: http://192.168.1.14:4533
        description: Music streaming
        icon: navidrome.png
        widget:
          type: navidrome
          url: http://192.168.1.14:4533
          user: imadsaddik
          token: paste_your_generated_md5_hash_here
          salt: abc123
```

## Native services and automation

### Music backup

I use YouTube Music, and I have a specific playlist where I save the best music with no lyrics. To keep a local copy on my server, I wrote a script to download the audio automatically using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

This script uses `uv` to manage dependencies and install the latest versions of `yt-dlp` and `mutagen` before every run, because Google changes the YouTube API often. It also uses `aria2` to speed up the downloads and pings `Healthchecks` when the job starts and finishes.

First, go to your Healthchecks dashboard and create a new check. Set the schedule to run weekly on Sundays at 10:00 AM, and copy the unique Ping URL it generates for you.

<!-- TODO: add images here -->

Next, create the project directory and the script file:

```bash
mkdir -p ~/scripts/yt-music
nano ~/scripts/yt-music/backup_music.sh
```

Paste this code into the file. Make sure to replace `your-uuid-here` in the `HEALTHCHECK_URL` variable with the UUID you just copied from your dashboard:

```bash
#!/bin/bash
set -e

main() {
    setup_variables
    create_directories
    ping_healthcheck_start
    update_dependencies
    run_download
    ping_healthcheck_success
}

setup_variables() {
    export UV_EXECUTABLE_PATH="/home/imad/.local/bin/uv"
    export PROJECT_DIRECTORY="/home/imad/scripts/yt-music"
    export MUSIC_DIRECTORY="/home/imad/Music/YouTubeMusic"
    export LOG_FILE_PATH="$PROJECT_DIRECTORY/download.log"
    export PLAYLIST_URL="https://www.youtube.com/playlist?list=PL22-qG2MGGhAr96FUEz9jv11sVx0nSZTY"
    export HEALTHCHECK_URL="http://192.168.1.14:6969/ping/your-uuid-here"
}

create_directories() {
    mkdir -p "$MUSIC_DIRECTORY"
    mkdir -p "$PROJECT_DIRECTORY"
}

ping_healthcheck_start() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL/start" > /dev/null
}

update_dependencies() {
    if [ ! -d "$PROJECT_DIRECTORY/.venv" ]; then
        "$UV_EXECUTABLE_PATH" venv "$PROJECT_DIRECTORY/.venv"
    fi
    
    "$UV_EXECUTABLE_PATH" pip install --python "$PROJECT_DIRECTORY/.venv" --upgrade yt-dlp mutagen --quiet
}

run_download() {
    echo "[JOB STARTED] $(date)" >> "$LOG_FILE_PATH"
    
    "$PROJECT_DIRECTORY/.venv/bin/yt-dlp" \
      --ignore-errors \
      --extract-audio \
      --audio-format mp3 \
      --js-runtimes node \
      --embed-metadata \
      --embed-thumbnail \
      --download-archive "$PROJECT_DIRECTORY/archive.txt" \
      --downloader aria2c \
      --downloader-args "aria2c:-x 16 -s 16 -k 1M" \
      --output "$MUSIC_DIRECTORY/%(title)s.%(ext)s" \
      "$PLAYLIST_URL" >> "$LOG_FILE_PATH" 2>&1 || true

    echo "[JOB SUCCEEDED] $(date)" >> "$LOG_FILE_PATH"
}

ping_healthcheck_success() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL" > /dev/null
}

main
```

Make the script executable:

```bash
chmod +x ~/scripts/yt-music/backup_music.sh
```

Finally, add the script to your cron jobs. Because we store music in your home directory, run the regular user crontab without `sudo` so that your user owns the files:

```bash
crontab -e
```

Add this line to run the script every Sunday at 10:00 AM:

```text
0 10 * * 0 /home/imad/scripts/yt-music/backup_music.sh
```

You can always check your local logs by looking at the file generated in the project folder:

```bash
cat ~/scripts/yt-music/download.log
```

### Planka backup

Because Planka holds important personal ideas, we should set up automated backups. We will download the official backup scripts provided by the developers and wrap them in our own script to integrate with Healthchecks and prevent cron race conditions.

First, go to your Healthchecks dashboard and create a new check. Set the schedule to run every night at 9:00 PM (using the Cron expression `0 21 * * *`), set the Grace Time to 30 minutes, and copy the unique Ping URL it generates.

<!-- TODO: add images -->

Next, create a folder for the backups and download the official scripts:

```bash
mkdir -p ~/docker-projects/planka/backup/logs
cd ~/docker-projects/planka/backup
curl -L https://raw.githubusercontent.com/plankanban/planka/master/docker-backup.sh -o backup.sh
curl -L https://raw.githubusercontent.com/plankanban/planka/master/docker-restore.sh -o restore.sh
chmod +x backup.sh restore.sh
```

You need to tell the official backup script the exact names of your Docker containers. Open the file:

```bash
nano backup.sh
```

Find the container variables and change them to match what we defined in the `docker-compose.yml` file:

```bash
DOCKER_CONTAINER_POSTGRES="planka-postgres"
DOCKER_CONTAINER_PLANKA="planka"
```

While you have the file open, we must fix a bug in the official script. By default, Docker runs the backup container as the root user, which locks the temporary files and causes our wrapper script to fail during cleanup.

Find the line that says `Exporting data volume` and add `--user $(id -u):$(id -g)` to the docker run command. It should look exactly like this:

```bash
echo -n "Exporting data volume ... "
docker run --rm --user $(id -u):$(id -g) --volumes-from "$DOCKER_CONTAINER_PLANKA" -v "$BACKUP_TEMP:/backup" node:22-alpine cp -r /app/data /backup/data
echo "Success!"
```

By passing `--user $(id -u):$(id -g)`, Docker forces the temporary Alpine container to run as you instead of its default `root` user. This guarantees that all the exported backup files and temporary folders belong to your user account, permanently preventing those `Permission denied` crashes when your wrapper script tries to delete them at the end of the run.

Save and exit the file. Now, create your wrapper script to automate the process, clean up old files, and ping Healthchecks in the correct order:

```bash
nano run_backup.sh
```

Paste this code into the file. Remember to replace `your-uuid-here` with the UUID you copied from your dashboard:

```bash
#!/bin/bash
set -e

main() {
    setup_variables
    ping_healthcheck_start
    run_planka_backup
    clean_old_backups
    ping_healthcheck_success
}

setup_variables() {
    export BACKUP_DIR="/home/imad/docker-projects/planka/backup"
    export LOG_DIR="$BACKUP_DIR/logs"
    export TIMESTAMP=$(date +%Y%m%d%H%M)
    export HEALTHCHECK_URL="http://192.168.1.14:6969/ping/your-uuid-here"
}

ping_healthcheck_start() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL/start" > /dev/null
}

run_planka_backup() {
    cd "$BACKUP_DIR"
    bash backup.sh > "$LOG_DIR/${TIMESTAMP}-backup.log" 2>&1
}

clean_old_backups() {
    find "$BACKUP_DIR" -maxdepth 1 -name "*.tgz" -type f -mtime +14 -delete > "$LOG_DIR/${TIMESTAMP}-delete-backup.log" 2>&1 || true
    find "$LOG_DIR" -maxdepth 1 -name "*.log" -type f -mtime +14 -delete > /dev/null 2>&1 || true
}

ping_healthcheck_success() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL" > /dev/null
}

main
```

Make the wrapper script executable:

```bash
chmod +x run_backup.sh
```

Finally, add the script to your user crontab:

```bash
crontab -e
```

Add this single line to run the wrapper script every night at 9:00 PM:

```text
0 21 * * * /home/imad/docker-projects/planka/backup/run_backup.sh
```

### Minecraft server

We use [Fabric](https://fabricmc.net/) to host a lightweight, modded Minecraft server directly on the mini PC. 

First, install the required dependencies. The server requires `Java 21` to run. You also need `screen` to run the server in the background and `unzip` for archive extraction:

```bash
sudo nala install openjdk-21-jre-headless screen unzip -y
```

Next, create the server directories. Because the `/opt/` directory is owned by the root system, we need to create the folders using `sudo` and then change the ownership to our main user (`imad`). This prevents permission errors later when our automated scripts and dashboard try to manage the files.

```bash
sudo mkdir -p /opt/minecraft/server
sudo mkdir -p /opt/minecraft/backups
sudo chown -R imad:imad /opt/minecraft
```

Now, navigate to the server folder and download the [Fabric installer](https://fabricmc.net/use/installer/):

```bash
cd /opt/minecraft/server
curl -o fabric-installer.jar https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.1.1/fabric-installer-1.1.1.jar
```

> [!NOTE]
> The version `1.1.1` of the installer is the latest at the time of writing, but you can check for newer versions on the [official Maven repository](https://maven.fabricmc.net/net/fabricmc/fabric-installer/) and update the URL accordingly.

Run the installer via the command line to generate the server files for Minecraft `1.21.11` and Fabric loader `0.18.4`. This will automatically download the necessary core `.jar` files:

```bash
java -jar fabric-installer.jar server -mcversion 1.21.11 -loader 0.18.4 -downloadMinecraft
```

> [!NOTE]
> You can change the `-mcversion` and `-loader` parameters to install different versions of Minecraft and Fabric.

Clean up the folder by removing the installer:

```bash
rm fabric-installer.jar
```

#### Accepting the EULA

Before the server can fully start, you must accept the [Minecraft End User License Agreement (EULA)](https://www.minecraft.net/en-us/eula). Run the server once to generate the necessary files. It will intentionally fail and create a `eula.txt` file:

```bash
java -jar fabric-server-launch.jar nogui
```

Open the file, or use this command to automatically accept the agreement:

```bash
echo "eula=true" > eula.txt
```

#### Start and stop scripts

We need to create scripts to easily start and stop the server in the background using `screen`. 

Create the start script:

```bash
nano start.sh
```

Paste the following code. This command creates a detached screen session named `mc-server` and allocates 4GB of RAM to the Java process:

```bash
#!/bin/bash
screen -dmS mc-server java -Xms4G -Xmx4G -jar fabric-server-launch.jar nogui
```

Create the stop script:

```bash
nano stop.sh
```

Paste the following code. Instead of killing the process abruptly, this script sends the graceful `stop` command directly into the running screen session:

```bash
#!/bin/bash
screen -S mc-server -X stuff "stop$(printf \\r)"
```

Make both scripts executable:

```bash
chmod +x start.sh stop.sh
```

You can now start the server by running `/opt/minecraft/server/start.sh`.

#### Server mods

Fabric requires mods to be placed in the `mods` folder inside the server directory. 

```bash
mkdir /opt/minecraft/server/mods
```

You must download the correct Fabric versions of the mods and place them in this folder. 

> [!WARNING]  
> Do not place client-side mods like `JourneyMap` or `Punchy` in this folder, or the headless server will crash. 

Here are some core server mods I installed:

- [Fabric API](https://www.curseforge.com/minecraft/mc-mods/fabric-api): The core library required by almost all Fabric mods.
- [Balm](https://www.curseforge.com/minecraft/mc-mods/balm): A required dependency library for Waystones.
- [Waystones](https://www.curseforge.com/minecraft/mc-mods/waystones): Allows players to teleport between activated monuments.
- [True Ending](https://www.curseforge.com/minecraft/mc-mods/true-ending): Overhauls the Ender Dragon fight.
- [Just Enough Items (JEI)](https://www.curseforge.com/minecraft/mc-mods/jei): Required on the server for Minecraft 1.21.2 and newer to sync crafting recipes to the players.

#### Automated backups

To prevent data loss, we will schedule a script to back up the world files every night. 

First, go to your Healthchecks dashboard, create a new check scheduled for 10:00 PM (`0 22 * * *`), and copy the unique Ping URL.

<!-- // TODO: Healthchecks dashboard showing the new Minecraft backup check and the Ping URL -->

Create the backup script:

```bash
nano /opt/minecraft/backup.sh
```

Paste the following code, ensuring you replace the `HEALTHCHECK_URL` with your new UUID:

```bash
#!/bin/bash
set -e

main() {
    setup_variables
    create_directory
    ping_healthcheck_start
    create_backup
    clean_old_backups
    ping_healthcheck_success
}

setup_variables() {
    export BACKUP_DIR="/opt/minecraft/backups"
    export SERVER_DIR="/opt/minecraft/server"
    export TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
    export BACKUP_FILE="$BACKUP_DIR/world_backup_$TIMESTAMP.tar.gz"
    export HEALTHCHECK_URL="http://192.168.1.14:6969/ping/your-uuid-here"
}

create_directory() {
    mkdir -p "$BACKUP_DIR"
}

ping_healthcheck_start() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL/start" > /dev/null
}

create_backup() {
    # We only backup the world folder, which contains DIM-1 and DIM1 in Fabric
    tar -czf "$BACKUP_FILE" -C "$SERVER_DIR" world
}

clean_old_backups() {
    # Delete backups older than 7 days to save SSD space
    find "$BACKUP_DIR" -type f -name "world_backup_*.tar.gz" -mtime +7 -delete || true
}

ping_healthcheck_success() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL" > /dev/null
}

main
```

Make the script executable:

```bash
chmod +x /opt/minecraft/backup.sh
```

Add it to your user crontab:

```bash
crontab -e
```

Add this line so it runs automatically every day at 10:00 PM:

```text
0 22 * * * /opt/minecraft/backup.sh
```

### Minecraft dashboard

The dashboard allows users on the local network to start and stop the Minecraft server from a web browser, see how many people are connected, and track the server uptime.

Because it needs direct access to the `screen` session running on the host machine, this application runs natively rather than in a Docker container. The backend is powered by [FastAPI](https://fastapi.tiangolo.com/) (managed by `uv`), and the frontend is built with [Vue.js](https://vuejs.org/).

The source code and built files live in `/opt/minecraft/dashboard`.

#### Systemd backend service

To keep the FastAPI backend running in the background and ensure it starts automatically when the mini PC boots up, we use a systemd service. 

Create the service file:

```bash
sudo nano /etc/systemd/system/minecraft-dashboard-api.service
```

Paste the following configuration. This tells systemd to run the API using the `uv` tool we installed earlier, binding it to the local loopback address on port `8000`:

```ini
[Unit]
Description=Minecraft dashboard API
After=network.target

[Service]
User=imad
WorkingDirectory=/opt/minecraft/dashboard/backend
ExecStart=/home/imad/.local/bin/uv run uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Reload the systemd daemon to recognize the new file, then enable and start the service simultaneously:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now minecraft-dashboard-api.service
```

#### Building the Vue.js frontend

Before Nginx can serve the frontend, you need to compile the Vue.js source code into static files. Whenever you make changes to the Vue components or API logic, you must run this build process again to see the changes.

Navigate to the frontend directory:

```bash
cd /opt/minecraft/dashboard/frontend
```

Install the dependencies and build the project using `pnpm`:

```bash
pnpm install
pnpm run build
```

This command will bundle your code and generate a `dist/` folder containing the compiled HTML, CSS, and JavaScript files.

#### Nginx frontend and reverse proxy

With the frontend compiled, we use Nginx to serve the static files from the `dist/` directory and route API requests to the FastAPI backend.

Create the Nginx site configuration:

```bash
sudo nano /etc/nginx/sites-available/minecraft-dashboard
```

Paste the following configuration. It listens on port `8080`, serves the frontend files, and proxies any request starting with `/api/` to the systemd service running on port `8000`:

```nginx
server {
    listen 8080;
    server_name _;

    root /opt/minecraft/dashboard/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the new site by creating a symbolic link from the `sites-available` directory to the `sites-enabled` directory:

```bash
sudo ln -s /etc/nginx/sites-available/minecraft-dashboard /etc/nginx/sites-enabled/
```

Next, remove the default Nginx welcome page:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Before restarting the service, test your new Nginx configuration to ensure there are no syntax errors:

```bash
sudo nginx -t
```

If the test is successful and reports no errors, gracefully reload the Nginx service to apply the new configuration without dropping any active connections:

```bash
sudo systemctl reload nginx
```

You can now access the dashboard by visiting [http://192.168.1.14:8080/](http://192.168.1.14:8080/).

### Automatic shutdown and boot

To save electricity, the mini PC is scheduled to automatically sleep at night and wake up the next morning. Before going to sleep, it safely shuts down specific services to prevent data corruption.

First, go to your Healthchecks dashboard and create a new check scheduled to run daily at 11:00 PM (`0 23 * * *`). Copy the unique Ping URL it generates.

<!-- TODO: add images -->

Create the shutdown script:

```bash
sudo nano /usr/local/bin/nightly_sleep.sh
```

Paste the following bash script. It cleanly shuts down the Minecraft server, pings Healthchecks to report success, and then uses `rtcwake` to suspend the machine to memory (`-m off`) and schedules the hardware clock to wake the system up `28800` seconds (8 hours) later.

Make sure to replace `your-uuid-here` with your actual Healthchecks UUID:

```bash
#!/bin/bash
set -e

MINECRAFT_STOP_SCRIPT="/opt/minecraft/server/stop.sh"
HEALTHCHECK_URL="http://192.168.1.14:6969/ping/your-uuid-here"

main() {
    echo "Starting nightly shutdown sequence"
    ping_healthcheck_start
    stop_all_projects
    sleep_system
}

ping_healthcheck_start() {
    curl -fsS --retry 3 "$HEALTHCHECK_URL/start" > /dev/null
}

stop_all_projects() {
    stop_minecraft
}

stop_minecraft() {
    if [ -f "$MINECRAFT_STOP_SCRIPT" ]; then
        echo "Calling Minecraft shutdown script"
        bash "$MINECRAFT_STOP_SCRIPT"
    fi
}

sleep_system() {
    echo "All projects stopped safely. Goodnight!"
    curl -fsS --retry 3 "$HEALTHCHECK_URL" > /dev/null
    /usr/sbin/rtcwake -m off -s 28800 # 8h
}

main
```

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/nightly_sleep.sh
```

Because `rtcwake` interacts directly with the motherboard hardware clock, this script must be run as root. Open the root crontab:

```bash
sudo crontab -e
```

Add this line to run the script every night at 11:00 PM (`0 23 * * *`). It will log its output to `/var/log/nightly_sleep.log` so you can verify it ran successfully:

```text
0 23 * * * /usr/local/bin/nightly_sleep.sh >> /var/log/nightly_sleep.log 2>&1
```

### Uninterruptible power supply setup

To protect the homelab from grid failures and data corruption, the infrastructure is backed by an [nJoy Horus Plus 2000 UPS](https://www.njoy.global/product/horus-plus-2000/PWUP-LI200H1-AZ01B). The end goal is to use [NUT (Network UPS Tools)](https://networkupstools.org/) to continuously monitor the battery state and automatically trigger a graceful shutdown of all connected machines before the backup power completely drains.

#### Hardware and network preparation

For the automated shutdown sequence to work reliably across multiple machines, both the power and network wiring must be set up intentionally. 

The following devices are plugged directly into the battery backup sockets of the UPS:

- Lenovo mini PC (the main server and UPS manager)
- Asus gaming laptop
- Local network switch

<!-- TODO: add this later -->
![Diagram showing the power and network wiring topology of the UPS, mini PC, laptop, and switch](./images/ups_topology.png)

My internet router is too far away to be plugged into the UPS. Because of this, the local network switch must be on the battery backup. 

During a power outage, the router will die and internet access will drop. However, the UPS will keep the switch powered on. This maintains the local network link so the mini PC can successfully send emergency shutdown signals over the network to other devices, like my gaming laptop, before shutting itself down.

#### Bypassing Ubuntu security

Ubuntu restricts direct access to physical USB ports for security reasons. Because the NUT service drops root privileges and runs as a restricted `nut` system user, Ubuntu will block it from reading the UPS data cable by default. You need to create a specific `udev` rule to grant permission.

First, plug the UPS into the server via USB and find its hardware ID:

```bash
lsusb
```

Your output will look something like this:

```text
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 0665:5161 Cypress Semiconductor USB to Serial
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
```

Look for the UPS in the list. Here, it shows up as a Cypress Semiconductor chip with the ID `0665:5161`.

Create a new `udev` rule file specifically for the UPS:

```bash
sudo nano /etc/udev/rules.d/99-nut-ups.rules
```

Paste the following line, replacing the Vendor and Product IDs with your exact numbers. This tells the kernel to grant the `nut` group access to this specific piece of hardware:

```text
SUBSYSTEM=="usb", ATTRS{idVendor}=="0665", ATTRS{idProduct}=="5161", MODE="0664", GROUP="nut"
```

Save the file. To apply the new permissions without rebooting the server, reload the `udev` rules and trigger them:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

> [!NOTE]
> After running the command, physically unplug the USB cable from the server, wait 3 seconds, and plug it back in to ensure the hardware registers the new group permissions.

#### Configuring the NUT data server

The NUT architecture is split into layers. The driver physically talks to the UPS, and the [data server (upsd)](https://networkupstools.org/docs/man/upsd.html) reads from that driver to share the metrics over the network.

First, install the Network UPS Tools package:

```bash
sudo nala install nut -y
```

##### Setting the server mode

Because this mini PC will broadcast the UPS data to Docker containers (Homepage, Netdata) and other devices on the network, it must be configured as a network server.

Open the main mode configuration file:

```bash
sudo nano /etc/nut/nut.conf
```

Find the `MODE` line at the bottom and change it to `netserver`:

```text
MODE=netserver
```

##### Connecting the driver

You need to tell NUT exactly which driver to use and what hardware IDs to look for. Open the UPS definition file:

```bash
sudo nano /etc/nut/ups.conf
```

Scroll to the bottom and paste the following block. The [nutdrv_qx](https://networkupstools.org/docs/man/nutdrv_qx.html) driver handles the Megatec Qx protocol. This is the standard communication protocol used by nJoy. It natively supports the Cypress chip inside the UPS:

```text
[njoy]
    driver = nutdrv_qx
    port = auto
    desc = "nJoy Horus Plus 2000"
    vendorid = "0665"
    productid = "5161"
```

> [!NOTE]
> Do not forget to change the `vendorid` and `productid` values to match the hardware ID you found with `lsusb`. In `desc`, put the name of your UPS so it is easily identifiable in the network.

##### Opening the network gates

By default, the [UPS data server](https://networkupstools.org/docs/man/upsd.conf.html) only listens to itself (`localhost`). Because Homepage runs inside a Docker network and the gaming laptop will connect over the local network, you must tell the server to accept external requests.

Open the main server configuration:

```bash
sudo nano /etc/nut/upsd.conf
```

Add this line to the bottom of the file to open the default NUT port (3493) to your local network:

```text
LISTEN 0.0.0.0 3493
```

##### Setting up authentication

Finally, create a secure user account. This prevents unauthorized devices on your network from reading your power metrics or triggering fake shutdown commands. 

First, generate a strong, random password in your terminal:

```bash
openssl rand -hex 16
```

Copy the output and keep it somewhere safe. Now, open the user file:

```bash
sudo nano /etc/nut/upsd.users
```

Paste this block at the bottom. The `upsmon primary` tag gives this user the authority to manage emergency shutdowns:

```text
[admin]
    password = your_generated_password_here
    upsmon primary
```

> [!IMPORTANT]
> Make sure to replace `your_generated_password_here` with the strong password you generated. This password will be used later when we configure the UPS monitoring clients on the mini PC and gaming laptop, so do not skip this step or use a weak password.

#### Verifying the data server

With the configuration files updated, restart the server daemon to apply the changes and start broadcasting:

```bash
sudo systemctl restart nut-server
```

To verify that the server is successfully talking to your UPS, use the client command to request the live metrics:

```bash
upsc njoy
```

If everything is configured correctly, your terminal will output a list of data points, including your current battery voltage and the UPS status.

```text
Init SSL without certificate database
battery.voltage: 27.18
device.type: ups
driver.debug: 0
driver.flag.allow_killpower: 0
driver.name: nutdrv_qx
driver.parameter.pollfreq: 30
driver.parameter.pollinterval: 2
driver.parameter.port: auto
driver.parameter.productid: 5161
driver.parameter.synchronous: auto
driver.parameter.vendorid: 0665
driver.state: quiet
driver.version: 2.8.1
driver.version.data: Voltronic-QS-Hex 0.10
driver.version.internal: 0.36
driver.version.usb: libusb-1.0.27 (API: 0x100010a)
input.voltage: 232.9
output.frequency: 50.9
output.voltage: 232.9
ups.beeper.status: enabled
ups.delay.shutdown: 30
ups.delay.start: 180
ups.firmware.aux: PM-P
ups.load: 17
ups.productid: 5161
ups.status: OL
ups.type: offline / line interactive
ups.vendorid: 0665
```

#### Configuring the automated shutdown monitor

With the data server running, you need to set up the monitor ([upsmon](https://networkupstools.org/docs/man/upsmon.html)). This background watcher reads the live data and executes a safe shutdown when the backup power runs out.

Open the monitor configuration file:

```bash
sudo nano /etc/nut/upsmon.conf
```

First, tell the monitor to watch the UPS using the admin credentials you just created. Add this line at the bottom, making sure the password matches:

```text
MONITOR njoy@localhost 1 admin your_generated_password_here primary
```

Next, scroll through the file to find the `SHUTDOWNCMD` line. You want to make sure it looks exactly like this:

```text
SHUTDOWNCMD "/sbin/shutdown -h +0"
```

> [!NOTE]
> The monitor is smart. It does not shut down your mini PC the second the power flickers. Instead, it waits for the UPS to broadcast two specific status flags at the exact same time: `OB` (On Battery) and `LB` (Low Battery). Only when the battery physically drains to its safe minimum limit will it trigger the shutdown command.

Save the file. Finally, enable and restart the NUT services so they start automatically whenever the server boots up:

```bash
sudo systemctl enable nut-server nut-monitor
sudo systemctl restart nut-server nut-monitor
```

You can confirm that the monitor is running and connected to the UPS by checking its status:

```bash
sudo systemctl status nut-monitor
```

You should see a line that mentions `UPS: njoy@localhost (primary)` in the output, indicating a successful connection.

```text
Apr 21 19:53:05 saddik-server nut-monitor[746774]: UPS: njoy@localhost (primary) (power value 1)
```

#### Dashboard integrations

With the UPS data broadcasting over the local network, you can easily plug these metrics into your existing monitoring tools to get both live overviews and historical data.

##### Netdata

Because Netdata was configured to use `network_mode: host` during its Docker installation, it has direct access to the mini PC's local ports. Netdata has a built-in auto-discovery engine that constantly scans for known services.

The moment you restart the `nut-server` on port `3493`, Netdata automatically detects it. There is zero configuration needed. If you open your Netdata dashboard at `http://192.168.1.14:19999`, a new UPS section will appear in the right menu. This gives you beautiful historical charts tracking your grid input voltage, battery voltage, and load over time.

<!-- TODO: show images here -->

##### PeaNUT (API Bridge)

Homepage cannot read the raw TCP data coming from the UPS directly. To fix this, we use a lightweight tool called [PeaNUT](https://github.com/Brandawg93/PeaNUT) to act as a bridge. It reads the raw NUT data and translates it into a clean JSON API.

Create a project directory for PeaNUT:

```bash
mkdir -p ~/docker-projects/peanut/config
cd ~/docker-projects/peanut
nano docker-compose.yml
```

Paste the following configuration. We map it to port `8082`, and we disable authentication so Homepage can read the API without a problem on your local network:

```yaml
services:
  peanut:
    image: brandawg93/peanut:latest
    container_name: PeaNUT
    restart: unless-stopped
    volumes:
      - ./config:/config
    ports:
      - "8082:8080"
    environment:
      - WEB_PORT=8080
      - AUTH_DISABLED=true
```

Start the container:

```bash
docker compose up -d
```

<!-- Add images showing how to do this -->

Open your browser and go to `http://192.168.1.14:8082`. In the PeaNUT settings, add your NUT server by entering your server's IP (`192.168.1.14`), Port (`3493`), and the `admin` username and password you created earlier in `upsd.users`.

##### Homepage

Now that PeaNUT is translating the data into an API, Homepage can read it using a custom API widget. 

Open your Homepage services file:

```bash
nano ~/docker-projects/homepage/config/services.yaml
```

Add a new category for your hardware and paste this block. Ensure the indentation is exactly as shown to avoid YAML parsing errors:

```yaml
- Hardware:
    - nJoy UPS:
        href: http://192.168.1.14:8082
        description: Horus Plus 2000
        icon: ups.png
        widget:
          type: customapi
          url: http://192.168.1.14:8082/api/v1/devices/njoy
          mappings:
            - field: battery.charge
              label: Battery
              format: percent
            - field: ups.load
              label: Load
              format: percent
            - field: ups.status
              label: Status
              format: text
              remap:
                - value: OL
                  to: Online
                - value: OB
                  to: On Battery
                - value: LB
                  to: Low Battery
                - any: true
                  to: Unknown
```

Save the file. Homepage updates automatically. If you refresh your browser at `http://192.168.1.14:3000`, you will see a live battery percentage, load percentage, and the current connection status.

##### Fixing missing battery percentages

When you open PeaNUT or Homepage, you might see **N/A** or **NaN%** instead of a battery percentage. This happens because many line-interactive UPS units do not calculate their own battery percentage. They only report their raw internal voltage to the server.

To fix this, you can force the `nutdrv_qx` driver to estimate the battery charge by telling it the physical voltage limits of the batteries. 

The Horus Plus 2000 uses a 24-volt internal system (two 12V lead-acid batteries). A healthy 24V system reaches a maximum of about 27.4V when floating at 100%, and is considered completely dead around 21.0V.

Open the UPS configuration file:

```bash
sudo nano /etc/nut/ups.conf
```

Add the `default.battery.voltage.high` and `low` limits to your `[njoy]` block so it looks like this:

```text
[njoy]
    driver = nutdrv_qx
    port = auto
    desc = "nJoy Horus Plus 2000"
    vendorid = "0665"
    productid = "5161"
    default.battery.voltage.high = 27.4
    default.battery.voltage.low = 21.0
```

Save the file and exit. Because you added new hardware variables, you must tell NUT to rebuild its background services. 

Run these three commands in this exact order to safely resync the configuration, start the driver, and restart the data server:

```bash
sudo upsdrvsvcctl resync
sudo upsdrvsvcctl start
sudo systemctl restart nut-server
```

You can verify that the driver is now successfully calculating the math by running this command:

```bash
upsc njoy | grep battery.charge
```

It should return a value like `battery.charge: 97`. Once the terminal confirms the percentage exists, Homepage and PeaNUT will automatically drop the "N/A" and display the correct percentage on their next refresh.

#### Secondary monitor configuration (gaming laptop)

Since my gaming laptop is plugged into the UPS and connected to the same switch, I configured it to listen to the mini PC and shut down automatically during a blackout.

On my gaming laptop, I installed the NUT client:

```bash
sudo nala install nut-client -y
```

Open the mode configuration file:

```bash
sudo nano /etc/nut/nut.conf
```

Change the mode to `netclient` because this machine will only listen for data over the network:

```text
MODE=netclient
```

Next, open the monitor configuration file:

```bash
sudo nano /etc/nut/upsmon.conf
```

Add the `MONITOR` line at the bottom. Use the mini PC's static IP and the `secondary` tag instead of primary:

```text
MONITOR njoy@192.168.1.14 1 admin your_generated_password_here secondary
```

> [!NOTE]
> Make sure to replace `your_generated_password_here` and `192.168.1.14` with your specific password and the mini PC's IP address.

Make sure the `SHUTDOWNCMD` line is uncommented and looks like this:

```text
SHUTDOWNCMD "/sbin/shutdown -h +0"
```

Save the file and restart the monitor service on the laptop:

```bash
sudo systemctl enable nut-monitor
sudo systemctl restart nut-monitor
```

Now, if the UPS battery hits a critical level, the mini PC will send a signal to your gaming laptop to shut down safely before the mini PC shuts itself down.

#### Testing the setup

It is important to test the shutdown sequence to make sure everything works before a real power outage happens. You can test just the network signaling, or you can test the entire system by simulating a blackout.

> [!WARNING]
> Both of these tests will shut down your computers. Save all your work before proceeding.

##### Software test

This test verifies that the mini PC can successfully send the emergency shutdown signal over the network to the gaming laptop, and that both machines handle the command correctly. This method ignores the battery level and forces the shutdown immediately.

On your mini PC, trigger the forced shutdown signal:

```bash
sudo upsmon -c fsd
```

Your other device will begin its shutdown sequence, followed by the mini PC. After you turn the mini PC back on, you must clear the emergency kill file before the NUT data server will start normally again:

```bash
sudo rm -f /etc/killpower
sudo systemctl restart nut-server
```

##### Real world test

This is the complete test. While the software test just sends the final shutdown command, this test verifies that the UPS correctly detects the power loss, monitors the battery drain, and automatically triggers the alert when it reaches the critical low state.

Follow these steps to simulate a blackout:

1. Physically unplug the UPS from the wall socket.
2. The UPS will start beeping. Your Homepage and PeaNUT dashboards will update to show the system is on battery.
3. Let the battery drain. 
4. Once the battery voltage drops to the `21.0V` critical limit we configured earlier, the UPS will flag a low battery state.
5. The mini PC will detect this state, broadcast the shutdown signal to the laptop over the network switch, and both machines will power off safely.
