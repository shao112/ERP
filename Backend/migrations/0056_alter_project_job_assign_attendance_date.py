# Generated by Django 3.2.20 on 2023-07-28 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0055_alter_project_job_assign_attendance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_job_assign',
            name='attendance_date',
            field=models.JSONField(blank=True, default=[], null=True, verbose_name='出勤日期'),
        ),
    ]
