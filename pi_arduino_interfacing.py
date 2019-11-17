'''
12 November 2019
Pi unit takes input from arduino and writes data into corresponding text file.
Strict care should be taken on the format of data received:
<Data_Tupe>=<Value>
eg:Temperature 23.34
People counter value is not being reset.
'''

import serial


file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"
file_temperature="Temperature.txt"
file_humidity="Humidity.txt"

people_counter_value=0


ser = serial.Serial('/dev/ttyUSB0', 9600)
while 1:
	try: 
		if(ser.in_waiting >0):
			line = ser.readline().decode("utf-8",errors="replace")
			print(line)
			arduino_data=line.split()
			if len(arduino_data) == 0:
				continue
			elif arduino_data[0]=="Temperature":#Temp
				s=open(file_temperature, "a")
				s.write(str(arduino_data[1])+"\n")
				s.close()

			elif arduino_data[0]=="Humidity":#Humidity
				s=open(file_humidity, "a")
				s.write(str(arduino_data[1])+"\n")
				s.close()

			elif arduino_data[0]=="PplCnt" and int(arduino_data[1])==1:#Motion Detected	
				people_counter_value+=1
				s=open(file_peoplecounter, "a")
				s.write(str(people_counter_value//2)+"\n")
				s.close()

			elif arduino_data[0]=="AirQua":#Smell Sensor
				s=open(file_smellsensor, "a")
				s.write(str(arduino_data[1])+"\n")
				s.close()
	except:
		pass
