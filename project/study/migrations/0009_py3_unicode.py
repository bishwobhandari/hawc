# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-02 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0008_delete_study_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='attachment',
            field=models.FileField(upload_to='study-attachment'),
        ),
        migrations.AlterField(
            model_name='study',
            name='ask_author',
            field=models.TextField(blank=True, help_text='Details on correspondence between data-extractor and author, if needed.', verbose_name='Correspondence details'),
        ),
        migrations.AlterField(
            model_name='study',
            name='bioassay',
            field=models.BooleanField(default=False, help_text='Study contains animal bioassay data', verbose_name='Animal bioassay'),
        ),
        migrations.AlterField(
            model_name='study',
            name='coi_details',
            field=models.TextField(blank=True, help_text='Details related to potential or disclosed conflict(s) of interest', verbose_name='COI details'),
        ),
        migrations.AlterField(
            model_name='study',
            name='coi_reported',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Authors report they have no COI'), (1, 'Authors disclosed COI'), (2, 'Unknown'), (3, 'Not reported')], default=0, help_text='Was a conflict of interest reported by the study authors?', verbose_name='COI reported'),
        ),
        migrations.AlterField(
            model_name='study',
            name='contact_author',
            field=models.BooleanField(default=False, help_text='Was the author contacted for clarification of methods or results?'),
        ),
        migrations.AlterField(
            model_name='study',
            name='epi',
            field=models.BooleanField(default=False, help_text='Study contains epidemiology data', verbose_name='Epidemiology'),
        ),
        migrations.AlterField(
            model_name='study',
            name='epi_meta',
            field=models.BooleanField(default=False, help_text='Study contains epidemiology meta-analysis/pooled analysis data', verbose_name='Epidemiology meta-analysis'),
        ),
        migrations.AlterField(
            model_name='study',
            name='full_citation',
            field=models.TextField(help_text='Complete study citation, in desired format.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='in_vitro',
            field=models.BooleanField(default=False, help_text='Study contains in-vitro data'),
        ),
        migrations.AlterField(
            model_name='study',
            name='published',
            field=models.BooleanField(default=False, help_text='If True, this study, risk of bias, and extraction details may be visible to reviewers and/or the general public (if assessment-permissions allow this level of visibility). Team-members and project-management can view both published and unpublished studies.'),
        ),
        migrations.AlterField(
            model_name='study',
            name='short_citation',
            field=models.CharField(help_text='How the study should be identified (i.e. Smith et al. (2012), etc.)', max_length=256),
        ),
        migrations.AlterField(
            model_name='study',
            name='study_identifier',
            field=models.CharField(blank=True, help_text='Reference descriptor for assessment-tracking purposes (for example, "{Author, year, #EndNoteNumber}")', max_length=128, verbose_name='Internal study identifier'),
        ),
        migrations.AlterField(
            model_name='study',
            name='summary',
            field=models.TextField(blank=True, help_text='Study summary or details on data-extraction needs.', verbose_name='Summary and/or extraction comments'),
        ),
    ]
