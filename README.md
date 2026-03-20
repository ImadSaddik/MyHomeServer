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
