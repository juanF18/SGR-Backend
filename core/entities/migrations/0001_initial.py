# Generated by Django 5.1.2 on 2024-11-27 23:04

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='name')),
                ('nit', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='nit')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='phone')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='city')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'entities',
                'ordering': ['id'],
            },
        ),
    ]
