from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..assessment.api import AssessmentLevelPermissions, DisabledPagination, InAssessmentFilter
from ..common.api import CleanupFieldsBaseViewSet
from ..common.helper import tryParseInt
from . import models, serializers


class Study(viewsets.ReadOnlyModelViewSet):
    assessment_filter_args = "assessment"
    model = models.Study
    pagination_class = DisabledPagination
    permission_classes = (AssessmentLevelPermissions,)
    filter_backends = (InAssessmentFilter, DjangoFilterBackend)
    list_actions = [
        "list",
        "rob_scores",
    ]

    def get_serializer_class(self):
        cls = serializers.VerboseStudySerializer
        if self.action == "list":
            cls = serializers.SimpleStudySerializer
        return cls

    def get_queryset(self):
        if self.action == "list":
            if not self.assessment.user_can_edit_object(self.request.user):
                return self.model.objects.published(self.assessment)
            return self.model.objects.get_qs(self.assessment)
        else:
            return self.model.objects.prefetch_related(
                "identifiers", "riskofbiases__scores__metric__domain",
            ).select_related("assessment__rob_settings", "assessment")

    @action(detail=False)
    def rob_scores(self, request):
        assessment_id = tryParseInt(self.request.query_params.get("assessment_id"), -1)
        scores = self.model.objects.rob_scores(assessment_id)
        return Response(scores)

    @action(detail=False)
    def types(self, request):
        study_types = self.model.STUDY_TYPE_FIELDS
        return Response(study_types)


class FinalRobStudy(Study):
    list_actions = ["list"]

    def get_serializer_class(self):
        return serializers.FinalRobStudySerializer


class StudyCleanupFieldsView(CleanupFieldsBaseViewSet):
    model = models.Study
    serializer_class = serializers.StudyCleanupFieldsSerializer
