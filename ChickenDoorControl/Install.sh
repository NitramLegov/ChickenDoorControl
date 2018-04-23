DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo 'Welcome to the Chicken door control setup'
echo 'Please note that the initial setup requires an active internet connection.'
echo 'First, we will update the apt-get database'
sudo apt-get -qq update
echo '----------------'
echo 'Installing python prerequisites for the Chicken door control Software: web.py and pyephem'
sudo pip install web.py pyephem
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_boot_behaviour B1
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