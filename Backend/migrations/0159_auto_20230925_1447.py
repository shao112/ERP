# Generated by Django 3.2.20 on 2023-09-25 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0158_auto_20230919_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_application',
            name='Application_date',
        ),
        migrations.AddField(
            model_name='travel_application',
            name='employee_Assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Travel_users', to='Backend.project_employee_assign'),
        ),
        migrations.AlterField(
            model_name='extraworkday',
            name='date_type',
            field=models.CharField(choices=[('extra_work', '補班、額外上班日(這天要上班)'), ('day_off', '國定假日、平日休假日(這天不用上班)')], max_length=10, verbose_name='日期類型'),
        ),
        migrations.AlterField(
            model_name='leave_application',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_list', to='Backend.employee', verbose_name='申請人'),
        ),
        migrations.AlterField(
            model_name='travel_application',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Travel_Application_author', to='Backend.employee', verbose_name='申請者'),
        ),
    ]