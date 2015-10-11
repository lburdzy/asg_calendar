# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0029_auto_20151011_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(verbose_name='data i czas', default=datetime.datetime(2015, 10, 11, 11, 51, 1, 158214)),
        ),
    ]
