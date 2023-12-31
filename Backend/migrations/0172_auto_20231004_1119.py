# Generated by Django 3.2.20 on 2023-10-04 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0171_merge_0170_auto_20231003_2027_0170_auto_20231003_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarydetail',
            name='tax_deduction',
            field=models.BooleanField(default=False, verbose_name='扣稅項目'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(blank=True, max_length=30, verbose_name='員工編號'),
        ),
        migrations.AlterField(
            model_name='project_employee_assign',
            name='remark',
            field=models.TextField(blank=True, null='', verbose_name='交接/備註'),
        ),
    ]
