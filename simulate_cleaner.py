'''Cleaner Activity Simulator
Allows user to select cleaner from collection Cleaning_Staff.cleaners, simulate cleaning and log time.
7 May 2020
'''

import pymongo
import datetime
from random import uniform

file_name='cleaner.txt' #bool:<odour><soap><people><dht><wetness>

def select_cleaner():	#Allows user to select cleaner, returns string
	Database_Name="Restroom_Management"
	Collection_Name="cleaners" #for list of cleaners

	myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
	db = myclient.test

	mydb = myclient[Database_Name]
	mycollection = mydb[Collection_Name]

	#Used for selecting separate collections, each representing a cleaner
	print("Enter Cleaner Number from among the following:")
	cleaner_serial_number=1;
	cleaner_serial_hash={}

	for document in mycollection.find({},{"_id":0,"Name":1}):
		print(str(cleaner_serial_number)+")"+document["Name"])
		cleaner_serial_hash[cleaner_serial_number]=document["Name"]
		cleaner_serial_number+=1
	try:
		Cleaner_Name=cleaner_serial_hash[int(input("Input:"))]
		return Cleaner_Name
	except Exception as e:
		print("Invalid Selection:"+str(e))
		return select_cleaner()


def select_restroom():	#Allows user to select restroom, returns string
	Database_Name="Restroom_Management"
	Collection_Name="restrooms" #for list of cleaners

	myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
	db = myclient.test

	mydb = myclient[Database_Name]
	mycollection = mydb[Collection_Name]

	#Used for selecting separate collections, each representing a restroom
	print("Enter Restroom Number from among the following:")
	restroom_serial_number=1;
	restroom_serial_hash={}

	for document in mycollection.find({},{"_id":0,"Name":1}):
		print(str(restroom_serial_number)+")"+document["Name"])
		restroom_serial_hash[restroom_serial_number]=document["Name"]
		restroom_serial_number+=1
	try:
		Restroom_Name=restroom_serial_hash[int(input("Input:"))]
		return Restroom_Name
	except Exception as e:
		print("Invalid Selection:"+str(e))
		return select_restroom()


Database_Name="Cleaning_Staff"
Collection_Name=select_cleaner()

myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
db = myclient.test

mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

restroom_name='Computer Center'		#select_restroom()

document={"Restroom":restroom_name,"Entry":str(datetime.datetime.now()),"Exit":str(datetime.datetime.now()+datetime.timedelta(seconds=int(uniform(300,600))))}
try:
	mycollection.insert_one(document)
	print("Document Uploaded:"+str(document))
	#informing the sensor simulators
	s=open(file_name, "w")
	s.write("11111")
	s.close()
except Exception as e:
	print("Document upload FAILED:"+str(e))

