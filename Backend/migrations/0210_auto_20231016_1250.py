# Generated by Django 3.2.20 on 2023-10-16 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0209_auto_20231016_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work_overtime_application',
            name='shift_of_overtime',
        ),
        migrations.RemoveField(
            model_name='work_overtime_application',
            name='type_of_overtime',
        ),
    ]
