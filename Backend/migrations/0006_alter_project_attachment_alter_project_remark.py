# Generated by Django 4.0.1 on 2023-07-02 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0005_remove_project_lead_employee_project_lead_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='project-attachment', verbose_name='工確單附件'),
        ),
        migrations.AlterField(
            model_name='project',
            name='remark',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='備註'),
        ),
    ]
