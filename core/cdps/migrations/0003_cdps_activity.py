# Generated by Django 5.1.2 on 2024-12-12 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('cdps', '0002_remove_cdps_document_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='cdps',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activities.activity'),
        ),
    ]
