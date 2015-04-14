
from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from . import views, api


router = DefaultRouter()
router.register(r'visual', api.Visual, base_name="visual")


urlpatterns = patterns('',
    # API
    url(r'^api/', include(router.urls)),

    # SUMMARY-TEXT
    url(r'^assessment/(?P<pk>\d+)/summaries/$',
        views.SummaryTextList.as_view(),
        name='list'),
    url(r'^assessment/(?P<pk>\d+)/summaries/modify/$',
        views.SummaryTextModify.as_view(),
        name='modify'),
    url(r'^assessment/(?P<pk>\d+)/summaries/json/$',
        views.SummaryTextJSON.as_view(),
        name='json'),

    # VISUALIZATIONS
    url(r'^assessment/(?P<pk>\d+)/visuals/$',
        views.VisualizationList.as_view(),
        name='visualization_list'),
    url(r'^assessment/(?P<pk>\d+)/visuals/create/$',
        views.VisualizationCreate.as_view(),
        name='visualization_create'),
    url(r'^visual/(?P<pk>\d+)/$',
        views.VisualizationDetail.as_view(),
        name='visualization_detail'),
    url(r'^visual/(?P<pk>\d+)/update/$',
        views.VisualizationUpdate.as_view(),
        name='visualization_update'),
    url(r'^visual/(?P<pk>\d+)/delete/$',
        views.VisualizationDelete.as_view(),
        name='visualization_delete'),

    # DATA-PIVOT
    url(r'^data-pivot/$',
        views.GeneralDataPivot.as_view(),
        name='dp_general'),
    url(r'^data-pivot/excel-unicode-saving/$',
        views.ExcelUnicode.as_view(),
        name="dp_excel-unicode"),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/$',
        views.DataPivotList.as_view(),
        name='dp_list'),

    url(r'^data-pivot/assessment/(?P<pk>\d+)/new/$',
        views.DataPivotNewPrompt.as_view(),
        name='dp_new-prompt'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/new/query/$',
        views.DataPivotQueryNew.as_view(),
        name='dp_new-query'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/new/file/$',
        views.DataPivotFileNew.as_view(),
        name='dp_new-file'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/new/copy-as-new-selector/$',
        views.DataPivotCopyAsNewSelector.as_view(),
        name='dp_copy_selector'),

    url(r'^data-pivot/assessment/(?P<pk>\d+)/search/json/$',
        views.DataPivotSearch.as_view(),
        name='dp_search'),
    url(r'^data-pivot/(?P<pk>\d+)/json/$',
        views.DataPivotJSON.as_view(),
        name='dp_json'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/(?P<slug>[\w-]+)/$',
        views.DataPivotDetail.as_view(),
        name='dp_detail'),

    url(r'^data-pivot/assessment/(?P<pk>\d+)/(?P<slug>[\w-]+)/update/$',
        views.DataPivotUpdateSettings.as_view(),
        name='dp_update'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/(?P<slug>[\w-]+)/query-update/$',
        views.DataPivotUpdateQuery.as_view(),
        name='dp_query-update'),
    url(r'^data-pivot/assessment/(?P<pk>\d+)/(?P<slug>[\w-]+)/file-update/$',
        views.DataPivotUpdateFile.as_view(),
        name='dp_file-update'),

    url(r'^data-pivot/assessment/(?P<pk>\d+)/(?P<slug>[\w-]+)/delete/$',
        views.DataPivotDelete.as_view(),
        name='dp_delete'),
)
