# Generated by Django 5.1.2 on 2024-12-18 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counterpartExecution', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counterpartexecution',
            name='temp_field',
        ),
    ]