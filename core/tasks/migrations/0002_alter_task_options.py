# Generated by Django 5.1.2 on 2024-12-09 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['task_num']},
        ),
    ]
