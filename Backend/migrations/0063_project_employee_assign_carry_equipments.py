# Generated by Django 3.2.20 on 2023-08-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0062_rename_reassignment_attachment_project_confirmation_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_employee_assign',
            name='carry_equipments',
            field=models.ManyToManyField(blank=True, related_name='carry_equipment', to='Backend.Equipment', verbose_name='攜帶資產'),
        ),
    ]
