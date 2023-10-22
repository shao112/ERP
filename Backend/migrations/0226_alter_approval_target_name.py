# Generated by Django 3.2.20 on 2023-10-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0225_miss_food_application_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval_target',
            name='name',
            field=models.CharField(choices=[('Project_Employee_Assign', '派工單'), ('Leave_Application', '請假單'), ('Work_Overtime_Application', '加班單'), ('Clock_Correction_Application', '補卡單'), ('Travel_Application', '車程津貼單'), ('Miss_Food_Application', '誤餐費單')], max_length=30, verbose_name='表單名稱'),
        ),
    ]