# Generated by Django 3.1.3 on 2020-11-30 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_times'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Times',
            new_name='Time',
        ),
    ]