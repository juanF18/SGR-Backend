# Generated by Django 5.1.2 on 2024-11-28 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cdps',
            old_name='rubro_id',
            new_name='rubro',
        ),
    ]