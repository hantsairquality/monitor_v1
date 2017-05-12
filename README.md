# monitor_v1


The scripts have been tested using Raspberry Pi 3 and Raspberry Pi Zero W with Rasbian Jessie Lite. This can be downloaded at
https://www.raspberrypi.org/downloads/raspbian/.

Currently only Python 2.7 is supported until the bitwise operations are updated to support python 3.

# The easy way to enable ssh and setup wireless

The boot partition is readable using a card reader with any operating system. Create the file /boot/wpa_supplicant.conf. Add your wifi settings as follows:

    network={
        ssid="YOUR_SSID"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }

On the first boot raspbian will copy the file to the normal location (/etc/wpa_supplicant/wpa_supplicant.conf).
To enable SSH on the raspberry pi, make an empty file named shh on the boot partition. 

# Installing monitor software to Raspberry Pi
Find the IP address of your Pi. The easiest way is through your home router. Then login using ssh.

    shh pi@<your ip address>

The PM sensor uses the serial port, this requires turning off the console. Do this by running

    sudo raspi-config

Go to /Interfacing Options/Serial answer no to a login shell and yes to the serial port being enabled. You will be prompted to reboot.

The monitor is in the early stages of development, this means things can change. Because of this it is recommended to use a virtual environment. The install script assumes you have python 2.7 and pip installed. If you need to install it run the following:

    sudo apt-get update
    sudo apt-get install -y python-pip git build-essential python-dev python-smbus
    
For development - create and activate a python 2.7 environment using

    virtualenv -p python2 sniffyPy2Env
    source ./sniffyPy2Env/bin/activate

To install the latest monitor scripts clone the repository and run

    git clone https://github.com/hantsairquality/monitor_v1/
    ./monitor_v1/install.sh
    
This includes the scripts for the analogue gas sensors which interface via the MCP3008 ADC chip on the SPI bus.

The monitor currently runs separate scripts for each sensor. These send data to a SQL via UDP. This is temporary until we migrate to MQTT. To run the scripts.

To start the monitor when the pi boots 
    
    sudo crontab -e

then add the following line (currently starts PM monitor only)
NB script assumes that your not using virtualenv.

    @reboot sh /home/pi/monitor_v1/sniffy.sh >/home/pi/logs/cronlog 2>&1
    

# Important scripts

- ppm.py               this sends PM data from the PMS1003 sensor to the SQL server via UDP
- 2_sensorAFE_v1.py    same but for analogue sensor data
- bmp180.py            likewise - for the bosch BMP180 environment chip
- pms1003_IOT.py       outputs PMS1003 data onscreen and uploads to opensensors.io using MQTT
   
