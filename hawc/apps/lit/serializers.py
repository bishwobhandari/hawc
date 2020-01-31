import logging
from typing import List

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from ..assessment.serializers import AssessmentRootedSerializer
from ..common.api import DynamicFieldsMixin
from ..common.serializers import validate_csv
from . import constants, models


class IdentifiersSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["database"] = instance.get_database_display()
        ret["url"] = instance.get_url()
        return ret

    class Meta:
        model = models.Identifiers
        fields = "__all__"


class ReferenceTagsSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        raise ParseError("Not implemented!")

    def to_representation(self, obj):
        # obj is a model-manager in this case; convert to list to serialize
        return list(obj.values("id", "name"))


class ReferenceFilterTagSerializer(AssessmentRootedSerializer):
    parent = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.ReferenceFilterTag
        fields = ("id", "name", "parent")


class ReferenceCleanupFieldsSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        cleanup_fields = model.TEXT_CLEANUP_FIELDS
        fields = cleanup_fields + ("id",)


def _validate_refs_in_assessment(assessment_id: int, reference_ids: List[int]):
    """
    Validate references are in assessment or throw serializer.ValidationError

    Args:
        assessment_id (int): Assessment ID
        reference_ids (pd.Series): A list of reference IDs
    """
    assessments = (
        models.Reference.objects.filter(id__in=reference_ids)
        .values_list("assessment_id", flat=True)
        .distinct()
    )
    if len(assessments) != 1 or assessments[0] != assessment_id:
        raise serializers.ValidationError(
            f"All reference ids are not from assessment {assessment_id}"
        )


class BulkReferenceTagSerializer(serializers.Serializer):
    operation = serializers.ChoiceField(choices=["append", "replace"], required=True)
    csv = serializers.CharField(required=True)

    def validate_csv(self, value):

        assessment_id = self.context["assessment"].id

        df = validate_csv(value, {"reference_id", "tag_id"})

        _validate_refs_in_assessment(assessment_id, df.reference_id.unique())

        # ensure that all tags are from this assessment
        expected_tag_ids = set(models.ReferenceFilterTag.get_descendants_pks(assessment_id))
        if not set(df.tag_id.unique()).issubset(expected_tag_ids):
            raise serializers.ValidationError(
                f"All tag ids are not from assessment {assessment_id}"
            )

        # success! save dataframe
        self.assessment = self.context["assessment"]
        self.df = df

        return value

    @transaction.atomic
    def bulk_create_tags(self):
        assessment_id = self.assessment.id
        operation = self.validated_data["operation"]

        existing = set()
        if operation == "append":
            existing = set(
                models.ReferenceTags.objects.filter(
                    content_object__assessment_id=assessment_id
                ).values_list("tag_id", "content_object_id")
            )

        if operation == "replace":
            tags_to_delete = models.ReferenceTags.objects.assessment_qs(assessment_id)
            logging.info(f"Deleting {tags_to_delete.count()} reference tags for {assessment_id}")
            tags_to_delete.delete()

        new_tags = [
            models.ReferenceTags(tag_id=row.tag_id, content_object_id=row.reference_id)
            for row in self.df.itertuples(index=False)
            if (row.tag_id, row.reference_id) not in existing
        ]

        if new_tags:
            logging.info(f"Creating {len(new_tags)} reference tags for {assessment_id}")
            models.ReferenceTags.objects.bulk_create(new_tags)

            models.Reference.delete_cache(assessment_id)


class BulkReferenceIdentifierAssignment(serializers.Serializer):
    csv = serializers.CharField(required=True)

    def validate_csv(self, value):

        assessment_id = self.context["assessment"].id

        # validate we have a csv with data
        df = validate_csv(value, {"reference_id", "hero_id", "pubmed_id"})

        # validate we're dealing with only our assessment's data
        _validate_refs_in_assessment(assessment_id, df.reference_id.unique())

        # success! save dataframe
        self.assessment = self.context["assessment"]
        self.df = df

        return value

    @transaction.atomic
    def create_and_apply_identifiers(self):
        """
        Apply all HERO and Pubmed IDs to all references in assessment, using the following process:
        - Batch create any HERO identifiers that don't currently exist
        - Batch create any Pubmed identifiers that don't currently exist
        - Assign all missing identifiers to references
        """
        # potentially create new HERO IDs
        hero_ids = set(self.df.hero_id.dropna().unique().astype(str))
        hero_qs = models.Identifiers.objects.filter(unique_id__in=hero_ids, database=constants.HERO)
        existing_hero_ids = set(hero_qs.values_list("unique_id", flat=True))
        missing_hero_ids = hero_ids - existing_hero_ids
        if len(missing_hero_ids) > 0:
            logging.info(f"New literature import: {len(missing_hero_ids)} HERO IDs")
            models.Identifiers.objects.get_hero_identifiers(missing_hero_ids)
        # use .all() to force qs re-evaluation; https://docs.djangoproject.com/en/3.0/ref/models/querysets/#all
        hero_ids = {el.unique_id: el for el in hero_qs.all()}

        # potentially create new Pubmed IDs
        pubmed_ids = set(self.df.pubmed_id.dropna().unique().astype(str))
        pubmed_qs = models.Identifiers.objects.filter(
            unique_id__in=pubmed_ids, database=constants.PUBMED
        )
        existing_pubmed_ids = set(pubmed_qs.values_list("unique_id", flat=True))
        missing_pubmed_ids = pubmed_ids - existing_pubmed_ids
        if len(missing_pubmed_ids) > 0:
            logging.info(f"New literature import: {len(missing_pubmed_ids)} Pubmed IDs")
            models.Identifiers.objects.get_pubmed_identifiers(missing_pubmed_ids)
        # use .all() to force qs re-evaluation; https://docs.djangoproject.com/en/3.0/ref/models/querysets/#all
        pubmed_ids = {el.unique_id: el for el in pubmed_qs.all()}

        # assign identifiers to references
        ref_ids = self.df.reference_id.dropna().unique()
        ref_qs = models.Reference.objects.filter(id__in=ref_ids).prefetch_related("identifiers")
        refs = {ref.id: ref for ref in ref_qs}
        for _, row in self.df.iterrows():
            if row.reference_id in refs:
                ref = refs[row.reference_id]

                # use new HERO ID where specified
                if (
                    row.hero_id in hero_ids
                    and not ref.identifiers.filter(
                        unique_id=str(row.hero_id), database=constants.HERO
                    ).exists()
                ):
                    # replace any existing HERO identifiers from this reference
                    ref.identifiers.filter(database=constants.HERO).delete()
                    ref.identifiers.add(hero_ids[row.hero_id])

                # use new Pubmed ID where specified
                if (
                    row.pubmed_id in pubmed_ids
                    and not ref.identifiers.filter(
                        unique_id=str(row.pubmed_id), database=constants.PUBMED
                    ).exists()
                ):
                    # replace any existing Pubmed identifiers from this reference
                    ref.identifiers.filter(database=constants.PUBMED).delete()
                    ref.identifiers.add(pubmed_ids[row.pubmed_id])

