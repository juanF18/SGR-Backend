# Generated by Django 5.1.2 on 2024-12-04 06:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cdps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('contract_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='contract_number')),
                ('contracting_nit', models.CharField(blank=True, max_length=100, null=True, verbose_name='contracting_nit')),
                ('contracted_nit', models.CharField(blank=True, max_length=100, null=True, verbose_name='contracted_nit')),
                ('contracting_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='contracting_name')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='start_date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='end_date')),
                ('contract_info', models.TextField(blank=True, null=True, verbose_name='contract_info')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='amount')),
                ('supervisor_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='supervisor_name')),
                ('supervisor_identification', models.CharField(blank=True, max_length=100, null=True, verbose_name='supervisor_identification')),
                ('contract_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='contract_url')),
                ('observations', models.TextField(blank=True, null=True, verbose_name='observations')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('cpds', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cdps.cdps')),
            ],
            options={
                'db_table': 'contracts',
                'ordering': ['id'],
            },
        ),
    ]
