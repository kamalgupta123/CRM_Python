# Generated by Django 3.2.12 on 2022-06-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0009_auto_20220610_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='message',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]