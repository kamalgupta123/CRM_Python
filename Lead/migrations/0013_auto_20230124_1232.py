# Generated by Django 3.2.13 on 2023-01-24 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0012_auto_20220620_1044'),
    ]

    operations = [
        
        migrations.AddField(
            model_name='lead',
            name='UpdateDate',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]