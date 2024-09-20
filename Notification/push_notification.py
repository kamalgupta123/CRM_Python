import requests, json
import time
import math
import mysql.connector

from pytz import timezone
from datetime import datetime as dt

# from global_fun import sendNotification
date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
time = dt.now(timezone("Asia/Kolkata")).strftime("%I:%M %p")
print(date)
print(time)

#import sys
#sys.path.append("../Mylib/")
#import config
#config = config.Config()

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#  password=config.sql['password'],
#  database=config.sql['database']
  password="$Bridge@2022#",
  database="cinntra_standalone"
)

mycursor = mydb.cursor(dictionary=True)
print("test comment")

from pyfcm import FCMNotification

def sendNotification(DeviceId, Title, Message):
    try:
        #push_service = FCMNotification(api_key="AAAAyIEFgFY:APA91bGXg9CJZc2Wus6UQx-z4Ic2Xe3OtiGKeTPdH6V8aGa41jwgbBSeNxwJRvmdcsTrEt4jlSvEtrr8581CSJsG_hGHM9skZGxXsBmM_33-g0RbbBJ5FPDnEEHoZNpGoYCv13qQdQG-") # cinntra
        push_service = FCMNotification(api_key="AAAAadlvIDU:APA91bGC0hY3zWK6NmIbR_m9Nyx9FmA7k_lrt4E0nPm9y576M91qU1UWk9V4J09DQYExgyF_DnXEAf7-P6FyHze1JKbsTOnwqAoV5QUUM0J9M7sa9rB6y-ObuGKCcM0iABWz3rpd4sdq") # cinntra by vijay
        
        #registration_id = "dctm43vtTQaJdCHDWZL8RZ:APA91bG1ukxTksiiAh3bI4FGUYyFPcv9UsJIj5xcVypu24vt8hfAc8SEncWOGYnRE1fUpNdjzA_PVNfMGYVd5HEWEp8IFIFNw5tg7n1_PmvylF1MRE7DxvaIdf_EN9PsUGQ_MNWbL_qV"
        registration_id = DeviceId
        # message_title = "Test Notification"
        # message_body = "Hi Abhishek, your customized news for today is ready"
        message_title = Title
        message_body = Message
        print(f'title:{ message_title}, body {message_body}')
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, content_available=True)

        # To support rich notifications on iOS 10, set
        extra_kwargs = {
            'mutable_content': True
        }

        print(result)
        return "sent"
    except Exception as e:
        return str(e)

notification_list_sql = "SELECT * FROM `Notification_notification` WHERE `Push` = '0' and `CreatedDate` = '"+date+"' AND STR_TO_DATE(`SourceTime`, '%h:%i') >= STR_TO_DATE('"+time+"', '%h:%i') AND STR_TO_DATE(`SourceTime`, '%h:%i') <= ADDTIME(STR_TO_DATE('"+time+"', '%h:%i'), '0:10:00')"
print(notification_list_sql)
mycursor.execute(notification_list_sql)
notification_list = mycursor.fetchall()
print(len(notification_list))
if len(notification_list) > 0:
    for noti in notification_list:

        Id = noti['id']
        Title = noti['Title']
        Description = noti['Description']
        EmpId = noti['Emp']

        sql_query = "SELECT `FCM` FROM `Employee_employee` WHERE `id` = '"+EmpId+"'"
        mycursor.execute(sql_query)
        emp_ob = mycursor.fetchone() # to get only one row from list
        fcmId = emp_ob['FCM']
        #fcmId="drJNiLFDSo2bZmkHwmz_oM:APA91bF8Rh2QP0XAOkWksZfMzABAU2egPVyMmaldBfxR5LzNkVH2g-gxT5gNJETtKxAJKJsdX_Sk3vELSjfqBhQMt9KwZFIUow8Y9TPjBD3nAHQmJAjoYQ5cnN1ulk-GR4hp2t4hdOUv"
        print(fcmId)

        result = sendNotification(DeviceId=fcmId, Title=Title, Message=Description)
        print(result)
        mycursor.execute("Update Notification_notification SET `Push`='1' where id='"+str(Id)+"'")
        mydb.commit()
