# Generated by Django 3.2.20 on 2023-08-19 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0085_alter_employee_uploaded_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval_targetdepartment',
            name='department',
        ),
        migrations.AddField(
            model_name='approval_targetdepartment',
            name='department_order',
            field=models.JSONField(blank=True, null=True, verbose_name='部門簽核順序'),
        ),
    ]
