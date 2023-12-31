# Generated by Django 4.0.1 on 2023-07-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0029_project_confirmation_project_confirmation_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_job_assign',
            name='lead_employee',
        ),
        migrations.AddField(
            model_name='project_job_assign',
            name='lead_employee',
            field=models.ManyToManyField(related_name='projects_lead_employee', to='Backend.Employee', verbose_name='帶班人員'),
        ),
        migrations.RemoveField(
            model_name='project_job_assign',
            name='work_employee',
        ),
        migrations.AddField(
            model_name='project_job_assign',
            name='work_employee',
            field=models.ManyToManyField(related_name='projects_work_employee', to='Backend.Employee', verbose_name='工作人員'),
        ),
    ]
