This is a guide for how to set up a raspberry pi headless (without a monitor or keyboard) over Wifi.
These two sites were used for reference:
- https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
- https://howchoo.com/g/ndy1zte2yjn/how-to-set-up-wifi-on-your-raspberry-pi-without-ethernet

## Prerequisites

This assumes you have

- A raspberry pi
- A wifi adapter for the pi
- An SD card with Raspbian (I'm using [Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/) with Desktop, but the Lite version makes more sense for headless)

## Before first boot

Insert the SD card into another computer and open the boot drive.

Enable SSH by adding an empty file to the drive named `ssh`.

Set the pi up to automatically connect to wifi by adding a file named `wpa_supplicant.conf`:
```conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```
This `wpa_supplicant` file format is specific to Raspbian Stretch and common wifi settings.
Multiple networks can be defined.

## Remoting in

Before booting up, know that this setup will not be secure. The raspberry pi will still have its default password of `raspberry` and anyone on the same network can gain access.

After booting up the pi, find the IP address so you can SSH in. The IP address can easily be found with the [Fing app](https://www.fing.io/), assuming the pi connected to wifi successfully.

If on Windows, SSH into the pi using [Putty](https://www.putty.org/) and the pi's IP address.

Log in with user `pi` and password `raspberry`. Change the password immediately using `passwd`.

## Next steps

Use these commands to set up the project.
```bash
mkdir workspace
cd workspace
git clone https://github.com/BotsForRoss/BotRoss.git
cd BotRoss
pip3 install -r requirements.txt
```

Remember to use `python3` to run scripts (not just `python`).


