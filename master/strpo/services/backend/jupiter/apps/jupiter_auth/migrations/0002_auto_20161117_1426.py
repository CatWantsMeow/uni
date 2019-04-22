# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 14:26
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('jupiter_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('identification_number', models.CharField(max_length=30)),
                ('passport_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('passport_expires', models.DateField()),
                ('birth_date', models.DateField()),
                ('family_status', models.TextField()),
                ('dependants', models.TextField()),
                ('income', models.TextField()),
                ('realty', models.TextField()),
                ('job', models.TextField()),
            ],
            options={
                'verbose_name': 'User profile',
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dependants',
        ),
        migrations.RemoveField(
            model_name='user',
            name='family_status',
        ),
        migrations.RemoveField(
            model_name='user',
            name='identification_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='income',
        ),
        migrations.RemoveField(
            model_name='user',
            name='job',
        ),
        migrations.RemoveField(
            model_name='user',
            name='passport_expires',
        ),
        migrations.RemoveField(
            model_name='user',
            name='passport_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='realty',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]