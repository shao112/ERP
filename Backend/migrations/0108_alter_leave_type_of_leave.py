# Generated by Django 3.2.20 on 2023-08-28 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0107_alter_leave_param_control'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='type_of_leave',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_param', to='Backend.leave_param', verbose_name='假別項目'),
        ),
    ]
