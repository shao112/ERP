# Generated by Django 3.2.20 on 2023-10-15 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0206_work_item_number_quotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project_job_assign',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='project_job_assign',
            name='vehicle',
            field=models.ManyToManyField(blank=True, related_name='project_job_assign_vehicle', to='Backend.Vehicle', verbose_name='使用車輛'),
        ),
    ]
