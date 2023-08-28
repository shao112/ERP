# Generated by Django 3.2.20 on 2023-08-28 04:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0098_auto_20230827_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leave_Param',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='建立日期')),
                ('update_date', models.DateField(auto_now=True, verbose_name='更新日期')),
                ('leave_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='假別名稱')),
                ('leave_type', models.CharField(blank=True, choices=[('特休假', '特休假'), ('一般假', '一般假'), ('特別假', '特別假')], max_length=5, null=True, verbose_name='項目類別')),
                ('days', models.IntegerField(blank=True, default=0, null=True, verbose_name='給假數')),
                ('minimum_leave_number', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='最低請假數(為0就不卡控)')),
                ('minimum_leave_unit', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='最小請假單位(為0就不卡控)')),
                ('unit', models.CharField(blank=True, choices=[('小時', '小時'), ('天', '天')], max_length=5, null=True, verbose_name='單位')),
                ('leave_reason', models.BooleanField(blank=True, default=False, verbose_name='附件稽核')),
                ('backlog', models.TextField(blank=True, max_length=1000, null=True, verbose_name='請假規定')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_param_author', to='Backend.employee')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Backend.employee')),
            ],
            options={
                'verbose_name': '假別參數',
                'verbose_name_plural': '假別參數',
            },
        ),
    ]
