# Generated by Django 3.2.20 on 2023-08-02 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0061_alter_vehicle_vehicle_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project_confirmation',
            old_name='reassignment_attachment',
            new_name='attachment',
        ),
    ]
