# Generated by Django 4.2.2 on 2023-07-03 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0006_alter_project_attachment_alter_project_remark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('clock_in_or_out', models.BooleanField()),
                ('clock_time', models.TimeField()),
                ('clock_GPS', models.CharField(max_length=255)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Backend.employee')),
            ],
            options={
                'verbose_name': '打卡紀錄',
                'verbose_name_plural': '打卡紀錄',
            },
        ),
    ]
