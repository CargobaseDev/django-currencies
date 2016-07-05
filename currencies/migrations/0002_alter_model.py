# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0002_auto_20160505_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(unique=True, max_length=3, verbose_name='code'),
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['name'], 'verbose_name': 'currency', 'verbose_name_plural': 'currencies'},
        ),
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(db_index=True, max_length=3, unique=True, verbose_name='code'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='factor',
            field=models.DecimalField(decimal_places=10, default=1.0, help_text='Specifies the difference of the currency to default one.', max_digits=30, verbose_name='factor'),
        ),
    ]
