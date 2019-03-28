"""Database Creator and Initialiser
11 March 2019
Creates a Database for information on every restroom,
Takes input as last value from text files created by other sensors, and then truncates those files.
Text files should be truncated often for optimality
https://www.w3schools.com/python/python_mongodb_getstarted.asp
"""
import pymongo
import time

Collection_Name="MNNIT"
file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"

myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
db = myclient.test


mydb = myclient["Restroom_Management"]
mycollection = mydb[Collection_Name]

test_time=int(input("Enter minutes to run code:"))

t0=time.clock()
while (time.clock()-t0)/60<test_time:
	s1=open(file_smellsensor,"r")
	s2=open(file_peoplecounter,"r")
	s3=open(file_soaplevel, "r")

	#latest values
	smell=s1.readlines()
	people=s2.readlines()
	soap=s3.readlines()

	if not smell or not people or not soap:  # empty files
		print("Empty file Discovered. Retrying!")
		s1.close()
		s2.close()
		s3.close()
		continue

	s1.close()
	s2.close()
	s3.close()

	#truncate the files
	s1 = open(file_smellsensor, "w")
	s2 = open(file_peoplecounter, "w")
	s3 = open(file_soaplevel, "w")
	s1.close()
	s2.close()
	s3.close()

	localtime = time.asctime( time.localtime(time.time()) ) #timestamp


	"""Fields of database: 		Time 	 SmellSensor 	 PeopleCounter 		SoapLevel
	"""
	mydict = {'Time':localtime, 'Smell_Sensor':smell[-1][:-1], 'People_Counter':people[-1][:-1], 'Soap_Level':soap[-1][:-1]}#slicing for excluding trailing \n

	x = mycollection.insert_one(mydict)
for document in mycollection.find():
	print(document)
