# Generated by Django 3.2.20 on 2023-10-05 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0175_auto_20231005_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarydetail',
            name='five',
            field=models.BooleanField(default=False, verbose_name='五號發薪'),
        ),
    ]
