# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bachelor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=30)),
                ('authorAffiliationowner', models.CharField(max_length=10)),
                ('authorActive', models.BooleanField()),
                ('authorStatus', models.CharField(max_length=30)),
                ('authorName', models.CharField(max_length=30)),
                ('authorSurname', models.CharField(max_length=30)),
                ('authorEmail', models.EmailField(max_length=254)),
                ('authorAffiliationId', models.CharField(max_length=60)),
                ('titlePL', models.TextField()),
                ('titleEN', models.TextField()),
                ('certifyingUnit', models.CharField(max_length=60)),
                ('affiliationUnit', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=15)),
                ('mark', models.CharField(max_length=20)),
                ('honored', models.CharField(max_length=20)),
                ('issueDate', models.DateField()),
                ('abstractPL', models.TextField()),
                ('abstractEN', models.TextField()),
                ('keywordsPL', models.TextField()),
                ('keywordsEN', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=30)),
                ('authorAffiliationowner', models.CharField(max_length=10)),
                ('authorActive', models.BooleanField()),
                ('authorStatus', models.CharField(max_length=30)),
                ('authorName', models.CharField(max_length=30)),
                ('authorSurname', models.CharField(max_length=30)),
                ('authorEmail', models.EmailField(max_length=254)),
                ('authorAffiliationId', models.CharField(max_length=60)),
                ('titlePL', models.TextField()),
                ('titleEN', models.TextField()),
                ('certifyingUnit', models.CharField(max_length=60)),
                ('affiliationUnit', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=15)),
                ('mark', models.CharField(max_length=20)),
                ('honored', models.CharField(max_length=20)),
                ('issueDate', models.DateField()),
                ('abstractPL', models.TextField()),
                ('abstractEN', models.TextField()),
                ('keywordsPL', models.TextField()),
                ('keywordsEN', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateBachelor',
            fields=[
                ('owner', models.CharField(max_length=30)),
                ('affiliationowner', models.CharField(max_length=10)),
                ('author_active', models.BooleanField()),
                ('author_status', models.CharField(max_length=30)),
                ('author_affiliation_id', models.CharField(max_length=60)),
                ('supervisor', models.OneToOneField(primary_key=True, serialize=False, to='polls.Supervisor')),
                ('certifyingUnit', models.CharField(max_length=60)),
                ('affiliationUnit', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=15)),
                ('mark', models.CharField(max_length=20)),
                ('honored', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateMaster',
            fields=[
                ('owner', models.CharField(max_length=30)),
                ('affiliationowner', models.CharField(max_length=10)),
                ('author_active', models.BooleanField()),
                ('author_status', models.CharField(max_length=30)),
                ('author_affiliation_id', models.CharField(max_length=60)),
                ('supervisor', models.OneToOneField(primary_key=True, serialize=False, to='polls.Supervisor')),
                ('certifyingUnit', models.CharField(max_length=60)),
                ('affiliationUnit', models.CharField(max_length=60)),
                ('language', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=15)),
                ('mark', models.CharField(max_length=20)),
                ('honored', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='master',
            name='supervisor',
            field=models.ForeignKey(to='polls.Supervisor'),
        ),
        migrations.AddField(
            model_name='bachelor',
            name='supervisor',
            field=models.ForeignKey(to='polls.Supervisor'),
        ),
    ]
