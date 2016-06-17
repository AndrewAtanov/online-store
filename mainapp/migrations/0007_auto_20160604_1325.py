# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_product_translit_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(to='mainapp.Customer', null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='mainapp.Product', null=True),
        ),
    ]
