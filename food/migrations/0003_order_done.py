# Generated by Django 3.1.2 on 2020-11-28 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
