# Generated by Django 3.2.20 on 2023-08-16 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0077_project_job_assign_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_employee_assign',
            name='Approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Project_Employee_Assign_Approval', to='Backend.approvalmodel'),
        ),
    ]
