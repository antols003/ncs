# !/usr/bin/python3
from subprocess import Popen
import sys
import datetime

# def clearMQTT():
# 	p = Popen("sudo service mosquitto stop", shell=True)
# 	p.wait()
# 	p = Popen("sudo rm /var/lib/mosquitto/mosquitto.db", shell=True)
# 	p.wait()
# 	p = Popen("sudo service mosquitto start", shell=True)
# 	p.wait()

# clearMQTT()

# f=open("/home/pi/ncs/web/BootTime.txt","w")
# f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# f.close()


# filename="/home/pi/ncs/web/main.py"
# while True:
#     print("\nStarting " + filename)
#     p = Popen("sudo python3 " + filename, shell=True)
#     p.wait()
