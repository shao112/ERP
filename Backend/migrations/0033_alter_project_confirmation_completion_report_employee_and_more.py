# Generated by Django 4.2.3 on 2023-07-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0032_equipment_alter_news_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_confirmation',
            name='completion_report_employee',
            field=models.ManyToManyField(blank=True, related_name='projects_confirmation_report_employee', to='Backend.employee', verbose_name='完工回報人'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='lead_employee',
            field=models.ManyToManyField(blank=True, related_name='projects_lead_employee', to='Backend.employee', verbose_name='帶班人員'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='work_employee',
            field=models.ManyToManyField(blank=True, related_name='projects_work_employee', to='Backend.employee', verbose_name='工作人員'),
        ),
    ]
