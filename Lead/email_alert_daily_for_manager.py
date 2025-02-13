# ###################################################################
# ###################################################################
# ######## Run every day-of-week from Monday through Friday #########
# ###################################################################
# ###################################################################
# “At 07:00 on every day-of-week from Monday through Friday.”
# 00 19 * * * * /usr/bin/python3 /home/www/b2b/cinntra_standalone/bridge/lead/email_alert_daily_for_manager.py
# 00 19 * * * * /usr/bin/python3 /home/www/b2b/cinntra_standalone/bridge/lead/email_alert_daily_for_salesman.py

print(">>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>Vison sales server<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<")

from datetime import date, datetime
import calendar
import mysql.connector

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)

import sys, os
sys.path.append('/home/www/b2b/cinntra_standalone/bridge/')
# sys.path.append('/home/www/b2b/cinntra_standalone_test/bridge/')
# sys.path.append('../../bridge/')

#--- start dynamic-----
dir = os.getcwd()
dir = dir.split("/bridge/")[0]+"/bridge"
sys.path.append(dir)

print("========== Cinntra Standalone Live ==========")
print(dir)

from camp_fun import sendMail
import sys

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
sqlSelectEmployee = "SELECT `id`,`SalesEmployeeCode`,`SalesEmployeeName`,`Email`,`Mobile` FROM `Employee_employee` WHERE `role` != 'admin' AND `SalesEmployeeCode` != 29 ORDER BY `id` ASC"
mycursor.execute(sqlSelectEmployee)
allEmp = mycursor.fetchall()
leadRow = ""
leadCount = 0
if len(allEmp)!= 0:
    for emp in allEmp:
        # print('---Employee---')
        # print(emp)
        id = emp['id']
        SalesEmployeeName = emp['SalesEmployeeName']
        Email = emp['Email']
        Mobile = emp['Mobile']
        SalesEmployeeCode = emp['SalesEmployeeCode']
        
        empArr = [SalesEmployeeCode]

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # >>>>>> List Lead by Employee >>>>>>>
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        empArr = ",".join(empArr)
        # print(empArr)
        sqlSelectLead = f"SELECT * FROM `Lead_lead` WHERE `assignedTo_id` in({empArr})"
        # print(sqlSelectLead)
        mycursor.execute(sqlSelectLead)
        allLead = mycursor.fetchall()
        if len(allLead) != 0:
            for leadData in allLead:
                # print('---Lead---')
                leadId = leadData['id']
                CompanyName = leadData['companyName']
                ContactPersonName = leadData['contactPerson']
                ContactPersonPhoneNo = leadData['phoneNumber']
                ContactPersonEmail = leadData['email']
                Remarks = leadData['message']
                status = leadData['status']
                leadType = leadData['leadType']
                leadDate = leadData['date']
                assignedTo_id = leadData['assignedTo_id']

                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # tempQuery = f"SELECT `id`, `SalesEmployeeCode`, `SalesEmployeeName`,`Email`,`Mobile` FROM `Employee_employee` WHERE `reportingTo` = {SalesEmployeeCode}"
                # mycursor.execute(tempQuery)
                # tempEmp = mycursor.fetchall()
                # if len(tempEmp)!=0:
                #     SalesEmployeeName = tempEmp[0]['SalesEmployeeName']
                
                lableColor = ""
                if str(leadType) == "Hot":
                    lableColor = "style='background-color: green;'"
                if str(leadType) == "Cold":
                    lableColor = "style='background-color: red;'"
                if str(leadType) == "Warm":
                    lableColor = "style='background-color: lightblue;'"

                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # sqlSelectActivity = f"SELECT `id`, `SourceID`, `Subject`, `Comment` FROM `Activity_activity` WHERE `SourceType` = 'Lead' AND `SourceID` = {leadId} AND `From` = {str(currentDate)} ORDER BY `id` DESC LIMIT 1"
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
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                print('=============lead ready to show==============')
                leadCount = leadCount+1
                sqlSelectLeadItems = f"SELECT * FROM `Lead_leaditem` WHERE `LeadID` = {leadId}"
                # print(sqlSelectLeadItems)
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
            # end for
        # end if
    # end if

    if leadRow == "":
        exit()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # after creating Lead mail alert to reporting person
    # empFirstName = SalesEmployeeName
    empFirstName = SalesEmployeeName
    empEmail = ['gagan.sharma@cinntra.com']
    # empEmail = ['bhoopendra.pal@cinntra.com']
    mailSubject = "New assigned Lead list"
    mailMessage = f"""
        <div>
            Dear Sir/Mam <br><br>
            Assigned lead with followups are:<br><br>
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

    cc   = ['abhishek.kaithwas@cinntra.com']
    # cc   = ['laxmikant.dixit@cinntra.com', 'nipun.dixit@cinntra.com']
    # cc   = ['abhishek.kaithwas@cinntra.com', 'ashutosh.kumar@cinntra.com']

    mailResponse = sendMail(toEmail= empEmail, subject = mailSubject, message = mailMessage, attachments = "", cc = cc)
    print(mailResponse)
    ## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>