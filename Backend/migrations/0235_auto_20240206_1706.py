# Generated by Django 3.2.20 on 2024-02-06 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0234_auto_20240127_1216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project_employee_assign',
            old_name='last_excel',
            new_name='attachment',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='last_excel',
        ),
    ]
