# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, verbose_name='code')),
                ('name', models.CharField(max_length=35, verbose_name='name')),
                ('symbol', models.CharField(blank=True, max_length=4, verbose_name='symbol')),
                ('factor', models.DecimalField(decimal_places=4, help_text='Specifies the difference of the currency to default one.', max_digits=10, verbose_name='factor')),
                ('is_active', models.BooleanField(default=True, help_text='The currency will be available.', verbose_name='active')),
                ('is_base', models.BooleanField(default=False, help_text='Make this the base currency against which rates are calculated.', verbose_name='base')),
                ('is_default', models.BooleanField(default=False, help_text='Make this the default user currency.', verbose_name='default')),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'currency',
                'ordering': ('name',),
                'verbose_name_plural': 'currencies',
            },
            bases=(models.Model,),
        ),
    ]
