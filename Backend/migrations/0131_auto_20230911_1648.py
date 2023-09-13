# Generated by Django 3.2.20 on 2023-09-11 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0130_auto_20230907_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_city_residence', models.CharField(choices=[('台東', '台東'), ('花蓮', '花蓮'), ('宜蘭', '宜蘭'), ('北北基', '北北基'), ('桃園', '桃園'), ('新竹', '新竹'), ('苗栗', '苗栗'), ('台中', '台中'), ('南投', '南投'), ('彰化', '彰化'), ('雲林', '雲林'), ('嘉義', '嘉義'), ('台南', '台南'), ('高雄', '高雄'), ('屏東', '屏東')], max_length=4, verbose_name='居住地')),
                ('location_city_business_trip', models.CharField(choices=[('台東', '台東'), ('花蓮', '花蓮'), ('宜蘭', '宜蘭'), ('北北基', '北北基'), ('桃園', '桃園'), ('新竹', '新竹'), ('苗栗', '苗栗'), ('台中', '台中'), ('南投', '南投'), ('彰化', '彰化'), ('雲林', '雲林'), ('嘉義', '嘉義'), ('台南', '台南'), ('高雄', '高雄'), ('屏東', '屏東')], max_length=4, verbose_name='出差地')),
                ('amount', models.PositiveIntegerField(verbose_name='金額')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': '參照表',
                'verbose_name_plural': '參照表',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='location_city',
            field=models.CharField(blank=True, choices=[('台東', '台東'), ('花蓮', '花蓮'), ('宜蘭', '宜蘭'), ('北北基', '北北基'), ('桃園', '桃園'), ('新竹', '新竹'), ('苗栗', '苗栗'), ('台中', '台中'), ('南投', '南投'), ('彰化', '彰化'), ('雲林', '雲林'), ('嘉義', '嘉義'), ('台南', '台南'), ('高雄', '高雄'), ('屏東', '屏東')], max_length=4, null=True, verbose_name='居住城市(用於計算津貼)'),
        ),
        migrations.AlterField(
            model_name='approval_target',
            name='name',
            field=models.CharField(choices=[('Project_Employee_Assign', '派工單'), ('Leave_Application', '請假單'), ('Work_Overtime_Application', '補卡單'), ('Clock_Correction_Application', '加班單')], max_length=30, verbose_name='表單名稱'),
        ),
    ]