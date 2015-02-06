# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.CharField(max_length=13)),
                ('bname', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=128, blank=True)),
                ('translator', models.CharField(max_length=128, blank=True)),
                ('byear', models.CharField(max_length=8, blank=True)),
                ('pagination', models.IntegerField(blank=True)),
                ('price', models.FloatField(blank=True)),
                ('bcover', models.URLField(blank=True)),
                ('publisher', models.CharField(max_length=30, blank=True)),
                ('totalnum', models.IntegerField()),
                ('available', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bnum', models.IntegerField()),
                ('btime', models.DateTimeField(default=None, blank=True)),
                ('hasaccepted', models.BooleanField(default=False)),
                ('hasborrowed', models.BooleanField(default=False)),
                ('book', models.ForeignKey(default=None, to='library.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('account', models.CharField(max_length=10, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=12)),
                ('lpnumber', models.CharField(max_length=12)),
                ('spnumber', models.CharField(max_length=6, blank=True)),
                ('credit', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('btime', models.DateTimeField()),
                ('rtime', models.DateTimeField(blank=True)),
                ('bsubc', models.TextField(blank=True)),
                ('rsubc', models.CharField(max_length=12, blank=True)),
                ('hasreturn', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='library.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('what', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watcher',
            fields=[
                ('account', models.CharField(max_length=10, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=12)),
                ('lpnumber', models.CharField(max_length=12)),
                ('spnumber', models.CharField(max_length=6, blank=True)),
                ('password', models.CharField(max_length=128)),
                ('watchsum', models.IntegerField(default=0)),
                ('iswatching', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='borrowrecord',
            name='boperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='library.Watcher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='borrowrecord',
            name='borrower',
            field=models.ForeignKey(related_name='+', to='library.Borrower'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='borrowrecord',
            name='roperator',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to='library.Watcher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, default=None, to='library.Borrower'),
            preserve_default=True,
        ),
    ]
