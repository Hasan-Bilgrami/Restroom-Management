#!/usr/bin/env python
# coding: utf-8

# In[11]:


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import pandas as pd
import matplotlib
import sklearn
import pymongo
from sklearn import preprocessing


# In[23]:


Collection_Name="MNNIT"
myclient = pymongo.MongoClient("mongodb+srv://shivangitandon:pass@cluster0-0bcsj.mongodb.net/test?retryWrites=true")
db = myclient.test
mydb = myclient["Restroom_Management"]
mycollection = mydb[Collection_Name]
print(myclient.list_database_names())


# In[13]:


#checking ammonia treshold


# In[14]:


#read ammonia sensor data
#ammonia=document['Smell_Sensor']
document=mycollection.find_one(sort=[("Smell_Sensor",-1)])
max_ammonia=document['Smell_Sensor']
#preset treshold for ammonia
ammonia_treshold=20


# In[ ]:


#check if max value is greater than treshhold or not
#max_ammonia=max(ammonia)


# In[5]:


max_ammonia=float(max_ammonia)
decision=False #by default


# In[ ]:


#alert for ammonia treshold is stored in string alert_ammonia
if(max_ammonia >= ammonia_treshold):
    alert_ammonia='Treshold level of ammonia is crossed and current level is '+str(max_ammonia)
    decision=True


# In[ ]:





# In[ ]:


#checkng counter treshold


# In[ ]:


#read counter sensor data
#counter=document['People_Counter']
document=mycollection.find_one(sort=[("People_Counter",-1)])
print(document)
max_count=document['People_Counter']
#preset treshold for counter
counter_treshold=100


# In[ ]:


#check if max value is greater than treshhold or not
#max_count=max(counter)


# In[ ]:


max_count=int(max_count)


# In[ ]:


#alert for counter treshold is stored in string alert_count
if(max_count >= counter_treshold):
    alert_count='Treshold level of ammonia is crossed and current level is '+str(max_count)
    decision=True


# In[ ]:





# In[ ]:


#checking soap dispenser treshold


# In[ ]:


#read soap level detector data
#soap=document['Soap_Level']
document=mycollection.find_one(sort=[("Soap_Level",1)])
min_level=document['Soap_Level']
#preset treshold for soap level
soap_treshold=10


# In[ ]:


#check if min value is less than treshhold or not
#min_level=min(soap)


# In[ ]:


min_level=float(min_level)


# In[ ]:


#alert for soap treshold is stored in string alert_soap
if(min_level <= soap_treshold):
    alert_soap='Treshold level of soap is crossed and current level is '+str(min_level)
    decision=True


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[24]:


train=pd.read_csv('toilet_dataset.csv')


# In[ ]:


train.shape


# In[ ]:


print(train.columns)


# In[ ]:


from sklearn.utils import shuffle
train = shuffle(train)


# In[ ]:


train.describe()


# In[ ]:


corrmat=train.corr()
fig=plt.figure(figsize=(12,9))
sns.heatmap(corrmat, annot=True, fmt="f")
#sns.heatmap(corrmat,vmax=.9,square=True)
plt.show()


# In[ ]:


col=['in ppm', 'persons', 'in cm']
target='output'


# In[25]:


from sklearn.model_selection import train_test_split
#training set
#train_set=train.sample(frac=0.7,random_state=1)
train_set=train.sample(frac=1,random_state=1)
#test set
d=mycollection.find()[-1]
a=pd.DataFrame([d.values()])


#test_set=train.loc[~train.index.isin(train_set.index)]
test_set=a
print(train_set.shape)
print(test_set.shape)


# In[ ]:


#Import svm model
from sklearn import svm

#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(train_set[col],train_set[target])

#Predict the response for test dataset
predictions = clf.predict(test_set[col])


# In[ ]:


#test_set predictions
new_list = []
for item in predictions:
    new_list.append(item)
    


# In[ ]:


if predictions==1:#1 means cleaning reqquired
    decision=True
    Collection_Name="restrooms"
    mycollection = mydb[Collection_Name]
    myquery = { "Name": "MNNIT" }
    mydoc = mycol.find_one(myquery)
    mycollection.delete_one(mydoc)
    mydoc["Cleaner_Required"]=True
    mycollection.insert_one(mydoc)
    decision=False #AssuminG cLEANING Done


# In[ ]:


#print(new_list)


# In[ ]:


#from sklearn.metrics import mean_squared_error
#mean_squared_error(new_list,test_set[target])


# In[ ]:


#import numpy as np
#from sklearn.metrics import accuracy_score

#accuracy_score(test_set[target], new_list)

#accuracy_score(test_set[target], new_list, normalize=False)


# In[ ]:


#my_submission = pd.DataFrame({'output': new_list})

#my_submission.to_csv('test_set_output.csv', index=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


Collection_Name="user_feedback"
mycollection = mydb[Collection_Name]
feedbacks=[]
for document in mycollection.find():
    #feedbacks.append([document.values()])
    feedbacks.append([document["odour_level"]])
df=pd.DataFrame(feedbacks)


# In[ ]:


#updating treshold value of ammonia


# In[ ]:


#df=pd.read_csv('Feedback.txt',header=None)


# In[ ]:


df.head()


# In[ ]:


df.columns=['ammonia(in ppm)','user_feedback']


# In[ ]:


df.head()


# In[ ]:


ammonia=df['ammonia(in ppm)']
user=df['user_feedback']


# In[ ]:


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
    


# In[ ]:


df['weight']=weight


# In[ ]:


df.head()


# In[ ]:


df.describe()


# In[ ]:


df


# In[ ]:


feedback_with_weight=[]
for i in range(len(ammonia)):
    feedback_with_weight.append(user[i]*weight[i])


# In[ ]:


total_weight=sum(weight)


# In[ ]:


print(total_weight)


# In[ ]:


new_feedback=sum(feedback_with_weight)/total_weight


# In[ ]:


print(new_feedback)


# In[ ]:


curr_treshold=19


# In[ ]:


#updating treshold
new_treshold=3-new_feedback
new_treshold=curr_treshold+new_treshold/2


# In[ ]:


print(new_treshold)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




