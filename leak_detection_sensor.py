from time import sleep
from random import uniform
from sys import argv
from os import getpid

'''Leak Detection Sensor(REES52_5)
Simulates moisture presence and returns high or low.
https://www.thegeekpub.com/wiki/sensor-wiki-water-level-sensor-leak-detection/
11 May 2020
'''

print("Moisture "+str(getpid()))
time=20 #periodicity of return value in seconds
file_name="Moisture.txt"
cleaner_file_name='cleaner.txt'
permanent_file_name="permanent_Moisture.txt"
cleaner_min_val=-0.1

test_time=int(argv[1])		#int(input("Enter minutes to run code:"))
randomvalue=0


for i in range((test_time*60)//time):
	try:
		f=open(cleaner_file_name, 'r')
		i=int(f.readline())					#wetness is LSB
		f.close()
		f=open(cleaner_file_name, 'w')
		f.write(str(i)[:4]+'0')
		f.close()
		if (i%10)>=1:
			randomvalue=0
	except Exception as e:
		pass

	s=open(file_name, "a")
	s.write(str(randomvalue)+"\n")
	s.close()
	f=open(permanent_file_name,'a')
	f.write(str(randomvalue)+"\n")
	f.close()
	randomvalue=min(randomvalue+int(uniform(0,2)),150)
	sleep(time)
