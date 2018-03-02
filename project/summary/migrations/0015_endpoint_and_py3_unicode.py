# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-02 20:00
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0014_visuals_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapivot',
            name='settings',
            field=models.TextField(default='undefined', help_text='Paste content from a settings file from a different data-pivot, or keep set to "undefined".'),
        ),
        migrations.AlterField(
            model_name='datapivot',
            name='slug',
            field=models.SlugField(help_text='The URL (web address) used to describe this object (no spaces or special-characters).', verbose_name='URL Name'),
        ),
        migrations.AlterField(
            model_name='datapivot',
            name='title',
            field=models.CharField(help_text='Enter the title of the visualization (spaces and special-characters allowed).', max_length=128),
        ),
        migrations.AlterField(
            model_name='datapivotquery',
            name='evidence_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Animal Bioassay'), (1, 'Epidemiology'), (4, 'Epidemiology meta-analysis/pooled analysis'), (2, 'In vitro'), (3, 'Other')], default=0),
        ),
        migrations.AlterField(
            model_name='datapivotquery',
            name='export_style',
            field=models.PositiveSmallIntegerField(choices=[(0, 'One row per Endpoint-group/Result-group'), (1, 'One row per Endpoint/Result')], default=0, help_text='The export style changes the level at which the data are aggregated, and therefore which columns and types of data are presented in the export, for use in the visual.'),
        ),
        migrations.AlterField(
            model_name='datapivotquery',
            name='preferred_units',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), default=list, help_text='List of preferred dose-values, in order of preference. If empty, dose-units will be random for each endpoint presented. This setting may used for comparing percent-response, where dose-units are not needed, or for creating one plot similar, but not identical, dose-units.', size=None),
        ),
        migrations.AlterField(
            model_name='datapivotquery',
            name='prefilters',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='datapivotquery',
            name='published_only',
            field=models.BooleanField(default=True, help_text='Only present data from studies which have been marked as "published" in HAWC.', verbose_name='Published studies only'),
        ),
        migrations.AlterField(
            model_name='datapivotupload',
            name='file',
            field=models.FileField(help_text='The data should be in unicode-text format, tab delimited (this is a standard output type in Microsoft Excel).', upload_to='data_pivot'),
        ),
        migrations.AlterField(
            model_name='summarytext',
            name='slug',
            field=models.SlugField(help_text='The URL (web address) used on the website to describe this object (no spaces or special-characters).', unique=True, verbose_name='URL Name'),
        ),
        migrations.AlterField(
            model_name='summarytext',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='visual',
            name='endpoints',
            field=models.ManyToManyField(blank=True, help_text='Endpoints to be included in visualization', related_name='visuals', to='animal.Endpoint'),
        ),
        migrations.AlterField(
            model_name='visual',
            name='prefilters',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='visual',
            name='settings',
            field=models.TextField(default='{}'),
        ),
        migrations.AlterField(
            model_name='visual',
            name='slug',
            field=models.SlugField(help_text='The URL (web address) used to describe this object (no spaces or special-characters).', verbose_name='URL Name'),
        ),
        migrations.AlterField(
            model_name='visual',
            name='studies',
            field=models.ManyToManyField(blank=True, help_text='Studies to be included in visualization', related_name='visuals', to='study.Study'),
        ),
        migrations.AlterField(
            model_name='visual',
            name='visual_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'animal bioassay endpoint aggregation'), (1, 'animal bioassay endpoint crossview'), (2, 'risk of bias heatmap'), (3, 'risk of bias barchart')]),
        ),
    ]
