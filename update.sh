cd /home/pi/WebRadiator
sudo systemctl stop web_radiator.service
git pull
sudo systemctl restart web_radiator.service
sudo systemctl status web_radiator.service
