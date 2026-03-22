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

## Core system configuration

After installing Ubuntu Server, there are a few core system configurations you should complete before hosting any services. These initial steps ensure your server is secure, stable, and ready to run applications smoothly.

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

