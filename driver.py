#!/bin/bash
import os
import subprocess

#os.system("cd /home/pi/Desktop/restroom_management/")
#os.system("source /home/pi/Desktop/restroom_management/bin/activate")

subprocess.call(r"python /home/pi/Desktop/restroom_management/Atlas\ Database\ Initialiser.py", shell=True)
