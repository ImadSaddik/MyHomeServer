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