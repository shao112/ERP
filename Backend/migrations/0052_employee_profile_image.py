# Generated by Django 3.2.20 on 2023-07-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0051_employee_modified_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='employee_profile/', verbose_name='大頭照'),
        ),
    ]