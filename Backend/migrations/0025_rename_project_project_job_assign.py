# Generated by Django 4.2.3 on 2023-07-11 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0024_remove_employee_departments_alter_clock_employee_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Project',
            new_name='Project_Job_Assign',
        ),
    ]
