# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('jupiter_auth', '0006_auto_20161226_1211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={
                'permissions': (
                ('view_user', 'Can view users'), ('manage_himself', 'Can manage himself'),
                ('user_change_password', 'Can change password')), 'verbose_name': 'User',
                'verbose_name_plural': 'Users'
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=300),
        ),
    ]