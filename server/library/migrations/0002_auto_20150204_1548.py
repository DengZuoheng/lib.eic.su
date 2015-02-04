# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingrecord',
            name='bdate',
        ),
        migrations.RemoveField(
            model_name='bookingrecord',
            name='bid',
        ),
        migrations.RemoveField(
            model_name='bookingrecord',
            name='uid',
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='book',
            field=models.ForeignKey(default=None, to='library.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=None, to='library.Borrower'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='btime',
            field=models.DateTimeField(default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='boperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, to='library.Watcher'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='bsubc',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='btime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='roperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='library.Watcher'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='rsubc',
            field=models.CharField(max_length=12, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='rtime',
            field=models.DateTimeField(blank=True),
            preserve_default=True,
        ),
    ]
