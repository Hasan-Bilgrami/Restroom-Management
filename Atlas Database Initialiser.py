"""Database Creator and Initialiser
Python 3.6 and Above
11 March 2019
Creates a Database for information on every restroom,
Takes input as last value from text files created by other sensors, and then truncates those files.
Input is taken only when significant difference exists between initial(1st) value and current(last)value.
Text files should be truncated often for optimality
https://www.w3schools.com/python/python_mongodb_getstarted.asp
"""
import pymongo
import time
import tkinter
import datetime



Database_Name="Restroom_Management"
Collection_Name="restrooms" #for list of restrooms
file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"
file_temperature="Temperature.txt"
file_humidity="Humidity.txt"
min_smell_difference=0.3 #in ppm
min_people_difference=20
min_soaplevel_difference=0.5 #in cm
min_temperature_difference=2
min_humidity_difference=2
max_len_of_document_buffer_list=5
max_time_of_holding_buffer=10 #minutes



myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
db = myclient.test

mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

print("Enter Restroom Number from among the following:")
restroom_serial_number=1;
restroom_serial_hash={}
for document in mycollection.find({},{"_id":0, "Number":0, "Cleaner_Required":0}):
	print(str(restroom_serial_number)+")"+document["Name"]+", "+document["Location"])
	restroom_serial_hash[restroom_serial_number]=document["Name"]
	restroom_serial_number+=1
Collection_Name=restroom_serial_hash[int(input("Input:"))]

test_time=int(input("Enter time to run:")) #May enter characters, then will cause error


Database_Name="Restroom_SensorData"
mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

print("Collection Name Selected:"+Collection_Name)

#test_time=int(input("Enter minutes to run code:"))
print("Minutes to run code:"+str(test_time))

t0=time.perf_counter()
list_documents=[]
last_uploaded=time.perf_counter()
while (time.perf_counter()-t0)/60<test_time:
	s1=open(file_smellsensor,"r")
	s2=open(file_peoplecounter,"r")
	s3=open(file_soaplevel, "r")
	s4=open(file_temperature, "r")
	s5=open(file_humidity, "r")

	#latest values
	smell=s1.readlines()
	people=s2.readlines()
	soap=s3.readlines()
	temperature=s4.readlines()
	humidity=s5.readlines()

	s1.close()
	s2.close()
	s3.close()
	s4.close()
	s5.close()

	if not smell and not people and not soap and not temperature and not humidity:  # empty files
		print("Empty file Discovered. Retrying!")
		continue

	if abs(float(smell[-1][:-1])-float(smell[0][:-1]))<min_smell_difference and \
		abs(int(people[-1][:-1])-int(people[0][:-1]))<min_people_difference and \
		abs(float(soap[-1][:-1])-float(soap[0][:-1]))<min_soaplevel_difference and \
		abs(float(temperature[-1][:-1])-float(temperature[0][:-1]))<min_temperature_difference and \
		abs(float(humidity[-1][:-1])-float(humidity[0][:-1]))<min_humidity_difference:#slicing for excluding trailing \n
		continue



	#truncate the files and add only latest value for future comparison
	if smell:# smell value will be false if file was empty
		s1 = open(file_smellsensor, "w")
		s1.write(str(smell[-1][:-1])+"\n")
		s1.close()
	if people:
		s2 = open(file_peoplecounter, "w")
		s2.write(str(people[-1][:-1]) + "\n")
		s2.close()
	if soap:
		s3 = open(file_soaplevel, "w")
		s3.write(str(soap[-1][:-1]) + "\n")
		s3.close()
	if temperature:
		s4=open(file_temperature,"w")
		s4.write(str(temperature[-1][:-1])+"\n")
		s4.close()
	if humidity:
		s5=open(file_humidity,"w")
		s5.write(str(humidity[-1][:-1])+"\n")
		s5.close()

	localtime = str(datetime.datetime.now())


	"""Fields of database: 		Time 	 Smell_Sensor 	 People_Counter 	Soap_Level 	Temperature 	Humidity
	"""
	mydict = {'Time':localtime}
	if smell:	
		mydict['Smell_Sensor']=float(smell[-1][:-1])
	if people:	
		mydict['People_Counter']=int(people[-1][:-1])
	if soap:	
		mydict['Soap_Level']=float(soap[-1][:-1])
	if temperature:	
		mydict['Temperature']=float(temperature[-1][:-1])
	if humidity:	
		mydict['Humidity']=float(humidity[-1][:-1])
	list_documents.append(mydict)
	
	if len(list_documents)>max_len_of_document_buffer_list or (time.perf_counter()-last_uploaded)/60>max_time_of_holding_buffer:
		mycollection.insert_many(list_documents)
		#for x in list_documents:
		#	mycollection.insert_one(x)
		list_documents=[]
		last_uploaded=time.perf_counter()
if len(list_documents)>0:	
	mycollection.insert_many(list_documents)
#for x in list_documents:
#	mycollection.insert_one(x)

for document in mycollection.find():
	print(document)
