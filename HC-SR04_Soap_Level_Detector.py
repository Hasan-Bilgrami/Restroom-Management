from time import sleep
from random import uniform, choice
from sys import argv
from os import getpid

"""HC-SR04 Ultrasonic Sensor Simulator
Returns heights of soap solution
https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/
28/02/2019"""

print("Soap "+str(getpid()))
time=20 #periodicity of return value in seconds
file_name="SoapUsage.txt"
permanent_file_name="permanenr_Soapusage.txt"
cleaner_file_name='cleaner.txt'

#s=open(file_name, "w")						#to be removed
#s.close()#truncating the file  				#to be removed

#for running individually

test_time=int(argv[1])		#int(input("Enter minutes to run code:"))
initial_soap_level=20#float(input("Enter initial height of soap(in cm):"))


for i in range((test_time*60)//time):
	try:
		f=open(cleaner_file_name, 'r')
		i=int(f.readline())					#soap is bit &:*&***
		f.close()
		f=open(cleaner_file_name, 'w')
		f.write(str(i)[0]+'0'+str(i)[2:])
		f.close()
		if (i%10000)/1000>=1:
			initial_soap_level=20
	except Exception as e:
		pass

	s=open(file_name, "a")
	s.write(str(max(initial_soap_level,0))[:4]+"\n")
	s.close()
	f=open(permanent_file_name,'a')
	f.write(str(max(initial_soap_level,0))[:4]+"\n")
	f.close()
	initial_soap_level-=(choice([0,1]))*uniform(0.3,max(time//10,2)//1.5) #soap used is a function of variable time
	sleep(time)