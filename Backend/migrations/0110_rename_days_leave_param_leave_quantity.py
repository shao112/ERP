# Generated by Django 3.2.20 on 2023-08-29 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0109_auto_20230829_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave_param',
            old_name='days',
            new_name='leave_quantity',
        ),
    ]