# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-05 20:17
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Formato numero di telefono: '+999999999', con un massimo di 15 cifre.", regex='^\\+?1?\\d{9,15}$')])),
                ('temporizzazione_giorni', models.PositiveIntegerField(default=0)),
                ('temporizzazione_data', models.DateTimeField(auto_now_add=True)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('vote_total', models.PositiveIntegerField(default=0)),
                ('vote_average', models.DecimalField(decimal_places=1, default=Decimal('0'), max_digits=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
