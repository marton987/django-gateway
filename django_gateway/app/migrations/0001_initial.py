# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('merchant_id', models.CharField(max_length=20, verbose_name='Merchant id')),
                ('gateway', models.CharField(max_length=10, verbose_name='Gateway', choices=[('braintree', 'Braintree Payments'), ('paypal', 'PayPal')])),
                ('status', models.CharField(max_length=10, verbose_name='Status', choices=[('success', 'Success'), ('failure', 'Failure')])),
                ('message', models.TextField(null=True, verbose_name='Message', blank=True)),
                ('response', models.TextField(null=True, verbose_name='Response', blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Merchant transaction',
                'verbose_name_plural': 'Merchant transactions',
            },
            bases=(models.Model,),
        ),
    ]
