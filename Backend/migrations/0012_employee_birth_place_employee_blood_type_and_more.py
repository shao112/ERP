# Generated by Django 4.0.1 on 2023-07-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0011_alter_employee_options_employee_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='birth_place',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='出生地'),
        ),
        migrations.AddField(
            model_name='employee',
            name='blood_type',
            field=models.CharField(blank=True, choices=[('A', 'A型'), ('B', 'B型'), ('AB', 'AB型'), ('O', 'O型')], max_length=2, null=True, verbose_name='血型'),
        ),
        migrations.AddField(
            model_name='employee',
            name='company_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='公司E_Mail'),
        ),
        migrations.AddField(
            model_name='employee',
            name='current_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='現居地址'),
        ),
        migrations.AddField(
            model_name='employee',
            name='current_address_city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='現居地址縣市'),
        ),
        migrations.AddField(
            model_name='employee',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='緊急聯絡人1'),
        ),
        migrations.AddField(
            model_name='employee',
            name='emergency_contact_phone',
            field=models.IntegerField(blank=True, max_length=20, null=True, verbose_name='聯絡人電話1'),
        ),
        migrations.AddField(
            model_name='employee',
            name='emergency_contact_relations',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='關係1'),
        ),
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '男'), ('F', '女')], max_length=1, null=True, verbose_name='性別'),
        ),
        migrations.AddField(
            model_name='employee',
            name='location',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='所在地'),
        ),
        migrations.AddField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('M', '已婚'), ('S', '未婚'), ('D', '離異')], max_length=1, null=True, verbose_name='婚姻狀況'),
        ),
        migrations.AddField(
            model_name='employee',
            name='military_status',
            field=models.CharField(blank=True, choices=[('M', '義務役'), ('E', '免服役'), ('A', '替代役')], max_length=1, null=True, verbose_name='兵役狀況'),
        ),
        migrations.AddField(
            model_name='employee',
            name='permanent_address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='戶籍地址'),
        ),
        migrations.AddField(
            model_name='employee',
            name='personal_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='個人E_Mail'),
        ),
    ]
