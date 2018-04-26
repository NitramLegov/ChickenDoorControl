# ChickenDoorControl
This repository contains code in order to automatically open and close a chicken door based on sunset and sunrise at a given location.

# Hardware prerequisites
The code is based on the following hardware: <br>
Raspberry pi (tested on a RPi A, Rev 2) <br>
[Sainsmart 2 channel Relai](https://www.sainsmart.com/products/2-channel-5v-relay-module) <br>
[DS3231 RTC](https://datasheets.maximintegrated.com/en/ds/DS3231.pdf) with [this board](https://smile.amazon.de/HALJIA-Präzision-Arbeitsspeicher-Arduino-Raspberry/dp/B01F6MJZGQ)

# Installation
Simply download the repository and run:
```bash
cd ChickenDoorControl/ChickenDoorControl/
sudo ./Install.sh
```

Please put special notice on the following manual task:<br>
In order to enable the RTC hardware, please do the following:<br>
1. reboot <br>
2. Edit the following file: /lib/udev/hwclock-set <br>
comment out the following lines:<br>
```bash
if [ -e /run/systemd/system ] ; then
    exit 0
fi
```

# Usage
1. Any configuration is stored in ChickenDoorControl/ChickenDoorControl/ChickenDoorControl.conf<br>
      In here, you can edit the pins for opening and closing the door (BCM Layout)<br>
      you can also edit the time needed for opening & closing (in seconds)<br>
      the default config is:<br>
      ```
      [Doorcontrol]
      up_pin = 27
      down_pin = 17
      time = 30
      ```
2. The sainsmart module should be powered with 5V<br>
3. Please note the system is designed to run headlesss. It uses the hardware watchdog to automatically reboot if the pi gets hung up.
