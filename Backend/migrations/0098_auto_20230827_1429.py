# Generated by Django 3.2.20 on 2023-08-27 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0097_approval_targetdepartment_employee_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval_targetdepartment',
            name='employee_order',
        ),
        migrations.AddField(
            model_name='approval_targetdepartment',
            name='employee_order',
            field=models.JSONField(null=True, verbose_name='員工簽核順序'),
        ),
    ]
