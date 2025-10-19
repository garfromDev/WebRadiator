# deploiement sur la rapsberry a partir du moment ou git est installé et le porjet cloné
#!!!!!! CE SCRIPT N'A JAMAIS ETE TESTE !!!!!!!!

#création de la venv
python3 -m venv webradiator
source webradiator/bin/activate

#installation des librairie systeme
sudo apt install swig 
# Installer toutes les bibliothèques GPIO depuis apt
sudo apt install python3-lgpio python3-rpi-lgpio python3-spidev

# Créer les liens symboliques
python3 -c "
import sys
import os
from pathlib import Path

venv_site = Path(sys.prefix) / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages'
system_site = Path('/usr/lib/python3/dist-packages')

for item in ['lgpio.py', 'RPi', 'spidev.py']:
    src = system_site / item
    dst = venv_site / item
    if src.exists() and not dst.exists():
        os.symlink(src, dst)
        print(f'Linked {item}')

# Lier les .so aussi
import glob
for so in glob.glob(str(system_site / '_lgpio*.so')):
    dst = venv_site / os.path.basename(so)
    if not dst.exists():
        os.symlink(so, dst)
        print(f'Linked {os.path.basename(so)}')

for so in glob.glob(str(system_site / 'spidev*.so')):
    dst = venv_site / os.path.basename(so)
    if not dst.exists():
        os.symlink(so, dst)
        print(f'Linked {os.path.basename(so)}')
"

# installation des librairies pythons
 pip install -r requirements.txt  --prefer-binary --default-timeout=1000 

# installation de sqlite3
sudo apt-get install sqlite3 
flask db init
flask db upgrade

cat "[Unit]
Description=Controle du radiateur

[Service]
ExecStart=/home/pi/WebRadiator/webRadiator/bin/gunicorn -b 0.0.0.0:3000 -w 2 web_radiator:app
User=pi
WorkingDirectory=/home/pi/WebRadiator
Environment=\"PATH=/home/pi/WebRadiator/webRadiator/bin\"
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=10
PrivateTmp=true

[Install]
WantedBy=multi-user.target" >>  /etc/systemd/system/web_radiator.service" >>  /etc/systemd/system/web_radiator.service

#mise en place du service
sudo systemctl enable web_radiator
sudo systemctl start web_radiator.service
sudo systemctl status web_radiator
