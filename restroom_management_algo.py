#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys
import pandas as pd
import sklearn
import pymongo
import datetime
import statistics
from sklearn import preprocessing

Collection_Name="Computer Center"
myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
mydb = myclient["Restroom_SensorData"]
mycollection = mydb[Collection_Name]
print(myclient.list_database_names())

def updation():
    Collection = "restrooms"
    mydb = myclient["Restroom_Management"]
    mycollection1 = mydb[Collection]
    myquery={ "Name": Collection_Name}
    newvalues={ "$set": { "Cleaner_Required": True}}
    mycollection1.update_many(myquery,newvalues)
    decision=False

#checking ammonia treshold
#read ammonia sensor data

document=mycollection.find_one(sort=[("Smell_Sensor",-1)])
max_ammonia=document['Smell_Sensor']

#preset treshold for ammonia

ammonia_treshold=20

#check if max value is greater than treshhold or not

max_ammonia=float(max_ammonia)
decision=False #by default

#alert for ammonia treshold is stored in string alert_ammonia

if(max_ammonia >= ammonia_treshold):
    alert_ammonia='Treshold level of ammonia is crossed and current level is '+str(max_ammonia)
    print(alert_ammonia)
    decision=True
    updation()

#checkng counter treshold
#read counter sensor data

document=mycollection.find_one(sort=[("People_Counter",-1)])
max_count=document['People_Counter']

#preset treshold for counter
counter_treshold=200

#check if max value is greater than treshhold or not
max_count=int(max_count)
#alert for counter treshold is stored in string alert_count
if(max_count >= counter_treshold):
    alert_count='Treshold level of ammonia is crossed and current level is '+str(max_count)
    print(alert_count)
    decision=True
    updation()

#read soap level detector data

document=mycollection.find_one(sort=[("Soap_Level",1)])
min_level=document['Soap_Level']

#preset treshold for soap level
soap_treshold=2


#check if min value is less than treshhold or not
min_level=float(min_level)

#alert for soap treshold is stored in string alert_soap
if(min_level <= soap_treshold):
    alert_soap='Treshold level of soap is crossed and current level is '+str(min_level)
    print(alert_soap)
    decision=True
    updation()

#DATASET OF TOILETS PRESENT PREHANDEDLY

train=pd.read_csv('toilet_dataset.csv')
from sklearn.utils import shuffle
train = shuffle(train)
train.describe()


col=['in ppm', 'persons', 'in cm']
target='output'

from sklearn.model_selection import train_test_split

#training set
train_set=train.sample(frac=1,random_state=1)

#test set
d=mycollection.find_one(sort=[("Time",-1)])
print(d)
al=[]
al=[d['Smell_Sensor'],d['People_Counter'],d['Soap_Level']]
a=pd.DataFrame(columns=['in ppm', 'persons', 'in cm'],data=[al])
print(a)
test_set=a
#IMPORT SVM MODEL

from sklearn import svm

#Create a svm Classifier

clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets

clf.fit(train_set[col],train_set[target])

#Predict the response for test dataset

predictions = clf.predict(test_set[col])

#test_set predictions
new_list = []
for item in predictions:
    new_list.append(item)

if predictions==1: #1 means cleaning reqquired
    print("Cleaner Required")
    updation()
else:
    print("Cleaner not required")
a['output']=predictions
a.to_csv('toilet_dataset.csv',mode='a',header=False,index=False)

#FEEDBACK_PORTION

def comparison(time):
    time=datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    Collection_Name = "MNNIT"
    # db = myclient.test
    mydb = myclient["Restroom_SensorData"]
    mycollection = mydb[Collection_Name]
    flag=False
    upper_limit=time
    lower_limit=time
    mydoc=mycollection.find_one({"Time":time})
    flag=1
    while not mydoc:
        flag+=1
        upper_limit=upper_limit+datetime.timedelta(minutes=1)
        lower_limit=lower_limit-datetime.timedelta(minutes=1)
        myquery={"Time":{"$gt":str(lower_limit),"$lt":str(upper_limit)}}
        mydoc=mycollection.find_one(myquery)
        if flag==30:
            print("No relevant sensor value found")
            return None
    return mydoc


mydb=myclient['Restroom_Management']
Collection_Name1="user_feedback"
mycollection2 = mydb[Collection_Name1]
feedbacks=[]
temp=[]
for document in mycollection2.find():
    current_document = comparison(document['Time'])  # returns appropriate document
    if current_document==None:
        continue
    temp=[document['Odour_level'],document['Cleanliness_level'],document['Is_soap'],document['Is_water'],document['Overall_rating'],document['Time'],current_document['Smell_Sensor'],current_document['People_Counter'],current_document['Soap_Level']]
    feedbacks.append(temp)
print(feedbacks)
#updating treshold value of ammonia

df=pd.DataFrame(columns=["Odour", "Cleanliness", "Soap Availability","Water availability","Overall Rating","Time","ammonia(in PPM)","People Count","Soap Level",""],data=feedbacks)
print(df)
ammonia=df['ammonia(in PPM)']
people=df['People Count']
soap=df['Soap Level']
userodour=df['Odour']
userclean=df['Cleanliness']
usersoap=df['Soap Availability']
userwater=df['Water availability']
useroverall=df['Overall Rating']
weight=[]
for i in range(len(ammonia)):
    if ammonia[i] >= 20:
        weight.append(1)
    else:
        ammo_prop=ammonia[i]/5+1
        user_feedback=userodour[i]
        ammo_prop=6-ammo_prop     #to calculate deviation
        dev=abs(ammo_prop-user_feedback)  #deviation
        weight.append(1-(1/4)*dev)
df['weight']=weight
feedback_with_weight=[]
#total_weight=sum(weight)
#mean_weight=total_weight/len(ammonia)

literacy_rate=0.7    #In Fractions
for i in range(len(ammonia)):
    feedback_with_weight.append(userodour[i]*weight[i]*literacy_rate)
minimum=min(feedback_with_weight)
maximum=max(feedback_with_weight)
range=maximum-minimum
mean_feedback=statistics.mean(feedback_with_weight)

for i in range(len(ammonia)):
    x=abs(feedback_with_weight[i]-mean_feedback)/range
    if(feedback_with_weight[i]<mean_feedback):
        normalized_weight=0.5-x
    else:
        normalized_weight=0.5+x

total_weight=sum(normalized_weight)
new_feedback=sum(normalized_weight)/total_weight
new_feedback=new_feedback*5

print("The mapped odour feedback is\n")
print(new_feedback)

curr_treshold=ammonia_treshold/5
#updating treshold
new_treshold=3-new_feedback
ammonia_treshold=curr_treshold+new_treshold/2
ammonia_treshold=ammonia_treshold*5
print("The updated Ammonia threshold is\n")
print(ammonia_treshold)

weight=[]
for i in range(len(people)):
    if people[i] >= 200:
        weight.append(1)
    else:
        ammo=people[i]/40+1
        user_feedback=userclean[i].
        ammo=6-ammo     #to calculate deviation
        dev=abs(ammo-user_feedback)  #deviation
        weight.append(1-(1/4)*dev)
df['weight']=weight
feedback_with_weight=[]
for i in range(len(people)):
    feedback_with_weight.append(userclean[i]*weight[i])
total_weight=sum(weight)
new_feedback=sum(feedback_with_weight)/total_weight
print("the mapped cleanliness feedback is")
print(new_feedback)
curr_treshold=2
#updating treshold
new_treshold=3-new_feedback
counter_treshold=curr_treshold+new_treshold/2
counter_treshold=counter_treshold*40
print("the updated people counter threshold is")
print(counter_treshold)






