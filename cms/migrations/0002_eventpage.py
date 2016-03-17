# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-16 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0012_copy_image_permissions_to_collections'),
        ('wagtailcore', '0028_merge'),
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('link', models.URLField(blank=True)),
                ('is_open', models.BooleanField(default=True)),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
