from time import sleep
from random import uniform, choice

"""HC-SR04 Ultrasonic Sensor Simulator
Returns heights of soap solution
https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/
28/02/2019"""

time=20 #periodicity of return value in seconds
file_name="SoapUsage.txt"

#s=open(file_name, "w")						#to be removed
#s.close()#truncating the file  				#to be removed

test_time=int(input("Enter minutes to run code:"))
initial_soap_level=float(input("Enter initial height of soap(in cm):"))


for i in range((test_time*60)//time):
	s=open(file_name, "a")
	s.write(str(max(initial_soap_level,0))+"\n")
	s.close()
	initial_soap_level-=(choice([0,1]))*uniform(0,max(time//10,2)) #soap used is a function of variable time
	sleep(time)