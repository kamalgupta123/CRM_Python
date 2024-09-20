# Generated by Django 3.2.7 on 2022-02-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyId', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(blank=True, max_length=250)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=35)),
                ('state', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('pincode', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('branch', models.CharField(blank=True, max_length=100)),
                ('active', models.IntegerField(default=1)),
                ('timestamp', models.CharField(max_length=30)),
            ],
        ),
    ]
