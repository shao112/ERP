# Generated by Django 4.0.1 on 2023-07-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0012_employee_birth_place_employee_blood_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='備註'),
        ),
    ]
