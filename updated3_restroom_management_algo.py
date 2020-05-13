# !/usr/bin/env python
# coding: utf-8
import numpy as np
import sys
import pandas as pd
import sklearn
import pymongo
import datetime
import statistics
from sklearn import preprocessing
from os import getpid


print("Algo "+str(getpid()))
Collection_Name = "Computer Center"
myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
mydb = myclient["Restroom_SensorData"]
mycollection = mydb[Collection_Name]
print(myclient.list_database_names())
route = "default"  # Define route AS <3> ROHIT ka paisa bachane ke liye


def updation(sense=0, threshold=0):  # Alerts cleaner when restrom reuires cleaning
    Collection = "restrooms"
    mydb = myclient["Restroom_Management"]
    mycollection1 = mydb[Collection]
    myquery = {"Name": Collection_Name}
    newvalues = {"$set": {"Cleaner_Required": True}}
    mycollection1.update_many(myquery, newvalues)
    '''
    18 November 2019
    The following script sends an SMS with the content in variable message.
    https://www.quora.com/What-is-the-difference-between-urllib2-and-urllib-vs-request-libraries-in-Python
    '''
    import requests  # Python URL functions

    authkey = "303847AkEQ95JxrjD5dcd505c"  # Your authentication key.
    mobiles = "9462718719"  # Multiple mobiles numbers separated by comma.
    if sense == 0:  # ML output
        message = "Computer Center Restroom(M/F) requires cleaning."  # Your message to send.
    elif sense == 1:  # Ammonia threshold exceeded
        message = "Ammonia Level at Computer Center Restroom(M/F) has exceeded the threshold value at " + str(
            threshold) + ". \nCleaner is required."
    elif sense == 2:  # People Counter exceeded
        message = "People Count at Computer Center Restroom (M/F) has exceeded the threshold value at " + str(
            threshold) + ". \nCleaner is required."
    elif sense == 3:  # Soap Dispenser Empty
        message = "Soap quantity in Soap Dispenser at Computer Center Restroom(M/F) is below " + str(
            threshold) + ". \nRe-fill is required."
    elif sense == 4:
        message = "Wetness level on the floor at Computer Center Restroom(M/F) is above " + str(
            threshold) + "\n Cleaning required"
    sender = "ADHOCS"  # Sender ID,While using route4 sender id should be 6 characters long.

    # Prepare you post parameters
    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route
    }

    url = "http://sms.amarsinha.in/api/sendhttp.php"  # API URL
    #r = requests.post(url, data=values)
    #print("restroom_management_algo:" + str(r))  # Print Response
    print("SMS Sent to Cleaner")
    decision = False


def updation_negative():  # Cleaner not required
    Collection = "restrooms"
    mydb = myclient["Restroom_Management"]
    mycollection1 = mydb[Collection]
    myquery = {"Name": Collection_Name}
    newvalues = {"$set": {"Cleaner_Required": False}}
    mycollection1.update_many(myquery, newvalues)


def sensor_failure(sense):  # Alerts supervisor if a sensor does not respond
    import requests  # Python URL functions

    authkey = "303847AkEQ95JxrjD5dcd505c"  # Your authentication key.
    mobiles = "7753842024"  # Multiple mobiles numbers separated by comma.

    if sense == 1:  # Ammonia threshold exceeded
        message = "Hi \nThe MQ-135 Air Quality Sensor in the restroom at Computer Center is not responding. \nPlease look into this matter at your earliest convenience. \nHave a nice day."
    elif sense == 2:  # People Counter exceeded
        message = "Hi \nThe PIR Motion Detector in the restroom at Computer Center is not responding. \nPlease look into this matter at your earliest convenience. \nHave a nice day."
    elif sense == 3:  # Soap Dispenser Empty
        message = "Hi \nThe Sensor installed inside the soap dispenser in the restroom at Computer Center is not responding. \nPlease look into this matter at your earliest convenience. \nHave a nice day."
    elif sense == 4:
        message = "Hi \nThe wetness in the restroom at Computer Center is not responding. \nPlease look into this matter at your earliest convenience. \nHave a nice day."
    sender = "ADHOCS"  # Sender ID,While using route4 sender id should be 6 characters long.

    # Prepare you post parameters
    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route
    }

    url = "http://sms.amarsinha.in/api/sendhttp.php"  # API URL
    print("SMS Sent to Supervisor")
    #r = requests.post(url, data=values)
    #print(r)  # Print Response


# checking ammonia treshold
# read ammonia sensor data
sensors_are_operational = True  # Makes false if any sensor does not respond
document = mycollection.find_one(sort=[("Time", -1)])
print("restroom_management_algo:" + str(document))

try:
    max_ammonia = document['Smell_Sensor']

    # preset threshold for ammonia

    ammonia_treshold = 1

    # check if max value is greater than treshhold or not

    max_ammonia = float(max_ammonia)
    decision = False  # by default

    # alert for ammonia treshold is stored in string alert_ammonia

    if (max_ammonia >= ammonia_treshold):
        alert_ammonia = 'Treshold level of ammonia is crossed and current level is ' + str(max_ammonia)
        print(alert_ammonia)
        decision = True
        updation(1, max_ammonia)
    else:
        updation_negative()
except KeyError:
    sensors_are_operational = False
    sensor_failure(1)
# checkng counter treshold
# read counter sensor data

try:
    max_count = document['People_Counter']

    # preset treshold for counter
    counter_treshold = 20

    # check if max value is greater than treshhold or not
    max_count = int(max_count)
    # alert for counter treshold is stored in string alert_count
    if (max_count >= counter_treshold):
        alert_count = 'Treshold level of people counter is crossed and current level is ' + str(max_count)
        print("restroom_management_algo:" + alert_count)
        decision = True
        updation(2, max_count)
    else:
        updation_negative()
except KeyError:
    sensors_are_operational = False
    sensor_failure(2)
# read soap level detector data

try:
    min_level = document['Soap_Level']

    # preset treshold for soap level
    soap_treshold = 2

    # check if min value is less than treshhold or not
    min_level = float(min_level)

    # alert for soap treshold is stored in string alert_soap
    if (min_level <= soap_treshold):
        alert_soap = 'Treshold level of soap is crossed and current level is ' + str(min_level)
        print("restroom_management_algo" + alert_soap)
        decision = True
        updation(3, min_level)
    else:
        updation_negative()
except KeyError:
    sensors_are_operational = False
    sensor_failure(3)

# wetness
try:
    max_level = document['Wetness']
    # preset treshold for soap level
    wetness_treshold = 50
    # check if max value is greater than threshold or not
    max_level = float(max_level)
    # alert for wetness treshold is stored in string alert_soap
    if (max_level >= wetness_treshold):
        alert_wetness = 'Treshold level of wetness is crossed and current level is ' + str(max_level)
        print("restroom_management_algo" + alert_wetness)
        decision = True
        updation(4, max_level)
    else:
        updation_negative()
except KeyError:
    sensors_are_operational = False
    sensor_failure(4)

# DATASET OF TOILETS PRESENT PREHANDEDLY


if 'People_Counter' in document and 'Smell_Sensor' in document and 'Soap_Level' in document:
    train = pd.read_csv('toilet_dataset.csv')
    from sklearn.utils import shuffle

    train = shuffle(train)
    train.describe()

    colum = ['in ppm', 'persons', 'in cm', 'output']
    col = ['in ppm', 'persons', 'in cm']
    target = 'output'
    train = train[colum]
    from sklearn.model_selection import train_test_split

    # training set
    train_set = train.sample(frac=1, random_state=1)

    # test set
    d = mycollection.find_one(sort=[("Time", -1)])
    print("restroom_management_algo:" + str(d))
    al = []
    al = [d['Smell_Sensor'], d['People_Counter'], d['Soap_Level']]
    a = pd.DataFrame(columns=['in ppm', 'persons', 'in cm'], data=[al])
    print("restroom_management_algo:" + str(a))
    test_set = a
    # IMPORT SVM MODEL

    from sklearn import svm

    # Create a svm Classifier

    clf = svm.SVC(kernel='linear')  # Linear Kernel

    # Train the model using the training sets

    clf.fit(train_set[col], train_set[target])

    # Predict the response for test dataset

    predictions = clf.predict(test_set[col])

    # test_set predictions
    new_list = []
    for item in predictions:
        new_list.append(item)

    if predictions == 1:  # 1 means cleaning reqquired
        print("restroom_management_algo:Cleaner Required")
        updation()
    else:
        print("restroom_management_algo:Cleaner not required")
        updation_negative()

    a['output'] = predictions
    a.to_csv('toilet_dataset.csv', mode='a', header=False, index=False)


# FEEDBACK_PORTION


# finds a document at the time

def comparison(time):
    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    Collection_Name = "Computer Center"
    # db = myclient.test
    mydb = myclient["Restroom_SensorData"]
    mycollection = mydb[Collection_Name]
    flag = False
    upper_limit = time
    lower_limit = time
    mydoc = mycollection.find_one({"Time": time})
    flag = 1
    while not mydoc:
        flag += 1
        upper_limit = upper_limit + datetime.timedelta(minutes=1)
        lower_limit = lower_limit - datetime.timedelta(minutes=1)
        myquery = {"Time": {"$gt": str(lower_limit), "$lt": str(upper_limit)}}
        mydoc = mycollection.find_one(myquery)
        if flag == 30:
            #print("restroom_management_algo:No relevant sensor value found")
            return None
    return mydoc


mydb = myclient['Restroom_Management']
Collection_Name1 = "user_feedback"
mycollection2 = mydb[Collection_Name1]
feedbacks = []
temp = []
for document in mycollection2.find():
    # print(document)
    current_document = comparison(document['Time'])
    # print(current_document)  # returns appropriate document
    if current_document == None:
        continue
    # temp=[document['Odour_level'],document['Cleanliness_level'],document['Is_soap'],document['Is_water'],document['Overall_rating'],document['Time'],current_document['Smell_Sensor'],current_document['People_Counter'],current_document['Soap_Level']]
    temp = [document['Odour_level'], document['Cleanliness_level'], document['Is_soap'], document['Is_water'],
            document['Overall_rating'], document['Time']]
    if 'Smell_Sensor' in current_document:
        temp.append(current_document['Smell_Sensor'])
    else:
        temp.append(-1)
    if 'People_Counter' in current_document:
        temp.append(current_document['People_Counter'])
    else:
        temp.append(-1)
    if 'Soap_Level' in current_document:
        temp.append(current_document['Soap_Level'])
    else:
        temp.append(-1)
    feedbacks.append(temp)
# print(feedbacks)
# print("feed len "+str(len(feedbacks)))
# updating treshold value of ammonia

df = pd.DataFrame(columns=["Odour", "Cleanliness", "Soap Availability", "Water availability", "Overall Rating", "Time",
                           "ammonia(in PPM)", "People Count", "Soap Level"], data=feedbacks)
print("restroom_management_algo:" + str(df))
# exit(0)
ammonia = df['ammonia(in PPM)']
people = df['People Count']
soap = df['Soap Level']
userodour = df['Odour']
userclean = df['Cleanliness']
usersoap = df['Soap Availability']
userwater = df['Water availability']
useroverall = df['Overall Rating']

doc = mycollection.find_one(sort=[("Time", -1)])

if 'Smell_Sensor' in doc:
    weight = []
    for i in range(len(ammonia)):
        if ammonia[i] >= 200:
            weight.append(1)
        else:
            if ammonia[i] != -1:
                ammo_prop = ammonia[i] / 50 + 1
                user_feedback = userodour[i]
                ammo_prop = 6 - ammo_prop  # to calculate deviation
                dev = abs(ammo_prop - user_feedback)  # deviation
                weight.append(1 - (1 / 6) * dev)
    length = len(weight)
    if length > 0:
        df['weight'] = weight
        feedback_with_weight = []
        # total_weight=sum(weight)
        # mean_weight=total_weight/len(ammonia)
        counter = 0
        literacy_rate = 0.7  # In Fractions
        for i in range(len(ammonia)):
            if ammonia[i] != -1:
                feedback_with_weight.append(userodour[i] * weight[counter] * literacy_rate)
                counter = counter + 1

        # minimum=min(feedback_with_weight)
        # maximum=max(feedback_with_weight)
        # diff=maximum-minimum
        # mean_feedback=statistics.mean(feedback_with_weight)
        # normalized_weight=[]
        # for i in range(length):
        # x=abs(feedback_with_weight[i]-mean_feedback)/diff
        # if(feedback_with_weight[i]<mean_feedback):
        # normalized_weight.append(0.5-x)
        # else:
        # normalized_weight.append(0.5+x)

        total_weight = sum(weight)
        new_feedback = sum(feedback_with_weight) / total_weight
        # new_feedback=new_feedback*5

        print("restroom_management_algo:The mapped odour feedback is\n")
        print(new_feedback)

        curr_treshold = ammonia_treshold / 40
        # updating treshold
        new_treshold = 3 - new_feedback
        ammonia_treshold = curr_treshold + new_treshold / 2
        ammonia_treshold = ammonia_treshold * 40
        print("restroom_management_algo:The updated Ammonia threshold is\n")
        print(ammonia_treshold)

if 'People_Counter' in doc:
    weight = []
    for i in range(len(people)):
        if people[i] >= 200:
            weight.append(1)
        else:
            if people[i] != -1:
                ammo = people[i] / 40 + 1
                user_feedback = userclean[i]
                ammo = 6 - ammo  # to calculate deviation
                dev = abs(ammo - user_feedback)  # deviation
                weight.append(1 - (1 / 4) * dev)
    length = len(weight)
    if length > 0:
        df['weight'] = weight
        feedback_with_weight = []
        counter = 0
        for i in range(len(people)):
            if people[i] != -1:
                feedback_with_weight.append(userclean[i] * weight[counter] * literacy_rate)
                counter = counter + 1
        total_weight = sum(weight)
        new_feedback = sum(feedback_with_weight) / total_weight
        print("restroom_management_algo:the mapped cleanliness feedback is")
        print(new_feedback)
        curr_treshold = counter_treshold / 40
        # updating treshold
        new_treshold = 3 - new_feedback
        counter_treshold = curr_treshold + new_treshold / 2
        counter_treshold = counter_treshold * 40
        print("restroom_management_algo:the updated people counter threshold is")
        print(counter_treshold)