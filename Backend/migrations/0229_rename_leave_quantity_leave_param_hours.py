# Generated by Django 3.2.20 on 2023-11-19 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0228_client_uploaded_files'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave_param',
            old_name='leave_quantity',
            new_name='hours',
        ),
    ]
