# Generated by Django 3.2.12 on 2022-06-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0008_auto_20220607_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='contactPerson',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
