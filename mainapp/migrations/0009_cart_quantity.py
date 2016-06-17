# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20160604_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=picklefield.fields.PickledObjectField(default=datetime.datetime(2016, 6, 4, 15, 49, 3, 970945, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
