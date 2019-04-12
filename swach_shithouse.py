#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import pandas as pd
import matplotlib
import sklearn
import pymongo
import datetime
from sklearn import preprocessing

Collection_Name="MNNIT"
myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
#db = myclient.test
mydb = myclient["Restroom_SensorData"]
mycollection = mydb[Collection_Name]
print(myclient.list_database_names())

def updation():
    Collection = "restrooms"
    mydb = myclient["Restroom_Management"]
    mycollection1 = mydb[Collection]
    myquery={ "Name": "MNNIT" }
    newvalues={ "$set": { "Cleaner_Required": True}}
    mycollection1.update_many(myquery,newvalues)
    decision=False

#checking ammonia treshold
#read ammonia sensor data

document=mycollection.find_one(sort=[("Smell_Sensor",-1)])
max_ammonia=document['Smell_Sensor']

#preset treshold for ammonia

ammonia_treshold=2

#check if max value is greater than treshhold or not

max_ammonia=float(max_ammonia)
decision=False #by default

#alert for ammonia treshold is stored in string alert_ammonia

if(max_ammonia >= ammonia_treshold):
    alert_ammonia='Treshold level of ammonia is crossed and current level is '+str(max_ammonia)
    decision=True
    updation()

#checkng counter treshold
#read counter sensor data

document=mycollection.find_one(sort=[("People_Counter",-1)])
max_count=document['People_Counter']

#preset treshold for counter
counter_treshold=100

#check if max value is greater than treshhold or not
max_count=int(max_count)
#alert for counter treshold is stored in string alert_count
if(max_count >= counter_treshold):
    alert_count='Treshold level of ammonia is crossed and current level is '+str(max_count)
    decision=True
    updation()

#read soap level detector data

document=mycollection.find_one(sort=[("Soap_Level",1)])
min_level=document['Soap_Level']

#preset treshold for soap level
soap_treshold=10


#check if min value is less than treshhold or not
min_level=float(min_level)

#alert for soap treshold is stored in string alert_soap
if(min_level <= soap_treshold):
    alert_soap='Treshold level of soap is crossed and current level is '+str(min_level)
    decision=True
    updation()

#DATASET OF TOILETS PRESENT PREHANDEDLY

train=pd.read_csv('toilet_dataset.csv')
print(train.shape)
print(train.columns)
from sklearn.utils import shuffle
train = shuffle(train)
train.describe()

#HEAT MAP
corrmat=train.corr()
fig=plt.figure(figsize=(12,9))
sns.heatmap(corrmat, annot=True, fmt="f")
#sns.heatmap(corrmat,vmax=.9,square=True)
plt.show()


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
print(train_set.shape)
print(test_set.shape)

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
    
print(predictions)
if predictions==1: #1 means cleaning reqquired
    updation()


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
    while not mydoc:
        upper_limit=upper_limit+datetime.timedelta(minutes=1)
        lower_limit=lower_limit-datetime.timedelta(minutes=1)
        myquery={"Time":{"$gt":lower_limit,"$lt":upper_limit}}
        mydoc=mycollection.find_one(myquery)
    return mydoc


mydb=myclient['Restroom_Management']
Collection_Name1="user_feedback"
mycollection2 = mydb[Collection_Name1]
feedbacks=[]
temp=[]
for document in mycollection2.find():
    temp=[document['odour_level'],document['cleanliness_level'],document['is_soap'],document['is_water'],document['overall_rating'],document['time']]
    current_document=comparison(document['time'])#returns appropriate document
    print(current_document)
    feedbacks.append(temp)
print(feedbacks)
#updating treshold value of ammonia
#df=pd.DataFrame(feedbacks)

df=pd.DataFrame(columns=["Odour", "Cleanliness", "Soap Availability","Water availability","Overall Rating","Time"],data=feedbacks)

#df=df.transpose()
#df.columns=["Odour", "Cleanliness", "Soap Availability","Water availability","Overall Rating"]
print(df)
#df.columns=['ammonia(in ppm)','user_feedback']
df.head()
ammonia=df['ammonia(in ppm)']
user=df['user_feedback']
weight=[]
for i in range(len(ammonia)):
    if ammonia[i] >= 20:
        weight.append(1)
    else:
        ammo_prop=ammonia[i]/5+1
        user_feedback=user[i]
        ammo_prop=6-ammo_prop     #to calculate deviation
        dev=abs(ammo_prop-user_feedback)  #deviation
        weight.append(1-(1/4)*dev)
df['weight']=weight
df.head()
df.describe()
feedback_with_weight=[]
for i in range(len(ammonia)):
    feedback_with_weight.append(user[i]*weight[i])
total_weight=sum(weight)
print(total_weight)
new_feedback=sum(feedback_with_weight)/total_weight
print(new_feedback)
curr_treshold=19

#updating treshold

new_treshold=3-new_feedback
new_treshold=curr_treshold+new_treshold/2
print(new_treshold)
