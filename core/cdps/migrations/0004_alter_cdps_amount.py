# Generated by Django 5.1.2 on 2024-12-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdps', '0003_cdps_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cdps',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='amount'),
        ),
    ]
