# Generated by Django 3.1.3 on 2021-01-24 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, upload_to='users/images/'),
        ),
    ]
