# Generated by Django 3.2.20 on 2023-09-14 04:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0139_auto_20230914_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='clock',
            name='clock_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='打卡時間'),
        ),
    ]