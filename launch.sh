# !! hard coded path - to be modified according environment !!
# allow to launch from crontab using  @reboot sleep 60 && bash  /home/pi/WebRadiator/launch.sh
# may also be used from terminal to launch  the application
cd /home/pi/WebRadiator
source .venv/webRadiator/bin/activate
export RADIATOR_TEST_ENVIRONMENT="false";flask run --host=0.0.0.0 -p 3000
