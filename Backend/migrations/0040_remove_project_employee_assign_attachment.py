# Generated by Django 4.0.1 on 2023-07-22 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0039_alter_project_job_assign_support_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_employee_assign',
            name='attachment',
        ),
    ]
