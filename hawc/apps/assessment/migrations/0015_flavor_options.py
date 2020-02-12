# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-04-11 11:35
from __future__ import unicode_literals

from django.db import migrations, models

from ..models import Assessment


class Migration(migrations.Migration):

    dependencies = [
        ("assessment", "0014_auto_20190401_1852"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="noel_name",
            field=models.PositiveSmallIntegerField(
                choices=[(2, "NEL/LEL"), (0, "NOEL/LOEL"), (1, "NOAEL/LOAEL")],
                default=Assessment.get_noel_name_default,
                help_text="What term should be used to refer to NEL/NOEL/NOAEL and LEL/LOEL/LOAEL?",
                verbose_name="NEL/NOEL/NOAEL name",
            ),
        ),
        migrations.AddField(
            model_name="assessment",
            name="rob_name",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Risk of bias"), (1, "Study evaluation")],
                default=Assessment.get_rob_name_default,
                help_text="What term should be used to refer to risk of bias/study evaluation questions?",
                verbose_name="Risk of bias/Study evaluation name",
            ),
        ),
    ]