# Generated by Django 3.2.20 on 2023-07-25 07:22

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Backend', '0047_alter_news_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='modified_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, on_update=True, to=settings.AUTH_USER_MODEL),
        ),
    ]