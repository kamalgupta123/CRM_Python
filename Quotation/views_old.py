from django.shortcuts import render, redirect  
from django.http import JsonResponse, HttpResponse
from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response
from .serializers import *
from rest_framework.parsers import JSONParser
# Create your views here.  

#Quotation Create API
@api_view(['POST'])
def create(request):
    TaxDate = request.data['TaxDate']
    DocDueDate = request.data['DocDueDate']
    DocDate = request.data['DocDate']
    ContactPersonCode = request.data['ContactPersonCode']
    DiscountPercent = request.data['DiscountPercent']
    CardCode = request.data['CardCode']
    CardName = request.data['CardName']
    Comments = request.data['Comments']
    SalesPersonCode = request.data['SalesPersonCode']
    U_OPPID = request.data['U_OPPID']
    U_OPPRNM = request.data['U_OPPRNM']
    U_QUOTNM = request.data['U_QUOTNM']
    
    CreateDate = request.data['CreateDate']
    CreateTime = request.data['CreateTime']
    UpdateDate = request.data['UpdateDate']
    UpdateTime = request.data['UpdateTime']
    
    lines = request.data['DocumentLines']
    DocTotal=0
    for line in lines:
        DocTotal = float(DocTotal) + float(line['Quantity']) * float(line['UnitPrice'])
    print(DocTotal)

    model=Quotation(TaxDate = TaxDate, DocDueDate = DocDueDate, ContactPersonCode = ContactPersonCode, DiscountPercent = DiscountPercent, DocDate = DocDate, CardCode = CardCode, CardName = CardName, Comments = Comments, SalesPersonCode = SalesPersonCode, DocumentStatus="bost_Open", DocTotal = DocTotal, U_OPPID=U_OPPID, U_OPPRNM=U_OPPRNM, U_QUOTNM=U_QUOTNM, U_FAV='N', CreateDate = CreateDate, CreateTime = CreateTime, UpdateDate = UpdateDate, UpdateTime = UpdateTime)
    
    model.save()
    qt = Quotation.objects.latest('id')
    
    addr = request.data['AddressExtension']
    
    model_add = AddressExtension(QuotationID = qt.id, BillToBuilding = addr['BillToBuilding'], ShipToState = addr['ShipToState'], BillToCity = addr['BillToCity'], ShipToCountry = addr['ShipToCountry'], BillToZipCode = addr['BillToZipCode'], ShipToStreet = addr['ShipToStreet'], BillToState = addr['BillToState'], ShipToZipCode = addr['ShipToZipCode'], BillToStreet = addr['BillToStreet'], ShipToBuilding = addr['ShipToBuilding'], ShipToCity = addr['ShipToCity'], BillToCountry = addr['BillToCountry'], U_SCOUNTRY = addr['U_SCOUNTRY'], U_SSTATE = addr['U_SSTATE'], U_SHPTYPB = addr['U_SHPTYPB'], U_BSTATE = addr['U_BSTATE'], U_BCOUNTRY = addr['U_BCOUNTRY'], U_SHPTYPS = addr['U_SHPTYPS'])
    
    model_add.save()
    
    LineNum = 0
    for line in lines:
        model_lines = DocumentLines(LineNum = LineNum, QuotationID = qt.id, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'])
        model_lines.save()
        LineNum=LineNum+1
    
    #return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id}]})

    with open("../bridge/bridge/db.json") as f:
        db = f.read()
        data = json.loads(db)
    
    r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
    token = json.loads(r.text)['SessionId']
    print(token)
    
    qt_data = {
		"TaxDate": request.data['TaxDate'],
		"DocDueDate": request.data['DocDueDate'],
		"DocDate": request.data['DocDate'],
		"ContactPersonCode": request.data['ContactPersonCode'],
		"DiscountPercent": request.data['DiscountPercent'],
		"CardCode": request.data['CardCode'],
		"CardName": request.data['CardName'],
		"Comments": request.data['Comments'],
		"SalesPersonCode": request.data['SalesPersonCode'],
		"AddressExtension": {
			"BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
			"ShipToState": request.data['AddressExtension']['ShipToState'],
			"BillToCity": request.data['AddressExtension']['BillToCity'],
			"ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
			"BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
			"ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
			"BillToState": request.data['AddressExtension']['BillToState'],
			"ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
			"BillToStreet": request.data['AddressExtension']['BillToStreet'],
			"ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
			"ShipToCity": request.data['AddressExtension']['ShipToCity'],
			"BillToCountry": request.data['AddressExtension']['BillToCountry']
		},
		"DocumentLines": lines
	}
    
    print(qt_data)
    print(json.dumps(qt_data))

    res = requests.post('http://103.107.67.94:50001/b1s/v1/Quotations', data=json.dumps(qt_data), cookies=r.cookies, verify=False)
    live = json.loads(res.text)
    
    fetchid = qt.id
    
    if "DocEntry" in live:
        print(live['DocEntry'])
        
        model = Quotation.objects.get(pk = fetchid)
        model.DocEntry = live['DocEntry']
        model.save()
        
        return Response({"message":"successful","status":200,"data":[{"qt_Id":qt.id, "DocEntry":live['DocEntry']}]})
    else:
        SAP_MSG = live['error']['message']['value']
        print(SAP_MSG)
        if "already exists" in SAP_MSG:
            fetchdata=Quotation.objects.filter(pk=fetchid).delete()
            return Response({"message":"Not created","SAP_error":SAP_MSG, "status":202,"data":[]})
        else:
            return Response({"message":"Partely successful","SAP_error":SAP_MSG, "status":202,"data":[]})


#Quotation Fav Update API
@api_view(['POST'])
def fav(request):
    fetchid = request.data['id']
    model = Quotation.objects.get(pk = fetchid)
    model.U_FAV  = request.data['U_FAV']
    model.save()
    return Response({"message":"successful","status":200, "data":[]})

#Quotation Update API
@api_view(['POST'])
def approve(request):
    fetchid = request.data['id']
    try:
        model = Quotation.objects.get(pk = fetchid)
        model.U_APPROVEID = request.data['U_APPROVEID']
        model.U_APPROVENM = request.data['U_APPROVENM']
        model.save()
        return Response({"message":"successful","status":200, "data":[]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})

#Quotation Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Quotation.objects.get(pk = fetchid)
        model.TaxDate = request.data['TaxDate']
        model.DocDate = request.data['DocDate']
        model.DocDueDate = request.data['DocDueDate']
        model.ContactPersonCode = request.data['ContactPersonCode']
        model.DiscountPercent = request.data['DiscountPercent']
        model.Comments = request.data['Comments']
        model.SalesPersonCode = request.data['SalesPersonCode']
        
        model.U_QUOTNM = request.data['U_QUOTNM']
        
        model.UpdateDate = request.data['UpdateDate']
        model.UpdateTime = request.data['UpdateTime']

        model.save()
        
        model_add = AddressExtension.objects.get(id = request.data['AddressExtension']['id'])
        print(model_add)
        
        model_add.BillToBuilding = request.data['AddressExtension']['BillToBuilding']
        model_add.ShipToState = request.data['AddressExtension']['ShipToState']
        model_add.BillToCity = request.data['AddressExtension']['BillToCity']
        model_add.ShipToCountry = request.data['AddressExtension']['ShipToCountry']
        model_add.BillToZipCode = request.data['AddressExtension']['BillToZipCode']
        model_add.ShipToStreet = request.data['AddressExtension']['ShipToStreet']
        model_add.BillToState = request.data['AddressExtension']['BillToState']
        model_add.ShipToZipCode = request.data['AddressExtension']['ShipToZipCode']
        model_add.BillToStreet = request.data['AddressExtension']['BillToStreet']
        model_add.ShipToBuilding = request.data['AddressExtension']['ShipToBuilding']
        model_add.ShipToCity = request.data['AddressExtension']['ShipToCity']
        model_add.BillToCountry = request.data['AddressExtension']['BillToCountry']
        model_add.U_SCOUNTRY = request.data['AddressExtension']['U_SCOUNTRY']
        model_add.U_SSTATE = request.data['AddressExtension']['U_SSTATE']
        model_add.U_SHPTYPB = request.data['AddressExtension']['U_SHPTYPB']
        model_add.U_BSTATE = request.data['AddressExtension']['U_BSTATE']
        model_add.U_BCOUNTRY = request.data['AddressExtension']['U_BCOUNTRY']
        model_add.U_SHPTYPS = request.data['AddressExtension']['U_SHPTYPS']
   
        model_add.save()
        print("add save")
        
        lines = request.data['DocumentLines']
        for line in lines:
            if "id" in line:
                model_line = DocumentLines.objects.get(pk = line['id'])
                model_line.Quantity=line['Quantity']
                model_line.UnitPrice=line['UnitPrice']
                model_line.DiscountPercent=line['DiscountPercent']
                model_line.ItemCode=line['ItemCode']
                model_line.ItemDescription=line['ItemDescription']
                model_line.TaxCode=line['TaxCode']            
                model_line.save()
            else:
                lastline = DocumentLines.objects.filter(QuotationID = fetchid).order_by('-LineNum')[:1]
                NewLine = int(lastline[0].LineNum) + 1
                model_lines = DocumentLines(QuotationID = fetchid, LineNum=NewLine, Quantity = line['Quantity'], UnitPrice = line['UnitPrice'], DiscountPercent = line['DiscountPercent'], ItemCode = line['ItemCode'], ItemDescription = line['ItemDescription'], TaxCode = line['TaxCode'])
                model_lines.save()

        with open("../bridge/bridge/db.json") as f:
            db = f.read()
            data = json.loads(db)
        
        r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
        token = json.loads(r.text)['SessionId']
        print(token)
        
        qt_data = {
            "TaxDate": request.data['TaxDate'],
            "DocDueDate": request.data['DocDueDate'],
            "DocDate": request.data['DocDate'],
            "ContactPersonCode": request.data['ContactPersonCode'],
            "DiscountPercent": request.data['DiscountPercent'],
            "Comments": request.data['Comments'],
            "SalesPersonCode": request.data['SalesPersonCode'],
            "AddressExtension": {
                "BillToBuilding": request.data['AddressExtension']['BillToBuilding'],
                "ShipToState": request.data['AddressExtension']['ShipToState'],
                "BillToCity": request.data['AddressExtension']['BillToCity'],
                "ShipToCountry": request.data['AddressExtension']['ShipToCountry'],
                "BillToZipCode": request.data['AddressExtension']['BillToZipCode'],
                "ShipToStreet": request.data['AddressExtension']['ShipToStreet'],
                "BillToState": request.data['AddressExtension']['BillToState'],
                "ShipToZipCode": request.data['AddressExtension']['ShipToZipCode'],
                "BillToStreet": request.data['AddressExtension']['BillToStreet'],
                "ShipToBuilding": request.data['AddressExtension']['ShipToBuilding'],
                "ShipToCity": request.data['AddressExtension']['ShipToCity'],
                "BillToCountry": request.data['AddressExtension']['BillToCountry']
            },
            "DocumentLines": lines
        }
        
        print(qt_data)
        print(json.dumps(qt_data))

    
        print("http://103.107.67.94:50001/b1s/v1/Quotations('"+model.DocEntry+"')");
        res = requests.patch("http://103.107.67.94:50001/b1s/v1/Quotations("+model.DocEntry+")", data=json.dumps(qt_data), cookies=r.cookies, verify=False)
        print(res.content)

        if len(res.content) !=0 :
            res1 = json.loads(res.content)
            SAP_MSG = res1['error']['message']['value']
            return Response({"message":"Partely successful","status":202,"SAP_error":SAP_MSG, "data":[request.data]})
        else:
            return Response({"message":"successful","status":200, "data":[json.loads(json.dumps(request.data))]})
    except Exception as e:
        return Response({"message":"Not Update","status":201,"data":[{"Error":str(e)}]})


#Quotation All API
@api_view(["GET"])
def all(request):
    allqt = [];
    quot_obj = Quotation.objects.all().order_by("-id")    
    allqt = QuotationShow(quot_obj)    
    return Response({"message": "Success","status": 200,"data":allqt})

def QuotationShow(quot_obj):
    allqt = []
    for qt in quot_obj:
        qtaddr = AddressExtension.objects.filter(QuotationID=qt.id)
        
        qtaddr_json = AddressExtensionSerializer(qtaddr, many=True)
        
        jss_ = json.loads(json.dumps(qtaddr_json.data))
        
        for j in jss_:
            jss0=j
        
        lines = DocumentLines.objects.filter(QuotationID=qt.id)
        
        lines_json = DocumentLinesSerializer(lines, many=True)
        
        jss1 = json.loads(json.dumps(lines_json.data))
        
        context = {
            'id':qt.id,
            'DocEntry':qt.DocEntry,
            'DocDueDate':qt.DocDueDate,
            'DocDate':qt.DocDate,
            'TaxDate':qt.TaxDate,
            'ContactPersonCode':qt.ContactPersonCode,
            'DiscountPercent':qt.DiscountPercent,
            'CardCode':qt.CardCode,
            'CardName':qt.CardName,
            'Comments':qt.Comments,
            'SalesPersonCode':qt.SalesPersonCode,
            
            'DocumentStatus':qt.DocumentStatus,
            'DocCurrency':qt.DocCurrency,
            'DocTotal':qt.DocTotal,
            'VatSum':qt.VatSum,
            'CreationDate':qt.CreationDate,
            'U_QUOTNM':qt.U_QUOTNM,            
            'U_OPPID':qt.U_OPPID,
            'U_OPPRNM':qt.U_OPPRNM,
            'U_FAV':qt.U_FAV,
            'AddressExtension':jss0,
            'DocumentLines':jss1,
            
            "CreateDate":qt.CreateDate,
            "CreateTime":qt.CreateTime,
            "UpdateDate":qt.UpdateDate,
            "UpdateTime":qt.UpdateTime
            }
            
        allqt.append(context)
    return allqt

#Quotation All API
@api_view(["POST"])
def all_filter(request):
    json_data = request.data
    
    if "U_OPPID" in json_data:
        if json_data['U_OPPID'] !='':
            
            quot_obj = Quotation.objects.filter(U_OPPID=json_data['U_OPPID']).order_by("-id")
            if len(quot_obj) ==0:
                return Response({"message": "Success","status": 200,"data":[]})
            else:
                
                allqt = QuotationShow(quot_obj)
                        
            return Response({"message": "Success","status": 200,"data":allqt})
                
    
    if "SalesPersonCode" in json_data:
        print("yes")
        
        if json_data['SalesPersonCode']!="":
            SalesPersonID = json_data['SalesPersonCode']
            
            emp_obj =  Employee.objects.get(SalesEmployeeCode=SalesPersonID)
            
            if emp_obj.role == 'manager':
                emps = Employee.objects.filter(reportingTo=SalesPersonID)#.values('id', 'SalesEmployeeCode')
                SalesPersonID=[SalesPersonID]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
                
            elif emp_obj.role == 'admin':
                emps = Employee.objects.filter(SalesEmployeeCode__gt=0)
                SalesPersonID=[]
                for emp in emps:
                    SalesPersonID.append(emp.SalesEmployeeCode)
            else:
                SalesPersonID = json_data['SalesPersonCode']
            
            print(SalesPersonID)
            
            for ke in json_data.keys():
                if ke =='U_FAV' :
                    print("yes filter")
                    if json_data['U_FAV'] !='':
                        quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, U_FAV=json_data['U_FAV']).order_by("-id")
                        if len(quot_obj) ==0:
                            return Response({"message": "Not Available","status": 201,"data":[]})
                        else:
                            allqt = QuotationShow(quot_obj)
                            return Response({"message": "Success","status": 200,"data":allqt})
                # elif ke =='U_TYPE' :
                    # if json_data['U_TYPE'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, U_TYPE=json_data['U_TYPE']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                # elif ke =='Status' :
                    # if json_data['Status'] !='':
                        # quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID, Status=json_data['Status']).order_by("-id")
                        # if len(quot_obj) ==0:
                            # return Response({"message": "Not Available","status": 201,"data":[]})
                        # else:
                            # quot_json = QuotationSerializer(quot_obj, many=True)
                            # return Response({"message": "Success","status": 200,"data":quot_json.data})
                
                else:
                    print("no filter")
                    # qt = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    # quot_json = QuotationSerializer(quot_obj, many=True)
                    # return Response({"message": "Success","status": 200,"data":quot_json.data})
                    quot_obj = Quotation.objects.filter(SalesPersonCode__in=SalesPersonID).order_by("-id")
                    allqt = QuotationShow(quot_obj)
                        
                    return Response({"message": "Success","status": 200,"data":allqt})
                    
            
        else:
            return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})
    else:
        print("no")
        return Response({"message": "Unsuccess","status": 201,"data":[{"error":"SalesPersonCode?"}]})


#Quotation One API
@api_view(["POST"])
def one(request):
    id=request.data['id']
    quot_obj = Quotation.objects.filter(id=id)
    allqt = QuotationShow(quot_obj)
    
    return Response({"message": "Success","status": 200,"data":allqt})


#Quotation delete
@api_view(['POST'])
def delete(request):
    fetchid=request.data['id']
    try:
        emp=Quotation.objects.get(pk=fetchid)
        SalesQuotationCode = emp.SalesQuotationCode
        
        fetchdata=Quotation.objects.filter(pk=fetchid).delete()
        
        with open("../bridge/bridge/db.json") as f:
            db = f.read()
        print(db)
        data = json.loads(db)
        print(data)
    
        try:
            r = requests.post('http://103.107.67.94:50001/b1s/v1/Login', data=json.dumps(data), verify=False)
            token = json.loads(r.text)['SessionId']
            print(token)
            res = requests.delete('http://103.107.67.94:50001/b1s/v1/SalesPersons('+SalesQuotationCode+')', cookies=r.cookies, verify=False)
            return Response({"message":"successful","status":"200","data":[]})
        except:
            return Response({"message":"successful","status":"200","data":[]})        
    except:
         return Response({"message":"Id wrong","status":"201","data":[]})

