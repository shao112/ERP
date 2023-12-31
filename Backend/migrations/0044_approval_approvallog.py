# Generated by Django 4.2.3 on 2023-07-23 05:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0043_remove_employee_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish', models.BooleanField(default=False, verbose_name='完成')),
            ],
            options={
                'verbose_name': '簽核狀態',
                'verbose_name_plural': '簽核狀態',
                'permissions': (('can_approval', '簽核權限'),),
            },
        ),
        migrations.CreateModel(
            name='ApprovalLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='內容')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='建立日期')),
                ('approval', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='approval_logs', to='Backend.approval')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Backend.employee', verbose_name='簽核者')),
            ],
            options={
                'verbose_name': '簽核記錄',
                'verbose_name_plural': '簽核記錄',
            },
        ),
    ]
