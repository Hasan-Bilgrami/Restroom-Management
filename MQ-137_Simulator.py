from time import sleep
from random import uniform

"""MQ-137 SENSOR Simulator
Returns ppm value of ammonia in the atmosphere.
https://components101.com/sensors/mq137-gas-sensor
https://circuitdigest.com/microcontroller-projects/arduino-mq137-ammonia-sensor
28/02/2019"""

time=20 #periodicity of return value in seconds
file_name="ammonia.txt"

#s=open(file_name, "w")					#to be removed
#s.close()#truncating the file 			#to be removed

test_time=int(input("Enter minutes to run code:"))
randomvalue=0


for i in range((test_time*60)//time):
	s=open(file_name, "a")
	s.write(str(randomvalue)+"\n")
	s.close()
	randomvalue+=uniform(0,0.05)
	sleep(time)