from time import sleep
from random import uniform
from sys import argv
from os import getpid

"""MQ-137 SENSOR Simulator
Returns ppm value of ammonia in the atmosphere.
https://components101.com/sensors/mq137-gas-sensor
https://circuitdigest.com/microcontroller-projects/arduino-mq137-ammonia-sensor
28/02/2019"""

print("MQ-137 "+str(getpid()))

time=20 #periodicity of return value in seconds
file_name="ammonia.txt"
cleaner_file_name='cleaner.txt'
cleaner_min_val=-0.1

#s=open(file_name, "w")					#to be removed
#s.close()#truncating the file 			#to be removed

test_time=int(argv[1])		#int(input("Enter minutes to run code:"))
randomvalue=0


for i in range((test_time*60)//time):
	try:
		f=open(cleaner_file_name, 'r')
		i=int(f.readline())					#msb is odour
		f.close()
		f=open(cleaner_file_name, 'w')
		f.write('0'+str(i)[1:])
		f.close()
		if i/10000>=1:
			randomvalue*=-1
	except Exception as e:
		pass

	s=open(file_name, "a")
	s.write(str(abs(randomvalue))[:5]+"\n")
	s.close()
	if randomvalue<cleaner_min_val:
		randomvalue=randomvalue - (randomvalue/10)+uniform(0,0.05)
	else:	
		randomvalue=(abs(randomvalue)+uniform(0,0.05))
	sleep(time)