# Generated by Django 3.2.20 on 2023-10-09 07:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0184_auto_20231009_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_items',
            name='format_and_voltage',
        ),
        migrations.RemoveField(
            model_name='test_items',
            name='level',
        ),
        migrations.RemoveField(
            model_name='test_items',
            name='number',
        ),
        migrations.RemoveField(
            model_name='test_items',
            name='test_date',
        ),
        migrations.RemoveField(
            model_name='test_items',
            name='test_location',
        ),
        migrations.CreateModel(
            name='Test_Items_Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='建立日期')),
                ('update_date', models.DateField(auto_now=True, verbose_name='更新日期')),
                ('test_date', models.DateField(blank=True, null=True, verbose_name='檢驗日期')),
                ('test_location', models.CharField(blank=True, max_length=300, null=True, verbose_name='試驗地點')),
                ('format_and_voltage', models.CharField(blank=True, max_length=300, null=True, verbose_name='廠牌規格/額定電壓')),
                ('level', models.CharField(blank=True, max_length=300, null=True, verbose_name='加壓等級')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Backend.employee')),
                ('test_items', models.ManyToManyField(blank=True, null=True, to='Backend.Test_Items', verbose_name='檢查項目')),
            ],
            options={
                'verbose_name': '檢查項目描述',
                'verbose_name_plural': '檢查項目描述',
            },
        ),
    ]