# Generated by Django 2.2.15 on 2020-09-16 02:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vocab", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="entitytermrelation",
            name="approved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="entitytermrelation",
            name="approved_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="entitytermrelation", name="notes", field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="entitytermrelation",
            name="entity",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vocab.Entity"),
        ),
        migrations.AlterField(
            model_name="entitytermrelation",
            name="term",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="vocab.Term"),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("last_url_visited", models.CharField(max_length=128)),
                ("comment", models.TextField()),
                ("reviewed", models.BooleanField(default=False)),
                ("reviewer_notes", models.TextField(blank=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "commenter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={"ordering": ("id",)},
        ),
    ]