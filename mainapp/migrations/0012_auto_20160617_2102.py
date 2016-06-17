# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20160604_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCart',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='productcart',
            name='cart',
            field=models.ForeignKey(to='mainapp.Cart'),
        ),
        migrations.AddField(
            model_name='productcart',
            name='product',
            field=models.ForeignKey(to='mainapp.Product'),
        ),
    ]
