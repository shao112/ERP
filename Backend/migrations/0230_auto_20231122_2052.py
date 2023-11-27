# Generated by Django 3.2.20 on 2023-11-22 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0229_rename_leave_quantity_leave_param_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='remark',
            field=models.TextField(blank=True, null=True, verbose_name='備註'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='pay_method',
            field=models.CharField(blank=True, choices=[('1', '(1)付款方式:完工請款100%.初次交易,請配合開立即期票或匯款，用於新客戶'), ('2', '(2)付款方式:完工請款100%.發票開立後期票30天，較常使用'), ('3', '(3)付款方式:與業主額外議定(此部分開放自行填寫,利配合部分廠商付款特殊要求)')], max_length=1, null=True, verbose_name='付款方式'),
        ),
    ]
