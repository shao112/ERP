# Generated by Django 3.2.20 on 2023-08-28 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0100_auto_20230828_1208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave_param',
            old_name='leave_reason',
            new_name='is_audit',
        ),
    ]