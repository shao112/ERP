# Generated by Django 3.2.20 on 2023-09-06 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0126_alter_salarydetail_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salarydetail',
            name='adjustment_amount',
            field=models.IntegerField(default=0, verbose_name='調整金額'),
        ),
        migrations.AlterField(
            model_name='salarydetail',
            name='system_amount',
            field=models.IntegerField(default=0, verbose_name='系統金額'),
        ),
    ]