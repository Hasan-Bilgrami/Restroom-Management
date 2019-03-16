"""Database Creator and Initialiser
11 March 2019
Creates a Database for information on every restroom,
Takes input as last value from text files created by other sensors, and then truncates those files.
Text files should be truncated often for optimality
"""
import pymongo
import time
import os
Collection_Name="Restroom_1"
file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
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




	localtime = time.asctime( time.localtime(time.time()) ) #timestamp


	"""Fields of database: 		Time 	 SmellSensor 	 PeopleCounter 		SoapLevel
	"""
	mydict = {'Time':localtime, 'Smell_Sensor':smell[-1], 'People_Counter':people[-1], 'Soap_Level':soap[-1]}

	x = mycollection.insert_one(mydict)
for document in mycollection.find():
	print(document)