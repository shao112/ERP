# Generated by Django 3.2.20 on 2023-08-01 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0060_auto_20230801_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='車牌編號'),
        ),
    ]