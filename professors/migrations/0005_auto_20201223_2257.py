# Generated by Django 3.1.3 on 2020-12-23 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professors', '0004_auto_20201223_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='Times',
            fields=[
                ('time_id', models.AutoField(primary_key=True, serialize=False)),
                ('weekday', models.CharField(choices=[('Saturday', 'شنبه'), ('Sunday', 'یکشنبه'), ('Monday', 'دوشنبه'), ('Tuesday', 'سه\u200cشنبه'), ('Wednesday', 'چهارشنبه'), ('Thursday', 'پنج\u200cشنبه'), ('Friday', 'جمعه')], max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='free_times',
            field=models.ManyToManyField(to='professors.Times'),
        ),
    ]
