from time import sleep
from random import uniform
from sys import argv
from os import getpid

"""PIR Movement Sensor Simulator
Returns count of number of people visiting the facility.
https://components101.com/sensors/hc-sr505-pir-sensor-pinout-datasheet
http://roboticadiy.com/arduino-tutorial-make-counter-using-pir-sensor-lcd-display/
28/02/2019"""

print("People Count "+str(getpid()))
time=20 #periodicity of return value in seconds
file_name="VisitorCount.txt"
permanent_file_name="permanent_VisitorCount.txt"
cleaner_file_name='cleaner.txt'


#s=open(file_name, "w")					#to be removed
#s.close()#truncating the file 			#to be removed

test_time=int(argv[1])		#int(input("Enter minutes to run code:"))
randomvalue=0


for i in range((test_time*60)//time):
	try:
		f=open(cleaner_file_name, 'r')
		i=int(f.readline())					#people is bit &:**&**
		f.close()
		f=open(cleaner_file_name, 'w')
		f.write(str(i)[:2]+'0'+str(i)[3:])
		f.close()
		if (i%1000)/100>=1:
			randomvalue=0
	except Exception as e:
		pass

	s=open(file_name, "a")
	s.write(str(randomvalue)+"\n")
	s.close()
	f=open(permanent_file_name,'a')
	f.write(str(randomvalue)+"\n")
	f.close()
	randomvalue+=int(uniform(0,time//2)) #MAX Number of People function of variable time
	sleep(time)