"""Database Creator and Initialiser
Python 3.6 and Above
11 March 2019
Creates a Database for information on every restroom,
Takes input as last value from text files created by other sensors, and then truncates those files, and writes the latest value in the first line for future comparison.
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
min_smell_difference=5 #in ppm
min_people_difference=20
min_soaplevel_difference=0.00001 #in cm
min_temperature_difference=2
min_humidity_difference=3
max_len_of_document_buffer_list=5
max_time_of_holding_buffer=1 #minutes


s1=open(file_smellsensor,"a")
s1.close()
s2=open(file_peoplecounter,"a")
s2.close()
s3=open(file_soaplevel, "a")
s3.close()
s4=open(file_temperature, "a")
s4.close()
s5=open(file_humidity, "a")
s5.close()


myclient = pymongo.MongoClient("172.31.132.10")
db = myclient.test

mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]


'''
#Used for selecting separate collections
print("Enter Restroom Number from among the following:")
restroom_serial_number=1;
restroom_serial_hash={}
for document in mycollection.find({},{"_id":0, "Number":0, "Cleaner_Required":0}):
	print(str(restroom_serial_number)+")"+document["Name"]+", "+document["Location"])
	restroom_serial_hash[restroom_serial_number]=document["Name"]
	restroom_serial_number+=1
Collection_Name=restroom_serial_hash[int(input("Input:"))]

test_time=int(input("Enter time to run:")) #May enter characters, then will cause error
'''

Collection_Name='Computer Center'
test_time=-1 #Run for infinite time

Database_Name="Restroom_SensorData"
mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

print("Atlas Database Initialiser:Collection Name Selected:"+Collection_Name)

#test_time=int(input("Enter minutes to run code:"))
print("Atlas Database Initialiser:Minutes to run code:"+str(test_time))

t0=time.time()
list_documents=[]
last_uploaded=time.time()
while True if test_time==-1 else (time.time()-t0)/60<test_time:
	s1=open(file_smellsensor,"r")
	smell=s1.readlines()
	s1.close()
	while smell and any(x not in '0123456789.' for x in smell[-1][:-1]):
		smell=smell[:-1]


	s2=open(file_peoplecounter,"r")
	people=s2.readlines()
	s2.close()
	while people and any(x not in '0123456789.' for x in people[-1][:-1]):
                people=people[:-1]

	s3=open(file_soaplevel, "r")
	soap=s3.readlines()
	s3.close()
	while soap and any(x not in '0123456789.' for x in soap[-1][:-1]):
                soap=soap[:-1]

	s4=open(file_temperature, "r")
	temperature=s4.readlines()
	s4.close()
	while temperature and any(x not in '0123456789.' for x in temperature[-1][:-1]):
                temperature=temperature[:-1]

	s5=open(file_humidity, "r")
	humidity=s5.readlines()
	s5.close()
	while humidity and any(x not in '0123456789.' for x in humidity[-1][:-1]):
                humidity=humidity[:-1]


	if ((time.time()-last_uploaded) >= max_time_of_holding_buffer*60 or len(list_documents)>max_len_of_document_buffer_list) and len(list_documents)>0:
                mycollection.insert_many(list_documents)
                print("Atlas Database Initialiser:Documents Uploaded:")
                print(list_documents)
                list_documents=[]
                last_uploaded=time.time()


	#truncate the files and add only latest value for future comparison
	if smell:	# smell value will be false if file was empty
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

	if (not smell or abs(float(smell[-1][:-1])-float(smell[0][:-1]))<min_smell_difference) and\
	(not people or abs(int(people[-1][:-1])-int(people[0][:-1]))<min_people_difference) and\
	(not soap or abs(float(soap[-1][:-1])-float(soap[0][:-1]))<min_soaplevel_difference) and\
	(not temperature or abs(float(temperature[-1][:-1])-float(temperature[0][:-1]))<min_temperature_difference) and\
	(not humidity or abs(float(humidity[-1][:-1])-float(humidity[0][:-1]))<min_humidity_difference):        #slicing for excluding trailing \n
		continue


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
	print("Atlas Database Initialiser:Entry collected:"+str(mydict))


exit(0)
if len(list_documents)>0:
	mycollection.insert_many(list_documents)
#for x in list_documents:
#	mycollection.insert_one(x)

for document in mycollection.find():
	print(document)
