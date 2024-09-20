# Generated by Django 3.2.13 on 2023-01-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0014_delete_casetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatter',
            name='Message',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='alter_email',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='lead',
            name='alter_phone',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='lead',
            name='companyName',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lead',
            name='designation',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lead',
            name='location',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lead',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='leaditem',
            name='ItemDescription',
            field=models.TextField(blank=True),
        ),
    ]
