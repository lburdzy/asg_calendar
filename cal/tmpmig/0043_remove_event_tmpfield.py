# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0042_event_tmpfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tmpfield',
        ),
    ]
