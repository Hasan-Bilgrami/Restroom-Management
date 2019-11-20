'''
17 November 2019
Raspberry_pi side script to receive sensor data from nodeMCU.
The received data is then written into text files for processing by Atlas Database Initialiser.py
Strict care should be taken on the format of data received:
<Data_Tupe>=<Value>
eg:Temperature 23.34
People counter value is not being reset.
'''
import urllib.request as req

file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"
file_temperature="Temperature.txt"
file_humidity="Humidity.txt"
people_counter_value=0
url = "http://192.168.43.12/"  # ESP's url, ex: https://192.168.102/ (Esp serial prints it when connected to wifi)


def get_data():
	#proxy = req.ProxyHandler({'http': r'http://edcguest:edcguest@172.31.100.27:3128'})
	#auth = req.HTTPBasicAuthHandler()
	#opener = req.build_opener(proxy, auth, req.HTTPHandler)
	#req.install_opener(opener)
	n = req.urlopen(url).read() # get the raw html data in bytes (sends request and warn our esp8266)
	n = n.decode("utf-8") # convert raw html bytes format to string :3
	return n	
	
# Example usage
while True:
	try:
		data=get_data()
		print("Your data(s) which we received from arduino: "+data)

		received_data=data.split()
		
		if (len(received_data)==0):
			continue

		for i in range(len(received_data)):
			if received_data[i]=="Temperature":#Temp
				s=open(file_temperature, "a")
				s.write(str(received_data[i+1])+"\n")
				s.close()

			elif received_data[i]=="Humidity":#Humidity
				s=open(file_humidity, "a")
				s.write(str(received_data[i+1])+"\n")
				s.close()

			elif received_data[i]=="PplCnt" and int(received_data[i+1])==1:#Motion Detected   
				people_counter_value+=1
				s=open(file_peoplecounter, "a")
				s.write(str(people_counter_value//2)+"\n")
				s.close()

			elif received_data[i]=="AirQua":#Smell Sensor
				s=open(file_smellsensor, "a")
				s.write(str(received_data[i+1])+"\n")
				s.close()

	except Exception as e:
		print("Exception:"+str(e))
