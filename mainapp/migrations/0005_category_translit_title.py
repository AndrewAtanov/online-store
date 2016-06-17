# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='translit_title',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
