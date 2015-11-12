# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.utils.timezone
import django.core.validators
import hoodcms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo', hoodcms.fields.ResizedImageField(format=b'PNG', upload_to=b'photos', max_width=190, min_height=0, max_height=190, blank=True, min_width=0, null=True, verbose_name='Photograph (square)')),
                ('notes', models.TextField(null=True, blank=True)),
                ('phone', models.CharField(max_length=8, null=True, verbose_name='Cell Phone', blank=True)),
                ('org', models.CharField(max_length=64, null=True, verbose_name='Organization', blank=True)),
                ('ophone', models.CharField(max_length=32, null=True, verbose_name='Office Phone', blank=True)),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='Description', blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_seen', models.DateTimeField(null=True, blank=True)),
                ('visits', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
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
                ('icon', models.CharField(max_length=32)),
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
            name='Road',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('alias', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.ForeignKey(to='users.City')),
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
                ('country', models.ForeignKey(to='users.Country')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='users.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building',
            name='road',
            field=models.ForeignKey(to='users.Road'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='building',
            unique_together=set([('number', 'road')]),
        ),
        migrations.AddField(
            model_name='address',
            name='building',
            field=models.ForeignKey(to='users.Building'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('apt', 'building')]),
        ),
        migrations.AddField(
            model_name='person',
            name='ctype',
            field=models.ForeignKey(verbose_name='Contact Type', blank=True, to='users.ContactType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
