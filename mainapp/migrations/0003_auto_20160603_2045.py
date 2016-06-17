# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20160516_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='categories',
            field=models.ForeignKey(to='mainapp.Category', null=True),
        ),
    ]
