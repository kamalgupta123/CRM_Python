# Generated by Django 3.2.13 on 2023-01-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activity', '0006_auto_20220627_0928'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='activity',
            name='Comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='Description',
            field=models.TextField(blank=True),
        ),
    ]
