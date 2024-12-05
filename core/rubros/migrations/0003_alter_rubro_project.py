# Generated by Django 5.1.2 on 2024-12-05 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_project_file_activities_and_more'),
        ('rubros', '0002_alter_rubro_value_sgr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubro',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
