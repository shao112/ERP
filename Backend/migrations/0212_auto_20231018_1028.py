# Generated by Django 3.2.20 on 2023-10-18 02:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0211_auto_20231017_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='referencetable',
            name='created_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='建立日期'),
        ),
        migrations.AddField(
            model_name='referencetable',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Backend.employee'),
        ),
        migrations.AddField(
            model_name='referencetable',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='更新日期'),
        ),
        migrations.AlterField(
            model_name='referencetable',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='錢/單位'),
        ),
    ]