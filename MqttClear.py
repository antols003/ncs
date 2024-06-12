from subprocess import Popen
import sys

p = Popen("sudo service mosquitto stop", shell=True)
p.wait()
p = Popen("sudo rm /var/lib/mosquitto/mosquitto.db", shell=True)
p.wait()
p = Popen("sudo service mosquitto start", shell=True)
p.wait()