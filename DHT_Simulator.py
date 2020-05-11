from time import sleep
from random import uniform
from sys import argv
from os import getpid

'''Digital Humidty and Temperature Simulator Simulator
Simulates temperature and Humidity
11 May 2020
'''

print("DHT "+str(getpid()))
time=20 #periodicity of return value in seconds
file_temperature="Temperature.txt"
file_humidity="Humidity.txt"

test_time=int(argv[1])		#int(input("Enter minutes to run code:"))

temp_value=37.0
humidity_value=54.0

for i in range((test_time*60)//time):
	s=open(file_temperature, "a")
	s.write(str(temp_value)[:4]+"\n")#Precision:0.1
	s.close()
	temp_value=max(min(40,temp_value+uniform(-0.1,0.1)),30)	#Temperature between 30 and 40

	s=open(file_humidity, "a")
	s.write(str(humidity_value)[:2]+"\n")#Precision:1
	s.close()
	humidity_value=max(min(60,humidity_value+uniform(-0.1,0.1)),50) #Humidity between 50 and 60

	sleep(time)