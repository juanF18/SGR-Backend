# Generated by Django 5.1.2 on 2024-12-05 20:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='amount')),
                ('description', models.CharField(blank=True, max_length=150, null=True, verbose_name='description')),
                ('type', models.CharField(choices=[('I', 'Income'), ('E', 'Expense')], default='I', max_length=1, verbose_name='type')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contracts.contract')),
            ],
            options={
                'db_table': 'movements',
                'ordering': ['id'],
            },
        ),
    ]
