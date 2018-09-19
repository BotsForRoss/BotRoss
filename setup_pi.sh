# This sets up a fresh Raspbian Stretch Lite (June 2018) to operate BotRoss

set -e  # stop on failures

cd ~

# do updates
sudo apt-get update && sudo apt-get upgrade -y

# get essential development tools
sudo apt-get install git -y
curl https://bootstrap.pypa.io/get-pip.py | sudo python3

# get repositories
set +e  # allow failures for git clone (in case the repo already exists)
git clone https://www.github.com/BotsForRoss/BotRoss.git
git clone https://www.github.com/BotsForRoss/PyCNC.git
set -e

# install repo dependencies
sudo pip install -r BotRoss/requirements.txt
sudo pip install PyCNC

# get xbox controller support
sudo pip install xbox360controller

# fix bluetooth
sudo sed -i 's|^ExecStart=/usr/lib/bluetooth/bluetoothd$|ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap|' \
    /lib/systemd/system/bluetooth.service
sudo adduser pi bluetooth
sudo apt install bluealsa -y

# get pygame for audio
# this is totally optional
sudo apt-get install mercurial -y
git clone https://github.com/pygame/pygame.git
cd pygame
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev -y
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev -y
sudo apt-get install python3-dev python3-numpy -y
python3 setup.py build
sudo python3 setup.py install

echo "Setup complete. You should probably reboot."
