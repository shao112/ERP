# Generated by Django 3.2.20 on 2023-10-15 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0204_work_item_number_quotation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work_item_number',
            name='quotation',
        ),
    ]
