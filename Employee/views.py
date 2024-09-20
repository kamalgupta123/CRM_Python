from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse

from Item.models import Item
from Item.serializers import ItemSerializer
from .forms import EmployeeForm  
from .models import *
from Activity.models import Activity
from Lead.models import Lead
from Invoice.models import Invoice
from Notification.models import Notification
import requests, json

from pytz import timezone
from datetime import date, datetime as dt, timedelta
from collections import Counter

from Order.models import Order, DocumentLines as OrderDocumentLines
from Invoice.models import Invoice, DocumentLines as InvoiceDocumentLines

from Mylib import *

tdate = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

from BusinessPartner.models import BusinessPartner
from Opportunity.models import Opportunity
from Order.models import Order, DocumentLines
from Quotation.models import Quotation

from django.contrib import messages

from django.db.models import Sum, F #added by millan on 05-September-2022

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import EmployeeSerializer
from Opportunity.serializers import OpportunitySerializer
from rest_framework.parsers import JSONParser
# Create your views here.  
    
#print(config())

@api_view(["GET"])
def top5itembyamount(request):
    #added by millan on 05-September-2022
    try:
        top2bp = InvoiceDocumentLines.objects.values('ItemCode').annotate(Total = Sum(F('Quantity')*F('UnitPrice'))).order_by('-Total')[:5]
    
        top5=[]

        for od in top2bp:
            top5dt = InvoiceDocumentLines.objects.filter(ItemCode = od['ItemCode']).values('ItemDescription')
            for desc in top5dt:
                print(desc)
            top5.append({"ItemCode":od['ItemCode'], "ItemName":desc['ItemDescription'], "Total":od['Total']})
        
        return Response({"message": "Success","status": 200,"data":top5}) #added by millan on 05-September-2022
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})

@api_view(["GET"])
def top5bp(request):

    try:
        
        #added by millan on 05-September-2022
        top2bp = Order.objects.values('CardCode').annotate(Total = Sum(F('DocTotal'))).order_by('-Total')[:5]
        print(top2bp)
        top5=[]
        for od in top2bp:
            try:
                cd = BusinessPartner.objects.filter(CardCode = od['CardCode']).values('CardName')
                for cName in cd:
                    print(cName)
                top5.append({"CardCode":od['CardCode'], "CardName":cName['CardName'], 'Total':od['Total']})
            except Exception as e:
                top5.append({"CardCode":od['CardCode'], "CardName":od['CardCode'], 'Total':od['Total']})
            
        return Response({"message": "Success","status": 200,"data":top5})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})



@api_view(["POST"])
def analytics(request):

    json_data = request.data
    month = int(json_data['month'])
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
            print(SalesEmployeeCode)
            
            tgt_all = Target.objects.filter(SalesPersonCode__in=SalesEmployeeCode).exclude(monthYear=yearmonth).order_by("-monthYear")[:month]
            #{"month":"3", "SalesEmployeeCode":"3"}
            amount = sum(tgt_all.values_list('amount', flat=True))            
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)
            
            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)
            
            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)
            
            notification = Notification.objects.filter(Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)
            
            
            return Response({"message": "Success","status": 200,"data":[{"notification":notification, "amount":amount, "sale":sale, "sale_diff":sale_diff}]})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})


#Target Create API
@api_view(['POST'])
def target(request):
    try:
        amount = request.data['amount']
        monthYear = request.data['monthYear']
        SalesPersonCode = request.data['SalesPersonCode']
        #sale = request.data['sale']
        #sale_diff = request.data['sale_diff']
        CreatedDate = request.data['CreatedDate']        
        model = Target(amount=amount, monthYear=monthYear, SalesPersonCode=SalesPersonCode, CreatedDate=CreatedDate, UpdatedDate=CreatedDate)
        model.save()
        
        tgt = Target.objects.latest('id')
        print(tgt.id)
        return Response({"message":"Success","status":"200","data":[]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})


@api_view(["POST"])
def dashboard(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emp_ids = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode).values_list('id', flat=True)
            print(emp_ids)
            #{"SalesEmployeeCode":4}
            
            lead_all = Lead.objects.filter(assignedTo__in=emp_ids).count()
            print(lead_all)
            
            opp_all = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode).count()
            #print(opp_all)
            
            quot_all = Quotation.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            #print(quot_all)
            
            ord_all = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            #print(ord_all)
            
            #bp_all = BusinessPartner.objects.filter(SalesPersonCode__in=SalesEmployeeCode).count()
            bp_all = BusinessPartner.objects.all().count()
            #print(bp_all)
            
            tgt_all = Target.objects.filter(SalesPersonCode__in=SalesEmployeeCode, monthYear=yearmonth)
            
            amount = sum(tgt_all.values_list('amount', flat=True))            
            print(amount)
            #amount = "{:.2f}".format(amount)
            #print(amount)
            
            sale = sum(tgt_all.values_list('sale', flat=True))
            print(sale)
            
            sale_diff = sum(tgt_all.values_list('sale_diff', flat=True))
            print(sale_diff)
            
            notification = Notification.objects.filter(Emp=emp_obj.id, CreatedDate=tdate, Read=0).order_by("-id").count()
            print(notification)

            ord_over = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__lt=tdate).count()
            print(ord_over)
            print(date)
            
            ord_open = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Open", DocDueDate__gte=tdate).count()
            print(ord_open)

            ord_close = Order.objects.filter(SalesPersonCode__in=SalesEmployeeCode, DocumentStatus="bost_Close").count()
            print(ord_close)
			
            #{"SalesEmployeeCode":"2"}
            return Response({"message": "Success","status": 200,"data":[{"notification":notification, "amount":amount, "sale":sale, "sale_diff":sale_diff, "Opportunity":opp_all, "Quotation":quot_all, "Order":ord_all, "Customer":bp_all, "Leads":lead_all, "Over":ord_over, "Open":ord_open, "Close":ord_close}]})
            
            #return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

@api_view(["POST"])
def invoice_counter(request):
    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[str(SalesEmployeeCode)]
                for emp in emps:
                    SalesEmployeeCode.append(str(emp.SalesEmployeeCode))
            else:
                SalesEmployeeCode=[str(SalesEmployeeCode)]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            #live=0
            inv_count = len(Invoice.objects.filter(SalesPersonCode__in=SalesEmployeeCode))
     
            return Response({"message": "Success","status": 200,"data":[{"Invoice":inv_count}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})

#Employee Create API
@api_view(['POST'])
def create(request):
    try:
        companyID = request.data['companyID']
        SalesEmployeeCode = request.data['SalesEmployeeCode']
        SalesEmployeeName = request.data['SalesEmployeeName']
        EmployeeID = request.data['EmployeeID']
        userName = request.data['userName']
        password = request.data['password']
        firstName = request.data['firstName']
        middleName = request.data['middleName']
        lastName = request.data['lastName']
        Email = request.data['Email']
        Mobile = request.data['Mobile']
        role = request.data['role']
        position = request.data['position']
        branch = request.data['branch']
        Active = request.data['Active']
        #passwordUpdatedOn = request.data['passwordUpdatedOn']
        #lastLoginOn = request.data['lastLoginOn']
        #logedIn = request.data['logedIn']
        reportingTo = request.data['reportingTo']
        timestamp = request.data['timestamp']

        model=Employee(companyID = companyID, SalesEmployeeCode = SalesEmployeeCode, SalesEmployeeName = SalesEmployeeName, EmployeeID = EmployeeID, userName = userName, password = password, firstName = firstName, middleName = middleName, lastName = lastName, Email = Email, Mobile = Mobile, role = role, position = position, branch = branch, Active=Active, reportingTo = reportingTo, timestamp = timestamp)
        
        model.save()
        
        sp = Employee.objects.latest('id')        
        sp.SalesEmployeeCode = sp.id
        sp.save()
        
        return Response({"message":"successful","status":200,"data":[{"Sp_Id":sp.id, "SalesEmployeeCode":sp.id}]})
    except Exception as e:
        return Response({"message":"Can not create","status":"201","data":[{"Error":str(e)}]})

#Employee All API
@api_view(["GET"])
def all(request):
    
    employees_obj = Employee.objects.all() 
    employee_json = EmployeeSerializer(employees_obj, many=True)
    return Response({"message": "Success","status": 200,"data":employee_json.data})

@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
                # emps = Employee.objects.filter(reportingTo=emp_obj.reportingTo)#.values('id', 'SalesEmployeeCode')
                # SalesEmployeeCode=[]
                # for emp in emps:
                    # SalesEmployeeCode.append(emp.SalesEmployeeCode)
            
            print(SalesEmployeeCode)
            
            emps_all = Employee.objects.filter(SalesEmployeeCode__in=SalesEmployeeCode)
            
            emps_json = EmployeeSerializer(emps_all, many=True)
            return Response({"message": "Success","status": 200,"data":emps_json.data})
            
            return Response({"message": "Success","status": 201,"data":[{"emp":SalesEmployeeCode}]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
               

#Employee All Filter API
@api_view(["POST"])
def all_filter_old(request):
    json_data = request.data
    
    if len(json_data) == 0:
        emps_obj = Employee.objects.all().order_by("-id")
        emps_json = EmployeeSerializer(emps_obj, many=True)
        return Response({"message": "Success","status": 200,"data":emps_json.data})
    else:
        #print(json_data.keys()[0])
        #if json_data['U_FAV']
        for ke in json_data.keys():
            if ke =='reportingTo' :
                if json_data['reportingTo'] !='':
                    emps_obj = Employee.objects.filter(reportingTo=json_data['reportingTo']).order_by("-id")
                    if len(emps_obj) ==0:
                        return Response({"message": "Not Available","status": 201,"data":[]})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":emps_json.data})
            elif ke =='role' :
                if json_data['role'] !='':
                    emps_obj = Employee.objects.filter(role=json_data['role']).order_by("-id")
                    if len(emps_obj) ==0:
                        return Response({"message": "Not Available","status": 201,"data":[]})
                    else:
                        emps_json = EmployeeSerializer(emps_obj, many=True)
                        return Response({"message": "Success","status": 200,"data":emps_json.data})
            else:
                return Response({"message": "Not Available","status": 201,"data":[]})

#Employee One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    employee_obj = Employee.objects.get(id=id)
    employee_json = EmployeeSerializer(employee_obj)
    return Response({"message": "Success","status": 200,"data":[employee_json.data]})

#Employee Login API
@api_view(["POST"])
def login(request):
    userName=request.data['userName']
    password=request.data['password']
    FCM = request.data['FCM']
    msg=[]
    try:
        employee_obj = Employee.objects.get(userName=userName,password=password)
        if FCM !="":
            employee_obj.FCM = FCM
            employee_obj.save()
        employee_json = EmployeeSerializer(employee_obj)
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
        data = json.loads(db)
        print(data)
        #{"userName":"admin", "password":"1234", "FCM":"1s45sd5s5d4"}

        return Response({"message": "Success","status": 200,"data":employee_json.data, "SAP":data})
        
    except:
        return Response({"message": "Username or Password is incorrect","status": 404,"data":[]})
		
#Employee Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Employee.objects.get(pk = fetchid)

        model.companyID = request.data['companyID']
        model.SalesEmployeeName = request.data['SalesEmployeeName']
        model.EmployeeID = request.data['EmployeeID']
        model.userName = request.data['userName']
        model.password = request.data['password']
        model.firstName = request.data['firstName']
        model.middleName = request.data['middleName']
        model.lastName = request.data['lastName']
        model.Email = request.data['Email']
        model.Mobile = request.data['Mobile']
        model.role = request.data['role']
        model.position = request.data['position']
        model.branch = request.data['branch']
        model.Active = request.data['Active']
        model.reportingTo = request.data['reportingTo']

        model.save()
        
        return Response({"message":"successful","status":200, "data":[request.data]})
    except:
        return Response({"message":"ID Wrong","status":"201","data":[request.data]})

#Employee delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        emp=Employee.objects.get(pk=fetchid)
        
        Employee.objects.filter(pk=fetchid).delete()
        
        return Response({"message":"successful","status":"200","data":[]})
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})




# most order item in last 30 days
@api_view(['GET'])
def movingitems(request):
    try:
        fastMovingdate = date.today() - timedelta(days=15)
        slowMovingdate = date.today() - timedelta(days=30)

        print(fastMovingdate)
        print(slowMovingdate)

        itemCodeList = []
        fastMovingItemList = []
        # ----------------------------------------------------------------------------
        # ------------------------- Fast Moving Items --------------------------------
        # ----------------------------------------------------------------------------
        fastMovingOrder_obj = Order.objects.filter(CreateDate__gte = fastMovingdate)
        fastMovingItemCodeArr = []
        for order in fastMovingOrder_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                # print(docLine)
                # docJason = DocumentLinesSerializer(docLine);
                itemCode = docLine.ItemCode
                itemObj = Item.objects.get(ItemCode = itemCode)
                itemJson = ItemSerializer(itemObj)

                if itemCode not in fastMovingItemCodeArr:
                    fastMovingItemList.append(itemJson.data)
                    fastMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        FastItemsCount = len(fastMovingItemCodeArr)
        
        # ----------------------------------------------------------------------------
        # ------------------------- Slow Moving Itmes --------------------------------
        # ----------------------------------------------------------------------------
        slowMovingdate_obj = Order.objects.filter(CreateDate__lte = fastMovingdate, CreateDate__gte = slowMovingdate)
        slowMovingItemCodeArr = []
        slowMovingItemList = []
        for order in slowMovingdate_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                # docJason = DocumentLinesSerializer(docLine);
                itemCode = docLine.ItemCode
                itemObj = Item.objects.get(ItemCode = itemCode)
                itemJson = ItemSerializer(itemObj)
                if itemCode not in fastMovingItemCodeArr:
                    slowMovingItemList.append(itemJson.data)
                    slowMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)
        
        SlowItemsCount = len(slowMovingItemCodeArr)

        dictItem = set(itemCodeList)
        # notMovingItemCount = Item.objects.all().exclude(ItemCode__in = dictItem).count()
        notMovingItemObj = Item.objects.all().exclude(ItemCode__in = dictItem)
        notMovingItemJson = ItemSerializer(notMovingItemObj, many=True)
        notMovingItemCount = len(notMovingItemObj)
        context = {
            "FastMovingItemsList": fastMovingItemList,
            "FastItemsCount": FastItemsCount,
            "SlowMovingItemsList": slowMovingItemList,
            "SlowItemsCount": SlowItemsCount,
            "NotMovingItemsList": notMovingItemJson.data,
            "NotMovingItemsCount": notMovingItemCount
        }

        print(FastItemsCount)
        print(SlowItemsCount)
        print(notMovingItemCount)

        return Response({"message":"successful","status":200,"data":[context]})
    except Exception as e:
        return Response({"message":"Error","status":201,"data":[str(e)]})

# most order item in last 30 days
@api_view(['GET'])
def movingitems_count(request):
    try:
        fastMovingdate = date.today() - timedelta(days=15)
        slowMovingdate = date.today() - timedelta(days=30)
        itemCodeList = []
        # --------------------------------------------------------------------------
        # ------------------------- Fast Moving Items ------------------------------
        # --------------------------------------------------------------------------
        fastMovingOrder_obj = Order.objects.filter(CreateDate__gte = fastMovingdate)
        fastMovingItemCodeArr = []
        for order in fastMovingOrder_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    fastMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)

        FastItemsCount = len(fastMovingItemCodeArr)
        
        # ----------------------------------------------------------------------------
        # ------------------------- Slow Moving Itmes --------------------------------
        # ----------------------------------------------------------------------------
        slowMovingdate_obj = Order.objects.filter(CreateDate__lte = fastMovingdate, CreateDate__gte = slowMovingdate)
        slowMovingItemCodeArr = []
        for order in slowMovingdate_obj:
            order_id = order.id
            docLineObj = OrderDocumentLines.objects.filter(OrderID = order_id)
            for docLine in docLineObj:
                itemCode = docLine.ItemCode
                if itemCode not in fastMovingItemCodeArr:
                    slowMovingItemCodeArr.append(itemCode)
                    itemCodeList.append(itemCode)
        
        SlowItemsCount = len(slowMovingItemCodeArr)

        # --------------------------------------------------------------------------
        # ------------------------- Not Moving Itmes -------------------------------
        # --------------------------------------------------------------------------
        dictItem = set(itemCodeList)
        notMovingItemCount = Item.objects.all().exclude(ItemCode__in = dictItem).count()

        context = {
            "FastItemsCount": FastItemsCount,
            "SlowItemsCount": SlowItemsCount,
            "NotMovingItemsCount": notMovingItemCount
        }

        return Response({"message":"successful","status":200,"data":[context]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[str(e)]})

@api_view(["POST"])
def opportunity_bystage(request):

    json_data = request.data
    
    if "SalesEmployeeCode" in json_data:
        print("yes")
        
        if json_data['SalesEmployeeCode']!="":
            SalesEmployeeCode = json_data['SalesEmployeeCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesEmployeeCode)
            if emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesEmployeeCode=[]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)                    
            elif emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesEmployeeCode)#.values('id', 'SalesEmployeeCode')
                SalesEmployeeCode=[SalesEmployeeCode]
                for emp in emps:
                    SalesEmployeeCode.append(emp.SalesEmployeeCode)
            else:
                SalesEmployeeCode=[SalesEmployeeCode]
            print(SalesEmployeeCode)
            
            opp_Lead_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Lead").count()
            opp_Need_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Need Analysis").count()
            opp_Quotation_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Quotation").count()
            opp_Negotiation_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Negotiation").count()
            opp_Order_count = Opportunity.objects.filter(SalesPerson__in=SalesEmployeeCode, CurrentStageName="Order").count()
            
            opportunity_context = {
                "Lead": opp_Lead_count,
                "NeedAnalysis": opp_Need_count,
                "Quotation": opp_Quotation_count,
                "Negotiation": opp_Negotiation_count,
                "Order": opp_Order_count
            }
            
            return Response({"message": "Success","status": 200,"data":[opportunity_context]})
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
    else:
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesEmployeeCode?"}]})
