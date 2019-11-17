'''
17 November 2019
Raspberry_pi side script to receive sensor data from nodeMCU.
The received data is then written into text files for processing by Atlas Database Initialiser.py
Strict care should be taken on the format of data received:
<Data_Tupe>=<Value>
eg:Temperature 23.34
People counter value is not being reset.
'''

import urllib.request
url = "http://192.168.43.246/"  # ESP's url, ex: https://192.168.102/ (Esp serial prints it when connected to wifi)

def get_data():
	n = urllib.request.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
	n = n.decode("utf-8") # convert raw html bytes format to string :3
	
	return n
#	data = n.split() #<optional> split datas we got. (if you programmed it to send more than one value) It splits them into seperate list elements.
#	data = list(map(int, data)) #<optional> turn datas to integers, now all list elements are integers.

# Example usage
while True:
	try:
		data=get_data()
		print("Your data(s) which we received from arduino: "+data)
		received_data=data.split()
		if (len(received_data)==0):
			continue
		elif received_data[0]=="Temperature":#Temp
			s=open(file_temperature, "a")
			s.write(str(received_data[1])+"\n")
			s.close()

		elif received_data[0]=="Humidity":#Humidity
			s=open(file_humidity, "a")
			s.write(str(received_data[1])+"\n")
			s.close()

		elif received_data[0]=="PplCnt" and int(received_data[1])==1:#Motion Detected	
			people_counter_value+=1
			s=open(file_peoplecounter, "a")
			s.write(str(people_counter_value//2)+"\n")
			s.close()

		elif received_data[0]=="AirQua":#Smell Sensor
			s=open(file_smellsensor, "a")
			s.write(str(received_data[1])+"\n")
			s.close()

	except Exception as e:
		print(e)
