# Generated by Django 2.2.15 on 2020-08-27 20:55

from django.db import migrations, models


def update_legacy_values(apps, schema_editor):

    Assessment = apps.get_model("assessment", "assessment")
    Assessment.objects.update(
        modify_uncontrolled_vocabulary=False, vocabulary=None,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("vocab", "0001_initial"),
        ("assessment", "0021_endpoint_ordering"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="modify_uncontrolled_vocabulary",
            field=models.BooleanField(
                default=True,
                help_text='If using a controlled vocabulary and content is added which requires the\n        definition of new terms, these may be modified and by curators who map new terms to the\n        controlled vocabulary. Opting in means the values may change. It is recommended to select\n        this option until you like to "freeze" your assessment, and then this can be unchecked, if\n        needed.',
                verbose_name="Curators can modify terms",
            ),
        ),
        migrations.AddField(
            model_name="assessment",
            name="vocabulary",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[(1, "EPA Environmental health vocabulary")],
                default=1,
                help_text="Attempt to use a controlled vocabulary for entering bioassay data into HAWC.\n        You still have the option to enter terms which are not available in the vocabulary.",
                null=True,
                verbose_name="Controlled vocabulary",
            ),
        ),
        migrations.AlterModelOptions(name="baseendpoint", options={"ordering": ("id",)},),
        migrations.RunPython(update_legacy_values, migrations.RunPython.noop),
    ]
