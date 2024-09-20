# ###################################################################
# ###################################################################
# ######## Run every day-of-week from Monday through Friday #########
# ###################################################################
# ###################################################################

# “At 07:00 on every day-of-week from Monday through Friday.”
# 00 7 * * 1-5 /usr/bin/python3 /home/www/b2b/cinntra_standalone/bridge/email_alert_daily_for_salesman.py


from datetime import date, datetime
import calendar
import mysql.connector

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

# if currentDay != 'Saturday' or currentDay != 'Sunday':
#     # print('day ok')
#     if currentTime == "09:30 AM":
#         # print('time ok ')

import sys, os
sys.path.append('/home/www/b2b/cinntra_standalone/bridge/')
# sys.path.append('../../cinntra_standalone_dev/bridge')
# sys.path.append('../../bridge/')
from camp_fun import sendMail

#--- start dynamic-----
dir = os.getcwd()
dir = dir.split("/bridge/")[0]+"/bridge"
sys.path.append(dir)

from bridge import settings
mydb = mysql.connector.connect(
    host=settings.DATABASES['default']['HOST'],
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['PASSWORD'],
    database=settings.DATABASES['default']['NAME']
)
#----end dynamic---

# mycursor = mydb.cursor()
mycursor = mydb.cursor(dictionary=True, buffered=True)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>> List Employee >>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
sqlSelectEmployee = "SELECT `id`,`SalesEmployeeCode`,`SalesEmployeeName`,`Email`,`Mobile` FROM `Employee_employee` WHERE `role` != 'admin' ORDER BY `id` ASC"
# sqlSelectEmployee = "SELECT `id`,`SalesEmployeeCode`,`SalesEmployeeName`,`Email`,`Mobile` FROM `Employee_employee` WHERE `role` != 'admin' AND `id` in(37)"
mycursor.execute(sqlSelectEmployee)
allEmp = mycursor.fetchall()
if len(allEmp)!= 0:
    for emp in allEmp:
        print('---Employee---')
        # print(emp)
        id = emp['id']
        SalesEmployeeCode = emp['SalesEmployeeCode']
        SalesEmployeeName = emp['SalesEmployeeName']
        Email = emp['Email']
        Mobile = emp['Mobile']
        print(Email)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>> List Opportunity by Employee >>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        sqlSelectLead = f"SELECT * FROM `Lead_lead` WHERE `assignedTo_id` = {id}"
        print(sqlSelectLead)
        mycursor.execute(sqlSelectLead)
        allLead = mycursor.fetchall()
        if len(allLead) != 0:
            leadRow = ""
            leadCount = 0
            for leadData in allLead:
                # print('---Lead---')
                # leadCount = leadCount+1
                leadId = leadData['id']

                CompanyName = leadData['companyName']
                ContactPersonName = leadData['contactPerson']
                ContactPersonPhoneNo = leadData['phoneNumber']
                ContactPersonEmail = leadData['email']
                Remarks = leadData['message']
                status = leadData['status']
                leadType = leadData['leadType']
                leadDate = leadData['date']

                lableColor = ""
                if str(leadType) == "Hot":
                    lableColor = "style='background-color: green;'"
                if str(leadType) == "Cold":
                    lableColor = "style='background-color: red;'"
                if str(leadType) == "Warm":
                    lableColor = "style='background-color: lightblue;'"

                sqlSelectActivity = f"SELECT * FROM `Activity_chatter` WHERE `SourceType` = 'Lead' AND `SourceID` = {leadId} AND `UpdateDate` = '{str(currentDate)}' ORDER BY `id` DESC LIMIT 1"
                # print(sqlSelectActivity)
                mycursor.execute(sqlSelectActivity)
                allActivity = mycursor.fetchall()
                if len(allActivity) != 0:
                    activityDetails = allActivity[0]
                    Remarks = activityDetails['Message']
                elif str(leadDate) == str(currentDate):
                    print('ok')
                else:
                    # print('=================no data to show===============')
                    continue
                
                # print('=================data to show===============')
                leadCount = leadCount+1
                sqlSelectLeadItems = f"SELECT * FROM `Lead_leaditem` WHERE `LeadID` = {leadId}"
                print(sqlSelectLeadItems)
                mycursor.execute(sqlSelectLeadItems)
                allItems = mycursor.fetchall()
                
                ItemNames = []
                if len(allItems) != 0:
                    for item in allItems:
                        ItemNames.append(item['ItemDescription'])
                        
                    ItemNames = ', '.join(ItemNames)
                else:
                    ItemNames = ""

                leadRow += f""" 
                    <tr style="text-align: left;">
                        <td>{leadCount}</td>
                        <td>{SalesEmployeeName}</td>
                        <td>{CompanyName}</td>
                        <td>{ItemNames}</td>
                        <td>{Remarks}</td>
                        <td>{status}</td>
                        <td {lableColor}>{leadType}</td>
                    </tr>
                """

            if leadRow == "":
                continue

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # after creating opportunity mail alert to reporting person
            empFirstName = SalesEmployeeName
            empEmail = [Email]
            mailSubject = "New assigned opportunity list"
            mailMessage = f"""
            <div>
                Hi Sir/Mam <b>{empFirstName}</b>,<br><br>
                You'r assigned opportunity are: <br><br>
            </div>
            <table cellpadding="10" cellspacing="0" border="1">
            <tr style="text-align: left;background-color: yellow;">
                <th>S.No.</th>
                <th>Sales Rep</th>
                <th>BP Name</th>
                <th>Products</th>
                <th>Remarks</th>
                <th>Status</th>
                <th>Priority</th>
            </tr>
            {leadRow}
            </table>"""
            # cc   = ['abhishek.kaithwas@cinntra.com']
            cc   = ['']
            mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = "", cc = cc)
            print(mailResponse)
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>