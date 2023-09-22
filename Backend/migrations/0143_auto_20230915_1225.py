# Generated by Django 3.2.20 on 2023-09-15 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0142_auto_20230915_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clock',
            name='clock_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='打卡日期'),
        ),
        migrations.AlterField(
            model_name='clock',
            name='clock_time',
            field=models.TimeField(verbose_name='打卡時間'),
        ),
    ]