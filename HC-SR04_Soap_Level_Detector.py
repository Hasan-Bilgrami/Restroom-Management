from time import sleep
from random import uniform, choice
import sys

"""HC-SR04 Ultrasonic Sensor Simulator
Returns heights of soap solution
https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/
28/02/2019"""

time=20 #periodicity of return value in seconds
file_name="SoapUsage.txt"

#s=open(file_name, "w")						#to be removed
#s.close()#truncating the file  				#to be removed

#for running individually

test_time=int(input("Enter minutes to run code:"))
initial_soap_level=float(input("Enter initial height of soap(in cm):"))

#for running through command line
'''
test_time=int(sys.argv[1])
initial_soap_level=float(sys.argv[2])
'''
print(test_time)

for i in range((test_time*60)//time):
	s=open(file_name, "a")
	s.write(str(max(initial_soap_level,0))+"\n")
	s.close()
	initial_soap_level-=(choice([0,1]))*uniform(0.3,max(time//10,2)//1.5) #soap used is a function of variable time
	sleep(time)