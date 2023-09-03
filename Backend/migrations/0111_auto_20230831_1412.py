# Generated by Django 3.2.20 on 2023-08-31 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0110_rename_days_leave_param_leave_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval_target',
            name='name',
            field=models.CharField(choices=[('Project_Confirmation', '工程確認單'), ('Project_Job_Assign', '工程派任計畫單'), ('Project_Employee_Assign', '派工單'), ('請假單', '請假單')], max_length=30, verbose_name='表單名稱'),
        ),
        migrations.AlterField(
            model_name='approvalmodel',
            name='current_status',
            field=models.CharField(choices=[('completed', '完成'), ('in_progress', '進行中'), ('rejected', '駁回')], default='in_progress', max_length=30),
        ),
    ]