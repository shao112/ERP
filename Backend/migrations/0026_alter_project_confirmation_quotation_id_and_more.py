# Generated by Django 4.0.1 on 2023-07-12 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0025_rename_project_project_job_assign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_confirmation',
            name='quotation_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='報價單號'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='quotation_id',
            field=models.CharField(max_length=100, verbose_name='報價單號'),
        ),
    ]
