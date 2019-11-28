#!/bin/bash
import time
import subprocess

print("Starting Driver")
time.sleep(60)
print("driver.py:Starting nodeMCU_pi_interfacing of sensors.")
subprocess.call(r"python /home/pi/Desktop/restroom_management/nodeMCU_pi_interfacing_dht.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
subprocess.call(r"python /home/pi/Desktop/restroom_management/nodeMCU_pi_interfacing_pir.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
time.sleep(10)
print("driver.py:Starting Atlas Database Initialiser.")
subprocess.call(r"python /home/pi/Desktop/restroom_management/Atlas\ Database\ Initialiser.py &>/home/pi/Desktop/restroom_management/boot_output.txt &", shell=True)
time.sleep(60)
print("driver.py:Starting restroom_management_algorithm.")
while True:
	subprocess.call(r"python /home/pi/Desktop/restroom_management/restroom_management_algo.py &>/home/pi/Desktop/restroom_management/boot_output.txt ", shell=True)
	time.sleep(2*60)
