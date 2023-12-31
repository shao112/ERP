# Generated by Django 3.2.20 on 2023-08-09 12:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0069_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='建立日期')),
                ('update_date', models.DateField(auto_now=True, verbose_name='更新日期')),
                ('requisition_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='請購單位')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Backend.employee')),
            ],
            options={
                'verbose_name': '請購單位',
                'verbose_name_plural': '請購單位',
            },
        ),
    ]
