# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='byear',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrower',
            name='credit',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='boperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='library.Watcher', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='btime',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='roperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='library.Watcher', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='rtime',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
