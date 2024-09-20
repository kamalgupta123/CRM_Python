from Employee.models import Employee


# function to get all reporting reporting person
def getAllReportingToIds(EmpCode):
    data = []
    def recrusiveMethod(id):
        print('recursive call')
        data.append(id)
        emp_obj =  Employee.objects.filter(reportingTo=id)
        for obj in emp_obj:
            recrusiveMethod(int(obj.SalesEmployeeCode))
    recrusiveMethod(EmpCode)
    return data