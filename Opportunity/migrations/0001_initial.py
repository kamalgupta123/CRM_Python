# Generated by Django 3.2.7 on 2022-02-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineNum', models.CharField(blank=True, max_length=9)),
                ('SalesPerson', models.CharField(blank=True, max_length=9)),
                ('StartDate', models.CharField(blank=True, max_length=50)),
                ('ClosingDate', models.CharField(blank=True, max_length=50)),
                ('StageKey', models.CharField(blank=True, max_length=9)),
                ('MaxLocalTotal', models.CharField(blank=True, max_length=100)),
                ('MaxSystemTotal', models.CharField(blank=True, max_length=100)),
                ('Remarks', models.CharField(blank=True, max_length=100)),
                ('Contact', models.CharField(blank=True, max_length=100)),
                ('Status', models.CharField(blank=True, max_length=100)),
                ('ContactPerson', models.CharField(blank=True, max_length=100)),
                ('SequenceNo', models.CharField(blank=True, max_length=9)),
                ('Opp_Id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SequentialNo', models.CharField(blank=True, max_length=9)),
                ('CardCode', models.CharField(blank=True, max_length=100)),
                ('SalesPerson', models.CharField(blank=True, max_length=9)),
                ('SalesPersonName', models.CharField(blank=True, max_length=50)),
                ('ContactPerson', models.CharField(blank=True, max_length=9)),
                ('ContactPersonName', models.CharField(blank=True, max_length=50)),
                ('Source', models.CharField(blank=True, max_length=100)),
                ('StartDate', models.CharField(blank=True, max_length=50)),
                ('PredictedClosingDate', models.CharField(blank=True, max_length=50)),
                ('MaxLocalTotal', models.CharField(blank=True, max_length=100)),
                ('MaxSystemTotal', models.CharField(blank=True, max_length=100)),
                ('Remarks', models.CharField(blank=True, max_length=200)),
                ('Status', models.CharField(blank=True, max_length=100)),
                ('ReasonForClosing', models.CharField(blank=True, max_length=100)),
                ('TotalAmountLocal', models.CharField(blank=True, max_length=100)),
                ('TotalAmounSystem', models.CharField(blank=True, max_length=100)),
                ('CurrentStageNo', models.CharField(blank=True, max_length=3)),
                ('CurrentStageNumber', models.CharField(blank=True, max_length=3)),
                ('CurrentStageName', models.CharField(blank=True, max_length=50)),
                ('OpportunityName', models.CharField(blank=True, max_length=100)),
                ('Industry', models.CharField(blank=True, max_length=100)),
                ('LinkedDocumentType', models.CharField(blank=True, max_length=100)),
                ('DataOwnershipfield', models.IntegerField(default=0)),
                ('DataOwnershipName', models.CharField(blank=True, max_length=50)),
                ('StatusRemarks', models.CharField(blank=True, max_length=100)),
                ('ProjectCode', models.CharField(blank=True, max_length=100)),
                ('CustomerName', models.CharField(blank=True, max_length=100)),
                ('ClosingDate', models.CharField(blank=True, max_length=100)),
                ('ClosingType', models.CharField(blank=True, max_length=100)),
                ('OpportunityType', models.CharField(blank=True, max_length=100)),
                ('UpdateDate', models.CharField(blank=True, max_length=50)),
                ('UpdateTime', models.CharField(blank=True, max_length=50)),
                ('U_TYPE', models.CharField(blank=True, max_length=100)),
                ('U_LSOURCE', models.CharField(blank=True, max_length=100)),
                ('U_FAV', models.CharField(blank=True, max_length=100)),
                ('U_PROBLTY', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SequenceNo', models.CharField(blank=True, max_length=9)),
                ('Name', models.CharField(blank=True, max_length=100)),
                ('Stageno', models.FloatField(default=0)),
                ('ClosingPercentage', models.CharField(blank=True, max_length=100)),
                ('Cancelled', models.CharField(blank=True, max_length=100)),
                ('IsSales', models.CharField(blank=True, max_length=100)),
                ('IsPurchasing', models.CharField(blank=True, max_length=100)),
                ('Comment', models.CharField(blank=True, max_length=500)),
                ('File', models.CharField(blank=True, max_length=200)),
                ('CreateDate', models.CharField(blank=True, max_length=60)),
                ('UpdateDate', models.CharField(blank=True, max_length=60)),
                ('Status', models.IntegerField(default=0)),
                ('Opp_Id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StaticStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SequenceNo', models.CharField(blank=True, max_length=9)),
                ('Name', models.CharField(blank=True, max_length=100)),
                ('Stageno', models.FloatField(default='0')),
                ('ClosingPercentage', models.CharField(blank=True, max_length=100)),
                ('Cancelled', models.CharField(blank=True, max_length=100)),
                ('IsSales', models.CharField(blank=True, max_length=100)),
                ('IsPurchasing', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]