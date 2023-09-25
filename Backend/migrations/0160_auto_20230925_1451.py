# Generated by Django 3.2.20 on 2023-09-25 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0159_auto_20230925_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_application',
            name='employee_Assign',
        ),
        migrations.AddField(
            model_name='travel_application',
            name='job_assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Travel_users', to='Backend.project_job_assign'),
        ),
    ]