# Generated by Django 3.2.20 on 2023-10-22 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0224_miss_food_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='miss_food_application',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='Miss_Food_Attachment', verbose_name='誤餐費附件'),
        ),
    ]
