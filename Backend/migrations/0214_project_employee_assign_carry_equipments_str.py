# Generated by Django 3.2.20 on 2023-10-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0213_auto_20231019_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_employee_assign',
            name='carry_equipments_str',
            field=models.TextField(blank=True, null='', verbose_name='紀錄資產字串'),
        ),
    ]