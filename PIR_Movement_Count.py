from time import sleep
from random import uniform

"""PIR Movement Sensor Simulator
Returns count of number of people visiting the facility.
https://components101.com/sensors/hc-sr505-pir-sensor-pinout-datasheet
http://roboticadiy.com/arduino-tutorial-make-counter-using-pir-sensor-lcd-display/
28/02/2019"""

time=20 #periodicity of return value in seconds
file_name="VisitorCount.txt"

#s=open(file_name, "w")					#to be removed
#s.close()#truncating the file 			#to be removed

test_time=int(input("Enter minutes to run code:"))
randomvalue=0


for i in range((test_time*60)//time):
	s=open(file_name, "a")
	s.write(str(randomvalue)+"\n")
	s.close()
	randomvalue+=int(uniform(0,time//2)) #MAX Number of People function of variable time
	sleep(time)