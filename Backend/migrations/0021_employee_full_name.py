# Generated by Django 4.0.1 on 2023-07-07 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0020_alter_project_confirmation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='full_name',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='員工名稱'),
        ),
    ]
