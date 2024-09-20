from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from Activity.models import Activity, Chatter as ActivityChatter

from global_fun import *
from .forms import LeadForm  
from .models import *
from Pagination.models import *
from Employee.models import Employee  
from Item.models import *
import json
from django.contrib import messages

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import date, datetime
import calendar
import mysql.connector

import os
from django.core.files.storage import FileSystemStorage

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
# Create your views here.  

#Lead Create API
@api_view(['POST'])
def create(request):
    leads = request.data
    log = []
    
    for lead in leads:
        date=lead['date']
        location=lead['location']
        companyName=lead['companyName']
        numOfEmployee = lead['numOfEmployee']
        turnover = lead['turnover']
        source=lead['source']
        contactPerson=lead['contactPerson']
        designation=lead['designation']
        phoneNumber=lead['phoneNumber']
        alter_phone=lead['alter_phone']
        message=lead['message']
        email=lead['email']
        alter_email=lead['alter_email']
        status=lead['status']
        leadType=lead['leadType']
        productInterest=lead['productInterest']
        assignedTo_id=lead['assignedTo']
        employeeId_id=lead['employeeId']
        timestamp=lead['timestamp']
        UpdateDate=lead['timestamp']
        
        
        if phoneNumber!="" and Lead.objects.filter(phoneNumber=phoneNumber).exists():
            log.append(phoneNumber)
        else:
            model=Lead(date=date, location=location, companyName=companyName, numOfEmployee=numOfEmployee, turnover=turnover, source=source, status=status, leadType=leadType, contactPerson=contactPerson, designation=designation, phoneNumber=phoneNumber, alter_phone=alter_phone, message=message, email=email, alter_email=alter_email, productInterest=productInterest, assignedTo_id=assignedTo_id, employeeId_id=employeeId_id, timestamp=timestamp, UpdateDate=UpdateDate)
            model.save()
            
            LeadID = Lead.objects.latest('id').id
            print(LeadID)
        
            if len(lead['LeadItem']) != 0:
                items = lead['LeadItem']
                for item in items:
                    try:
                        if (Item.objects.filter(ItemCode=item).exists()):
                            it = Item.objects.get(ItemCode=item)                    
                            model_lines = LeadItem(LeadID = LeadID, UnitPrice = it.UnitPrice, DiscountPercent = it.Discount, ItemCode = it.ItemCode, ItemName = it.ItemName, ItemDescription = it.Description, TaxCode = it.TaxCode)
                            model_lines.save()
                    except Exception as e:
                        Lead.objects.filter(pk=LeadID).delete()
                        leadItems = LeadItem.objects.filter(LeadID=LeadID)
                        for litem in leadItems:
                            litem.delete()                           
                        return Response({"message":str(e),"status":"202","data":[]})
        print(log)
        if len(log) > 0:
            log_msg = "Mobile number is already exist: "+str(log)
        else:
            log_msg = 'successful'
    return Response({"message":log_msg,"status":"200","data":[]})


#Lead Chat Create API
@api_view(['POST'])
def chatter(request):
    try:
        Message = request.data['Message']
        Lead_Id = request.data['Lead_Id']
        Emp_Id = request.data['Emp_Id']
        Emp_Name = request.data['Emp_Name']
        UpdateDate = request.data['UpdateDate']
        UpdateTime = request.data['UpdateTime']

        model = Chatter(Message=Message, Lead_Id=Lead_Id, Emp_Id=Emp_Id, Emp_Name=Emp_Name, UpdateDate=UpdateDate, UpdateTime=UpdateTime)
        
        model.save()
        chat = Chatter.objects.latest('id')
        print(chat.id)
        return Response({"message":"Success","status":200,"data":[{"id":chat.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":201,"data":[str(e)]})


#Chatter All API
@api_view(["POST"])
def chatter_all(request):
    try:
        Emp=request.data['Emp']
        SourceID=request.data['SourceID']
        SourceType=request.data['SourceType']
        chat_obj = []
        if str(SourceType).lower() == 'lead':
            chat_obj = Chatter.objects.filter(SourceType=SourceType, SourceID=SourceID).order_by("id")
        else:
            allEmpIds = getAllReportingToIds(Emp)
            chat_obj = Chatter.objects.filter(Emp__in = allEmpIds, SourceType=SourceType, SourceID=SourceID).order_by("id")
        chat_json = ChatterSerializer(chat_obj, many=True)
        return Response({"message": "Success","status": 200,"data":chat_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})
    
# #Chatter All API
# @api_view(["POST"])
# def chatter_all(request):
#     Lead_Id=request.data['Lead_Id']
#     print(Lead_Id)
#     chat_obj = Chatter.objects.filter(Lead_Id=Lead_Id).order_by("id")
#     chat_json = ChatterSerializer(chat_obj, many=True)
#     return Response({"message": "Success","status": 200,"data":chat_json.data})

#Lead All API
@api_view(["GET"])
def all(request):
    try:
        leads_obj = Lead.objects.all().order_by("-id")
        result = showLead(leads_obj)
        return Response({"message": "Success","status": 200,"data":result})
        # lead_json = LeadSerializer(leads_obj, many=True)
        # return Response({"message": "Success","status": 200,"data":lead_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

#Lead All Filter API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    if len(json_data) == 0:
        leads_obj = Lead.objects.all(junk=0).order_by("-id")
        result = showLead(leads_obj)
        return Response({"message": "Success","status": 200,"data":result})
        #leads_json = LeadSerializer(leads_obj, many=True)
        # allld = []
        # for obj in leads_obj:
        #     lead_json = LeadSerializer(obj, many=False)
        #     lead_json_dump = json.loads(json.dumps(lead_json.data))
        #     items = LeadItem.objects.filter(LeadID = obj.id)
        #     item_json = LeadItemSerializer(items, many=True)
        #     lead_json_dump['LeadItem'] = item_json.data
        #     allld.append(lead_json_dump)
        # return Response({"message": "Success","status": 200,"data":allld})
    else:
        SalesPersonID = json_data['assignedTo']                
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
        
        leadType = request.data['leadType']
        
        if leadType !="All":
            leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")
        else:
            leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")                        
            
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            result = showLead(leads_obj)
            return Response({"message": "Success","status": 200,"data":result})
            #leads_json = LeadSerializer(leads_obj, many=True)
            # allld = []
            # for obj in leads_obj:
            #     lead_json = LeadSerializer(obj, many=False)
            #     lead_json_dump = json.loads(json.dumps(lead_json.data))
            #     items = LeadItem.objects.filter(LeadID = obj.id)
            #     item_json = LeadItemSerializer(items, many=True)
            #     lead_json_dump['LeadItem'] = item_json.data
            #     allld.append(lead_json_dump)
            # return Response({"message": "Success","status": 200,"data":allld})


# #Lead All Filter API
# @api_view(["POST"])
# def all_filter_page(request):
#     json_data = request.data
    
#     PageNo = request.data['PageNo']
#     MaxSize = request.data['MaxSize']

#     page_obj = Pagination.objects.filter(MaxSize=MaxSize).first()
#     if MaxSize != "All":
#         size = int(page_obj.MaxSize)
#         endWith = (PageNo * size)
#         startWith = (endWith - size)

#     if len(json_data) == 0:
#         leads_obj = Lead.objects.all(junk=0).order_by("-id")
#         #leads_json = LeadSerializer(leads_obj, many=True)
#         allld = []
#         for obj in leads_obj:
#             lead_json = LeadSerializer(obj, many=False)
#             lead_json_dump = json.loads(json.dumps(lead_json.data))
#             items = LeadItem.objects.filter(LeadID = obj.id)
#             item_json = LeadItemSerializer(items, many=True)
#             lead_json_dump['LeadItem'] = item_json.data
#             allld.append(lead_json_dump)
#         return Response({"message": "Success","status": 200,"data":allld})
#         #return Response({"message": "Success","status": 200,"data":leads_json.data})
#     else:
#         SalesPersonID = json_data['assignedTo']                
#         emp_obj = Employee.objects.get(pk=SalesPersonID)
        
#         if emp_obj.role == 'manager':
#             emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
#             SalesPersonID=[SalesPersonID]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
            
#         elif emp_obj.role == 'admin':
#             emps = Employee.objects.filter(id__gt=0)
#             SalesPersonID=[]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
#         else:
#             SalesPersonID = [json_data['assignedTo']]
        
#         print(SalesPersonID)
        
#         leadType = request.data['leadType']

#         if MaxSize != "All":
#             if leadType !="All":
#                 leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")[startWith:endWith]
#                 leads_count = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).count()
#             else:
#                 leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")[startWith:endWith]                        
#                 leads_count = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).count()
#         else:
#             if leadType !="All":
#                 leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")
#                 leads_count = leads_obj.count()
#             else:
#                 leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")   
#                 leads_count = leads_obj.count()
#         if len(leads_obj) ==0:
#             return Response({"message": "Success","status": 200,"data":[]})
#         else:
#             #leads_json = LeadSerializer(leads_obj, many=True)
#             allld = []
#             for obj in leads_obj:
#                 lead_json = LeadSerializer(obj, many=False)
#                 lead_json_dump = json.loads(json.dumps(lead_json.data))
#                 items = LeadItem.objects.filter(LeadID = obj.id)
#                 item_json = LeadItemSerializer(items, many=True)
#                 lead_json_dump['LeadItem'] = item_json.data
#                 allld.append(lead_json_dump)
#             return Response({"message": "Success","status": 200,"data":allld, "extra":{"total_count":leads_count}})
#             #return Response({"message": "Success","status": 200,"data":leads_json.data})
         

#Lead All Filter API
@api_view(["POST"])
def all_filter_page(request):
    json_data = request.data
    
    PageNo = request.data['PageNo']
    MaxSize = request.data['MaxSize']

    page_obj = Pagination.objects.filter(MaxSize=MaxSize).first()
    if MaxSize != "All":
        size = int(page_obj.MaxSize)
        endWith = (PageNo * size)
        startWith = (endWith - size)

    if len(json_data) == 0:
        leads_obj = Lead.objects.all(junk=0).order_by("-id")
        #leads_json = LeadSerializer(leads_obj, many=True)
        allld = []
        for obj in leads_obj:
            lead_json = LeadSerializer(obj, many=False)
            lead_json_dump = json.loads(json.dumps(lead_json.data))
            items = LeadItem.objects.filter(LeadID = obj.id)
            item_json = LeadItemSerializer(items, many=True)
            lead_json_dump['LeadItem'] = item_json.data
            allld.append(lead_json_dump)
        return Response({"message": "Success","status": 200,"data":allld})
        #return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        SalesPersonID = json_data['assignedTo']                
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
        
        leadType = request.data['leadType']
        search = request.data['search']
        status = request.data['status']
        toDate = request.data['toDate']
        fromDate = request.data['fromDate']
        assignTo = request.data['assignTo']
        createdBy = request.data['createdBy']

        if MaxSize != "All":
            if leadType !="All":
                if json_data['assignedTo'] == "33":
                    leads_obj = Lead.objects.filter(junk=0, leadType=leadType).order_by("-id")
                    # leads_count = Lead.objects.filter(junk=0, leadType=leadType).count()
                else:
                    leads_obj = Lead.objects.filter(junk=0, assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")
                    # leads_count = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).count()
            else:
                if json_data['assignedTo'] == "33":
                    leads_obj = Lead.objects.filter(junk=0).order_by("-id")                    
                    # leads_count = Lead.objects.filter(junk=0).count()
                else:
                    leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")                      
                    # leads_count = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).count()
        else:
            if leadType !="All":
                if json_data['assignedTo'] == "33":
                    leads_obj = Lead.objects.filter(junk=0, leadType=leadType).order_by("-id")
                else:
                    leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID, leadType=leadType).order_by("-id")
            else:
                if json_data['assignedTo'] == "33":
                    leads_obj = Lead.objects.filter(junk=0).order_by("-id")   
                else:
                    leads_obj = Lead.objects.filter(junk=0,assignedTo__in=SalesPersonID).order_by("-id")   
        print("datssssss",leads_obj, SalesPersonID)
        # if json_data['assignedTo']=="33":
        #     leads_obj = Lead.objects.filter(junk=0)
        
        leads_obj = leads_obj.filter(Q(companyName__icontains=search)|Q(phoneNumber__icontains=search)|Q(email__icontains=search)|Q(location__icontains=search)|Q(source__icontains=search)|Q(productInterest__icontains=search)|Q(date__icontains=search)|Q(contactPerson__icontains=search))
        print(leads_obj)
        if leads_obj:
            if status!="":
                leads_obj = leads_obj.filter(status=status)
            if fromDate!="":
                leads_obj = leads_obj.filter(date__gte=fromDate)
            if toDate!="":
                leads_obj = leads_obj.filter(date__lte=toDate)
            if assignTo!="":
                leads_obj = leads_obj.filter(assignedTo=assignTo)
            if createdBy!="":
                leads_obj = leads_obj.filter(employeeId=createdBy)
            if leadType != "All":
                leads_obj = leads_obj.filter(leadType=leadType)
        
        leads_count = leads_obj.count()
        if MaxSize!="All":
            leads_obj = leads_obj.order_by('-id')[startWith:endWith]
        else:
            leads_obj = leads_obj.order_by('-id')
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            #leads_json = LeadSerializer(leads_obj, many=True)
            allld = []
            for obj in leads_obj:
                lead_json = LeadSerializer(obj, many=False)
                lead_json_dump = json.loads(json.dumps(lead_json.data))
                items = LeadItem.objects.filter(LeadID = obj.id)
                item_json = LeadItemSerializer(items, many=True)
                lead_json_dump['LeadItem'] = item_json.data
                allld.append(lead_json_dump)
            return Response({"message": "Success","status": 200,"data":allld, "extra":{"total_count":leads_count}})
            #return Response({"message": "Success","status": 200,"data":leads_json.data})
        


            
#Lead All Filter API
@api_view(["POST"])
def all_filter_junk(request):
    json_data = request.data
    
    if len(json_data) == 0:
        leads_obj = Lead.objects.filter(junk=1).order_by("-id")
        allld = showLead(leads_obj)
        #leads_json = LeadSerializer(leads_obj, many=True)
        # allld = []
        # for obj in leads_obj:
        #     lead_json = LeadSerializer(obj, many=False)
        #     lead_json_dump = json.loads(json.dumps(lead_json.data))
        #     items = LeadItem.objects.filter(LeadID = obj.id)
        #     item_json = LeadItemSerializer(items, many=True)
        #     lead_json_dump['LeadItem'] = item_json.data
        #     allld.append(lead_json_dump)
        return Response({"message": "Success","status": 200,"data":allld})
    else:
        SalesPersonID = json_data['assignedTo']         
        print(SalesPersonID)
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        
        print(SalesPersonID)
        
        leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id")            
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            allld = showLead(leads_obj)
            #leads_json = LeadSerializer(leads_obj, many=True)
            # allld = []
            # for obj in leads_obj:
            #     lead_json = LeadSerializer(obj, many=False)
            #     lead_json_dump = json.loads(json.dumps(lead_json.data))
            #     items = LeadItem.objects.filter(LeadID = obj.id)
            #     item_json = LeadItemSerializer(items, many=True)
            #     lead_json_dump['LeadItem'] = item_json.data
            #     allld.append(lead_json_dump)
            return Response({"message": "Success","status": 200,"data":allld})         



# #Lead All Filter API
# @api_view(["POST"])
# def all_filter_junk_page(request):
#     json_data = request.data
    
#     PageNo = request.data['PageNo']
#     MaxSize = request.data['MaxSize']

#     page_obj = Pagination.objects.filter(MaxSize=MaxSize).first()
#     if MaxSize != "All":
#         size = int(page_obj.MaxSize)
#         endWith = (PageNo * size)
#         startWith = (endWith - size)
#     if len(json_data) == 0:
#         leads_obj = Lead.objects.filter(junk=1).order_by("-id")
#         #leads_json = LeadSerializer(leads_obj, many=True)
#         allld = []
#         for obj in leads_obj:
#             lead_json = LeadSerializer(obj, many=False)
#             lead_json_dump = json.loads(json.dumps(lead_json.data))
#             items = LeadItem.objects.filter(LeadID = obj.id)
#             item_json = LeadItemSerializer(items, many=True)
#             lead_json_dump['LeadItem'] = item_json.data
#             allld.append(lead_json_dump)
#         return Response({"message": "Success","status": 200,"data":allld})
#         #return Response({"message": "Success","status": 200,"data":leads_json.data})
#     else:
#         SalesPersonID = json_data['assignedTo']         
#         print(SalesPersonID)
#         emp_obj = Employee.objects.get(pk=SalesPersonID)
        
#         if emp_obj.role == 'manager':
#             emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
#             SalesPersonID=[SalesPersonID]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
            
#         elif emp_obj.role == 'admin':
#             emps = Employee.objects.filter(id__gt=0)
#             SalesPersonID=[]
#             for emp in emps:
#                 SalesPersonID.append(emp.id)
#         else:
#             SalesPersonID = [json_data['assignedTo']]
        
#         print(SalesPersonID)
#         if MaxSize != "":
#             leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id")[startWith:endWith] 
#             leads_count = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).count()
#         else:
#             leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id") 
#             leads_count = leads_obj.count()
#         if len(leads_obj) ==0:
#             return Response({"message": "Success","status": 200,"data":[]})
#         else:
#             #leads_json = LeadSerializer(leads_obj, many=True)
#             allld = []
#             for obj in leads_obj:
#                 lead_json = LeadSerializer(obj, many=False)
#                 lead_json_dump = json.loads(json.dumps(lead_json.data))
#                 items = LeadItem.objects.filter(LeadID = obj.id)
#                 item_json = LeadItemSerializer(items, many=True)
#                 lead_json_dump['LeadItem'] = item_json.data
#                 allld.append(lead_json_dump)
#             return Response({"message": "Success","status": 200,"data":allld, "extra":{"total_count":leads_count}})
#             #return Response({"message": "Success","status": 200,"data":leads_json.data})            



#Lead All Filter API
@api_view(["POST"])
def all_filter_junk_page(request):
    json_data = request.data
    
    PageNo = request.data['PageNo']
    MaxSize = request.data['MaxSize']

    page_obj = Pagination.objects.filter(MaxSize=MaxSize).first()
    if MaxSize != "All":
        size = int(page_obj.MaxSize)
        endWith = (PageNo * size)
        startWith = (endWith - size)
    if len(json_data) == 0:
        leads_obj = Lead.objects.filter(junk=1).order_by("-id")
        #leads_json = LeadSerializer(leads_obj, many=True)
        allld = []
        for obj in leads_obj:
            lead_json = LeadSerializer(obj, many=False)
            lead_json_dump = json.loads(json.dumps(lead_json.data))
            items = LeadItem.objects.filter(LeadID = obj.id)
            item_json = LeadItemSerializer(items, many=True)
            lead_json_dump['LeadItem'] = item_json.data
            allld.append(lead_json_dump)
        return Response({"message": "Success","status": 200,"data":allld})
        #return Response({"message": "Success","status": 200,"data":leads_json.data})
    else:
        SalesPersonID = json_data['assignedTo']         
        emp_obj = Employee.objects.get(pk=SalesPersonID)
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)

        else:
            SalesPersonID = [json_data['assignedTo']]

        leadType = request.data['leadType']
        search = request.data['search']
        status = request.data['status']
        toDate = request.data['toDate']
        fromDate = request.data['fromDate']
        assignTo = request.data['assignTo']
        createdBy = request.data['createdBy']
        print("SalesPersonID",SalesPersonID, Lead.objects.filter(junk=1).values("assignedTo"))
        # print(SalesPersonID)
        # if MaxSize != "All":
        #     leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id")[startWith:endWith] 
        #     # leads_count = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).count()
        # else:
        leads_obj = Lead.objects.filter(junk=1, assignedTo__in=SalesPersonID).order_by("-id") 
        leads_obj = leads_obj.filter(Q(companyName__icontains=search)|Q(phoneNumber__icontains=search)|Q(email__icontains=search)|Q(location__icontains=search)|Q(source__icontains=search)|Q(productInterest__icontains=search)|Q(date__icontains=search)|Q(contactPerson__icontains=search))
        print("ffffffffffff",leads_obj)
        if leads_obj:
            if status!="":
                leads_obj = leads_obj.filter(status=status)
            if fromDate!="":
                leads_obj = leads_obj.filter(date__gte=fromDate)
            if toDate!="":
                leads_obj = leads_obj.filter(date__lte=toDate)
            if assignTo!="":
                leads_obj = leads_obj.filter(assignedTo=assignTo)
            if createdBy!="":
                leads_obj = leads_obj.filter(employeeId=createdBy)
            if leadType != "All":
                leads_obj = leads_obj.filter(leadType=leadType)

        leads_count = leads_obj.count()
        print("leads_countleads_countleads_countleads_countleads_count",leads_count)
        if MaxSize != "All":
            leads_obj = leads_obj.order_by('-id')[startWith:endWith]
        if len(leads_obj) ==0:
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            #leads_json = LeadSerializer(leads_obj, many=True)
            allld = []
            for obj in leads_obj:
                lead_json = LeadSerializer(obj, many=False)
                lead_json_dump = json.loads(json.dumps(lead_json.data))
                items = LeadItem.objects.filter(LeadID = obj.id)
                item_json = LeadItemSerializer(items, many=True)
                lead_json_dump['LeadItem'] = item_json.data
                allld.append(lead_json_dump)
            return Response({"message": "Success","status": 200,"data":allld, "extra":{"total_count":leads_count}})
            #return Response({"message": "Success","status": 200,"data":leads_json.data})            







#Lead One API
@api_view(["POST"])
def one(request):
    id=request.data['id']    
    lead_obj = Lead.objects.filter(id=id)
    result = showLead(lead_obj)
    return Response({"message": "Success","status": 200,"data":result})

    # lead_obj = Lead.objects.get(id=id)
    # #lead_json = LeadSerializer(lead_obj)
    # lead_json = LeadSerializer(lead_obj, many=False)
    # lead_json_dump = json.loads(json.dumps(lead_json.data))
    # items = LeadItem.objects.filter(LeadID = lead_obj.id)
    # item_json = LeadItemSerializer(items, many=True)
    # lead_json_dump['LeadItem'] = item_json.data
    # return Response({"message": "Success","status": 200,"data":[lead_json_dump]})

#Lead Update API
@api_view(['POST'])
def update(request):
    print(request.data)
    fetchid = request.data['id']
    try:
        model = Lead.objects.get(pk = fetchid)
        model.date  = request.data['date']
        model.location  = request.data['location']
        model.companyName  = request.data['companyName']
        model.numOfEmployee  = request.data['numOfEmployee']
        model.turnover  = request.data['turnover']
        model.source  = request.data['source']
        model.contactPerson  = request.data['contactPerson']
        model.designation  = request.data['designation']
        model.phoneNumber  = request.data['phoneNumber']
        model.alter_phone  = request.data['alter_phone']
        model.message  = request.data['message']
        model.email  = request.data['email']
        model.alter_email  = request.data['alter_email']
        model.status  = request.data['status']
        model.leadType  = request.data['leadType']
        model.productInterest  = request.data['productInterest']
        model.assignedTo_id  = request.data['assignedTo']
        model.employeeId_id  = request.data['employeeId']
        model.timestamp  = request.data['timestamp']
        model.UpdateDate  = request.data['UpdateDate']
        model.junk  = request.data['junk']

        model.save()
        lditems = LeadItem.objects.filter(LeadID=fetchid)
        for lditem in lditems:
            print(lditem.ItemCode)
            if not lditem.ItemCode in list(request.data['LeadItem']):
                    print("Delete")
                    print(lditem.ItemCode)
                    LeadItem.objects.get(LeadID=fetchid,ItemCode=lditem.ItemCode).delete()
        if len(request.data['LeadItem']) !=0:
            for item in request.data['LeadItem']:
                if not LeadItem.objects.filter(ItemCode=item,LeadID=fetchid).exists():
                    try:
                        if (Item.objects.filter(ItemCode=item).exists()):
                            it = Item.objects.get(ItemCode=item)                    
                            model_lines = LeadItem(LeadID = fetchid, UnitPrice = it.UnitPrice, DiscountPercent = it.Discount, ItemCode = it.ItemCode, ItemName = it.ItemName, ItemDescription = it.Description, TaxCode = it.TaxCode)
                            model_lines.save()
                        else:
                            return Response({"message":"ItemCode not Exist","status":201,"data":[]})
                    except Exception as e:
                        return Response({"message":str(e),"status":201,"data":[]})
        return Response({"message":"successful","status":200,"data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Lead delete
@api_view(['POST'])
def delete(request):
    fetchids=request.data['id']
    naid = []
    for fetchid in fetchids:
        if Lead.objects.filter(pk=fetchid).exists():
           fetchdata=Lead.objects.filter(pk=fetchid).delete()
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})

#Lead Mark Junk
@api_view(['POST'])
def mark_junk(request):
    fetchids=request.data['id']
    status=request.data['status']
    naid = []
    for fetchid in fetchids:
        print(fetchid)
        if Lead.objects.filter(pk=fetchid).exists():
           fetchdata=Lead.objects.filter(pk=fetchid).update(junk=status)
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})


# @api_view(['POST'])
# def delete(request):
    # fetchid=request.data['id']
    # try:
        # fetchdata=Lead.objects.filter(pk=fetchid).delete()
        # return Response({"message":"successful","status":"200","data":[]})
    # except:
         # return Response({"message":"Id wrong","status":"201","data":[]})

#Lead Assign
@api_view(['POST'])
def assign(request):
    fetchids=request.data['id']
    empid=request.data['employeeId']
    emp=Employee.objects.get(pk=empid)
    naid = []
    for fetchid in fetchids:
        if Lead.objects.filter(pk=fetchid).exists():
           model=Lead.objects.get(pk=fetchid)
           model.assignedTo = emp
           model.save()
        else:
            naid.append(fetchid)
    print(str(naid))
    return Response({"message":"successful","status":"200","data":[]})
             #return Response({"message":"Id wrong","status":"201","data":[]})

#Type Create API
@api_view(['POST'])
def type_create(request):
    Name = request.data['Name']    
    if Type.objects.filter(Name=Name).exists():        
        return Response({"message":"Already exist","status":409,"data":[]})
    else:        
        try:
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']

            model=Type(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)
            
            model.save()
            
            tp = Type.objects.latest('id')        
            
            return Response({"message":"successful","status":200,"data":[{"id":tp.id}]})
        except Exception as e:
            return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})
        
#Type Update API
@api_view(['POST'])
def type_update(request):
    fetchid = request.data['id']
    try:
        model = Type.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})

        
#Source Create API
@api_view(['POST'])
def source_create(request):
    Name = request.data['Name']    
    if Source.objects.filter(Name=Name).exists():        
        return Response({"message":"Already exist","status":409,"data":[]})
    else:        
        try:
            CreatedDate = request.data['CreatedDate']
            CreatedTime = request.data['CreatedTime']
            model=Source(Name = Name, CreatedDate = CreatedDate, CreatedTime = CreatedTime)            
            model.save()            
            sc = Source.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":sc.id}]})
        except Exception as e:
            return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})        

#Type Update API
@api_view(['POST'])
def source_update(request):
    fetchid = request.data['id']
    try:
        model = Source.objects.get(pk = fetchid)
        model.Name  = request.data['Name']
        model.CreatedDate  = request.data['CreatedDate']
        model.CreatedTime  = request.data['CreatedTime']
        model.save()
        return Response({"message":"successful","status":200,"data":[request.data]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})

#LeadType All API
@api_view(["GET"])
def type_all(request):
    type_obj = Type.objects.all()        
    type_json = TypeSerializer(type_obj, many=True)
    return Response({"message": "Success","status": 200,"data":type_json.data})


#SourceType All API
@api_view(["GET"])
def source_all(request):
    source_obj = Source.objects.all()        
    source_json = SourceSerializer(source_obj, many=True)
    return Response({"message": "Success","status": 200,"data":source_json.data})

#Type delete
@api_view(['POST'])
def type_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Type.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})


#Source delete
@api_view(['POST'])
def source_delete(request):
    fetchid=request.data['id']
    try:
        fetchdata=Source.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})


# ####################################################################
# ####################################################################
# ####################################################################
def showLead(objs):
    allLead = []
    for obj in objs:
        lead_json = LeadSerializer(obj, many=False)
        lead_json_dump = json.loads(json.dumps(lead_json.data))
        items = LeadItem.objects.filter(LeadID = obj.id)
        item_json = LeadItemSerializer(items, many=True)
        lead_json_dump['LeadItem'] = item_json.data

        LastFollowup = ""
        # if Chatter.objects.filter(SourceType = 'Lead', SourceID = obj.id, UpdateDate = currentDate).exists():
        if ActivityChatter.objects.filter(SourceType = 'Lead', SourceID = obj.id).exists():
            act_obj = ActivityChatter.objects.filter(SourceType = 'Lead', SourceID = obj.id).order_by('-id')[0]
            LastFollowup = act_obj.Message

        lead_json_dump['LastFollowup'] = LastFollowup
        allLead.append(lead_json_dump)
    return allLead

# tempMethod for employe tree ids
@api_view(['POST'])
def getEmps(request):
    try:
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        result = getAllReportingToIds(SalesEmployeeCode)

        return Response({"message":"successful","status":"200","data":result})
    except Exception as e:
        return Response({"message":str(e), "status":"201", "data":[]})



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Lead All Filter API
@api_view(["POST"])
def all_count(request):
    json_data = request.data
    if len(json_data) == 0:
        leads_obj = Lead.objects.filter(junk=0).count()
        return Response({"message": "Success","status": 200,"data":[{"lead_count":leads_obj}]})
    else:
        SalesPersonID = json_data['assignedTo']                      
        emp_obj = Employee.objects.get(pk=SalesPersonID)             
        
        if emp_obj.role == 'manager':
            emps = Employee.objects.filter(reportingTo=emp_obj.SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
            SalesPersonID=[SalesPersonID]
            for emp in emps:
                SalesPersonID.append(emp.id)
            
        elif emp_obj.role == 'admin':
            emps = Employee.objects.filter(id__gt=0)
            SalesPersonID=[]
            for emp in emps:
                SalesPersonID.append(emp.id)
        else:
            SalesPersonID = [json_data['assignedTo']]
        leadType = request.data['leadType']
        
        if leadType =="None":
            leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID).count()
        elif leadType !="All":
            leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID, leadType=leadType,junk=0).count()
        else:
            leads_obj = Lead.objects.filter(assignedTo__in=SalesPersonID,junk=0).count()                   
        if leads_obj ==0:
            return Response({"message": "Success","status": 200,"data":[[{"lead_count":0}]]})
        else:
            return Response({"message": "Success","status": 200,"data":[{"lead_count":leads_obj}]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#added by millan on 06-October-2022 for adding attachment
@api_view(["POST"])
def lead_attachment_create(request):
    try:
        lead_id = request.data['lead_id']
        CreateDate = request.data['CreateDate']
        CreateTime = request.data['CreateTime']
        CreatedBy = request.data['CreatedBy']
        print(request.FILES.getlist('Attach'))
        for File in request.FILES.getlist('Attach'):
            attachmentsImage_url = ""
            target ='./bridge/static/image/LeadAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attachmentsImage_url = productImage_url.replace('/bridge', '')
            print(attachmentsImage_url)

            att=LeadAttachment(File=attachmentsImage_url, LeadId=lead_id, CreateDate=CreateDate, CreateTime=CreateTime, CreatedBy=CreatedBy, Size=Size)
            
            att.save()  
            
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"message": "Error","status": 201,"data":str(e)})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#for updating attachment
@api_view(['POST'])
def lead_attachment_update(request):
    try:
        lead_id = request.data['lead_id']
        fetchid = request.data['id']
        
        File = request.data['Attach']
        
        model = LeadAttachment.objects.get(pk = fetchid, LeadId=lead_id)
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']
        
        model.UpdatedBy = request.data['UpdatedBy']

        attechmentsImage_url = ""
        if File:
            target ='./bridge/static/image/LeadAttachment'
            os.makedirs(target, exist_ok=True)
            fss = FileSystemStorage()
            file = fss.save(target+"/"+File.name, File)
            file_size = os.stat(file)
            Size = file_size.st_size
            productImage_url = fss.url(file)
            attechmentsImage_url = productImage_url.replace('/bridge', '')
            print(attechmentsImage_url)
            model.File = attechmentsImage_url
            model.Size = Size
        else:
            model.File= model.File
            print('no image')
        
        model.save()
        
        return Response({"message": "success","status": 200,"data":[]})
    except Exception as e:
        return Response({"status":"201","message":"error","data":[str(e)]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#for deleting an attachment
@api_view(['POST'])
def lead_attachment_delete(request):
    try:
        fetchid = request.data['id']
        
        lead_id = request.data['lead_id']
        
        if LeadAttachment.objects.filter(pk=fetchid, LeadId=lead_id).exists():
            
            LeadAttachment.objects.filter(pk=fetchid, LeadId=lead_id).delete()
            
            return Response({"message":"successful","status":"200","data":[]})
        else:
            return Response({"message":"ID Not Found","status":"201","data":[]})
        
    except Exception as e:
        return Response({"message":str(e),"status":"201","data":[]})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#get all attachment based on lead id
@api_view(["POST"])
def lead_attachments(request):
    try:
        lead_id=request.data['lead_id']
        if lead_id > 0:
            leadAttachObjs = LeadAttachment.objects.filter(LeadId = lead_id)
            leadAttachArr = []
            for attchObj in leadAttachObjs:
                leadAttachjson = LeadAttachmentSerilaizer(attchObj)
                leadData = json.loads(json.dumps(leadAttachjson.data))
                CreatedBy = attchObj.CreatedBy
                UpdatedBy = attchObj.UpdatedBy
                
                if leadData['CreatedBy'] > 0:
                    empObj = Employee.objects.filter(pk = CreatedBy).values('firstName', 'lastName')
                    leadData['CreatedBy'] = empObj
                    leadAttachArr.append(leadData)
                if leadData['UpdatedBy'] > 0:
                    empObj = Employee.objects.filter(pk = UpdatedBy).values('firstName', 'lastName')
                    leadData['UpdatedBy'] = empObj
                    leadAttachArr.append(leadData)
                
            return Response({"message": "Success","status": 200,"data":leadAttachArr})
        else:
            return Response({"message": "Customer ID Not Found","status": 201,"data":[]})
    except Exception as e: 
        return Response({"message": "Error","status": 201,"data":str(e)})
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>