# Generated by Django 5.1.2 on 2024-12-09 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='value',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=20, verbose_name='value'),
        ),
    ]