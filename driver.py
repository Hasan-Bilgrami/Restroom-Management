#!/bin/bash
import time
import subprocess

time.sleep(30)
subprocess.call(r"python /home/pi/Desktop/restroom_management/nodeMCU_pi_interfacing_dht.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
subprocess.call(r"python /home/pi/Desktop/restroom_management/nodeMCU_pi_interfacing_pir.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
time.sleep(10)
subprocess.call(r"python /home/pi/Desktop/restroom_management/Atlas\ Database\ Initialiser.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
time.sleep(60)

while True:
	subprocess.call(r"python /home/pi/Desktop/restroom_management/restroom_management_algo.py &>/home/pi/Desktop/restroom_management/boot_output.txt ", shell=True)
	time.sleep(2*60)
