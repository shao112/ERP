# Generated by Django 3.2.20 on 2023-09-19 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0157_alter_extraworkday_date_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extraworkday',
            options={'ordering': ['-id'], 'verbose_name': '工作日調整', 'verbose_name_plural': '工作日調整'},
        ),
        migrations.RemoveField(
            model_name='leave_application',
            name='applicant',
        ),
        migrations.RemoveField(
            model_name='travel_application',
            name='applicant',
        ),
        migrations.AlterField(
            model_name='extraworkday',
            name='date',
            field=models.DateField(verbose_name='調整日期'),
        ),
        migrations.AlterField(
            model_name='leave_application',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_created', to='Backend.employee', verbose_name='申請人'),
        ),
    ]
