# Generated by Django 3.1.3 on 2021-01-24 12:29

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210124_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_joined',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login',
            field=django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='last login'),
        ),
    ]
