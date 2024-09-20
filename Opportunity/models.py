from django.db import models  

class Opportunity(models.Model):
	SequentialNo = models.CharField(max_length=9, blank=True) #56,
	CardCode = models.CharField(max_length=100, blank=True) #"C00002",
	SalesPerson = models.CharField(max_length=9, blank=True) #5,
	SalesPersonName = models.CharField(max_length=50, blank=True) #"Sunil Kumar",
	ContactPerson = models.CharField(max_length=9, blank=True) #6,
	ContactPersonName = models.CharField(max_length=50, blank=True) #"Manish Kumar",
	Source = models.CharField(max_length=100, blank=True) #null,  
	StartDate = models.CharField(max_length=50, blank=True) #"2021-09-10",
	PredictedClosingDate = models.CharField(max_length=50, blank=True) #"2021-09-15",
	MaxLocalTotal = models.CharField(max_length=100, blank=True) #100.0,
	MaxSystemTotal = models.CharField(max_length=100, blank=True) #1.515152, 
	Remarks = models.CharField(max_length=200, blank=True) #"Testing",
	Status = models.CharField(max_length=100, blank=True) #"sos_Open",
	ReasonForClosing = models.CharField(max_length=100, blank=True) #null,
	TotalAmountLocal = models.CharField(max_length=100, blank=True) #100.0,
	TotalAmounSystem = models.CharField(max_length=100, blank=True) #1.515152,
	CurrentStageNo = models.CharField(max_length=3, blank=True) #3,
	CurrentStageNumber = models.CharField(max_length=3, blank=True) #3,
	CurrentStageName = models.CharField(max_length=50, blank=True) #"Lead",
	OpportunityName = models.CharField(max_length=100, blank=True) #"Abs",
	Industry = models.CharField(max_length=100, blank=True) #null,
	LinkedDocumentType = models.CharField(max_length=100, blank=True) #null,
	DataOwnershipfield = models.IntegerField(default=0) #null,    
	DataOwnershipName = models.CharField(max_length=50, blank=True) #"Rakesh Kumar",
	StatusRemarks = models.CharField(max_length=100, blank=True) #null,
	ProjectCode = models.CharField(max_length=100, blank=True) #null,
	CustomerName = models.CharField(max_length=100, blank=True) #"SBI Bank",
	ClosingDate = models.CharField(max_length=100, blank=True) #null,
	ClosingType = models.CharField(max_length=100, blank=True) #"sos_Days",
	OpportunityType = models.CharField(max_length=100, blank=True) #"boOpSales",
	UpdateDate = models.CharField(max_length=50, blank=True) #"2021-09-10",
	UpdateTime = models.CharField(max_length=50, blank=True) #"16:31:10",
	U_FAV = models.CharField(max_length=10, default="N", blank=False) #null,
	U_TYPE = models.CharField(max_length=100, blank=True) #null,
	U_LSOURCE = models.CharField(max_length=100, blank=True) #null,
	U_LEADID = models.IntegerField(default=0)
	U_LEADNM = models.CharField(max_length=150, blank=True)
	U_PROBLTY = models.CharField(max_length=100, blank=True) #null,

#--------line 0 ----
class Line(models.Model):
	LineNum = models.CharField(max_length=9, blank=True) #0,
	SalesPerson = models.CharField(max_length=9, blank=True) #-1,
	StartDate = models.CharField(max_length=50, blank=True) #"2021-09-10",
	ClosingDate = models.CharField(max_length=50, blank=True) #"2021-09-14",
	StageKey = models.CharField(max_length=9, blank=True) #2,
	MaxLocalTotal = models.CharField(max_length=100, blank=True) #100.0,
	MaxSystemTotal = models.CharField(max_length=100, blank=True) #1.520,
	Remarks = models.CharField(max_length=100, blank=True) #null,
	Contact = models.CharField(max_length=100, blank=True) #"tNO",------
	Status = models.CharField(max_length=100, blank=True) #"so_Closed",
	ContactPerson = models.CharField(max_length=100, blank=True) #null,
	SequenceNo = models.CharField(max_length=9, blank=True) #56,
	Opp_Id = models.IntegerField(default=0) #56,

class Stage(models.Model):
    SequenceNo = models.CharField(max_length=9, blank=True) #2,
    Name = models.CharField(max_length=100, blank=True) #Lead",
    Stageno = models.FloatField(default=0) #1,
    ClosingPercentage = models.CharField(max_length=100, blank=True) # 0.0,
    Cancelled = models.CharField(max_length=100, blank=True) #tNO",
    IsSales = models.CharField(max_length=100, blank=True) #tYES",
    IsPurchasing = models.CharField(max_length=100, blank=True) #tYES"
    Comment = models.CharField(max_length=500, blank=True)
    File = models.CharField(max_length=200, blank=True)
    CreateDate = models.CharField(max_length=60, blank=True)
    UpdateDate = models.CharField(max_length=60, blank=True)
    Status = models.IntegerField(default=0)
    Opp_Id = models.IntegerField(default=0) #tYES"

class StaticStage(models.Model):
    SequenceNo = models.CharField(max_length=9, blank=True) #2,
    Name = models.CharField(max_length=100, blank=True) #Lead",
    Stageno = models.FloatField(default='0') #1,
    ClosingPercentage = models.CharField(max_length=100, blank=True) # 0.0,
    Cancelled = models.CharField(max_length=100, blank=True) #tNO",
    IsSales = models.CharField(max_length=100, blank=True) #tYES",
    IsPurchasing = models.CharField(max_length=100, blank=True) #tYES"

