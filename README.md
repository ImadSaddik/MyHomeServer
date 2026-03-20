# Home server documentation

In this repository, I am documenting my home server setup and the projects running on it. The home server is a `Lenovo ThinkCentre M720Q Tiny Core`, which is a small form factor desktop computer.

It is running `Ubuntu Server 24.04 LTS`, and is used to self-host applications, game servers, and run daily/weekly tasks.

My goal with this documentation is to make it easier for myself to remember how to set up and maintain my home server, as well as to share my setup with others who may be interested in self-hosting.

![A banner showing a title and a description on the left. On the right, we have an illustration of the Lenovo ThinkCentre M720Q Tiny Core](./images/banner_introduction.png)

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
