# Generated by Django 3.2.20 on 2023-08-04 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0064_auto_20230803_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_job_assign',
            name='job_assign_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工派單編號'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='is_check',
            field=models.BooleanField(blank=True, default=True, verbose_name='校驗類別'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='normal_or_abnormal',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='正常/異常'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='produced_stickers',
            field=models.BooleanField(blank=True, default=True, verbose_name='需補產編貼紙'),
        ),
    ]
