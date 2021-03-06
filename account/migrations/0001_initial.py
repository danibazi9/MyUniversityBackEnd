# Generated by Django 3.1.3 on 2020-12-30 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('student_id', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('mobile_number', models.CharField(default='09100000000', max_length=11)),
                ('password', models.CharField(blank=True, max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.CharField(default='student', max_length=20, verbose_name='role')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
