# Generated by Django 4.1.6 on 2023-03-13 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pagination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MaxSize', models.CharField(blank=True, max_length=50)),
                ('Status', models.CharField(blank=True, default='Active', max_length=50)),
            ],
        ),
    ]
