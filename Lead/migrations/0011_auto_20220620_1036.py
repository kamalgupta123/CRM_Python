# Generated by Django 3.2.12 on 2022-06-20 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0010_auto_20220616_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='alter_email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='lead',
            name='alter_phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='lead',
            name='junk',
            field=models.IntegerField(default='0'),
        ),
    ]