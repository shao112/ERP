# Generated by Django 3.2.20 on 2023-10-04 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0173_alter_salarydetail_tax_deduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='food_addition',
        ),
    ]
