# Generated by Django 3.2.20 on 2023-10-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0179_auto_20231006_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='labor_pension_moeny',
            field=models.PositiveIntegerField(blank=True, default=6, null=True, verbose_name='勞退級距'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='health_insurance',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='健保級距'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='labor_protection',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='勞保級距'),
        ),
    ]
