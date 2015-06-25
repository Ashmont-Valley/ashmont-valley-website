# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import person.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0011_auto_20150419_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apt', models.CharField(max_length=32, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, verbose_name='Adress Phone', blank=True)),
                ('kind', models.CharField(default=b'-', max_length=1, verbose_name='Type', choices=[(b'-', b'Unknown'), (b'R', b'Residence'), (b'B', b'Business'), (b'C', b'Community Space'), (b'G', b'Governmental')])),
                ('importid', models.CharField(max_length=128, null=True, verbose_name='Whitepages ID', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=64)),
                ('postcode', models.CharField(max_length=22)),
                ('location', geoposition.fields.GeopositionField(max_length=42, null=True, blank=True)),
                ('plot', models.TextField(null=True, verbose_name='Building Plot', blank=True)),
                ('foot', models.TextField(null=True, verbose_name='Building Footprint', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_user', models.ForeignKey(related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='from_friends', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupPhotoPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('style', models.CharField(max_length=1, verbose_name='Display Style', choices=[(b'L', 'Simple List'), (b'P', 'Photo Heads'), (b'B', 'Photo Bios')])),
                ('source', models.ForeignKey(to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', person.fields.ResizedImageField(format=b'PNG', upload_to=b'photos', max_width=190, min_height=0, max_height=190, blank=True, min_width=0, null=True, verbose_name='Photograph (square)')),
                ('notes', models.TextField(null=True, blank=True)),
                ('phone', models.CharField(max_length=8, null=True, verbose_name='Cell Phone', blank=True)),
                ('org', models.CharField(max_length=64, null=True, verbose_name='Organization', blank=True)),
                ('ophone', models.CharField(max_length=32, null=True, verbose_name='Office Phone', blank=True)),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='Description', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_seen', models.DateTimeField(null=True, blank=True)),
                ('visits', models.IntegerField(default=0)),
                ('auser', person.fields.AutoOneToOneField(related_name='details', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('ctype', models.ForeignKey(verbose_name='Contact Type', blank=True, to='person.ContactType', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('alias', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.ForeignKey(to='person.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=2)),
                ('country', models.ForeignKey(to='person.Country')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='person.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building',
            name='road',
            field=models.ForeignKey(to='person.Road'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='building',
            unique_together=set([('number', 'road')]),
        ),
        migrations.AddField(
            model_name='address',
            name='building',
            field=models.ForeignKey(to='person.Building'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('apt', 'building')]),
        ),
    ]
