# Generated by Django 3.2.20 on 2023-10-11 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0193_quotation_quote_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='invoice_attachment',
        ),
    ]