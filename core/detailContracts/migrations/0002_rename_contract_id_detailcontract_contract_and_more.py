# Generated by Django 5.1.2 on 2024-11-28 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detailContracts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detailcontract',
            old_name='contract_id',
            new_name='contract',
        ),
        migrations.RenameField(
            model_name='detailcontract',
            old_name='task_id',
            new_name='task',
        ),
    ]
