# Generated by Django 3.2.20 on 2023-10-23 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0227_quotation_pay_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='uploaded_files',
            field=models.ManyToManyField(blank=True, related_name='clientfile', to='Backend.UploadedFile'),
        ),
    ]
