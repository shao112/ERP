# Generated by Django 3.2.20 on 2023-08-03 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0063_project_employee_assign_carry_equipments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='is_check',
            field=models.BooleanField(blank=True, default=False, verbose_name='校驗類別'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='normal_or_abnormal',
            field=models.BooleanField(blank=True, default=False, max_length=100, verbose_name='正常/異常'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='produced_stickers',
            field=models.BooleanField(blank=True, default=False, verbose_name='需補產編貼紙'),
        ),
    ]
