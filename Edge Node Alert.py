"""Edge Node Alert Script
Python 3.6 and Above
11 April 2019
Generates Alert if any Threshold has been violated
Takes input as last(latest) value from text files created by other sensors.
Text files should be truncated often for optimality
https://www.w3schools.com/python/python_mongodb_getstarted.asp
"""

import sys

Database_Name="Restroom_Management"
Collection_Name="restrooms"



threshold_smellsensor=float(sys.argv[1])
threshold_peoplecounter=int(sys.argv[2])
threshold_soaplevel=float(sys.argv[3])
file_smellsensor="ammonia.txt"
file_peoplecounter="VisitorCount.txt"
file_soaplevel="SoapUsage.txt"

s1=open(file_smellsensor,"r")
s2=open(file_peoplecounter,"r")
s3=open(file_soaplevel, "r")

#latest values
smell=s1.readlines()
people=s2.readlines()
soap=s3.readlines()

s1.close()
s2.close()
s3.close()

if (smell and float(smell[-1])>threshold_smellsensor) or (people and int(people[-1])>threshold_peoplecounter) or (soap and float(soap[-1])>threshold_soaplevel):
	print("Alert")

