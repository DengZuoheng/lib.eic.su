# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('bdate', models.DateField()),
                ('hasaccepted', models.BooleanField(default=False)),
                ('hasborrowed', models.BooleanField(default=False)),
                ('bid', models.ForeignKey(to='library.Book')),
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
                ('btime', models.DateField()),
                ('rtime', models.DateField()),
                ('rsubc', models.TextField()),
                ('bsubc', models.IntegerField()),
                ('hasreturn', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='library.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128)),
                ('iswatching', models.BooleanField(default=False)),
                ('watchsum', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='borrowrecord',
            name='boperator',
            field=models.ForeignKey(related_name='+', to='library.Watcher'),
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
            field=models.ForeignKey(related_name='+', to='library.Watcher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookingrecord',
            name='uid',
            field=models.ForeignKey(to='library.Borrower'),
            preserve_default=True,
        ),
    ]
