# Generated by Django 4.0.1 on 2023-07-16 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0028_alter_project_job_assign_c_a_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_confirmation',
            name='project_confirmation_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工確單編號'),
        ),
        migrations.AlterField(
            model_name='project_confirmation',
            name='c_a',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='母案編號'),
        ),
        migrations.AlterField(
            model_name='project_confirmation',
            name='client',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='客戶簡稱'),
        ),
        migrations.AlterField(
            model_name='project_confirmation',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='訂單編號'),
        ),
        migrations.AlterField(
            model_name='project_confirmation',
            name='project_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工程名稱'),
        ),
        migrations.AlterField(
            model_name='project_confirmation',
            name='requisition',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='請購單位'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='c_a',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='母案編號'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工作地點'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='projecet_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工派單編號'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='project_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工程名稱'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='project_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='工作類型'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='support',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='支援人力'),
        ),
        migrations.AlterField(
            model_name='project_job_assign',
            name='vehicle',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='使用車輛'),
        ),
    ]
