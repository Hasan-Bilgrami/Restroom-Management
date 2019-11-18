'''
18 November 2019
The following script sends an SMS with the content in variable message.
'''


import requests # Python URL functions


authkey = "303847AkEQ95JxrjD5dcd505c" # Your authentication key.
mobiles = "7753842024" # Multiple mobiles numbers separated by comma.
message = "Cleaner required" # Your message to send.
sender = "ADHOCS" # Sender ID,While using route4 sender id should be 6 characters long.
route = 3 # Define route AS <3> ROHIT ka paisa bachane ke liye

# Prepare you post parameters
values = {
          'authkey' : authkey,
          'mobiles' : mobiles,
          'message' : message,
          'sender' : sender,
          'route' : route
          }

url = "http://sms.amarsinha.in/api/sendhttp.php" # API URL
r = requests.post(url, data=values)
print (r) # Print Response