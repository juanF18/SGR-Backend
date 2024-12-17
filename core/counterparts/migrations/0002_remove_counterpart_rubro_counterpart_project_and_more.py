# Generated by Django 5.1.2 on 2024-12-16 04:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counterparts', '0001_initial'),
        ('projects', '0006_remove_project_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counterpart',
            name='rubro',
        ),
        migrations.AddField(
            model_name='counterpart',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.project'),
        ),
        migrations.AlterField(
            model_name='counterpart',
            name='value_chash',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='value_chash'),
        ),
        migrations.AlterField(
            model_name='counterpart',
            name='value_species',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='value_species'),
        ),
    ]