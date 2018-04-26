toggle_setting_on_off()
{
lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=False
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=True
  end
  print(line)
end
if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}

enter_full_setting()
{
lua - "$1" "$2" <<EOF > "$2.bak"
local key=assert(arg[1])
local fn=assert(arg[2])
local file=assert(io.open(fn))
local made_change=False
for line in file:lines() do
  if line:match("^#?%s*"..key) then
    line=key
    made_change=True
  end
  print(line)
end
if not made_change then
  print(key)
end
EOF
mv "$2.bak" "$2"
}


CONFIG=/boot/config.txt
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo 'Welcome to the Chicken door control setup'
echo 'Please note that the initial setup requires an active internet connection.'
#echo 'First, we will update the apt-get database'
sudo apt-get -qq update
sudo apt-get -qq -y install build-essential python-dev python-pip
echo '----------------'
echo 'Installing python prerequisites for the Chicken door control Software: web.py and pyephem'
sudo pip install web.py pyephem
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_boot_behaviour B1
toggle_setting_on_off watchdog on $CONFIG
enter_full_setting 'dtoverlay=i2c-rtc,ds3231' $CONFIG
sudo echo 'KERNEL=="watchdog", MODE="0666", OWNER="pi"' > /etc/udev/rules.d/60-watchdog.rules

echo '----------------'
echo 'Registering the chicken door control as a service for systemctl'
echo 'For this, we follow the instructions from https://www.raspberrypi.org/documentation/linux/usage/systemd.md'
SERVICE_FILE="/etc/systemd/system/ChickenDoor.service"
sudo echo "[Unit]" > $SERVICE_FILE
sudo echo "Description=Chicken Door Control" >> $SERVICE_FILE
sudo echo "[Service]" >> $SERVICE_FILE
sudo echo "ExecStart=/usr/bin/python ${DIR}/AppStarter.py" >> $SERVICE_FILE
sudo echo "WorkingDirectory=${DIR}" >> $SERVICE_FILE
sudo echo "StandardOutput=inherit" >> $SERVICE_FILE
sudo echo "StandardError=inherit" >> $SERVICE_FILE
sudo echo "Restart=always" >> $SERVICE_FILE
sudo echo "User=pi" >> $SERVICE_FILE
sudo echo "[Install]" >> $SERVICE_FILE
sudo echo "WantedBy=multi-user.target" >> $SERVICE_FILE

sudo systemctl daemon-reload
sudo systemctl start ChickenDoor.service
sudo systemctl enable ChickenDoor.service


echo 'In order to enable the RTC hardware, please do the following:'
echo 'edit the following file: /lib/udev/rwclock-set '
echo 'comment out the following lines:'
echo 'if [ -e /run/systemd/system ] ; then'
echo '    exit 0'
echo 'fi'