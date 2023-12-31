# Generated by Django 3.2.20 on 2023-09-19 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0154_leave_application_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel_application',
            name='Application_date',
            field=models.DateField(blank=True, null=True, verbose_name='申請時間'),
        ),
        migrations.AddField(
            model_name='travel_application',
            name='Approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Travel_Application_Approval', to='Backend.approvalmodel'),
        ),
    ]
