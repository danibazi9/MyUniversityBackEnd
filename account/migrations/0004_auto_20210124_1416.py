# Generated by Django 3.1.3 on 2021-01-24 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210124_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, upload_to='users/images/'),
        ),
    ]
