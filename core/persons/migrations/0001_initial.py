# Generated by Django 5.1.2 on 2024-11-22 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='job_title')),
                ('dedication', models.CharField(blank=True, max_length=100, null=True, verbose_name='dedication')),
                ('weeks', models.CharField(blank=True, max_length=100, null=True, verbose_name='weeks')),
                ('fees', models.CharField(blank=True, max_length=100, null=True, verbose_name='fees')),
                ('value_hour', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='value_hour')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='total')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='deleted_at')),
            ],
            options={
                'db_table': 'persons',
                'ordering': ['id'],
            },
        ),
    ]