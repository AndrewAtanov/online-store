# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20160604_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=picklefield.fields.PickledObjectField(editable=False),
        ),
    ]
