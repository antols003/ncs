#!/usr/bin/python3
from subprocess import Popen
import sys

filename="/home/pi/tkndspunit/blemain.py"
while True:
    print("\nStarting " + filename)
    p = Popen("sudo python3 " + filename, shell=True)
    p.wait()
