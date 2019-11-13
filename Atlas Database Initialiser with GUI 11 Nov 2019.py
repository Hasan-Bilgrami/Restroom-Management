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
min_smell_difference=0.3 #in ppm
min_people_difference=20
min_soaplevel_difference=0.5 #in cm
max_len_of_document_buffer_list=5
max_time_of_holding_buffer=10 #minutes




def select(s): #Command from Select Restroom Button
	global Collection_Name
	Collection_Name=s
	for j in button_list:
		j.destroy()
	window.destroy()

def submit_command():
	global test_time
	test_time=int(test_time_input.get()) #May enter characters, then will cause error
	window.destroy()

window=tkinter.Tk()  #Collection Selector
window_width=800
window_height=600
window.geometry(str(window_width)+"x"+str(window_height)+"+300+75") #width x height
window.resizable(width=False, height=False)
window.config(bg="#ffd700")

myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
db = myclient.test

mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

caption = tkinter.Button(window, text="Restroom Name:", relief="flat", state="disabled", bg="#ffd700", width=50)
caption.grid(row=0,pady=10,padx=200)
row=1 #preceding rows occupied by caption
#defaultbg = window.cget('bg')
button_list=[caption]

for document in mycollection.find({},{"_id":0, "Number":0, "Cleaner_Required":0}):
	button_list.append(tkinter.Button(window,
									  text=document["Name"]+", "+document["Location"],
									  bg="#7fff00",
									  width=50,
									  command=lambda s=document["Name"]:select(s)
									  )
					   )
	#button_list[-1].pack()
	button_list[-1].grid(row=row,pady=5)
	row+=1

window.protocol("WM_DELETE_WINDOW", lambda :exit(1001))
window.mainloop()


Database_Name="Restroom_SensorData"
mydb = myclient[Database_Name]
mycollection = mydb[Collection_Name]

print("Collection Name Selected:"+Collection_Name)

window=tkinter.Tk() #Time Input
window_width=400
window_height=300
window.geometry(str(window_width)+"x"+str(window_height)+"+450+115") #width x height
window.resizable(width=False, height=False)
window.config(bg="#ffd700")

caption = tkinter.Button(window, text="Enter time to Run:", relief="flat", state="disabled", bg="#ffd700", width=50)
caption.grid(row=0,pady=10,padx=25)
test_time_input=tkinter.Entry(window)
submit=tkinter.Button(window,
              text="Submit",
              bg="#7fff00",
              #width=25,
              command=submit_command
              )

test_time_input.grid()
submit.grid(pady=10)

window.protocol("WM_DELETE_WINDOW", lambda :exit(1002))
window.mainloop()

#test_time=int(input("Enter minutes to run code:"))
print("Minutes to run code:"+str(test_time))

t0=time.perf_counter()
list_documents=[]
last_uploaded=time.perf_counter()
while (time.perf_counter()-t0)/60<test_time:
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

	if abs(float(smell[-1][:-1])-float(smell[0][:-1]))<min_smell_difference and abs(int(people[-1][:-1])-int(people[0][:-1]))<min_people_difference and abs(float(soap[-1][:-1])-float(soap[0][:-1]))<min_soaplevel_difference:
		s1.close()
		s2.close()
		s3.close()
		continue



	#truncate the files and add only latest value for future comparison
	s1 = open(file_smellsensor, "w")
	s1.write(str(smell[-1][:-1])+"\n")
	s1.close()
	s2 = open(file_peoplecounter, "w")
	s2.write(str(people[-1][:-1]) + "\n")
	s2.close()
	s3 = open(file_soaplevel, "w")
	s3.write(str(soap[-1][:-1]) + "\n")
	s3.close()

	localtime = str(datetime.datetime.now())


	"""Fields of database: 		Time 	 SmellSensor 	 PeopleCounter 		SoapLevel
	"""
	mydict = {'Time':localtime, 'Smell_Sensor':float(smell[-1][:-1]), 'People_Counter':int(people[-1][:-1]), 'Soap_Level':float(soap[-1][:-1])}#slicing for excluding trailing \n
	list_documents.append(mydict)
	if len(list_documents)>max_len_of_document_buffer_list or (time.perf_counter()-last_uploaded)/60>max_time_of_holding_buffer:
		mycollection.insert_many(list_documents)
		#for x in list_documents:
		#	mycollection.insert_one(x)
		list_documents=[]
		last_uploaded=time.perf_counter()
mycollection.insert_many(list_documents)
#for x in list_documents:
#	mycollection.insert_one(x)

for document in mycollection.find():
	print(document)
