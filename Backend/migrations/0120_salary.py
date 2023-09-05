# Generated by Django 3.2.20 on 2023-09-05 08:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0119_salarydetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(default=django.utils.timezone.now, verbose_name='建立日期')),
                ('update_date', models.DateField(auto_now=True, verbose_name='更新日期')),
                ('year', models.PositiveIntegerField(verbose_name='年')),
                ('month', models.PositiveIntegerField(verbose_name='月')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Salary_author', to='Backend.employee')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Backend.employee')),
                ('salary_details', models.ManyToManyField(to='Backend.SalaryDetail', verbose_name='薪資明細')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='salary_user', to='Backend.employee', verbose_name='員工')),
            ],
            options={
                'verbose_name': '薪資',
                'verbose_name_plural': '薪資',
            },
        ),
    ]
